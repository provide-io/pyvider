# Provider Lifecycle

This guide explains the complete lifecycle of a Pyvider provider, from initialization through termination. Understanding the lifecycle helps you implement providers correctly and debug issues effectively.

## Overview

The Pyvider provider lifecycle consists of several distinct phases that occur in a specific order:

```
1. Plugin Startup
   ↓
2. Component Discovery
   ↓
3. Setup Hook
   ↓
4. Schema Retrieval
   ↓
5. Provider Configuration
   ↓
6. Resource Operations (CRUD)
   ↓
7. Provider Shutdown
```

Each phase has specific responsibilities and hooks where you can add custom logic.

## Phase 1: Plugin Startup

**When**: Terraform starts the provider plugin as a separate process

**What Happens**:
1. Terraform launches the provider binary (e.g., `terraform-provider-pyvider`)
2. Provider process starts and initializes gRPC server
3. Terraform and provider perform gRPC handshake
4. Plugin protocol version negotiation (v6)

**Your Code**:
```python
# This happens automatically when using pyvider CLI
# Entry point: pyvider provide

from pyvider.cli import main

if __name__ == "__main__":
    main()
```

**Logging**:
```
INFO  - Starting Pyvider provider
DEBUG - gRPC server listening on localhost:50051
DEBUG - Plugin protocol version: 6
```

## Phase 2: Component Discovery

**When**: Immediately after startup, before any Terraform operations

**What Happens**:
1. Framework scans for registered components using decorators
2. Resources discovered via `@register_resource`
3. Data sources discovered via `@register_data_source`
4. Functions discovered via `@register_function`
5. Provider discovered via `@register_provider`
6. Components registered in the hub

**Your Code**:
```python
# Components are discovered automatically via decorators

@register_provider("local")
class LocalProvider(BaseProvider):
    """Discovered during component discovery."""
    pass

@register_resource("pyvider_file_content")
class FileContentResource(BaseResource):
    """Discovered during component discovery."""
    pass

@register_data_source("pyvider_env_variables")
class EnvVariablesDataSource(BaseDataSource):
    """Discovered during component discovery."""
    pass
```

**Logging**:
```
DEBUG - Discovering components...
INFO  - Registered provider: local
INFO  - Registered resource: pyvider_file_content
INFO  - Registered data source: pyvider_env_variables
INFO  - Registered function: format_string
DEBUG - Component discovery complete: 1 providers, 3 resources, 2 data sources, 5 functions
```

**Key Points**:
- Discovery happens once per provider process
- All components must be importable (in Python path)
- Registration decorators are evaluated at import time
- Hub maintains registry of all discovered components

## Phase 3: Setup Hook

**When**: After discovery, before serving any requests

**What Happens**:
1. Framework calls `provider.setup()` method
2. Provider can perform one-time initialization
3. Capabilities are integrated
4. Final schema is assembled
5. Provider marked as ready

**Your Code**:
```python
@register_provider("mycloud")
class MyCloudProvider(BaseProvider):

    async def setup(self) -> None:
        """
        Called once after discovery, before serving requests.
        Ideal for:
        - Assembling final schema
        - Integrating capabilities
        - One-time initialization
        - Setting up connection pools
        """
        logger.info("Provider setup starting")

        # Integrate capabilities into schema
        await self._integrate_capabilities()

        # Set up connection pool
        self.http_client = httpx.AsyncClient(
            timeout=30.0,
            limits=httpx.Limits(max_connections=100)
        )

        # Assemble final schema
        self._final_schema = self._build_schema()

        logger.info("Provider setup complete")
```

**Logging**:
```
INFO  - Provider setup starting
DEBUG - Integrating capabilities...
DEBUG - Building provider schema
INFO  - Provider setup complete
```

**Important**:
- `setup()` is called exactly once per provider instance
- Must set `self._final_schema` before serving requests
- Async operations are supported
- Exceptions here will prevent provider from starting

## Phase 4: Schema Retrieval

**When**: Terraform needs to know the provider's schema (first `terraform plan/apply`)

**What Happens**:
1. Terraform calls `GetProviderSchema` gRPC method
2. Framework calls `provider.schema` property
3. Provider returns schema for:
   - Provider configuration
   - All resources
   - All data sources
   - All functions
4. Terraform caches schema for the session

