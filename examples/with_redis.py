"""
Example showing Redis integration for distributed monitoring.

Redis enables:
- Distributed deduplication (prevents duplicate alerts from multiple workers)
- Shared statistics across all application instances
- Better performance monitoring
"""

from fastapi import FastAPI
from redis import asyncio as aioredis
from monitoring import setup_monitoring, monitoring_config

# Configure monitoring
monitoring_config.TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
monitoring_config.TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"
monitoring_config.MONITORING_ENV = "production"

# Create FastAPI app
app = FastAPI()


@app.on_event("startup")
async def startup():
    """Initialize Redis and setup monitoring on startup"""
    
    # Create Redis client
    redis_client = aioredis.from_url(
        "redis://localhost:6379",
        encoding="utf-8",
        decode_responses=True
    )
    
    # Verify Redis connection
    try:
        await redis_client.ping()
        print("✅ Redis connected")
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        # Monitoring will still work without Redis, but with limited functionality
    
    # Setup monitoring with Redis
    setup_monitoring(app, redis_client=redis_client)
    
    print("✅ Monitoring configured with Redis")


@app.on_event("shutdown")
async def shutdown():
    """Cleanup on shutdown"""
    from monitoring import get_redis_adapter
    
    redis_adapter = get_redis_adapter()
    if redis_adapter and hasattr(redis_adapter, '_client'):
        await redis_adapter._client.close()


@app.get("/")
async def root():
    return {"message": "API with Redis-backed monitoring"}


@app.get("/cache-example")
async def cache_example():
    """Example showing how to use Redis adapter directly"""
    from monitoring import get_redis_adapter
    
    redis = get_redis_adapter()
    if not redis:
        return {"error": "Redis not configured"}
    
    # Use Redis for your own caching needs
    cached = await redis.get("example_key")
    if cached:
        return {"source": "cache", "value": cached}
    
    # Compute and cache
    value = "computed_value"
    await redis.setex("example_key", 300, value)  # 5 minutes TTL
    
    return {"source": "computed", "value": value}


@app.get("/test-deduplication")
async def test_deduplication():
    """
    Test deduplication across multiple workers.
    Call this endpoint from multiple workers simultaneously.
    Only one will send the alert!
    """
    from monitoring import telegram_reporter, AlertLevel
    from monitoring.decorators import deduplicated
    
    @deduplicated(key="test_alert", ttl=60)
    async def send_test_alert():
        await telegram_reporter.send_message(
            text="🧪 Test alert - this should only appear once!",
            level=AlertLevel.INFO
        )
        return "Alert sent"
    
    result = await send_test_alert()
    return {"result": result or "Alert was deduplicated"}


if __name__ == "__main__":
    import uvicorn
    
    # Run with multiple workers to test distributed features
    uvicorn.run(
        "with_redis:app",
        host="0.0.0.0",
        port=8000,
        workers=2  # Multiple workers will share Redis state
    )