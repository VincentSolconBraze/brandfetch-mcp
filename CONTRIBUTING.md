# Contributing to Brandfetch MCP Server

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Set up your development environment:

```bash
# Install dependencies
uv add --dev

# Install pre-commit hooks
pre-commit install
```

## Development Guidelines

### Code Style

This project uses:
- [Ruff](https://github.com/astral-sh/ruff) for linting and formatting
- Type hints for all functions
- Docstrings for all public functions

### Commits

- Use clear, descriptive commit messages
- Reference issue numbers when applicable

### Pull Requests

1. Create a new branch for your feature or bugfix
2. Make your changes
3. Run tests and ensure pre-commit hooks pass
4. Submit a pull request with a clear description of the changes

### Testing

- Write tests for all new functionality
- Ensure existing tests continue to pass

## Release Process

1. Version bumps follow [Semantic Versioning](https://semver.org/)
2. Update version in `pyproject.toml`
3. Update documentation as needed
4. Create a GitHub release

## Documentation

- Keep documentation up to date with code changes
- Use clear, concise language
- Include examples where appropriate