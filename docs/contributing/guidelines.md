# Contributing to Pyvider

Thank you for your interest in contributing to Pyvider! This guide will help you get started with contributing code, documentation, or bug reports.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Testing Requirements](#testing-requirements)
- [Documentation Updates](#documentation-updates)
- [Pull Request Process](#pull-request-process)
- [Code Style Guidelines](#code-style-guidelines)
- [Reporting Bugs](#reporting-bugs)
- [Requesting Features](#requesting-features)

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](code-of-conduct.md). Please read it before contributing.

## Getting Started

### First Time Contributors

Welcome! Here's how to get started:

1. **Look for "good first issue" labels** in the [issue tracker](https://github.com/provide-io/pyvider/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)
2. **Read the architecture docs** to understand how Pyvider works:
   - [Architecture Overview](../explanation/architecture.md)
   - [Component Model](../explanation/component-model.md)
3. **Ask questions** in [GitHub Discussions](https://github.com/provide-io/pyvider/discussions)

### Prerequisites

- Python 3.11 or higher
- Git
- [uv](https://github.com/astral-sh/uv)
- Basic understanding of Terraform concepts
- Familiarity with async/await in Python

## Development Workflow

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR-USERNAME/pyvider.git
cd pyvider

# Add upstream remote
git remote add upstream https://github.com/provide-io/pyvider.git
```

### 2. Set Up Development Environment

```bash
# Install dependencies with uv (recommended)
uv sync --group dev
```

### 3. Create a Branch

```bash
# Update your main branch
git checkout main
git pull upstream main

# Create a feature branch
git checkout -b feature/my-new-feature
# Or for bug fixes:
git checkout -b fix/issue-123
```

### 4. Make Changes

See `CLAUDE.md` in the repository root for detailed development commands:

```bash
# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=pyvider

# Run linting
uv run ruff check

# Auto-fix linting issues
uv run ruff check --fix

# Format code
uv run ruff format

# Type checking
uv run mypy src/pyvider
```

### 5. Commit Your Changes

```bash
# Stage your changes
git add .

# Commit with a descriptive message
git commit -m "Add feature: description of what you added"
```

**Commit Message Guidelines:**
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- First line should be 50 characters or less
- Reference issues and PRs liberally

## Testing Requirements

### Before Submitting a PR

Your PR must include tests and pass all checks:

```bash
# 1. Run the full test suite
uv run pytest

# 2. Check test coverage (should be >80% for new code)
uv run pytest --cov=pyvider --cov-report=term-missing

# 3. Run linters
uv run ruff check

# 4. Run type checker
uv run mypy src/pyvider

# 5. Format code
uv run ruff format

# All of these must pass before your PR can be merged
```

### Writing Tests

- **Unit tests** for individual functions and classes
- **Integration tests** for protocol handlers
- **Async tests** using `pytest.mark.asyncio`
- **Property-based tests** using Hypothesis where appropriate

Example test structure:

```python
import pytest
from pyvider.resources.context import ResourceContext
from my_module import MyResource

@pytest.mark.asyncio
async def test_resource_creation():
    """Test that resource creation works correctly."""
    resource = MyResource()

    ctx = ResourceContext(
        config=MyResource.Config(name="test")
    )

    state, private = await resource._create_apply(ctx)

    assert state is not None
    assert state.name == "test"
```

See the [Testing Providers Guide](../guides/development/testing-providers.md) for more details.

## Documentation Updates

### When to Update Documentation

Update documentation when you:

- Add new public APIs or features
- Change existing behavior
- Fix bugs that were unclear in docs
- Add new examples or use cases

### Documentation Locations

- **API docs**: Docstrings in source code (Google style)
- **Guides**: `docs/guides/*.md`
- **API reference**: `docs/api/*.md`
- **Examples**: Link to [pyvider-components](https://github.com/provide-io/pyvider-components)

### API Documentation Approach

Pyvider uses a **hybrid approach** for API reference documentation:

**Manual Documentation** (`api/cli.md`, `api/common.md`, `api/hub.md`, etc.):
- Curated examples and explanations
- Context and usage patterns
- Best practices and common pitfalls
- Cross-references to guides

**Auto-Generated Sections** (via mkdocstrings):
- Rendered directly from Python docstrings
- Always up-to-date with code
- Complete parameter listings
- Type signatures

**Why both?**
- Manual docs provide context, examples, and guidance
- Auto-generated docs ensure technical accuracy
- Together they serve different reader needs

**When contributing:**
- Update docstrings for code changes (will auto-generate)
- Update manual pages for new features or changed workflows
- Keep both in sync

### Documentation Style

- Use clear, concise language
- Include code examples
- Add cross-references to related docs
- Test all code examples
- Run the documentation build locally:

```bash
# Build documentation
mkdocs build

# Serve locally to preview
mkdocs serve

# Build in strict mode (fails on warnings)
mkdocs build --strict
```

## Pull Request Process

### Before Submitting

1. ✅ All tests pass (`uv run pytest`)
2. ✅ Linters pass (`uv run ruff check`)
3. ✅ Type checking passes (`uv run mypy src/pyvider`)
4. ✅ Code is formatted (`uv run ruff format`)
5. ✅ Documentation is updated
6. ✅ Commit messages are clear
7. ✅ Branch is up to date with main

### Submitting Your PR

1. **Push your branch** to your fork:
   ```bash
   git push origin feature/my-new-feature
   ```

2. **Open a Pull Request** on GitHub

3. **Fill out the PR template** with:
   - Clear description of changes
   - Link to related issue(s)
   - Summary of testing done
   - Any breaking changes
   - Screenshots (if UI changes)

4. **Request review** from maintainers

### PR Review Process

- Maintainers will review your PR within a few days
- Address feedback by pushing new commits
- Once approved, maintainers will merge your PR
- Your contribution will be in the next release!

### PR Guidelines

- **Keep PRs focused** - One feature or bug fix per PR
- **Small PRs are better** - Easier to review and merge
- **Add tests** - All new code must have tests
- **Update docs** - User-facing changes need documentation
- **Follow conventions** - Match existing code style
- **Be responsive** - Address review feedback promptly

## Code Style Guidelines

### Python Code Style

- **Follow PEP 8** with exceptions noted in `pyproject.toml`
- **Line length**: 100 characters (enforced by ruff)
- **Type hints**: Required for all function signatures
- **Docstrings**: Google style for all public APIs
- **Imports**: Organized by ruff (stdlib, third-party, local)

### Type Hints

```python
# Good - Full type hints
async def create_resource(
    self,
    config: ResourceConfig
) -> tuple[ResourceState | None, PrivateState | None]:
    pass

# Bad - Missing type hints
async def create_resource(self, config):
    pass
```

### Docstrings

Use Google-style docstrings:

```python
def example_function(param1: str, param2: int) -> bool:
    """Short one-line description.

    Longer description if needed. Explain what the function does,
    any important details, and edge cases.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When param2 is negative

    Example:
        >>> example_function("test", 42)
        True
    """
    pass
```

### Async/Await

- Use `async def` for I/O operations
- Always `await` async calls
- Use `asyncio.gather()` for parallel operations
- Avoid blocking calls in async functions

## Reporting Bugs

Found a bug? Please report it!

### Before Reporting

1. **Search existing issues** - Your bug may already be reported
2. **Try the latest version** - Bug might be fixed in main
3. **Gather information** - Version, OS, error messages

### Bug Report Template

Create an issue with:

```markdown
### Description
Clear description of the bug

### Steps to Reproduce
1. Step one
2. Step two
3. See error

### Expected Behavior
What should happen

### Actual Behavior
What actually happens

### Environment
- Pyvider version: (from `uv run python -c "import importlib.metadata as m; print(m.version('pyvider'))"`)
- Python version: (from `python --version`)
- Terraform version: (from `terraform version`)
- OS: (e.g., macOS 14.0, Ubuntu 22.04)

### Logs/Error Messages
```
Paste relevant logs here
```

### Minimal Reproducible Example
```python
# Minimal code that reproduces the issue
```

## Requesting Features

Have an idea for a new feature?

1. **Search existing issues** - Someone may have requested it
2. **Open a discussion** - Discuss the idea before implementing
3. **Create a feature request** - With clear use case and examples

## Getting Help

Need help contributing?

- **Documentation**: Read our [guides](../guides/building-components/creating-providers.md)
- **Discussions**: Ask in [GitHub Discussions](https://github.com/provide-io/pyvider/discussions)
- **Issues**: Search [existing issues](https://github.com/provide-io/pyvider/issues)
- **Examples**: Check [pyvider-components](https://github.com/provide-io/pyvider-components)

## Development Reference

Quick reference for common tasks:

```bash
# Run specific test file
uv run pytest tests/test_specific.py

# Run tests matching a pattern
uv run pytest -k "test_resource"

# Run tests with verbose output
uv run pytest -v

# Run tests in parallel
uv run pytest -n auto

# Update dependencies
uv sync --upgrade

# Build distribution
uv build

# Build provider binary
python scripts/build_provider.py
```

See `CLAUDE.md` for the complete development command reference.

## Recognition

Contributors are recognized in:
- Release notes
- GitHub contributors page
- Special thanks in documentation

Thank you for contributing to Pyvider! 🎉
