## Description

<!-- Provide a brief description of the changes in this PR -->

## Type of Change

<!-- Mark the relevant option with an "x" -->

- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ✨ New feature (non-breaking change which adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📝 Documentation update
- [ ] 🎨 Code style update (formatting, renaming)
- [ ] ♻️ Code refactoring (no functional changes)
- [ ] ⚡ Performance improvement
- [ ] ✅ Test update
- [ ] 🔧 Build/CI configuration change
- [ ] 🔒 Security fix

## Related Issues

<!-- Link related issues here using #issue_number -->

Fixes #
Closes #
Related to #

## Changes Made

<!-- Describe the changes in detail -->

- 
- 
- 

## Testing

<!-- Describe how you tested these changes -->

### Test Coverage

- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

### Test Results

```bash
# Paste relevant test output
pytest --cov
```

## Security Considerations

<!-- If this PR involves security changes, describe them here -->

- [ ] No sensitive data exposed in logs/alerts
- [ ] Security documentation reviewed/updated
- [ ] No new security vulnerabilities introduced
- [ ] Security scan passed (`bandit`, `safety check`)

## Breaking Changes

<!-- If this PR introduces breaking changes, describe them and the migration path -->

### Before
```python
# Old API
```

### After
```python
# New API
```

### Migration Guide

<!-- Steps for users to migrate from old to new API -->

1. 
2. 
3. 

## Documentation

- [ ] README.md updated
- [ ] CHANGELOG.md updated
- [ ] Docstrings added/updated
- [ ] Examples added/updated
- [ ] Type hints added/updated

## Code Quality

- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] No unnecessary comments or debug code
- [ ] No console.log or print statements (except logging)

## Pre-commit Checks

- [ ] `black .` (code formatting)
- [ ] `ruff check .` (linting)
- [ ] `mypy monitoring` (type checking)
- [ ] `pytest` (all tests pass)
- [ ] `safety check` (security scan)
- [ ] `pre-commit run --all-files` (all checks pass)

## Checklist

<!-- Mark completed items with an "x" -->

- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published in downstream modules
- [ ] I have updated the CHANGELOG.md
- [ ] All sensitive data has been sanitized from tests and examples

## Screenshots

<!-- If applicable, add screenshots to demonstrate the changes -->

## Additional Notes

<!-- Any additional information that reviewers should know -->

---

**Reviewer Notes:**
<!-- This section is for reviewers to add their comments -->

### Review Checklist

- [ ] Code quality and style
- [ ] Test coverage adequate
- [ ] Documentation complete
- [ ] No security concerns
- [ ] Breaking changes properly handled
- [ ] Performance implications considered