**Your Code**:
```python
@register_provider("mycloud")
class MyCloudProvider(BaseProvider):

    @property
    def schema(self) -> PvsSchema:
        """
        Return the provider configuration schema.
        Called by framework during GetProviderSchema RPC.
        """
        if self._final_schema is None:
            raise FrameworkConfigurationError(
                "Provider schema requested before setup() hook was run."
            )
        return self._final_schema

    def _build_schema(self) -> PvsSchema:
        """Build the provider configuration schema."""
        return s_provider({
            "api_endpoint": a_str(
                required=True,
                description="API endpoint URL"
            ),
            "api_key": a_str(
                required=True,
                sensitive=True,
                description="API authentication key"
            ),
            "timeout": a_num(
                default=30,
                description="Request timeout in seconds"
            ),
        })
```

**Logging**:
```
DEBUG - GetProviderSchema called
DEBUG - Returning schema: 1 provider, 3 resources, 2 data sources, 5 functions
```

**Schema Includes**:
- **Provider config schema**: What the `provider` block requires
- **Resource schemas**: All `resource` types and their attributes
- **Data source schemas**: All `data` types and their attributes
- **Function schemas**: All function signatures and parameters

## Phase 5: Provider Configuration

**When**: Terraform processes the `provider` block in configuration

**What Happens**:
1. Terraform validates configuration against schema
2. Terraform calls `ConfigureProvider` gRPC method
3. Framework calls `provider.configure(config)` method
4. Provider stores configuration
5. Provider performs authentication/connection setup
6. Provider marked as configured

**Your Code**:
```python
@register_provider("mycloud")
class MyCloudProvider(BaseProvider):

    async def configure(self, config: dict[str, CtyType]) -> None:
        """
        Configure the provider with user-supplied configuration.

        Args:
            config: Configuration from provider block (in CTY format)

        Called when Terraform processes:
            provider "mycloud" {
              api_endpoint = "https://api.example.com"
              api_key      = var.api_key
              timeout      = 30
            }
        """
        logger.info("Configuring provider", endpoint=config.get("api_endpoint"))

        # Store configuration
        self.api_endpoint = config["api_endpoint"]
        self.api_key = config["api_key"]
        self.timeout = config.get("timeout", 30)

        # Validate configuration
        if not self.api_endpoint.startswith("https://"):
            raise ProviderConfigurationError(
                "API endpoint must use HTTPS"
            )

        # Test authentication
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_endpoint}/auth/test",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=self.timeout
                )
                response.raise_for_status()
        except Exception as e:
            raise ProviderConfigurationError(
                f"Failed to authenticate with API: {e}"
            )

        # Mark as configured
        self._configured = True
        logger.info("Provider configured successfully")
```

**Terraform Configuration**:
```hcl
provider "mycloud" {
  api_endpoint = "https://api.example.com"
  api_key      = var.api_key
  timeout      = 30
}
```

**Logging**:
```
INFO  - Configuring provider endpoint=https://api.example.com
DEBUG - Validating configuration...
DEBUG - Testing authentication...
INFO  - Provider configured successfully
```

**Key Points**:
- `configure()` called once per provider block
- Configuration is validated by framework before calling
- Use this to authenticate, connect to APIs, validate credentials
- Exceptions here prevent all resource operations
- Thread-safe: uses async lock to prevent concurrent configuration

## Phase 6: Resource Operations (CRUD)

**When**: During `terraform plan`, `terraform apply`, `terraform destroy`

**What Happens**:

### For `terraform plan`:
1. Terraform calls `ReadResource` for existing resources
2. Provider's `resource.read()` methods are called
3. Current state is fetched and returned
4. Terraform compares with desired state
5. Plan shows what will change

### For `terraform apply`:
1. For each resource change in plan:
   - **Create**: `resource._create()` called
   - **Update**: `resource.read()` then `resource._update()` called
   - **Delete**: `resource._delete()` called
2. New state returned and stored by Terraform

### For `terraform destroy`:
1. `resource._delete()` called for each resource
2. Resources removed from state

