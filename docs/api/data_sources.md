# Data Sources API

Base classes and utilities for creating Terraform data sources (read-only resources).

## Overview

Data sources in Pyvider provide read-only access to external data that can be referenced in Terraform configurations.

### Key Components

- **`BaseDataSource`** - Base class for all data sources
- **`@register_data_source`** - Decorator for data source registration
- **Data Source Context** - Per-query context with provider access

### Usage

Data sources implement a single `read(ctx: ResourceContext)` method that:
- Reads configuration via `ctx.config`
- Queries external systems
- Returns data as computed attributes
- Does not modify any state

```python
from pyvider.resources.context import ResourceContext

async def read(self, ctx: ResourceContext) -> ImageState | None:
    if ctx.config is None:
        return None
    response = await self.client.get_image(ctx.config.image_id)
    return ImageState(**response)
```

## Module Reference

::: pyvider.data_sources
    options:
      show_source: true
      show_root_heading: true
      members_order: source
      show_if_no_docstring: false
      filters:
        - "!^_"
        - "^__init__$"
