# Providers API

Base classes and utilities for creating Terraform providers.

## Overview

Providers in Pyvider are the entry point for your Terraform provider implementation. They handle:
- **Configuration** and authentication
- **Metadata** (name, version, protocol)
- **Component discovery** and registration
- **Shared state** and resources

### Key Components

- **`BaseProvider`** - Base class for all providers
- **`@register_provider`** - Decorator for provider registration
- **`ProviderMetadata`** - Provider metadata definition
- **`ProviderContext`** - Provider runtime context
- **Provider capabilities** - Reusable provider behaviors

### Lifecycle

Providers implement:
- `setup()` - Initialize provider (called once)
- `configure()` - Configure with user settings
- `get_schema()` - Return provider configuration schema

## Module Reference

::: pyvider.providers
    options:
      show_source: true
      show_root_heading: true
      members_order: source
      show_if_no_docstring: false
      filters:
        - "!^_"
        - "^__init__$"
