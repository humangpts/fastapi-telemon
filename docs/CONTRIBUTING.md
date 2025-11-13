# Contributing to FastAPI TeleMon

Thank you for considering contributing to FastAPI TeleMon! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

**When filing a bug report, include:**
- **Clear title** describing the issue
- **Detailed description** of the problem
- **Steps to reproduce** the behavior
- **Expected behavior** vs actual behavior
- **Environment details:**
  - Python version
  - FastAPI version
  - fastapi-telemon version
  - Redis version (if applicable)
- **Code snippets** or minimal reproduction example
- **Error messages** and tracebacks (sanitized!)

**Example:**
```markdown
**Bug:** Alerts not sent in multi-worker setup

**Steps to reproduce:**
1. Deploy with Uvicorn workers=4
2. Configure monitoring without Redis
3. Trigger error endpoint
4. Observe multiple duplicate alerts

**Expected:** Single alert via deduplication
**Actual:** 4 duplicate alerts (one per worker)

**Environment:**
- Python 3.12
- FastAPI 0.115.0
- fastapi-telemon 1.0.0
- Redis: Not configured
```

### Suggesting Features

Feature requests are welcome! Please provide:
- **Clear use case** - why is this needed?
- **Proposed solution** - how should it work?
- **Alternatives considered** - what other approaches did you think about?
- **Additional context** - mockups, examples, etc.

### Security Issues

**Do not report security issues in public issues!**

Please see [SECURITY.md](SECURITY.md) for reporting security vulnerabilities.

## Development Setup

### Prerequisites

- Python 3.12+
- Git
- Redis (for integration tests)

### Setting Up Development Environment

1. **Fork and clone:**
```bash
git clone https://github.com/YOUR_USERNAME/fastapi-telemon.git
cd fastapi-telemon
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install development dependencies:**
```bash
pip install -e ".[dev]"
```

4. **Install pre-commit hooks:**
```bash
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=monitoring --cov-report=html

# Run specific test file
pytest tests/test_middleware.py

# Run specific test
pytest tests/test_middleware.py::test_normal_request
```

### Code Style

We use:
- **Black** for formatting
- **Ruff** for linting
- **MyPy** for type checking

```bash
# Format code
black .

# Lint code
ruff check .

# Type check
mypy monitoring
```

### Running Pre-commit Checks

```bash
pre-commit run --all-files
```

## Pull Request Process

### Before Submitting

1. **Create a feature branch:**
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

2. **Make your changes:**
- Follow existing code style
- Add tests for new features
- Update documentation
- Keep commits focused and atomic

3. **Run tests and checks:**
```bash
pytest
black .
ruff check .
mypy monitoring
```

4. **Update CHANGELOG.md:**
Add your changes under `[Unreleased]` section:
```markdown
### Added
- Feature: Your new feature description

### Fixed
- Bug: Your bug fix description
```

### Submitting PR

1. **Push to your fork:**
```bash
git push origin feature/your-feature-name
```

2. **Create Pull Request:**
- Clear title describing the change
- Reference related issues (e.g., "Fixes #123")
- Describe what changed and why
- Include screenshots/examples if relevant

3. **PR Description Template:**
```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Fixes #123

## How Has This Been Tested?
- [ ] Unit tests
- [ ] Integration tests
- [ ] Manual testing

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] All tests pass
```

### Review Process

- Maintainers will review your PR
- Address review comments
- Once approved, a maintainer will merge

## Development Guidelines

### Code Style

- Follow PEP 8
- Use type hints everywhere
- Write docstrings for public APIs
- Keep functions focused and small

**Example:**
```python
async def send_alert(
    self,
    title: str,
    message: str,
    level: AlertLevel = AlertLevel.WARNING,
    details: Optional[Dict[str, Any]] = None,
) -> bool:
    """
    Send formatted alert message.
    
    Args:
        title: Alert title
        message: Main message
        level: Alert severity
        details: Additional details dict
        
    Returns:
        True if sent successfully
        
    Raises:
        ValueError: If title is empty
    """
    # Implementation
```

### Testing

- Write tests for all new features
- Maintain >80% code coverage
- Include both unit and integration tests
- Use fixtures for common setup

**Example:**
```python
@pytest.mark.asyncio
async def test_send_alert_success(mock_telegram_client):
    """Test successful alert sending"""
    reporter = TelegramReporter()
    reporter.client = mock_telegram_client
    
    result = await reporter.send_alert(
        title="Test",
        message="Test message",
        level=AlertLevel.INFO
    )
    
    assert result is True
    mock_telegram_client.post.assert_called_once()
```

### Documentation

- Update README.md for user-facing changes
- Update docstrings for API changes
- Add examples for new features
- Keep documentation clear and concise

### Commit Messages

Use conventional commits format:

```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation only
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

**Examples:**
```
feat(telegram): add rate limiting for API calls

Implement exponential backoff when hitting Telegram rate limits.
Respects Retry-After header from API responses.

Fixes #42

---

fix(middleware): correct fire-and-forget task cleanup

Tasks were not being properly removed from tracking set,
causing memory leaks in long-running applications.

---

docs(readme): add security best practices section

Covers sensitive data in tracebacks and multi-worker setup.
```

## Project Structure

```
fastapi-telemon/
├── monitoring/           # Main package
│   ├── __init__.py      # Public API
│   ├── config.py        # Configuration
│   ├── middleware.py    # Exception monitoring
│   ├── telegram.py      # Telegram integration
│   ├── adapters.py      # Database/Redis/Queue adapters
│   ├── decorators.py    # Utility decorators
│   ├── tasks.py         # Background tasks
│   ├── batch_alerts.py  # Alert batching
│   ├── arq_monitoring.py # ARQ integration
│   └── utils.py         # Utilities
├── tests/               # Test suite
│   ├── conftest.py      # Test fixtures
│   ├── test_*.py        # Test files
│   └── ...
├── examples/            # Usage examples
│   ├── basic_setup.py
│   ├── with_redis.py
│   └── ...
├── docs/                # Additional documentation
├── .env.example         # Example configuration
├── pyproject.toml       # Package configuration
├── requirements.txt     # Dependencies
├── requirements-dev.txt # Dev dependencies
├── README.md           # Main documentation
├── CHANGELOG.md        # Version history
├── CONTRIBUTING.md     # This file
├── SECURITY.md         # Security policy
└── LICENSE             # MIT License
```

## Release Process

(For maintainers)

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create release branch: `git checkout -b release/v1.x.x`
4. Run all tests: `pytest`
5. Build package: `python -m build`
6. Test on TestPyPI
7. Create Git tag: `git tag v1.x.x`
8. Push tag: `git push origin v1.x.x`
9. Publish to PyPI: `twine upload dist/*`
10. Create GitHub release

## Questions?

- 📖 Check [README.md](README.md)
- 🐛 Search [existing issues](https://github.com/humangpts/fastapi-telemon/issues)
- 💬 Start a [discussion](https://github.com/humangpts/fastapi-telemon/discussions)
- 📧 Email: humangpts@users.noreply.github.com

## Recognition

Contributors will be recognized in:
- GitHub contributors page
- Release notes
- CHANGELOG.md (for significant contributions)

Thank you for helping make FastAPI TeleMon better! 🎉