# API Reference

Complete API documentation for Pyvider's public and internal interfaces.

## Overview

This section provides detailed API documentation for Pyvider's modules, classes, and functions. The API reference is a combination of:

- **Manual documentation**: Curated guides for key APIs with examples and best practices
- **Auto-generated documentation**: Extracted from Python docstrings using mkdocstrings

!!! warning "API Stability - Pre-release (v0.3.0)"
    Pyvider is in its pre-release series. Breaking changes are documented in release notes.
    Some APIs may change during the pre-release series.

    **Important Notes:**
    - Some documented APIs may not be fully implemented yet
    - Test thoroughly before using in production environments
    **Public API Stability:**
    - ✅ **Stable**: Decorator API (`@register_resource`, `@register_provider`, etc.)
    - ✅ **Stable**: Schema factory functions (`s_resource`, `a_str`, `a_num`, etc.)
    - ✅ **Stable**: Base classes (`BaseResource`, `BaseProvider`, `BaseDataSource`, etc.)
    - ⚠️ **Evolving**: Internal conversion and protocol handlers
    - ⚠️ **Experimental**: Capabilities system and advanced features marked in documentation

## When to Use This Reference

### For Building Providers
Most provider developers should start with the **[Guides](../guides/building-components/creating-providers.md)** section, which provides task-oriented tutorials. Use the API reference when you need:

- Detailed parameter information for specific functions
- Complete list of available schema types and validators
- Exception hierarchy for error handling
- Metrics available for monitoring

### For Framework Development
If you're contributing to Pyvider or building advanced integrations, the API reference documents internal interfaces. However, note that internal APIs are subject to change.

## API Modules

### Core Components

#### [CLI](cli.md)
Command-line interface for the `pyvider` command. Includes commands for component management, configuration, installation, and provider service launching.

**Key commands:** `provide`, `components list`, `config show`, `install`, `launch-context`

#### [Common](common.md)
Shared utilities, configuration management, encryption, and context handling used across all modules.

**Key exports:** `PyviderConfig`, `OperationContext`, `LaunchContext`, encryption utilities

#### [Hub](hub.md)
Component registry and discovery system. Manages registration and lifecycle of all provider components.

**Key exports:** `ComponentRegistry`, `ComponentDiscovery`, validators

### Component Types

#### [Providers](providers/index.md)
Provider implementation, configuration, and capabilities.

**Key exports:** `BaseProvider`, `ProviderMetadata`, `@register_provider`, `ProviderContext`

#### [Resources](resources.md)
Resource components with full CRUD lifecycle management.

**Key exports:** `BaseResource`, `ResourceContext`, `@register_resource`, `PrivateState`

#### [Data Sources](data_sources.md)
Read-only data source components for querying existing infrastructure.

**Key exports:** `BaseDataSource`, `@register_data_source`

#### [Functions](functions.md)
Provider functions for data transformation and computation.

**Key exports:** `BaseFunction`, `@register_function`, function adapters

#### [Ephemeral Resources](ephemerals.md)
Short-lived resources with open/renew/close lifecycle (e.g., temporary credentials, connections).

**Key exports:** `BaseEphemeralResource`, `@register_ephemeral_resource`, `EphemeralResourceContext`

### Type System & Validation

#### [Schema](schema/index.md)
Type-safe schema definition system with factory functions for attributes, blocks, and validators.

**Key exports:** `s_resource()`, `s_data_source()`, `s_provider()`, `a_str()`, `a_num()`, `b_list()`, etc.

#### [Exceptions](exceptions.md)
Comprehensive exception hierarchy for error handling and diagnostics.

**Key exports:** `PyviderError`, `ResourceError`, `ProviderError`, `ValidationError`, `SchemaError`

### Data Handling

#### [Conversion](conversion/index.md) ⚠️ Advanced
Bidirectional type conversion between Python and Terraform's CTY type system.

**Key exports:** `cty_to_native`, `marshal`, `unmarshal`, `pvs_schema_to_proto`

!!! note "Advanced API"
    Most users don't need to use conversion functions directly - Pyvider handles conversions automatically.

#### [Protocols](protocols/index.md) 🔒 Internal
Terraform Plugin Protocol v6 implementation and gRPC handlers.

