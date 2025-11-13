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

### Features
- FastAPI middleware for exception monitoring
- Telegram Bot API integration for alerts
- Redis-based distributed deduplication
- Configurable alert levels (CRITICAL, WARNING, INFO)
- Environment-based configuration via .env
- Abstract adapters for database, queue, and Redis integration
- Comprehensive documentation and examples
- Support for multiple background task schedulers (ARQ, APScheduler, Celery)

### Documentation
- Comprehensive README with quick start guide
- Integration examples for different use cases
- Adapter implementation guide
- Environment variable documentation
- Setup instructions for Telegram bot

### Development
- MIT License
- Python 3.12+ support
- Type hints throughout
- Async/await support
- Comprehensive docstrings

---

## Version History Summary

- **1.0.0** - Initial public release with core monitoring features
- **Future releases** - Additional integrations, metrics, and features

## Upgrade Guide

### From Private Repository
If you're migrating from the internal version:

1. Update imports:
   ```python
   # Old
   from app.monitoring import setup_monitoring
   
   # New
   from monitoring import setup_monitoring
   ```

2. Implement adapters:
   ```python
   # Old: Direct model access
   
   # New: Use DatabaseAdapter
   from monitoring import DatabaseAdapter, set_database_adapter
   
   class MyDatabaseAdapter(DatabaseAdapter):
       # Implement required methods
       pass
   
   set_database_adapter(MyDatabaseAdapter())
   ```

3. Update configuration:
   ```python
   # Old: app_settings.MONITORING_*
   
   # New: monitoring_config.* or env vars
   monitoring_config.TELEGRAM_BOT_TOKEN = "..."
   ```

## Support

For issues, questions, or contributions:
- 🐛 [Issue Tracker](https://github.com/humangpts/fastapi-telemon/issues)
- 💬 [Discussions](https://github.com/humangpts/fastapi-telemon/discussions)
- 📖 [Documentation](https://github.com/humangpts/fastapi-telemon/tree/main/docs)