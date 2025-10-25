# Contributing to Pyvider

We welcome contributions to `pyvider`! This document outlines the process for contributing to the project.

## How to Contribute

1.  **Fork the repository:** Fork the `pyvider` repository to your own GitHub account.
2.  **Create a branch:** Create a new branch for your changes.
3.  **Make your changes:** Make your changes to the code.
4.  **Test your changes:** Make sure to test your changes thoroughly.
5.  **Submit a pull request:** Submit a pull request to the `pyvider` repository.

## Submitting a Pull Request

When you submit a pull request, please make sure to include the following:

-   A clear and descriptive title for the pull request.
-   A detailed description of the changes you have made.
-   A link to the issue you are addressing, if applicable.
-   A summary of the testing you have done.

## Reporting a Bug

If you find a bug in `pyvider`, please report it by creating an issue on the GitHub repository. When you report a bug, please make sure to include the following:

-   A clear and descriptive title for the issue.
-   A detailed description of the bug.
-   Steps to reproduce the bug.
-   The version of `pyvider` you are using.
-   The version of Terraform you are using.
-   Any relevant logs or error messages.

## Development Setup

To set up a development environment for Pyvider:

```bash
# Clone the repository
git clone https://github.com/provide-io/pyvider.git
cd pyvider

# Install dependencies with uv
uv sync --group dev

# Run tests
uv run pytest

# Run linters
uv run ruff check
uv run mypy src/pyvider
```

See `CLAUDE.md` in the repository root for detailed development commands and workflows.

## Code Style

-   Follow PEP 8 guidelines
-   Use type hints for all function signatures
-   Use `ruff` for formatting and linting
-   Write docstrings for all public APIs (Google style)
-   Keep test coverage above 90%

## Pull Request Guidelines

-   Keep PRs focused on a single feature or bug fix
-   Add tests for new functionality
-   Update documentation for user-facing changes
-   Ensure all tests pass and linters are clean
-   Reference related issues in the PR description

## Questions?

-   Open a [GitHub Discussion](https://github.com/provide-io/pyvider/discussions) for questions
-   Check existing issues before creating a new one
-   Join our community channels (links in README)
