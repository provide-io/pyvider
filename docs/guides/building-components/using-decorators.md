# Using Decorators

Pyvider uses decorators to register components with the hub-based discovery system. This guide shows how to use each decorator type correctly.

## Overview

All Pyvider components use decorators for registration:
- `@register_provider` - Register providers
- `@register_resource` - Register resources
- `@register_data_source` - Register data sources
- `@register_function` - Register functions
- `@register_ephemeral_resource` - Register ephemeral resources
- `@register_capability` - Register capabilities

## Provider Decorator

### `@register_provider(name: str)`

Registers a provider class with the Pyvider hub.

**Parameters:**
- `name` - Provider name used in Terraform (e.g., `"mycloud"`)

**Complete Example:**

```python
from pyvider.providers import register_provider, BaseProvider, ProviderMetadata
from pyvider.schema import s_provider, a_str, PvsSchema
import attrs

@attrs.define
class MyCloudConfig:
    """Provider runtime configuration."""
    api_key: str
    region: str = "us-east-1"
    timeout: int = 30

@register_provider("mycloud")
class MyCloudProvider(BaseProvider):
    """MyCloud infrastructure provider."""

    def __init__(self):
        super().__init__(
            metadata=ProviderMetadata(
                name="mycloud",
                version="1.0.0",
                protocol_version="6"
            )
        )
        self.api_client = None
        self.provider_config: MyCloudConfig | None = None

    def _build_schema(self) -> PvsSchema:
        """Define provider configuration schema."""
        return s_provider({
            "api_key": a_str(
                required=True,
                sensitive=True,
                description="API key for authentication"
            ),
            "region": a_str(
                default="us-east-1",
                description="Default region for resources"
            ),
            "timeout": a_num(
                default=30,
                description="API request timeout in seconds"
            ),
        })

    async def configure(self, config: dict) -> None:
        """Configure the provider with user settings."""
        await super().configure(config)

        # Convert config dict to attrs instance
        self.provider_config = MyCloudConfig(
            api_key=config["api_key"],
            region=config.get("region", "us-east-1"),
            timeout=config.get("timeout", 30),
        )

        # Initialize API client
        self.api_client = MyCloudAPIClient(
            api_key=self.provider_config.api_key,
            region=self.provider_config.region,
            timeout=self.provider_config.timeout,
        )
```

**Terraform usage:**
```hcl
provider "mycloud" {
  api_key = var.api_key
  region  = "us-west-2"
  timeout = 60
}
```

## Resource Decorator

### `@register_resource(name: str)`

Registers a resource class with the Pyvider hub.

**Parameters:**
- `name` - Resource type name without provider prefix (e.g., `"instance"`)

**Complete Example:**

