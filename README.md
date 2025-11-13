# FastAPI Monitoring

Production-ready monitoring solution for FastAPI applications with Telegram alerts.

## ✨ Features

- 🔴 **Exception Monitoring**: Automatic error tracking with smart deduplication
- 📊 **Health Checks**: Monitor database, Redis, and background queues
- 📈 **Daily Reports**: Automated statistics delivered via Telegram
- ⚡ **Performance Monitoring**: Track and alert on slow requests
- 🔄 **Background Task Monitoring**: Optional ARQ task tracking
- 🎯 **Smart Rate Limiting**: Prevents alert spam with configurable thresholds
- 📦 **Batch Alerts**: Groups non-critical warnings into digest reports
- 🔌 **Pluggable Architecture**: Easy integration via adapters

## 🚀 Quick Start

### Installation

```bash
pip install fastapi-telemon
```

### Basic Setup

```python
from fastapi import FastAPI
from monitoring import setup_monitoring, monitoring_config

# Configure Telegram
monitoring_config.TELEGRAM_BOT_TOKEN = "your_bot_token_here"
monitoring_config.TELEGRAM_CHAT_ID = "your_chat_id_here"

# Create app and setup monitoring
app = FastAPI()
setup_monitoring(app)

@app.get("/test")
async def test_endpoint():
    raise ValueError("This will send an alert to Telegram!")
```

### Configuration via Environment Variables

Create a `.env` file:

```env
MONITORING_ENABLED=true
MONITORING_ENV=production
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id

# Optional settings
MONITORING_SLOW_REQUEST_THRESHOLD_SECONDS=3.0
MONITORING_ALERT_RATE_LIMIT_MINUTES=10
```

## 📖 Documentation

### Setting up Telegram Bot

