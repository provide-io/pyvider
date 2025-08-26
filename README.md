# Pyvider

Pyvider is a Python framework for building Terraform providers. It provides a native Python API for building providers, type-safe data models, a built-in testing framework, and more.

## Features

-   **Native Python API**: Build Terraform providers in Python without dealing with the complexity of the Terraform plugin protocol.
-   **Type-Safe Data Models**: Define your provider's schema using Python's type hints and get type-safe data models for your resources and data sources.
-   **Built-in Testing Framework**: Write unit and integration tests for your provider using `pytest`.
-   **Hub-Based Discovery**: Components self-register via decorators, making it easy to add new resources, data sources, and functions.
-   **CLI**: `pyvider` has a CLI for managing your provider, including a development server and a component registry.
