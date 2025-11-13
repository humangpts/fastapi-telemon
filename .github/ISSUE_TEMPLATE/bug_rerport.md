---
name: Bug Report
about: Create a report to help us improve
title: '[BUG] '
labels: bug
assignees: ''

---

**⚠️ Security Notice**
If this is a security vulnerability, please **DO NOT** create a public issue. Instead, report it via [GitHub Security Advisories](https://github.com/humangpts/fastapi-telemon/security/advisories/new) or email humangpts@users.noreply.github.com.

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Configure monitoring with '...'
2. Make request to '...'
3. See error '...'

**Expected behavior**
A clear and concise description of what you expected to happen.

**Actual behavior**
What actually happened instead.

**Code snippet**
```python
# Minimal reproducible example
# Please sanitize any sensitive data!
from monitoring import setup_monitoring

# Your code here
```

**Environment**
- OS: [e.g. Ubuntu 22.04, macOS 14, Windows 11]
- Python version: [e.g. 3.12.0]
- FastAPI version: [e.g. 0.115.0]
- fastapi-telemon version: [e.g. 1.0.0]
- Redis version (if applicable): [e.g. 7.0]
- Deployment: [e.g. Uvicorn, Gunicorn, Docker]
- Workers: [e.g. single worker, 4 workers]

**Configuration**
```env
# Relevant configuration (sanitize tokens!)
MONITORING_ENV=production
MONITORING_ENABLED=true
# ... other relevant settings
```

**Logs**
```
# Relevant error messages or logs
# Please sanitize any sensitive data!
```

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Additional context**
Add any other context about the problem here.

**Checklist**
- [ ] I have searched existing issues to avoid duplicates
- [ ] I have sanitized all sensitive data from this report
- [ ] I have included a minimal reproducible example
- [ ] I have included relevant environment information