1. Create a bot via [@BotFather](https://t.me/botfather)
2. Get your bot token
3. Add bot to your channel/group
4. Get chat ID (use [@userinfobot](https://t.me/userinfobot) or check bot logs)

### With Redis (Recommended)

Redis enables distributed deduplication and statistics:

```python
from redis import asyncio as aioredis
from monitoring import setup_monitoring

redis_client = aioredis.from_url("redis://localhost")
setup_monitoring(app, redis_client=redis_client)
```

### With Database Statistics

Implement the `DatabaseAdapter` to enable database metrics:

```python
from monitoring import setup_monitoring, DatabaseAdapter
from sqlalchemy import select, func
from datetime import datetime

class MyDatabaseAdapter(DatabaseAdapter):
    def __init__(self, session_maker):
        self.session_maker = session_maker
    
    async def get_new_users_count(self, start_date: datetime, end_date: datetime) -> int:
        async with self.session_maker() as session:
            result = await session.execute(
                select(func.count()).select_from(User)
                .where(User.created_at.between(start_date, end_date))
            )
            return result.scalar() or 0
    
    async def get_total_users_count(self) -> int:
        async with self.session_maker() as session:
            result = await session.execute(select(func.count()).select_from(User))
            return result.scalar() or 0
    
    # Implement other required methods...

# Setup
db_adapter = MyDatabaseAdapter(async_session_maker)
setup_monitoring(app, database_adapter=db_adapter)
```

### With Background Queue Monitoring

Monitor ARQ or other queue systems:

```python
from monitoring import setup_monitoring, QueueAdapter

class MyQueueAdapter(QueueAdapter):
    async def health_check(self) -> bool:
        # Check if queue is processing jobs
        return True
    
    async def get_queue_size(self) -> int:
        # Return number of pending jobs
        return 0
    
    async def get_last_job_time(self) -> Optional[float]:
        # Return timestamp of last completed job
        return time.time()

queue_adapter = MyQueueAdapter()
setup_monitoring(app, queue_adapter=queue_adapter)
```

### ARQ Task Monitoring (Optional)

If you use ARQ for background tasks:

```python
from monitoring.arq_monitoring import monitored_task

@monitored_task
async def my_background_task(ctx):
    # Your task logic
    # Failures will be reported to Telegram
    pass
```

## 🎯 Configuration Options

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `MONITORING_ENABLED` | `true` | Enable/disable monitoring |
| `MONITORING_ENV` | `development` | Environment name (appears in alerts) |
| `TELEGRAM_BOT_TOKEN` | - | Your Telegram bot token |
| `TELEGRAM_CHAT_ID` | - | Target chat/channel ID |
| `MONITORING_ALERT_RATE_LIMIT_MINUTES` | `10` | Cooldown between duplicate alerts |
| `MONITORING_SLOW_REQUEST_THRESHOLD_SECONDS` | `3.0` | Threshold for slow request alerts |
| `MONITORING_HEALTH_CHECK_INTERVAL_MINUTES` | `30` | Health check frequency |
| `MONITORING_DAILY_REPORT_ENABLED` | `true` | Enable daily statistics reports |
| `MONITORING_DAILY_REPORT_HOUR` | `9` | Hour to send daily report (UTC) |

See [Configuration Guide](docs/configuration.md) for all options.

## 📊 What Gets Monitored

### Automatic Monitoring

- **500 errors** - Unhandled exceptions in your API
- **Slow requests** - Requests exceeding threshold
- **System health** - Database, Redis, queue status
- **Performance metrics** - Response times and error rates

### Alert Types

**🔴 Critical Alerts** (immediate notification):
- Unhandled exceptions
- System component failures
- Repeated task failures

**⚠️ Warning Alerts** (batched):
- Slow requests
- First-time issues
- Performance degradation

**ℹ️ Info Messages** (silent):
- Daily reports
- System startup notifications

## 🔧 Advanced Usage

### Custom Alerts

Send your own monitoring alerts:

```python
from monitoring import telegram_reporter, AlertLevel

await telegram_reporter.send_alert(
    title="Custom Business Metric",
    message="Revenue threshold exceeded",
    level=AlertLevel.WARNING,
    details={
        "Current Revenue": "$50,000",
        "Threshold": "$45,000"
    }
)
```

### Deduplication Decorator

Ensure functions run only once in distributed systems:

```python
from monitoring import deduplicated

@deduplicated(key="daily_cleanup", ttl=86400)
async def cleanup_old_data():
    # Runs once per day across all workers
    pass
```

### Health Check Integration

Add health endpoint to your API:

```python
from monitoring import get_database_adapter, get_redis_adapter

@app.get("/health")
async def health_check():
    db_healthy = await get_database_adapter().health_check()
    redis_adapter = get_redis_adapter()
    redis_healthy = await redis_adapter.ping() if redis_adapter else True
    
    return {
        "status": "healthy" if (db_healthy and redis_healthy) else "unhealthy",
        "database": db_healthy,
        "redis": redis_healthy
    }
```

## 📸 Screenshots

### Exception Alert
```
🔴 ERROR 500
PRODUCTION

Unhandled exception in /api/users

Details:
• Endpoint: POST /api/users
• Status: 500
• User: john@example.com (123)
• User-Agent: Mozilla/5.0...

Error: ValueError: Invalid user data

Traceback:
```
File "/app/main.py", line 42, in create_user
    validate_user_data(data)
ValueError: Invalid user data
```

⏰ 2024-01-15 14:30:25 UTC
```

### Daily Report
```
📊 Daily Report
PRODUCTION
Date: 2024-01-15

👤 Users
• New: 145
• Active: 1,234
• Total: 12,456

📁 Projects
• Created: 89
• Updated: 456
• Total: 5,678

❌ Errors
• Total: 3
• By type:
  - ValueError: 2
  - KeyError: 1
```

## 🛠️ Development

### Running Tests

```bash
pip install -e ".[dev]"
pytest
```

### Code Style

```bash
black .
ruff check .
```

## 📋 Requirements

- Python 3.12+
- FastAPI
- Redis (optional, but recommended)
- Telegram Bot

## 🤝 Contributing

Contributions welcome! Please check our [Contributing Guide](CONTRIBUTING.md).

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Redis](https://redis.io/)

## 💬 Support

- 📖 [Documentation](docs/)
- 🐛 [Issue Tracker](https://github.com/yourusername/fastapi-telemon/issues)
- 💬 [Discussions](https://github.com/yourusername/fastapi-telemon/discussions)

---

**Made with ❤️ for FastAPI developers who want production-ready monitoring without the complexity**