```python
from pyvider.resources import register_resource, BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.schema import s_resource, a_str, a_num, PvsSchema
import attrs

@attrs.define
class InstanceConfig:
    """Resource configuration from user."""
    name: str
    size: str = "t2.micro"
    ami: str | None = None

@attrs.define
class InstanceState:
    """Resource state managed by provider."""
    id: str
    name: str
    size: str
    ami: str
    public_ip: str
    status: str

@register_resource("instance")
class Instance(BaseResource):
    """Cloud compute instance resource."""

    config_class = InstanceConfig
    state_class = InstanceState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        """Define Terraform schema."""
        return s_resource({
            # User inputs
            "name": a_str(required=True, description="Instance name"),
            "size": a_str(default="t2.micro", description="Instance size"),
            "ami": a_str(description="AMI ID (defaults to latest)"),

            # Provider outputs
            "id": a_str(computed=True, description="Instance ID"),
            "public_ip": a_str(computed=True, description="Public IP address"),
            "status": a_str(computed=True, description="Instance status"),
        })

    async def _validate_config(self, config: InstanceConfig) -> list[str]:
        """Validate configuration."""
        errors = []
        valid_sizes = ["t2.micro", "t2.small", "t2.medium", "t3.micro"]
        if config.size not in valid_sizes:
            errors.append(f"size must be one of: {', '.join(valid_sizes)}")
        return errors

    async def read(self, ctx: ResourceContext) -> InstanceState | None:
        """Refresh instance state from API."""
        if not ctx.state:
            return None

        # Fetch from API
        instance = await self.api.get_instance(ctx.state.id)
        if not instance:
            return None  # Instance deleted

        return InstanceState(
            id=ctx.state.id,
            name=instance.name,
            size=instance.size,
            ami=instance.ami,
            public_ip=instance.public_ip,
            status=instance.status,
        )

    async def _create_apply(self, ctx: ResourceContext) -> tuple[InstanceState | None, None]:
        """Create instance (apply phase)."""
        if not ctx.config:
            return None, None

        # Create via API
        instance = await self.api.create_instance(
            name=ctx.config.name,
            size=ctx.config.size,
            ami=ctx.config.ami or "ami-latest",
        )

        return InstanceState(
            id=instance.id,
            name=instance.name,
            size=instance.size,
            ami=instance.ami,
            public_ip=instance.public_ip,
            status=instance.status,
        ), None

    async def _update_apply(self, ctx: ResourceContext) -> tuple[InstanceState | None, None]:
        """Update instance (apply phase)."""
        if not ctx.config or not ctx.state:
            return None, None

        # Update via API
        instance = await self.api.update_instance(
            id=ctx.state.id,
            name=ctx.config.name,
            size=ctx.config.size,
        )

        return InstanceState(
            id=ctx.state.id,
            name=instance.name,
            size=instance.size,
            ami=ctx.state.ami,  # AMI can't change
            public_ip=instance.public_ip,
            status=instance.status,
        ), None

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        """Delete instance (apply phase)."""
        if not ctx.state:
            return

        await self.api.delete_instance(ctx.state.id)
```

**Terraform usage:**
```hcl
resource "mycloud_instance" "web" {
  name = "web-server"
  size = "t3.large"
  ami  = "ami-12345678"
}

output "instance_ip" {
  value = mycloud_instance.web.public_ip
}
```

## Data Source Decorator

### `@register_data_source(name: str)`

Registers a data source class with the Pyvider hub.

**Parameters:**
- `name` - Data source type name without provider prefix (e.g., `"ami"`)

**Complete Example:**

```python
from pyvider.data_sources import register_data_source, BaseDataSource
from pyvider.schema import s_data_source, a_str, a_list, PvsSchema
import attrs

@attrs.define
class AMILookupConfig:
    """Data source configuration (input)."""
    name_filter: str
    owner: str = "amazon"

@attrs.define
class AMILookupData:
    """Data source result (output)."""
    id: str
    ami_id: str
    name: str
    description: str
    architecture: str
    creation_date: str

@register_data_source("ami")
class AMILookup(BaseDataSource):
    """Looks up AMI information."""

    config_class = AMILookupConfig
    data_class = AMILookupData

    @classmethod
    def get_schema(cls) -> PvsSchema:
        """Define data source schema."""
        return s_data_source({
            # Inputs
            "name_filter": a_str(
                required=True,
                description="AMI name filter pattern"
            ),
            "owner": a_str(
                default="amazon",
                description="AMI owner"
            ),

            # Outputs
            "id": a_str(computed=True, description="Data source ID"),
            "ami_id": a_str(computed=True, description="AMI ID"),
            "name": a_str(computed=True, description="AMI name"),
            "description": a_str(computed=True, description="AMI description"),
            "architecture": a_str(computed=True, description="Architecture"),
            "creation_date": a_str(computed=True, description="Creation date"),
        })

    async def read(self, config: AMILookupConfig) -> AMILookupData:
        """Query API for AMI information."""
        # Search for AMI
        amis = await self.api.search_amis(
            name_filter=config.name_filter,
            owner=config.owner,
        )

        if not amis:
            raise DataSourceError(f"No AMI found matching '{config.name_filter}'")

        # Return most recent
        ami = amis[0]
        return AMILookupData(
            id=ami.id,
            ami_id=ami.id,
            name=ami.name,
            description=ami.description,
            architecture=ami.architecture,
            creation_date=ami.creation_date,
        )
```

**Terraform usage:**
```hcl
data "mycloud_ami" "ubuntu" {
  name_filter = "ubuntu-*-22.04-*"
  owner       = "canonical"
}

resource "mycloud_instance" "web" {
  ami  = data.mycloud_ami.ubuntu.ami_id
  name = "web-server"
}
```

## Function Decorator