**Note:** This is an internal module. Provider developers should use high-level component APIs instead.

### Observability

#### [Observability](observability.md)
Built-in metrics for monitoring provider operations, resource lifecycle, and performance.

**Key exports:** `resource_create_total`, `handler_duration`, `function_calls`, etc. (33+ metrics)

## Public vs Internal APIs

### Public APIs ✅
These APIs are designed for provider developers and are relatively stable:

- **Decorators**: `@register_provider`, `@register_resource`, `@register_data_source`, `@register_function`, `@register_ephemeral_resource`, `@register_capability`
- **Base Classes**: `BaseProvider`, `BaseResource`, `BaseDataSource`, `BaseFunction`, `BaseEphemeralResource`
- **Schema Factories**: `s_resource()`, `s_data_source()`, `s_provider()`, `a_*()`, `b_*()` functions
- **Context Objects**: `ResourceContext`, `ProviderContext`, `EphemeralResourceContext`
- **Exceptions**: All exception classes in `pyvider.exceptions`

### Internal APIs ⚠️
These APIs are used by the framework itself and may change without notice:

- **Conversion functions**: Internal type conversion (unless you're debugging)
- **Protocol handlers**: gRPC handler implementations
- **Hub internals**: Component registration implementation details
- **Private state**: Internal encryption mechanism

**Use internal APIs only when:**
- Building framework extensions
- Debugging complex issues
- Contributing to Pyvider core

## Documentation Conventions

### Type Annotations
All API functions include Python type hints. For example:

```python
async def _create_apply(
    self,
    ctx: ResourceContext
) -> tuple[State | None, None]:
    ...
```

### Return Types
Many resource methods return tuples like `tuple[State | None, PrivateState | None]`:
- First element: Public state (visible in Terraform)
- Second element: Private state (encrypted, never shown to users)

### Async Methods
Most component methods are async. Always use `await`:

```python
# Correct
state = await resource.read(ctx)

# Wrong - will return a coroutine, not the result!
state = resource.read(ctx)  # ❌
```

## Examples

### Basic Provider Setup

```python
from pyvider.providers import register_provider, BaseProvider, ProviderMetadata
from pyvider.schema import s_provider, a_str

@register_provider("mycloud")
class MyCloudProvider(BaseProvider):
    def __init__(self):
        super().__init__(
            metadata=ProviderMetadata(
                name="mycloud",
                version="1.0.0",
                protocol_version="6"
            )
        )

    def _build_schema(self):
        return s_provider({
            "api_key": a_str(required=True, sensitive=True),
            "region": a_str(default="us-east-1"),
        })

    async def configure(self, config):
        self.api_key = config["api_key"]
        self.region = config["region"]
```

### Basic Resource

```python
from pyvider.resources import register_resource, BaseResource, ResourceContext
from pyvider.schema import s_resource, a_str, a_num
import attrs

@attrs.define
class ServerConfig:
    name: str
    size: str = "small"

@attrs.define
class ServerState:
    id: str
    name: str
    size: str
    ip_address: str

@register_resource("server")
class Server(BaseResource):
    config_class = ServerConfig
    state_class = ServerState

    @classmethod
    def get_schema(cls):
        return s_resource({
            "name": a_str(required=True),
            "size": a_str(default="small"),
            "id": a_str(computed=True),
            "ip_address": a_str(computed=True),
        })

    async def _create_apply(self, ctx: ResourceContext) -> tuple[ServerState | None, None]:
        server = await self.api.create_server(ctx.config)
        return ServerState(
            id=server.id,
            name=server.name,
            size=server.size,
            ip_address=server.public_ip
        ), None
```

## Getting Help

- **Guides**: Start with [developer guides](../guides/building-components/creating-providers.md) for task-oriented tutorials
- **Examples**: See [pyvider-components](https://github.com/provide-io/pyvider-components) for 100+ working examples
- **Issues**: Report bugs at [GitHub Issues](https://github.com/provide-io/pyvider/issues)
- **Discussions**: Ask questions at [GitHub Discussions](https://github.com/provide-io/pyvider/discussions)

## Contributing

Found an error in the API documentation? See our [Contributing Guidelines](../contributing/guidelines.md) for how to submit improvements.

---

## Module List

Below is the complete auto-generated API documentation for the `pyvider` package:
