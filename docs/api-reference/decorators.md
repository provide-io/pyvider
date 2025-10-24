# Decorators API Reference

This page documents the core decorators used to register components in Pyvider.

## Overview

Pyvider uses decorators to register components with the hub-based discovery system. All components must be decorated to be recognized by the framework.

## Provider Decorators

### `@register_provider`

Registers a provider class with the Pyvider hub.

**Signature:**
```python
def register_provider(name: str) -> Callable
```

**Parameters:**
- `name` (str): The provider name used in Terraform configurations

**Example:**
```python
from pyvider.providers import register_provider, BaseProvider, ProviderMetadata
from pyvider.schema import Attribute
import attrs

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

    @attrs.define
    class Config:
        api_key: str = Attribute(
            required=True,
            sensitive=True,
            description="API key for authentication"
        )
        region: str = Attribute(
            default="us-east-1",
            description="Default region"
        )

    async def configure(self, config: Config) -> None:
        """Configure the provider."""
        # Initialize API client, etc.
        pass
```

**Usage in Terraform:**
```hcl
provider "mycloud" {
  api_key = var.api_key
  region  = "us-west-2"
}
```

## Resource Decorators

### `@register_resource`

Registers a resource class with the Pyvider hub.

**Signature:**
```python
def register_resource(name: str) -> Callable
```

**Parameters:**
- `name` (str): The resource type name (without provider prefix)

**Example:**
```python
from pyvider.resources import register_resource, BaseResource
from pyvider.schema import Attribute
import attrs

@register_resource("instance")
class Instance(BaseResource):
    """Cloud compute instance resource."""

    @attrs.define
    class Config:
        name: str = Attribute(required=True, description="Instance name")
        size: str = Attribute(default="t2.micro", description="Instance size")
        ami: str = Attribute(required=True, description="AMI ID")

    @attrs.define
    class State:
        id: str = Attribute(computed=True, description="Instance ID")
        public_ip: str = Attribute(computed=True, description="Public IP")
        status: str = Attribute(computed=True, description="Instance status")

    async def create(self, config: Config) -> State:
        """Create the instance."""
        # Create instance via API
        return State(
            id=f"i-{config.name}",
            public_ip="203.0.113.42",
            status="running"
        )

    async def read(self, state: State) -> State | None:
        """Read the instance state."""
        # Check if instance exists
        return state

    async def update(self, config: Config, state: State) -> State:
        """Update the instance."""
        # Update instance via API
        return state

    async def delete(self, state: State) -> None:
        """Delete the instance."""
        # Delete instance via API
        pass
```

**Usage in Terraform:**
```hcl
resource "mycloud_instance" "web" {
  name = "web-server"
  size = "t3.large"
  ami  = "ami-12345678"
}
```

## Data Source Decorators

### `@register_data_source`

Registers a data source class with the Pyvider hub.

**Signature:**
```python
def register_data_source(name: str) -> Callable
```

**Parameters:**
- `name` (str): The data source type name (without provider prefix)

**Example:**
```python
from pyvider.data_sources import register_data_source, BaseDataSource
from pyvider.schema import Attribute
import attrs

@register_data_source("image")
class Image(BaseDataSource):
    """Cloud machine image data source."""

    @attrs.define
    class Config:
        name_filter: str = Attribute(
            required=True,
            description="Name filter for images"
        )
        most_recent: bool = Attribute(
            default=True,
            description="Return most recent image"
        )

    @attrs.define
    class Data:
        id: str = Attribute(computed=True, description="Image ID")
        name: str = Attribute(computed=True, description="Image name")
        created_at: str = Attribute(computed=True, description="Creation timestamp")

    async def read(self, config: Config) -> Data:
        """Read image data from API."""
        # Query API for images
        return Data(
            id="ami-12345678",
            name="ubuntu-22.04",
            created_at="2024-01-01T00:00:00Z"
        )
```

**Usage in Terraform:**
```hcl
data "mycloud_image" "ubuntu" {
  name_filter = "ubuntu-22.04"
  most_recent = true
}

resource "mycloud_instance" "web" {
  ami = data.mycloud_image.ubuntu.id
}
```

## Function Decorators