### `@register_function(name: str)`

Registers a function class with the Pyvider hub.

**Parameters:**
- `name` - Function name (e.g., `"base64_encode"`)

**Complete Example:**

```python
from pyvider.functions import register_function, BaseFunction
from pyvider.schema import s_function, a_str, PvsSchema
import base64

@register_function("base64_encode")
class Base64EncodeFunction(BaseFunction):
    """Encodes a string to base64."""

    @classmethod
    def get_schema(cls) -> PvsSchema:
        """Define function signature."""
        return s_function(
            parameters=[
                a_str(description="String to encode"),
            ],
            return_type=a_str(description="Base64-encoded string"),
        )

    async def call(self, input: str) -> str:
        """Execute the function."""
        encoded = base64.b64encode(input.encode()).decode()
        return encoded
```

**Terraform usage:**
```hcl
locals {
  encoded = provider::mycloud::base64_encode("Hello, World!")
  # Result: "SGVsbG8sIFdvcmxkIQ=="
}
```

## Ephemeral Resource Decorator

### `@register_ephemeral_resource(name: str)`

Registers an ephemeral resource class with the Pyvider hub.

**Parameters:**
- `name` - Ephemeral resource type name (e.g., `"token"`)

**Complete Example:**

```python
from pyvider.ephemerals import register_ephemeral_resource, BaseEphemeral
from pyvider.schema import s_ephemeral, a_str, a_num, PvsSchema
import attrs

@attrs.define
class TokenConfig:
    """Ephemeral configuration."""
    scope: str
    ttl: int = 3600

@attrs.define
class TokenData:
    """Ephemeral data."""
    token: str
    expires_at: str

@register_ephemeral_resource("token")
class Token(BaseEphemeral):
    """Generates temporary access tokens."""

    config_class = TokenConfig
    data_class = TokenData

    @classmethod
    def get_schema(cls) -> PvsSchema:
        """Define ephemeral schema."""
        return s_ephemeral({
            # Inputs
            "scope": a_str(required=True, description="Token scope"),
            "ttl": a_num(default=3600, description="Time to live in seconds"),

            # Outputs
            "token": a_str(computed=True, sensitive=True, description="Access token"),
            "expires_at": a_str(computed=True, description="Expiration timestamp"),
        })

    async def open(self, config: TokenConfig) -> TokenData:
        """Create ephemeral resource."""
        # Generate token
        token = await self.api.create_token(
            scope=config.scope,
            ttl=config.ttl,
        )

        return TokenData(
            token=token.value,
            expires_at=token.expires_at,
        )

    async def renew(self, config: TokenConfig, data: TokenData) -> TokenData:
        """Renew ephemeral resource."""
        # Refresh token
        token = await self.api.refresh_token(data.token)

        return TokenData(
            token=token.value,
            expires_at=token.expires_at,
        )

    async def close(self, data: TokenData) -> None:
        """Cleanup ephemeral resource."""
        # Revoke token
        await self.api.revoke_token(data.token)
```

**Terraform usage:**
```hcl
ephemeral "mycloud_token" "api" {
  scope = "read:api"
  ttl   = 7200
}

resource "mycloud_api_call" "data" {
  token = ephemeral.mycloud_token.api.token
  # Token is automatically revoked when no longer needed
}
```

## Capability Decorator

### `@register_capability`

Registers a capability class with the Pyvider hub.

**Complete Example:**

```python
from pyvider.capabilities import register_capability, BaseCapability
import time

@register_capability
class CachingCapability(BaseCapability):
    """Adds response caching to components."""

    def __init__(self, ttl: int = 300):
        self.ttl = ttl
        self.cache = {}

    async def setup(self):
        """Initialize capability."""
        self.cache.clear()

    async def teardown(self):
        """Cleanup capability."""
        self.cache.clear()

    async def get(self, key: str):
        """Get from cache."""
        if key in self.cache:
            entry = self.cache[key]
            if time.time() < entry["expires"]:
                return entry["value"]
            else:
                del self.cache[key]
        return None

    async def set(self, key: str, value):
        """Set in cache."""
        self.cache[key] = {
            "value": value,
            "expires": time.time() + self.ttl,
        }
```

**Usage with resources:**

