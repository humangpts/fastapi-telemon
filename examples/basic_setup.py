"""
Basic setup example for fastapi-telemon.

This is the minimal configuration needed to get started.
Errors in your API will automatically be reported to Telegram.
"""

from fastapi import FastAPI
from monitoring import setup_monitoring, monitoring_config

# Configure monitoring
monitoring_config.TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
monitoring_config.TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"
monitoring_config.MONITORING_ENV = "development"

# Create FastAPI app
app = FastAPI(title="My API")

# Setup monitoring - this adds exception tracking middleware
setup_monitoring(app)


# Example endpoints
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/error")
async def trigger_error():
    """
    This endpoint will trigger an error that gets reported to Telegram.
    Try accessing it: http://localhost:8000/error
    """
    raise ValueError("This is a test error!")


@app.get("/slow")
async def slow_endpoint():
    """
    This endpoint simulates a slow request.
    If it takes longer than SLOW_REQUEST_THRESHOLD_SECONDS,
    it will be reported.
    """
    import asyncio
    await asyncio.sleep(5)  # Default threshold is 3 seconds
    return {"message": "This was slow"}


if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    uvicorn.run(app, host="0.0.0.0", port=8000)