**Your Code**:
```python
@register_resource("mycloud_server")
class ServerResource(BaseResource):

    async def read(self, ctx: ResourceContext) -> State | None:
        """
        Read current state of the resource.
        Called during: refresh, before updates, during plan
        """
        from pyvider.hub import hub
        provider = hub.get_component("singleton", "provider")

        logger.debug("Reading resource", resource_id=ctx.state.id)

        server = await provider.api.get_server(ctx.state.id)

        if not server:
            logger.debug("Resource not found", resource_id=ctx.state.id)
            return None  # Resource was deleted outside Terraform

        return State(
            id=server.id,
            name=server.name,
            status=server.status,
        )

    async def _create(self, ctx: ResourceContext, base_plan: dict):
        """
        Create new resource.
        Called during: terraform apply (for new resources)
        """
        from pyvider.hub import hub
        provider = hub.get_component("singleton", "provider")

        logger.info("Creating resource", name=base_plan["name"])

        server = await provider.api.create_server(
            name=base_plan["name"],
            size=base_plan["size"]
        )

        return {**base_plan, "id": server.id, "status": "running"}, None

    async def _update(self, ctx: ResourceContext, base_plan: dict):
        """
        Update existing resource.
        Called during: terraform apply (for changed resources)
        """
        from pyvider.hub import hub
        provider = hub.get_component("singleton", "provider")

        logger.info("Updating resource", resource_id=ctx.state.id)

        await provider.api.update_server(
            ctx.state.id,
            name=base_plan["name"],
            size=base_plan["size"]
        )

        return base_plan, None

    async def _delete(self, ctx: ResourceContext):
        """
        Delete resource.
        Called during: terraform destroy, terraform apply (for removed resources)
        """
        from pyvider.hub import hub
        provider = hub.get_component("singleton", "provider")

        logger.info("Deleting resource", resource_id=ctx.state.id)

        await provider.api.delete_server(ctx.state.id)
```

**Operation Flow**:

```
terraform plan:
  └─> ReadResource (for each existing resource)
      └─> resource.read()
      └─> Return current state

terraform apply (create):
  └─> ApplyResourceChange
      └─> resource._create()
      └─> Store new state

terraform apply (update):
  └─> ReadResource
      └─> resource.read()
  └─> ApplyResourceChange
      └─> resource._update()
      └─> Store updated state

terraform apply (delete):
  └─> ApplyResourceChange
      └─> resource._delete()
      └─> Remove from state
```

**Logging**:
```
DEBUG - ReadResource called: mycloud_server.web
DEBUG - Reading resource resource_id=srv_123abc
DEBUG - Resource found, returning state
INFO  - ApplyResourceChange called: mycloud_server.web (create)
INFO  - Creating resource name=web-server
DEBUG - API create_server returned id=srv_456def
INFO  - Resource created successfully
```

## Phase 7: Provider Shutdown

**When**: Terraform is done with all operations and exits

**What Happens**:
1. Terraform signals provider to shut down
2. Provider closes connections and cleans up resources
3. Provider process exits
4. gRPC server stops

**Your Code**:
```python
@register_provider("mycloud")
class MyCloudProvider(BaseProvider):

    async def cleanup(self) -> None:
        """
        Called during provider shutdown.
        Use this to clean up resources:
        - Close HTTP connections
        - Disconnect from databases
        - Release file handles
        - Clean up temporary files
        """
        logger.info("Provider cleanup starting")

        # Close HTTP client
        if hasattr(self, 'http_client'):
            await self.http_client.aclose()
            logger.debug("HTTP client closed")

        # Close database connections
        if hasattr(self, 'db_pool'):
            await self.db_pool.close()
            logger.debug("Database pool closed")

        logger.info("Provider cleanup complete")
```

**Logging**:
```
INFO  - Provider shutdown requested
INFO  - Provider cleanup starting
DEBUG - HTTP client closed
DEBUG - Database pool closed
INFO  - Provider cleanup complete
DEBUG - gRPC server stopped
DEBUG - Provider process exiting
```

**Key Points**:
- Cleanup is best-effort (Terraform may force-kill)
- Close connections gracefully
- Don't perform long-running operations
- Exceptions are logged but don't prevent shutdown

## Lifecycle Hooks Summary

| Hook | When | Purpose | Required |
|------|------|---------|----------|
| `setup()` | After discovery, before requests | One-time initialization, build schema | No |
| `configure(config)` | When Terraform processes provider block | Store config, authenticate | Yes* |
| `read(ctx)` | During plan, refresh, before updates | Fetch current resource state | Yes |
| `_create(ctx, plan)` | During apply for new resources | Create the resource | Yes |
| `_update(ctx, plan)` | During apply for changed resources | Update the resource | Yes |
| `_delete(ctx)` | During destroy or resource removal | Delete the resource | Yes |
| `cleanup()` | Provider shutdown | Close connections, cleanup | No |

