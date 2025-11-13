# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned for 1.1.0
- Built-in health check endpoint
- Prometheus metrics export
- More scheduler integration examples
- Improved documentation
- Grafana dashboard template

## [1.0.0] - 2025-11-15

### Added
- Initial public release of fastapi-telemon
- **Exception Monitoring**: Automatic error tracking with smart deduplication
- **Health Checks**: Monitor database, Redis, and background queues
- **Daily Reports**: Automated statistics delivered via Telegram
- **Performance Monitoring**: Track and alert on slow requests
- **Background Task Monitoring**: Optional ARQ task tracking
- **Smart Rate Limiting**: Prevents alert spam with configurable thresholds
- **Batch Alerts**: Groups non-critical warnings into digest reports
- **Pluggable Architecture**: Easy integration via adapters
- **Fire-and-Forget Alerts**: Non-blocking alert delivery for optimal performance
- **Markdown Escaping**: Proper escaping of special characters in Telegram messages
- **Rate Limiting**: Built-in rate limiting to respect Telegram API limits
- **Security Features**:
  - Configurable traceback line limits
  - Path-based monitoring exclusions
  - Sensitive data protection warnings
  - Redis security recommendations

### Features
- FastAPI middleware for exception monitoring
- Telegram Bot API integration for alerts
- Redis-based distributed deduplication
- Configurable alert levels (CRITICAL, WARNING, INFO)
- Environment-based configuration via .env
- Abstract adapters for database, queue, and Redis integration
- Comprehensive documentation and examples
- Support for multiple background task schedulers (ARQ, APScheduler, Celery)
- Background task tracking and cleanup
- Exponential backoff retry logic for Telegram API
- Multi-worker support with Redis

### Documentation
- Comprehensive README with quick start guide
- Security best practices and warnings
- Integration examples for different use cases
- Adapter implementation guide
- Environment variable documentation
- Setup instructions for Telegram bot
- SECURITY.md with detailed security guidelines
- CONTRIBUTING.md with development guidelines

### Development
- MIT License
- Python 3.12+ support
- Type hints throughout
- Async/await support
- Comprehensive docstrings
- 80%+ test coverage
- Pre-commit hooks for code quality
- Security scanning with Bandit and Safety

### Security
- ⚠️ **Important**: Tracebacks may contain sensitive data
  - Configurable `ALERT_MAX_TRACEBACK_LINES` setting
  - Path-based exclusions via `IGNORED_PATHS`
  - Markdown escaping to prevent injection
- ⚠️ **Multi-Worker Warning**: Redis required for proper deduplication
- Rate limiting to prevent Telegram API abuse
- Secure Redis connection examples
- Private Telegram group recommendations

### Performance
- Fire-and-forget alert delivery (configurable)
- Async task tracking with proper cleanup
- Efficient deduplication using Redis
- Batch alert processing
- Rate-limited Telegram API calls

---

## Version History Summary

- **1.0.0** - Initial public release with core monitoring features and security improvements
- **Future releases** - Additional integrations, metrics, and features

## Upgrade Guide

### From Private Repository
If you're migrating from the internal version:

1. **Update imports:**
   ```python
   # Old
   from app.monitoring import setup_monitoring
   
   # New
   from monitoring import setup_monitoring
   ```

2. **Implement adapters:**
   ```python
   # Old: Direct model access
   
   # New: Use DatabaseAdapter
   from monitoring import DatabaseAdapter, set_database_adapter
   
   class MyDatabaseAdapter(DatabaseAdapter):
       # Implement required methods
       pass
   
   set_database_adapter(MyDatabaseAdapter())
   ```

3. **Update configuration:**
   ```python
   # Old: app_settings.MONITORING_*
   
   # New: monitoring_config.* or env vars
   monitoring_config.TELEGRAM_BOT_TOKEN = "..."
   ```

4. **Security review:**
   - Review `IGNORED_PATHS` for sensitive endpoints
   - Set `ALERT_MAX_TRACEBACK_LINES` appropriately
   - Configure Redis for multi-worker deployments
   - Review Telegram chat permissions

## Breaking Changes

None yet - this is the first public release.

## Migration Notes

### For Production Deployments

**Critical:** If you're deploying with multiple workers, you **must** configure Redis:

```python
from redis import asyncio as aioredis
from monitoring import setup_monitoring

redis_client = aioredis.from_url("redis://localhost")
setup_monitoring(app, redis_client=redis_client)
```

Without Redis, you'll receive duplicate alerts from each worker!

### Security Configuration

Review and configure these settings before production deployment:

```python
# Limit sensitive data exposure
monitoring_config.ALERT_MAX_TRACEBACK_LINES = 5  # or 0 to disable

# Exclude sensitive endpoints
monitoring_config.IGNORED_PATHS = [
    "/health",
    "/metrics",
    "/auth",       # Add your sensitive paths
    "/payment",
    "/admin",
]

# Use private Telegram groups
monitoring_config.TELEGRAM_CHAT_ID = "your_private_group_id"
```

## Support

For issues, questions, or contributions:
- 🐛 [Issue Tracker](https://github.com/humangpts/fastapi-telemon/issues)
- 💬 [Discussions](https://github.com/humangpts/fastapi-telemon/discussions)
- 🔒 [Security](https://github.com/humangpts/fastapi-telemon/security)
- 📖 [Documentation](https://github.com/humangpts/fastapi-telemon/tree/main/docs)

## Acknowledgments

Special thanks to:
- FastAPI community for the excellent framework
- Contributors who helped test and improve this package
- Security researchers who provided feedback

---

**Note**: This is a Beta release. While functional and tested, the API may change before v1.0.0. We welcome feedback and contributions!