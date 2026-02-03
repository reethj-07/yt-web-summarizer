# Contributing to Content Summarizer Pro

We appreciate your interest in contributing! This guide will help you get started.

## Code of Conduct

Be respectful, inclusive, and professional in all interactions.

## Getting Started

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Write tests for new functionality
5. Ensure tests pass: `pytest test_app.py -v`
6. Commit: `git commit -m "Add your feature"`
7. Push: `git push origin feature/your-feature`
8. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/yt-web-summarizer.git
cd yt-web-summarizer

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install with dev dependencies
pip install -r requirements.txt

# Run tests
pytest test_app.py -v

# Format code
black .

# Lint code
pylint **/*.py
```

## Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for all functions
- Keep functions focused and testable

## Testing Requirements

- All new features must include tests
- Tests should cover both happy path and error cases
- Run `pytest --cov` to check coverage
- Aim for >80% coverage

## Commit Messages

```
<type>: <subject>

<body>

<footer>
```

Types: feat, fix, docs, style, refactor, test, chore

Examples:
```
feat: add multi-language support
fix: resolve rate limiting issue
docs: update deployment guide
```

## Pull Request Process

1. Update README.md if adding features
2. Update requirements.txt if adding dependencies
3. Add tests for new functionality
4. Ensure CI/CD passes
5. Request review from maintainers
6. Address review comments

## Reporting Issues

- Use GitHub Issues
- Include version information
- Provide minimal reproducible example
- Describe expected vs actual behavior

## Feature Requests

- Open GitHub Discussion
- Describe use case and benefits
- Consider performance impact
- Discuss before implementing

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🙏