*`configure()` is required if provider has a configuration schema

## Common Lifecycle Patterns

### Pattern 1: Lazy Authentication

Authenticate only when first needed, not during configure:

```python
class MyProvider(BaseProvider):

    def __init__(self):
        super().__init__()
        self._authenticated = False
        self._access_token = None

    async def configure(self, config: dict[str, CtyType]):
        # Just store credentials
        self.api_endpoint = config["api_endpoint"]
        self.api_key = config["api_key"]

    async def _ensure_authenticated(self):
        """Authenticate on first use."""
        if not self._authenticated:
            response = await self.http_client.post(
                f"{self.api_endpoint}/auth",
                json={"api_key": self.api_key}
            )
            self._access_token = response.json()["access_token"]
            self._authenticated = True

    async def get_server(self, server_id: str):
        await self._ensure_authenticated()  # Lazy auth
        # ... use self._access_token
```

### Pattern 2: Connection Pooling

Set up connection pool during setup, use throughout lifecycle:

```python
class MyProvider(BaseProvider):

    async def setup(self):
        """Set up connection pool during initialization."""
        self.http_client = httpx.AsyncClient(
            timeout=30.0,
            limits=httpx.Limits(
                max_connections=100,
                max_keepalive_connections=20
            )
        )

    async def cleanup(self):
        """Close pool during shutdown."""
        await self.http_client.aclose()
```

### Pattern 3: Capability Integration

Integrate capabilities during setup:

```python
class MyProvider(BaseProvider):

    async def setup(self):
        """Integrate capabilities into provider."""
        # Discover capability components
        auth_capability = self.hub.get_capability("authentication")
        cache_capability = self.hub.get_capability("caching")

        # Integrate into provider
        self.capabilities = {
            "authentication": auth_capability,
            "caching": cache_capability,
        }

        # Build schema with capabilities
        self._final_schema = self._build_schema_with_capabilities()
```

## Debugging Lifecycle Issues

### Issue: "Provider schema requested before setup()"

**Cause**: Framework trying to get schema before `setup()` completed

**Solution**: Ensure `setup()` sets `self._final_schema`

```python
async def setup(self):
    self._final_schema = self._build_schema()  # Must be set!
```

### Issue: "Provider already configured"

**Cause**: `configure()` called multiple times

**Solution**: This shouldn't happen. Framework prevents it. If you see this, it's a framework bug.

### Issue: Resources failing with "No provider configured"

**Cause**: Accessing provider config before `configure()` called

**Solution**: Check configuration state:

```python
async def _create(self, ctx: ResourceContext, base_plan: dict):
    from pyvider.hub import hub
    provider = hub.get_component("singleton", "provider")

    if not provider._configured:
        raise ProviderError("Provider not configured")

    # Now safe to use provider config
    await provider.api.create_resource(...)
```

## Lifecycle Logging

Enable full lifecycle logging:

```bash
export PYVIDER_LOG_LEVEL=DEBUG
export TF_LOG=DEBUG

terraform apply
```

Look for these lifecycle markers:

```
# Startup
INFO  - Starting Pyvider provider

# Discovery
DEBUG - Discovering components...
INFO  - Registered provider: mycloud

# Setup
INFO  - Provider setup starting
INFO  - Provider setup complete

# Schema
DEBUG - GetProviderSchema called

# Configuration
INFO  - Configuring provider

# Operations
DEBUG - ReadResource called
INFO  - ApplyResourceChange called

# Shutdown
INFO  - Provider shutdown requested
INFO  - Provider cleanup complete
```

## Related Documentation

- [Creating Providers](../building-components/creating-providers.md) - How to implement providers
- [Best Practices](../production/best-practices.md) - Provider development patterns
- [Debugging](../development/debugging.md) - Debugging lifecycle issues
- [Error Handling](../development/error-handling.md) - Exception handling in lifecycle
- [Testing Providers](../development/testing-providers.md) - Testing lifecycle hooks

---

**Remember**: The lifecycle is deterministic and predictable. Understanding the order of operations helps you implement providers correctly and debug issues when they arise.
