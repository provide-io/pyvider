# Contributing to Pyvider

Thank you for your interest in contributing to Pyvider! This document provides guidelines and standards for contributing to the project.

## 📚 Complete Contributing Guide

For comprehensive contributing guidelines including testing requirements, documentation standards, and pull request process, see:

**→ [Complete Contributing Guidelines](docs/contributing/guidelines.md)**

## Development Environment

### Setup
```bash
# Clone the repository
git clone https://github.com/provide-io/pyvider.git
cd pyvider

# Install dependencies
uv sync

# Run tests
uv run pytest

# Run linting
uv run ruff check
uv run ruff format

# Run type checking
uv run mypy src/pyvider
```

## Commit Message Standards

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification for clear and semantic commit messages.

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Commit Types

- **feat**: A new feature for the user
- **fix**: A bug fix
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **test**: Adding or updating tests
- **docs**: Documentation changes
- **chore**: Maintenance tasks (dependencies, build scripts, etc.)
- **perf**: Performance improvements
- **style**: Code style changes (formatting, missing semicolons, etc.)
- **ci**: Changes to CI/CD configuration

### Scope Guidelines

Common scopes in Pyvider:

- `tests` - Test-related changes
- `handlers` - Protocol handler implementations
- `schema` - Schema system changes
- `resources` - Resource lifecycle functionality
- `providers` - Provider configuration
- `functions` - Provider function implementations
- `ephemerals` - Ephemeral resource handling
- `cli` - CLI tool changes
- `hub` - Component registry/discovery
- `conversion` - Type conversion and marshaling

### Examples

#### Good Commit Messages

```
feat(handlers): add support for MoveResourceState RPC

Implements the MoveResourceState handler to support Terraform's
resource move operations. Includes state validation and migration.

Closes #123
```

```
fix(schema): resolve type inference for nested blocks

Fixes an issue where nested block types were incorrectly inferred
as dynamic types instead of their declared types.

Fixes #456
```

```
refactor(tests): consolidate handler test fixtures

Moves common test fixtures to conftest.py to reduce duplication
and improve test maintainability.
```

```
test(conversion): add edge case tests for CTY marshaling

Adds tests for null values, unknown values, and deeply nested
structures in the CTY conversion layer.
```

```
docs(readme): update installation instructions for Python 3.11+

Updates README to reflect new minimum Python version and clarifies
uv usage for dependency management.
```

```
chore(deps): update provide-foundation to v2.1.0

Updates provide-foundation dependency for improved error handling
and new utility functions.
```

#### Bad Commit Messages

```
✗ fix stuff
✗ WIP
✗ update
✗ fix tests
✗ changes
✗ 🔼⚙️ [skip ci] auto-commit
```

### Breaking Changes

If your change introduces a breaking change, add `BREAKING CHANGE:` in the footer:

```
feat(schema): change attribute definition API

Refactors the attribute definition system for improved type safety.

BREAKING CHANGE: Attribute() now requires explicit type parameter.
Migration guide: Replace `Attribute()` with `Attribute(type=CtyString())`.
```

### Multiple Changes

If a commit contains multiple related changes, list them in the body:

```
refactor(hub): improve component registry performance

- Cache component lookups for faster retrieval
- Use lazy loading for component metadata
- Add benchmarks for registry operations

Improves average lookup time from 2ms to 0.3ms.
```

## Pull Request Guidelines

1. **Create a feature branch** from `main`
2. **Follow commit standards** for all commits
3. **Write or update tests** for your changes
4. **Update documentation** if adding features
5. **Run linting and tests** before submitting
6. **Write a clear PR description** explaining the change

### PR Title Format

PR titles should follow the same format as commit messages:

```
feat(handlers): add OpenEphemeralResource implementation
fix(schema): resolve nullable type handling
refactor(tests): improve test organization
```

## Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/)
- Use `ruff` for linting and formatting
- Add type hints to all public functions
- Write docstrings for classes and public methods
- Keep line length to 111 characters (configured in pyproject.toml)

## Testing

- Write unit tests for new functionality
- Maintain >90% coverage for critical paths
- Use descriptive test names: `test_handler_returns_error_for_unknown_resource`
- Group tests in classes by functionality
- Use fixtures for common test setup

## Questions?

- Open an issue for bug reports or feature requests
- Check existing issues before creating a new one
- Be respectful and constructive in discussions

Thank you for contributing to Pyvider! 🐍
