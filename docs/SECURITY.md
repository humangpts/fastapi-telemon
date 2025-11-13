# Security Policy

## Overview

This monitoring module sends error information to Telegram for alerting purposes. While designed with security in mind, users must be aware of potential security implications when deploying to production.

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Security Considerations

### 1. Sensitive Data in Alerts

**⚠️ CRITICAL: Error tracebacks and exception messages may contain sensitive information.**

The module automatically sanitizes the following:
- HTTP headers (Authorization, Cookie, API keys)
- Database connection strings
- Passwords and tokens in error messages
- AWS credentials
- Query parameters with sensitive names

However, you should still:

#### Configure Alert Verbosity
```python
# Limit traceback lines sent to Telegram
monitoring_config.ALERT_MAX_TRACEBACK_LINES = 5  # Default: 15

# Or disable tracebacks entirely for very sensitive apps
monitoring_config.ALERT_MAX_TRACEBACK_LINES = 0
```

#### Ignore Sensitive Paths
```python
monitoring_config.IGNORED_PATHS = [
    "/auth/login",
    "/admin",
    "/payment/process",
    "/api/sensitive-endpoint",
]
```

#### Review Before Production
1. Test alerts in staging environment first
2. Review what data appears in test alerts
3. Adjust `IGNORED_PATHS` and `IGNORED_EXCEPTIONS` accordingly

### 2. Multi-Worker Deployments

**⚠️ Redis is REQUIRED for production deployments with multiple workers/processes.**

Without Redis:
- ❌ Duplicate alerts from each worker
- ❌ No shared deduplication
- ❌ Inaccurate statistics
- ❌ Potential alert spam

```python
# ❌ UNSAFE for multi-worker production
setup_monitoring(app)

# ✅ SAFE for multi-worker production
from redis import asyncio as aioredis
redis_client = aioredis.from_url("redis://localhost")
setup_monitoring(app, redis_client=redis_client)
```

### 3. Telegram Bot Security

#### Bot Token Protection
- **NEVER commit** `TELEGRAM_BOT_TOKEN` to version control
- Use environment variables or secret management
- Rotate tokens periodically (every 90 days recommended)

```bash
# .env (add to .gitignore!)
MONITORING_TELEGRAM_BOT_TOKEN=your_token_here
MONITORING_TELEGRAM_CHAT_ID=your_chat_id
```

#### Chat/Channel Security
- Use **private groups** or channels for production alerts
- Enable **2-factor authentication** on admin Telegram accounts
- Limit bot permissions to only **send messages**
- Use **separate bots** for different environments (dev/staging/prod)
- Regularly audit group members

#### Rate Limiting
Telegram API has rate limits. Respect them:
```python
# Prevent hitting rate limits
monitoring_config.ALERT_RATE_LIMIT_MINUTES = 10  # Min time between same error
monitoring_config.BATCH_WINDOW_MINUTES = 15      # Batch non-critical alerts
```

### 4. Data Retention

#### Redis Data
- Monitoring data expires automatically (default: 24 hours)
- Adjust retention if needed:
```python
monitoring_config.REDIS_KEY_TTL_HOURS = 24  # Adjust as needed
```

#### Telegram Messages
- Messages in Telegram are **permanent** unless manually deleted
- Consider message retention policies for compliance
- Use private channels with appropriate data handling policies

### 5. Access Control

#### Application Level
```python
# Restrict health check endpoint
@app.get("/health")
async def health_check(api_key: str = Header(...)):
    if api_key != os.getenv("HEALTH_CHECK_API_KEY"):
        raise HTTPException(401)
    # ... health check logic
```

#### Telegram Level
- Create monitoring-specific Telegram accounts
- Use bot access restrictions in BotFather
- Implement IP whitelisting for bot API calls if possible

## Known Limitations

### Automatic Sanitization

While the module sanitizes many common patterns, it cannot catch everything:

1. **Custom sensitive fields**: Add your own patterns if needed
2. **Business logic secrets**: May require custom exception handlers
3. **PII in variable names**: Could still appear in tracebacks

### Example: Custom Sanitization

```python
from monitoring.security_utils import SENSITIVE_PATTERNS

# Add custom patterns
SENSITIVE_PATTERNS.append(
    (re.compile(r'customer_id:\s*\d+', re.IGNORECASE), 'customer_id:***')
)
```

## Reporting a Vulnerability

If you discover a security vulnerability, please email security@yourproject.com instead of using the issue tracker.

### What to Include

1. Description of the vulnerability
2. Steps to reproduce
3. Potential impact
4. Suggested fix (if any)

### Response Timeline

- **Initial response**: Within 48 hours
- **Status update**: Within 7 days
- **Fix timeline**: Depends on severity
  - Critical: 24-48 hours
  - High: 7 days
  - Medium: 30 days
  - Low: Next release

## Security Best Practices

### Deployment Checklist

Before deploying to production:

- [ ] Redis configured and connected
- [ ] `TELEGRAM_BOT_TOKEN` in secrets/env vars (not in code)
- [ ] Using private Telegram group/channel
- [ ] Tested alerts in staging environment
- [ ] Reviewed alert content for sensitive data
- [ ] `IGNORED_PATHS` configured for sensitive endpoints
- [ ] `ALERT_MAX_TRACEBACK_LINES` set appropriately
- [ ] Rate limiting configured (`ALERT_RATE_LIMIT_MINUTES`)
- [ ] Separate bots for different environments
- [ ] Bot permissions minimized in BotFather
- [ ] Team members trained on alert handling
- [ ] Data retention policy documented

### Regular Maintenance

- [ ] Review and rotate Telegram bot token quarterly
- [ ] Audit Telegram group membership monthly
- [ ] Review `IGNORED_PATHS` as endpoints change
- [ ] Test alert sanitization with new features
- [ ] Monitor Redis memory usage
- [ ] Review Telegram message history for leaks

### Compliance Considerations

If your application handles:
- **PII (Personal Identifiable Information)**
- **PHI (Protected Health Information)**
- **PCI (Payment Card Information)**
- **Financial data**

Additional steps required:
1. Implement custom sanitization for domain-specific data
2. Consider disabling tracebacks entirely
3. Use separate, compliant monitoring for sensitive endpoints
4. Document data flows in privacy policy
5. Implement alert retention policies

## Security Updates

Subscribe to security announcements:
- GitHub Security Advisories
- Release notes for security patches
- Security mailing list (if available)

## Contact

- **Security issues**: security@yourproject.com
- **General support**: GitHub Issues
- **Urgent security issues**: Contact maintainers directly

---

**Last updated**: 2024-01-15  
**Version**: 1.0.0