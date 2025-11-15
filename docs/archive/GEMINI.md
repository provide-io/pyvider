# GEMINI.md: Your AI Assistant for the `pyvider` Project

This document provides context and instructions for interacting with the `pyvider` project. It is intended to be used by the Gemini AI assistant to help you with your development tasks.

## Project Overview

`pyvider` is a Python framework for building Terraform providers. It provides a native Python API for building providers, type-safe data models, a built-in testing framework, and more.

## Core Components

`pyvider` uses a hub-based discovery system where components self-register via decorators:

*   **Provider**: Entry point that configures authentication and shared settings (`@register_provider` decorator)
*   **Resources**: CRUD lifecycle management for infrastructure (`@register_resource` decorator)
*   **Data Sources**: Read-only data fetchers (`@register_data_source` decorator)
*   **Functions**: Callable logic for transformations (`@register_function` decorator)
*   **Ephemerals**: Short-lived resources with open/renew/close lifecycle (`@register_ephemeral_resource` decorator)

## Building and Running

### Environment Setup

```bash
# Set up development environment (creates venv, installs dependencies)
source ./env.sh

# Alternative for PowerShell
. ./env.ps1
```

### Building

`pyvider` is built using `setuptools`.

```bash
# Build distribution packages
uv build
```

### Testing

The tests are in the `tests` directory and can be run with `pytest`.

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pyvider
```

### Linting and Formatting

The code is linted with `ruff check` and formatted with `ruff format`.

```bash
# Format code
ruff format

# Lint code
ruff check
```

### Type Checking

Type checking is done with `mypy`.

```bash
# Type checking with mypy
mypy src/pyvider
```

### CLI

`pyvider` has a CLI entry point: `pyvider`.

```bash
# pyvider CLI
pyvider --help
```

## Development Conventions

*   **Coding Style**: The code is formatted with `ruff format` and linted with `ruff check`.
*   **Testing**: The project is tested with `pytest`. Unit tests for individual components, integration tests for protocol handlers, and property-based testing with Hypothesis are used.
*   **Type Checking**: Type checking is done with `mypy`.
*   **Dependencies**: Dependencies are managed with `uv` and specified in the `pyproject.toml` file.
*   **Component Registration**: Components must use decorators to register with the hub.
*   **Schema Definition**: `attrs`-based models with type annotations are used for schema definition.