```python
from pyvider.capabilities import use_capability

@register_resource("instance")
@use_capability(CachingCapability(ttl=600))
class Instance(BaseResource):
    """Instance with caching."""
    pass
```

## Decorator Combinations

### Multiple Decorators

You can combine decorators:

```python
@register_resource("server")
@use_capability(CachingCapability())
@use_capability(MetricsCapability())
class Server(BaseResource):
    """Server with caching and metrics."""
    pass
```

### Conditional Registration

Register components conditionally:

```python
import os

# Only register in certain environments
if os.getenv("ENABLE_BETA_FEATURES"):
    @register_resource("beta_feature")
    class BetaFeature(BaseResource):
        pass
```

## Best Practices

### 1. Use Descriptive Names

```python
# ✅ Good: Clear, descriptive name
@register_resource("compute_instance")
class ComputeInstance(BaseResource):
    pass

# ❌ Bad: Vague name
@register_resource("thing")
class Thing(BaseResource):
    pass
```

### 2. Register in Component Modules

```python
# my_provider/resources/instance.py
@register_resource("instance")
class Instance(BaseResource):
    """Keep decorator with class definition."""
    pass
```

### 3. Follow Naming Conventions

```python
# Provider name: lowercase, no underscores
@register_provider("mycloud")  # ✅

# Resource/data source: lowercase with underscores
@register_resource("compute_instance")  # ✅
@register_data_source("ami_lookup")     # ✅

# Function: lowercase with underscores
@register_function("base64_encode")     # ✅
```

### 4. One Decorator Per Component

```python
# ✅ Good: One decorator per class
@register_resource("instance")
class Instance(BaseResource):
    pass

# ❌ Bad: Don't register same class multiple times
@register_resource("instance")
@register_resource("server")  # Don't do this
class Instance(BaseResource):
    pass
```

### 5. Import Decorators from Correct Module

```python
# ✅ Good: Import from correct module
from pyvider.resources import register_resource
from pyvider.data_sources import register_data_source
from pyvider.functions import register_function

# ❌ Bad: Don't import from pyvider.decorators (doesn't exist)
```

## Common Patterns

### Provider with Multiple Resources

```python
# provider.py
@register_provider("mycloud")
class MyCloudProvider(BaseProvider):
    pass

# resources/instance.py
@register_resource("instance")
class Instance(BaseResource):
    pass

# resources/network.py
@register_resource("network")
class Network(BaseResource):
    pass
```

### Shared Base Classes

```python
# Don't register base classes
class MyBaseResource(BaseResource):
    """Shared functionality for all resources."""

    async def _common_validation(self):
        pass

# Register concrete implementations
@register_resource("instance")
class Instance(MyBaseResource):
    pass

@register_resource("database")
class Database(MyBaseResource):
    pass
```

### Testing Decorated Components

```python
import pytest

@pytest.fixture
def instance_resource():
    """Create instance resource for testing."""
    return Instance()

async def test_instance_creation(instance_resource):
    """Test instance resource."""
    # Test implementation
    pass
```

## Debugging Registration

### Check Registered Components

```python
# Inspect components registered in the hub
from pyvider.hub import hub

# List all registered resources
resources = hub.get_components("resource")
print(f"Registered resources: {list(resources.keys())}")

# Get specific component
instance_class = hub.get_component("resource", "instance")
```

### Common Registration Errors

**Error: Component not found**
```python
# Ensure decorator is applied and module is imported
@register_resource("instance")  # ← Decorator required
class Instance(BaseResource):
    pass

# Ensure module is imported in __init__.py
from .resources.instance import Instance  # ← Must import
```

**Error: Duplicate registration**
```python
# Don't register same name twice
@register_resource("instance")
class Instance1(BaseResource):
    pass

@register_resource("instance")  # ← Error: duplicate name
class Instance2(BaseResource):
    pass
```

## See Also

- [Creating Providers](../building-components/creating-providers.md) - Provider implementation guide
- [Creating Resources](../building-components/creating-resources.md) - Resource implementation guide
- [Creating Data Sources](../building-components/creating-data-sources.md) - Data source implementation guide
- [Creating Functions](../building-components/creating-functions.md) - Function implementation guide
- [Capabilities Overview](../../capabilities/overview.md) - Capabilities system
