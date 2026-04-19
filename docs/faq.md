# Frequently Asked Questions (FAQ)

Common questions and answers about Pyvider.

## General Questions

### What is Pyvider?

Pyvider is a Python framework for building Terraform providers. It implements the Terraform Plugin Protocol v6, allowing you to create infrastructure providers using pure Python instead of Go.

### Why use Pyvider instead of the Go SDK?

**Use Pyvider when:**

- You're more comfortable with Python than Go
- You want to leverage Python's rich ecosystem (httpx, pydantic, etc.)
- Your team already has Python expertise
- You're building internal tooling or prototypes
- You prefer Python's async/await over Go's goroutines

**Use Go SDK when:**

- You need absolute maximum performance
- You're building a high-traffic public provider
- Your team has Go expertise
- You want the most mature, battle-tested framework

### Is Pyvider production-focused?

Pyvider is in its pre-release series. It implements the full Terraform Plugin Protocol v6 and is well-tested. It's best suited for:

Some APIs may change during the pre-release series.

- Internal tooling and automation
- Rapid prototyping
- Learning and experimentation
- Custom providers for specific needs

### What Python version is required?

Python **3.11 or higher** is required. Pyvider uses modern Python features like:

- Native async/await
- Type hints and `|` union syntax
- Structured pattern matching (in some areas)

### Can I use existing Python libraries?

Yes! One of Pyvider's main benefits is access to Python's ecosystem:

- **HTTP clients**: httpx, aiohttp
- **Cloud SDKs**: boto3, azure-sdk, google-cloud
- **Data**: pandas, polars
- **Utilities**: arrow (dates), pydantic (validation)

Just ensure they support async/await if you're using them in async contexts.

## Architecture Questions

### How does Pyvider work?

Pyvider acts as a bridge between Terraform and your Python code:

1. Terraform calls your provider via gRPC
1. Pyvider handles the protocol communication
1. Your Python code handles the business logic
1. Pyvider translates responses back to Terraform

See [Architecture](explanation/architecture.md) for details.

### What is the Component Hub?

The Component Hub is Pyvider's auto-discovery system. When you use decorators like `@register_provider` or `@register_resource`, components automatically register themselves with the hub. Terraform can then discover and use them.

See [Component Model](explanation/component-model.md).

### Do I need to understand the Terraform Plugin Protocol?

No! Pyvider abstracts away the protocol details. You just implement:

- Provider configuration
- Resource CRUD operations
- Data source reads
- Function calls

Pyvider handles all the gRPC, message serialization, and protocol compliance.

## Development Questions

### How do I start building a provider?

Follow these steps:

1. **Read the [Quick Start](getting-started/quick-start.md)** - Build your first provider in 5 minutes
1. **Try the [Tutorial](tutorials/intermediate-provider.md)** - Build a real HTTP API provider
1. **Study [Examples](https://github.com/provide-io/pyvider-components)** - 100+ working examples
1. **Read the Guides** - [Creating Providers](guides/building-components/creating-providers.md), [Creating Resources](guides/building-components/creating-resources.md)

### What's the difference between a resource and a data source?

**Resources** manage infrastructure lifecycle (create, update, delete):

```python
@register_resource("server")
class Server(BaseResource):
    async def _create_apply(self, ctx):
        # Create the server
        pass
```

**Data Sources** fetch read-only data:

```python
@register_data_source("user")
class User(BaseDataSource):
    async def read(self, ctx):
        # Fetch user data
        pass
```

See [Core Concepts](explanation/component-model.md).

### How do I handle secrets and credentials?

1. **Mark as sensitive** in schema:

   ```python
   "api_key": a_str(required=True, sensitive=True)
   ```

1. **Use private state** for encrypted storage:

   ```python
   return state, {"password": db.password}  # Encrypted
   ```

1. **Never hardcode** secrets in code

1. **Never log** sensitive data

See [Security Best Practices](guides/production/security-best-practices.md).

### How do I test my provider?

Use pytest with async support:

```python
import pytest

@pytest.mark.asyncio
async def test_resource_create():
    resource = MyResource()
    ctx = ResourceContext(config=MyConfig(...))
    state, _ = await resource._create_apply(ctx)
    assert state.id
```

See [Testing Providers](guides/development/testing-providers.md).

### How do I debug my provider?

Enable debug logging:

```bash
export TF_LOG=DEBUG
export PYVIDER_LOG_LEVEL=DEBUG
terraform apply
```

Use the Python debugger:

```python
import pdb; pdb.set_trace()
# Or use breakpoint()
```

See [Debugging Guide](guides/development/debugging.md).

## Schema Questions

### What are the available attribute types?

Pyvider provides comprehensive type support:

- **Primitives**: `a_str()`, `a_num()`, `a_bool()`
- **Collections**: `a_list()`, `a_map()`, `a_set()`
- **Complex**: `a_obj()`, `a_tuple()`
- **Special**: `a_dyn()` (any type)

See [Schema Types](schema/types.md).

### How do I make an attribute required?

```python
"name": a_str(required=True)
```

### How do I add a default value?

```python
"size": a_str(default="medium")
```

### How do I make an attribute computed?

```python
"id": a_str(computed=True)  # Provider sets this
```

### How do I validate attribute values?

Use validators:

```python
"port": a_num(
    validators=[
        lambda x: 1 <= x <= 65535 or "Invalid port",
    ]
)
```

See [Schema Validators](schema/validators.md).

### Can I have nested blocks?

Yes! Use block factories:

```python
schema = s_resource({
    "name": a_str(required=True),
    "config": b_single("config"),  # Single nested block
    "rule": b_list("rule"),         # Multiple blocks
})
```

See [Schema Blocks](schema/blocks.md).

## Performance Questions

### Is Python fast enough for a Terraform provider?

Yes, for most use cases. Terraform providers are typically I/O bound (API calls, network), not CPU bound. Python's async/await handles I/O efficiently.

**Tips for performance:**

- Use async/await properly
- Implement connection pooling
- Cache expensive lookups
- Batch API calls

See [Performance Optimization](guides/production/performance-optimization.md).

### How do I make my provider faster?

1. **Use async properly** - Never block the event loop
1. **Cache data** - Cache expensive API calls
1. **Batch operations** - Avoid N+1 queries
1. **Connection pooling** - Reuse HTTP connections
1. **Profile** - Use py-spy to find bottlenecks

See [Performance Optimization](guides/production/performance-optimization.md).

### Should I use caching?

Cache data that:

- Changes infrequently (region info, image catalogs)
- Is expensive to fetch
- Is accessed multiple times

Don't cache:

- Resource state (must be fresh)
- User credentials
- Frequently changing data

## Deployment Questions

### How do I distribute my provider?

Options:

1. **Development** - Use `pyvider install` for local testing
1. **Internal** - Package with Flavor and distribute binary
1. **Public** - Publish to Terraform Registry (after 1.0)

See [Installation Guide](getting-started/installation.md).

### Does my provider need to be compiled?

No! Pyvider providers run as Python scripts. However, you can package them into standalone binaries using [Flavor](https://github.com/provide-io/flavorpack) for easier distribution.

### Can I publish to the Terraform Registry?

Public registry support is not available yet. For now, use:

- Local dev provider file
- Private distribution
- Internal package repository

## Troubleshooting

### Why isn't Terraform finding my provider?

Check:

1. Provider is installed (`pyvider install`)
1. Terraform is initialized (`terraform init`)
1. Provider name matches in Terraform config
1. Provider is in the correct directory

See [Troubleshooting](troubleshooting.md#provider-not-found-error).

### Why isn't my resource updating?

Ensure you implemented `_update_apply()`:

```python
async def _update_apply(self, ctx):
    # Actually update the resource
    await self.api.update_resource(ctx.state.id, ctx.config)
    return updated_state, None
```

See [Troubleshooting](troubleshooting.md#resource-update-not-applied).

### Why isn't drift being detected?

Implement `read()` correctly - it must fetch **current** state, not return cached state:

```python
async def read(self, ctx):
    # Fetch CURRENT state from API
    current = await self.api.get_resource(ctx.state.id)
    return State(**current)  # Return current, not ctx.state!
```

See [Troubleshooting](troubleshooting.md#state-drift-not-detected).

### Why is my provider crashing?

Common causes:

1. Unhandled exceptions
1. Blocking I/O in async code
1. Missing await on async calls
1. Type mismatches

Enable debug logging and check for stack traces:

```bash
export TF_LOG=DEBUG
export PYVIDER_LOG_LEVEL=DEBUG
terraform apply 2>&1 | tee debug.log
```

See [Troubleshooting](troubleshooting.md#provider-crashes-on-apply).

## Advanced Questions

### Can I use capabilities?

Capabilities are experimental. For production, use:

- Inheritance (base classes)
- Composition (helper classes)
- Utility modules

See [Capabilities Overview](capabilities/overview.md).

### How do I handle provider-specific state?

Use instance variables in your provider:

```python
@register_provider("mycloud")
class MyCloudProvider(BaseProvider):
    async def configure(self, config):
        await super().configure(config)
        self.api_client = APIClient(config["api_key"])
        self.cache = {}
```

Resources can access the provider via the hub:

```python
from pyvider.hub import hub
provider = hub.get_component("singleton", "provider")
await provider.api_client.create(...)
```

### Can I have multiple providers in one package?

Yes! Register multiple providers:

```python
@register_provider("aws")
class AWSProvider(BaseProvider):
    pass

@register_provider("gcp")
class GCPProvider(BaseProvider):
    pass
```

Each will be available as a separate Terraform provider.

### How do I handle pagination?

Fetch all pages before returning:

```python
async def read(self, ctx):
    all_items = []
    page_token = None

    while True:
        response = await provider.api.list_items(
            page_token=page_token,
            page_size=100
        )

        all_items.extend(response.items)

        if not response.next_page_token:
            break

        page_token = response.next_page_token

    return ItemsData(items=all_items, count=len(all_items))
```

### How do I implement resource timeouts?

Use asyncio.wait_for:

```python
import asyncio

async def _create_apply(self, ctx):
    try:
        # Timeout after 5 minutes
        result = await asyncio.wait_for(
            self.api.create_resource(ctx.config),
            timeout=300
        )
        return State(**result), None

    except asyncio.TimeoutError:
        raise ResourceError("Resource creation timed out after 5 minutes")
```

## Getting Help

### Where can I get help?

- **Examples**: [pyvider-components](https://github.com/provide-io/pyvider-components)
- **Discussions**: [GitHub Discussions](https://github.com/provide-io/pyvider/discussions)
- **Issues**: [GitHub Issues](https://github.com/provide-io/pyvider/issues)

### How do I report a bug?

[Open an issue](https://github.com/provide-io/pyvider/issues/new) with:

- Clear description
- Steps to reproduce
- Environment details (Pyvider version, Python version, OS)
- Relevant logs

See [Contributing Guidelines](contributing/guidelines.md#reporting-bugs).

### How can I contribute?

We welcome contributions!

1. Read [Contributing Guidelines](contributing/guidelines.md)
1. Find a [good first issue](https://github.com/provide-io/pyvider/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)
1. Submit a pull request

## Additional Resources

- [Quick Start Guide](getting-started/quick-start.md)
- [Tutorial: HTTP API Provider](tutorials/intermediate-provider.md)
- [Best Practices](guides/production/best-practices.md)
- [Troubleshooting Guide](troubleshooting.md)
- [API Reference](api/index.md)

______________________________________________________________________

**Don't see your question?** Ask in [GitHub Discussions](https://github.com/provide-io/pyvider/discussions)!
