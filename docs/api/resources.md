# Resources API

Base classes and utilities for creating Terraform resources with full CRUD lifecycle management.

## Overview

Resources in Pyvider represent manageable infrastructure with create, read, update, and delete operations.

### Key Components

- **`BaseResource`** - Base class for all resources
- **`@register_resource`** - Decorator for resource registration
- **Resource Context** - Per-operation context with provider access
- **Private State** - Encrypted storage for sensitive data
- **Lifecycle Protocols** - Standard CRUD interfaces

### Lifecycle Methods

Resources implement standard lifecycle methods:
- `create()` - Create new resource instance
- `read()` - Refresh resource state
- `update()` - Modify existing resource
- `delete()` - Remove resource
- `import_resource()` - Import existing resources (optional)

## Module Reference

::: pyvider.resources
    options:
      show_source: true
      show_root_heading: true
      members_order: source
      show_if_no_docstring: false
      filters:
        - "!^_"
        - "^__init__$"