### `@register_function`

Registers a provider function with the Pyvider hub.

**Signature:**
```python
def register_function(name: str) -> Callable
```

**Parameters:**
- `name` (str): The function name

**Example:**
```python
from pyvider.functions import register_function, BaseFunction
from pyvider.schema import Attribute
import attrs
import hashlib

@register_function("hash")
class HashFunction(BaseFunction):
    """Compute hash of input string."""

    @attrs.define
    class Parameters:
        input: str = Attribute(required=True, description="Input string")
        algorithm: str = Attribute(
            default="sha256",
            description="Hash algorithm"
        )

    @attrs.define
    class Result:
        output: str = Attribute(computed=True, description="Hash output")

    async def call(self, params: Parameters) -> Result:
        """Compute the hash."""
        if params.algorithm == "sha256":
            hash_obj = hashlib.sha256(params.input.encode())
        elif params.algorithm == "md5":
            hash_obj = hashlib.md5(params.input.encode())
        else:
            raise ValueError(f"Unsupported algorithm: {params.algorithm}")

        return Result(output=hash_obj.hexdigest())
```

**Usage in Terraform:**
```hcl
locals {
  config_hash = provider::mycloud::hash({
    input     = "my-config-string"
    algorithm = "sha256"
  }).output
}
```

## Ephemeral Resource Decorators

### `@register_ephemeral`

Registers an ephemeral resource class with the Pyvider hub.

**Signature:**
```python
def register_ephemeral(name: str) -> Callable
```

**Parameters:**
- `name` (str): The ephemeral resource type name (without provider prefix)

**Example:**
```python
from pyvider.ephemerals import register_ephemeral, BaseEphemeral
from pyvider.schema import Attribute
import attrs

@register_ephemeral("token")
class Token(BaseEphemeral):
    """Temporary authentication token."""

    @attrs.define
    class Config:
        scope: str = Attribute(required=True, description="Token scope")
        ttl: int = Attribute(default=3600, description="Time to live in seconds")

    @attrs.define
    class Data:
        token: str = Attribute(
            computed=True,
            sensitive=True,
            description="Authentication token"
        )
        expires_at: str = Attribute(
            computed=True,
            description="Expiration timestamp"
        )

    async def open(self, config: Config) -> Data:
        """Generate a new token."""
        # Request token from API
        return Data(
            token="tok_abcdef123456",
            expires_at="2024-01-01T01:00:00Z"
        )

    async def renew(self, config: Config, data: Data) -> Data:
        """Renew the token."""
        # Renew token via API
        return data

    async def close(self, data: Data) -> None:
        """Revoke the token."""
        # Revoke token via API
        pass
```

**Usage in Terraform:**
```hcl
ephemeral "mycloud_token" "api" {
  scope = "read:write"
  ttl   = 7200
}

resource "mycloud_instance" "web" {
  token = ephemeral.mycloud_token.api.token
}
```

## Best Practices

### Naming Conventions

1. **Provider names**: Use lowercase, hyphen-separated names (e.g., `my-cloud`)
2. **Resource names**: Use singular nouns (e.g., `instance`, not `instances`)
3. **Data source names**: Use singular nouns describing the data (e.g., `image`)
4. **Function names**: Use verb or descriptive names (e.g., `hash`, `validate`)

### Type Safety

Always use `attrs.define` for Config, State, Data, Parameters, and Result classes:

```python
@attrs.define
class Config:
    # Configuration attributes
    pass
```

### Async Methods

All lifecycle methods should be async:

```python
async def create(self, config: Config) -> State:
    # Implementation
    pass
```

### Documentation

Always include docstrings:

```python
@register_resource("instance")
class Instance(BaseResource):
    """
    Cloud compute instance resource.

    Manages virtual machine instances in MyCloud.
    """
    pass
```

## See Also

- [Creating Providers](../guides/creating-providers.md) - Complete provider development guide
- [Creating Resources](../guides/creating-resources.md) - Resource implementation guide
- [Creating Data Sources](../guides/creating-data-sources.md) - Data source guide
- [Creating Functions](../guides/creating-functions.md) - Function development guide
- [Schema API](schema.md) - Schema system reference
