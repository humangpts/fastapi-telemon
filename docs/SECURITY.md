# Security Policy

## Supported Versions

We provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via:
- Email: humangpts@users.noreply.github.com
- GitHub Security Advisories (preferred): [Report a vulnerability](https://github.com/humangpts/fastapi-telemon/security/advisories/new)

You should receive a response within 48 hours. If for some reason you do not, please follow up via email to ensure we received your original message.

Please include the following information:
- Type of issue (e.g., information disclosure, authentication bypass, etc.)
- Full paths of source file(s) related to the manifestation of the issue
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

## Security Best Practices

### 1. Protect Your Bot Token

**Critical:** Your `TELEGRAM_BOT_TOKEN` is a secret credential.

✅ **DO:**
- Store in environment variables
- Use secret management systems (AWS Secrets Manager, HashiCorp Vault, etc.)
- Rotate tokens periodically
- Use different tokens for dev/staging/production
- Keep tokens out of Git history

❌ **DON'T:**
- Hardcode in source code
- Commit to version control
- Share in public channels
- Log to files
- Include in error messages

### 2. Traceback Data Exposure

Error tracebacks may contain sensitive information:
- Database credentials
- API keys in environment variables
- User data in local variables
- Internal file paths
- Business logic details

**Mitigation:**

```python
# Option 1: Reduce traceback lines
monitoring_config.ALERT_MAX_TRACEBACK_LINES = 5  # or 0 to disable

# Option 2: Ignore sensitive paths
monitoring_config.IGNORED_PATHS = [
    "/auth",
    "/payment",
    "/admin",
]

# Option 3: Custom sanitization
from monitoring import telegram_reporter

class SanitizedReporter(telegram_reporter.__class__):
    async def send_alert(self, **kwargs):
        # Sanitize traceback before sending
        if 'traceback_str' in kwargs:
            kwargs['traceback_str'] = self._sanitize(kwargs['traceback_str'])
        return await super().send_alert(**kwargs)
    
    def _sanitize(self, traceback: str) -> str:
        # Remove sensitive patterns
        import re
        traceback = re.sub(r'password["\']:\s*["\'][^"\']+["\']', 'password":"***"', traceback)
        traceback = re.sub(r'token["\']:\s*["\'][^"\']+["\']', 'token":"***"', traceback)
        return traceback
```

### 3. Multi-Worker Security

**Without Redis:** Each worker has separate deduplication, potentially exposing the same error multiple times.

**With Redis:** Ensure Redis is secured:
- Use authentication (`requirepass`)
- Bind to localhost or private network only
- Use TLS for remote connections
- Regular security updates
- Monitor for unauthorized access

```python
# Secure Redis connection
from redis import asyncio as aioredis

redis_client = aioredis.from_url(
    "rediss://username:password@redis-host:6379/0",  # SSL/TLS
    ssl_cert_reqs="required",
    ssl_ca_certs="/path/to/ca.crt"
)
```

### 4. Telegram Chat Security

**Protect your alert destination:**

✅ **DO:**
- Use private groups/channels
- Enable 2FA on Telegram accounts
- Limit group membership
- Review member list regularly
- Use separate groups per environment
- Monitor group access logs

❌ **DON'T:**
- Use public channels for production alerts
- Share invite links publicly
- Add unnecessary members
- Use personal chats for production

### 5. Rate Limiting

**Prevent abuse and API quota exhaustion:**

```python
# Configure appropriate limits
monitoring_config.ALERT_RATE_LIMIT_MINUTES = 10
monitoring_config.BATCH_WINDOW_MINUTES = 15

# Monitor your Telegram API usage
# Telegram limits: ~30 messages/second per bot
```

### 6. Data Retention

**Minimize sensitive data lifetime:**

```python
# Adjust retention
monitoring_config.REDIS_KEY_TTL_HOURS = 24  # Default

# Clean up old data regularly
from monitoring import get_redis_adapter

async def cleanup_old_monitoring_data():
    redis = get_redis_adapter()
    # Implement custom cleanup logic
    pass
```

### 7. Access Control

**Implement proper authentication:**

```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.post("/admin/trigger-alert")
async def trigger_alert(token = Depends(security)):
    # Verify token before allowing alert triggers
    if not verify_admin_token(token.credentials):
        raise HTTPException(403)
    
    await telegram_reporter.send_alert(...)
```

### 8. Input Validation

**Sanitize user input before logging:**

```python
from monitoring import telegram_reporter

# ❌ Dangerous - user input in alert
await telegram_reporter.send_alert(
    title="User Error",
    message=f"User {user_input} failed"  # Could contain malicious content
)

# ✅ Safe - sanitized input
from html import escape

await telegram_reporter.send_alert(
    title="User Error",
    message=f"User {escape(user_input[:100])} failed"  # Limited and escaped
)
```

### 9. Dependency Security

**Keep dependencies updated:**

```bash
# Check for vulnerabilities
pip install safety
safety check

# Update dependencies
pip install --upgrade fastapi-telemon

# Monitor GitHub security advisories
# Enable Dependabot on your repository
```

### 10. Production Deployment Checklist

Before deploying to production:

- [ ] Redis deployed and secured
- [ ] Bot token in secret management system
- [ ] Private Telegram group configured
- [ ] Sensitive paths added to `IGNORED_PATHS`
- [ ] Traceback lines limited or disabled
- [ ] Rate limits configured
- [ ] Data retention policies set
- [ ] Access controls implemented
- [ ] Security scan performed (`safety check`)
- [ ] Dependencies up to date
- [ ] Monitoring tested in staging
- [ ] Incident response plan documented
- [ ] Team trained on security practices

## Known Limitations

### 1. Traceback Content

We cannot automatically sanitize all sensitive data from tracebacks. You must configure `IGNORED_PATHS` and `ALERT_MAX_TRACEBACK_LINES` appropriately for your application.

### 2. Telegram Storage

Messages sent to Telegram are stored on Telegram's servers. Consider this when deciding what information to send.

### 3. Redis Security

We do not implement Redis encryption at rest. Use Redis Enterprise or similar if you need this feature.

### 4. No Authentication

This package does not provide authentication for Telegram webhooks or admin endpoints. You must implement this yourself.

## Security Updates

We will announce security updates via:
- GitHub Security Advisories
- Release notes in CHANGELOG.md
- Git tags with `security` label

Subscribe to repository notifications to stay informed.

## Acknowledgments

We appreciate responsible disclosure from the security community. Contributors who report valid security issues will be acknowledged in our security advisories (unless they prefer to remain anonymous).

## Contact

For security concerns, contact:
- Security issues: GitHub Security Advisories (preferred)
- General questions: humangpts@users.noreply.github.com

---

Last updated: 2025-11-15