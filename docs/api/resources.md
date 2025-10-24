# Resources API

Base classes and utilities for creating Terraform resources with full CRUD lifecycle management.

## Overview

Resources in Pyvider represent manageable infrastructure components that Terraform can plan and apply through Pyvider's async lifecycle.

### Key Components

- **`BaseResource`** - Base class for all resources
- **`@register_resource`** - Decorator for resource registration
- **Resource Context** - Per-operation context with provider access
- **Private State** - Encrypted storage for sensitive data
- **Lifecycle Protocols** - Standard CRUD interfaces

### Lifecycle Methods

Resources interact with Terraform via a plan/apply cycle:
- `read(ctx: ResourceContext)` — refresh the latest state (called by Terraform refresh and after apply)
- `plan(ctx)` — framework-provided method that calls `_create/_update/_delete_plan` hooks to build a planned state
- `apply(ctx)` — framework-provided method that calls `_create_apply/_update_apply/_delete_apply` hooks to enact the plan

Resource authors typically override:
- `_create(ctx, base_plan)` / `_update(ctx, base_plan)` / `_delete_plan(ctx)` to shape the plan output
- `_create_apply(ctx)` / `_update_apply(ctx)` / `_delete_apply(ctx)` to perform real API calls and return final state/private state tuples

See `src/pyvider/resources/base.py` for the exact signatures.

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
