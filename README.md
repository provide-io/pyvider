# Pyvider

Pyvider is a Python framework for building Terraform providers. It provides a native Python API for building providers, type-safe data models, a built-in testing framework, and more.

## Features

-   **Native Python API**: Build Terraform providers in Python without dealing with the complexity of the Terraform plugin protocol.
-   **Type-Safe Data Models**: Define your provider's schema using Python's type hints and get type-safe data models for your resources and data sources.
-   **Built-in Testing Framework**: Write unit and integration tests for your provider using `pytest`.
-   **Hub-Based Discovery**: Components self-register via decorators, making it easy to add new resources, data sources, and functions.
-   **CLI**: `pyvider` has a CLI for managing your provider, including a development server and a component registry.

## Getting Started

To get started with `pyvider`, you need to install it and create a new provider.

### Installation

```bash
# Install pyvider
pip install pyvider
```

### Creating a Provider

To create a new provider, you need to create a new Python package and define your provider, resources, data sources, and functions.

Here is an example of a simple provider:

```python
from pyvider import provider, resource

@provider
class MyProvider:
    pass

@resource
class MyResource:
    pass
```

## Core Concepts

`pyvider` uses a hub-based discovery system where components self-register via decorators.

-   **Provider**: The entry point for your provider. It configures authentication and shared settings.
-   **Resources**: Manage the lifecycle of your infrastructure resources.
-   **Data Sources**: Read-only data fetchers for your provider.
-   **Functions**: Callable logic for transformations and other operations.
-   **Ephemerals**: Short-lived resources with an open/renew/close lifecycle.

## Development

To contribute to the development of `pyvider`, you need to set up the development environment.

### Environment Setup

```bash
# Set up the development environment (creates venv, installs dependencies)
source ./env.sh
```

### Testing

```bash
# Run all tests
pytest
```

### Building

```bash
# Build the package
uv build
```
