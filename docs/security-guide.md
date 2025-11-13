# Security Guide for Production Deployment

This guide covers security considerations when deploying fastapi-telemon to production.

## Quick Security Checklist

Before deploying to production, ensure:

- [ ] Redis configured and secured
- [ ] Telegram bot token in secret management
- [ ] Private Telegram group/channel configured
- [ ] `IGNORED_PATHS` set for sensitive endpoints
- [ ] `ALERT_MAX_TRACEBACK_LINES` reviewed and limited
- [ ] Multi-worker setup tested with Redis
- [ ] Security scan completed (`safety check`, `bandit`)
- [ ] Team trained on sensitive data handling
- [ ] Incident response plan documented

## 1. Sensitive Data in Tracebacks

### The Problem

Error tracebacks can expose:

```python
# ❌ This error might expose:
def process_payment(card_number, cvv, api_key):
    validate_card(card_number)  # card_number in traceback
    charge_api(api_key=api_key)  # api_key in traceback
```

### Solutions

#### Option 1: Limit Traceback Lines

```python
# Show only first 5 lines
monitoring_config.ALERT_MAX_TRACEBACK_LINES = 5

# Or disable completely for sensitive apps
monitoring_config.ALERT_MAX_TRACEBACK_LINES = 0
```

#### Option 2: Exclude Sensitive Endpoints

```python
monitoring_config.IGNORED_PATHS = [
    "/auth/login",
    "/auth/reset-password",
    "/payment",
    "/admin",
    "/api/keys",
]
```

#### Option 3: Custom Exception Handler

```python
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def custom_exception_handler(request: Request, exc: Exception):
    # Log locally but don't send to Telegram
    if request.url.path.startswith("/payment"):
        logger.error(f"Payment error: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Payment processing error"}
        )
    
    # Let monitoring handle other errors
    raise exc
```

#### Option 4: Sanitize Before Sending

```python
from monitoring import telegram_reporter

class SanitizedReporter(telegram_reporter.__class__):
    def _sanitize_traceback(self, tb: str) -> str:
        import re
        # Remove common sensitive patterns
        patterns = [
            (r'password["\']:\s*["\'][^"\']+["\']', 'password":"***"'),
            (r'api_key["\']:\s*["\'][^"\']+["\']', 'api_key":"***"'),
            (r'token["\']:\s*["\'][^"\']+["\']', 'token":"***"'),
            (r'\d{13,19}', '****CARD****'),  # Credit card numbers
        ]
        
        for pattern, replacement in patterns:
            tb = re.sub(pattern, replacement, tb, flags=re.IGNORECASE)
        
        return tb
    
    async def send_alert(self, **kwargs):
        if 'traceback_str' in kwargs and kwargs['traceback_str']:
            kwargs['traceback_str'] = self._sanitize_traceback(
                kwargs['traceback_str']
            )
        return await super().send_alert(**kwargs)
```

## 2. Multi-Worker Security

### The Problem

Without Redis, each worker sends duplicate alerts:

```
Worker 1: 🔴 ERROR 500 - ValueError in /api/users
Worker 2: 🔴 ERROR 500 - ValueError in /api/users
Worker 3: 🔴 ERROR 500 - ValueError in /api/users
Worker 4: 🔴 ERROR 500 - ValueError in /api/users
```

This exposes the same sensitive information 4 times!

### Solution: Secure Redis Setup

```python
from redis import asyncio as aioredis

# ✅ Production Redis configuration
redis_client = aioredis.from_url(
    "rediss://username:password@redis-host:6379/0",  # Note: rediss:// for TLS
    ssl_cert_reqs="required",
    ssl_ca_certs="/path/to/ca.crt",
    decode_responses=True
)

setup_monitoring(app, redis_client=redis_client)
```

### Redis Security Checklist

```bash
# In redis.conf:
requirepass your_strong_password
bind 127.0.0.1  # Or your private network
protected-mode yes
maxmemory 256mb
maxmemory-policy allkeys-lru

# Enable TLS/SSL
tls-port 6380
tls-cert-file /path/to/redis.crt
tls-key-file /path/to/redis.key
tls-ca-cert-file /path/to/ca.crt
```

## 3. Telegram Bot Security

### Bot Token Protection

```python
# ❌ NEVER do this
TELEGRAM_BOT_TOKEN = "123456:ABC-hardcoded-token"

# ✅ Use environment variables
import os
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# ✅✅ Use secret management
from your_secret_manager import get_secret
TELEGRAM_BOT_TOKEN = get_secret("telegram-bot-token")
```

### Telegram Group Security

1. **Create Private Groups**
   - Settings → Group Type → Private
   - Don't share invite links publicly
   - Use invite links with user limits

2. **Separate Environments**
   - Development bot → Dev Telegram group
   - Staging bot → Staging Telegram group
   - Production bot → Production Telegram group

3. **Access Control**
   ```python
   # Development
   if monitoring_config.MONITORING_ENV == "development":
       monitoring_config.TELEGRAM_CHAT_ID = "-1001234567890"
   
   # Production
   elif monitoring_config.MONITORING_ENV == "production":
       monitoring_config.TELEGRAM_CHAT_ID = "-1009876543210"
   ```

4. **Regular Audits**
   - Review group members monthly
   - Remove ex-employees immediately
   - Monitor for suspicious activity

## 4. Rate Limiting & Abuse Prevention

### Telegram API Limits

Telegram limits: ~30 messages/second per bot

### Configure Appropriate Limits

```python
# Prevent spam from repeated errors
monitoring_config.ALERT_RATE_LIMIT_MINUTES = 10

# Batch non-critical alerts
monitoring_config.BATCH_WINDOW_MINUTES = 15

# Limit slow request alerts
monitoring_config.SLOW_REQUESTS_BATCH_MINUTES = 15
```

### Monitor Usage

```python
from monitoring import telegram_reporter

# Add custom metrics
class MeteredReporter(telegram_reporter.__class__):
    def __init__(self):
        super().__init__()
        self.message_count = 0
        self.last_reset = time.time()
    
    async def send_message(self, **kwargs):
        # Track usage
        self.message_count += 1
        
        # Reset counter every hour
        if time.time() - self.last_reset > 3600:
            logger.info(f"Telegram messages sent: {self.message_count}/hour")
            self.message_count = 0
            self.last_reset = time.time()
        
        return await super().send_message(**kwargs)
```

## 5. Environment-Specific Configuration

### Development

```env
# .env.development
MONITORING_ENV=development
TELEGRAM_BOT_TOKEN=dev_bot_token
TELEGRAM_CHAT_ID=dev_group_id
ALERT_MAX_TRACEBACK_LINES=20  # More detail for debugging
ALERT_RATE_LIMIT_MINUTES=1    # Faster testing
MONITORING_IGNORED_PATHS=/health,/metrics
```

### Production

```env
# .env.production
MONITORING_ENV=production
TELEGRAM_BOT_TOKEN=${SECRET_TELEGRAM_TOKEN}  # From secret manager
TELEGRAM_CHAT_ID=${SECRET_TELEGRAM_CHAT}
ALERT_MAX_TRACEBACK_LINES=5   # Limit sensitive data
ALERT_RATE_LIMIT_MINUTES=10   # Prevent spam
MONITORING_IGNORED_PATHS=/health,/metrics,/auth,/payment,/admin
```

## 6. Incident Response

### When Sensitive Data is Exposed

1. **Immediate Actions:**
   - Delete Telegram messages containing sensitive data
   - Rotate exposed credentials immediately
   - Disable affected bot temporarily
   - Review audit logs

2. **Follow-up:**
   - Investigate how data was exposed
   - Update `IGNORED_PATHS` configuration
   - Reduce `ALERT_MAX_TRACEBACK_LINES`
   - Implement additional sanitization
   - Document incident for team

3. **Prevention:**
   - Regular security reviews
   - Automated sensitive data detection
   - Team training on security practices

### Audit Log Example

```python
import logging

# Configure audit logger
audit_logger = logging.getLogger('monitoring.audit')
audit_logger.setLevel(logging.INFO)
audit_handler = logging.FileHandler('monitoring_audit.log')
audit_logger.addHandler(audit_handler)

# Track all alerts sent
from monitoring import telegram_reporter

class AuditedReporter(telegram_reporter.__class__):
    async def send_alert(self, title, message, **kwargs):
        # Log to audit trail
        audit_logger.info(
            f"Alert sent: {title} | "
            f"Level: {kwargs.get('level', 'UNKNOWN')} | "
            f"Env: {monitoring_config.MONITORING_ENV}"
        )
        
        return await super().send_alert(title, message, **kwargs)
```

## 7. Security Scanning

### Before Each Release

```bash
# Check for known vulnerabilities
pip install safety
safety check

# Security linting
pip install bandit
bandit -r monitoring/

# Check dependencies
pip-audit
```

### Continuous Integration

```yaml
# .github/workflows/security.yml
name: Security Scan

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          pip install safety bandit
          pip install -e .
      - name: Run safety check
        run: safety check
      - name: Run bandit
        run: bandit -r monitoring/
```

## 8. Compliance Considerations

### GDPR

- User data in alerts may be personal data
- Ensure proper consent and data processing agreements
- Implement data retention policies
- Document data flows

### PCI DSS

- Never log full credit card numbers
- Sanitize payment-related data
- Exclude payment endpoints from monitoring
- Regular security audits

### Example: PCI-Compliant Configuration

```python
monitoring_config.IGNORED_PATHS = [
    "/payment",
    "/checkout",
    "/billing",
]

monitoring_config.ALERT_MAX_TRACEBACK_LINES = 0  # No tracebacks

# Custom sanitization for payment errors
@app.exception_handler(PaymentException)
async def payment_exception_handler(request, exc):
    # Log sanitized version only
    logger.error(f"Payment error: {type(exc).__name__}")
    
    # Send generic alert without details
    await telegram_reporter.send_alert(
        title="Payment System Error",
        message="A payment processing error occurred",
        level=AlertLevel.CRITICAL,
        details={"Type": "Payment", "Status": "Failed"}
    )
    
    return JSONResponse(status_code=500, content={"error": "Payment failed"})
```

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Telegram Bot Security](https://core.telegram.org/bots/security)
- [Redis Security](https://redis.io/docs/management/security/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)

## Getting Help

Security questions? Contact:
- GitHub Security Advisories: [Report Vulnerability](https://github.com/humangpts/fastapi-telemon/security/advisories/new)
- Email: humangpts@users.noreply.github.com

---

**Remember**: Security is a process, not a destination. Regular reviews and updates are essential!