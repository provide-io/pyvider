# Creating Providers

This comprehensive guide walks you through creating production-focused Terraform providers using Pyvider, from basic setup to advanced features.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Provider Anatomy](#provider-anatomy)
- [Step-by-Step Provider Creation](#step-by-step-provider-creation)

---

## Prerequisites

Before creating a provider, you should understand:
- Basic Terraform concepts (providers, resources, state)
- Python async/await programming
- attrs for class definitions
- Type hints in Python

## Provider Anatomy

A complete provider consists of several components:

```
my_provider/
├── __init__.py           # Package initialization
├── provider.py           # Provider definition
├── resources/            # Resource implementations
│   ├── __init__.py
│   ├── server.py
│   └── network.py
├── data_sources/         # Data source implementations
│   ├── __init__.py
│   └── images.py
├── functions/            # Provider functions
│   ├── __init__.py
│   └── validators.py
└── tests/                # Test suite
    ├── __init__.py
    └── test_provider.py
```

## Step-by-Step Provider Creation

### Step 1: Define Provider Class

Create the main provider class with metadata and configuration:

```python
# provider.py
from pyvider.providers import register_provider, BaseProvider, ProviderMetadata
from pyvider.schema import s_provider, a_str, a_num, a_bool, PvsSchema
import attrs
import httpx

@attrs.define
class MyCloudConfig:
    """Provider runtime configuration."""
    api_key: str
    api_endpoint: str = "https://api.mycloud.com/v1"
    region: str = "us-east-1"
    timeout: int = 30
    max_retries: int = 3
    verify_ssl: bool = True

@register_provider("mycloud")
class MyCloudProvider(BaseProvider):
    """
    MyCloud Infrastructure Provider

    Manages resources in the MyCloud platform including compute instances,
    storage, and networking components.
    """

    def __init__(self):
        """Initialize provider with metadata."""
        super().__init__(
            metadata=ProviderMetadata(
                name="mycloud",
                version="1.0.0",
                protocol_version="6",
                description="MyCloud infrastructure provider"
            )
        )
        self.api_client = None
        self.provider_config: MyCloudConfig | None = None

    def _build_schema(self) -> PvsSchema:
        """Define provider configuration schema."""
        return s_provider({
            # Required authentication
            "api_key": a_str(
                required=True,
                sensitive=True,
                description="API key for MyCloud authentication"
            ),

            # Optional configuration
            "api_endpoint": a_str(
                default="https://api.mycloud.com/v1",
                description="MyCloud API endpoint URL"
            ),

            "region": a_str(
                default="us-east-1",
                description="Default region for resources",
                validators=[
                    lambda x: x in ["us-east-1", "us-west-2", "eu-central-1"]
                              or "Invalid region"
                ]
            ),

            "timeout": a_num(
                default=30,
                description="API request timeout in seconds",
                validators=[
                    lambda x: 5 <= x <= 300 or "Timeout must be between 5 and 300 seconds"
                ]
            ),

            "max_retries": a_num(
                default=3,
                description="Maximum API retry attempts",
                validators=[
                    lambda x: 0 <= x <= 10 or "Max retries must be between 0 and 10"
                ]
            ),

            "verify_ssl": a_bool(
                default=True,
                description="Verify SSL certificates"
            ),
        })

    async def configure(self, config: dict) -> None:
        """
        Configure the provider with user settings.

        This method is called by Terraform with the provider configuration
        from the user's Terraform files.
        """
        await super().configure(config)

        # Convert config dict to attrs instance
        self.provider_config = MyCloudConfig(
            api_key=config["api_key"],
            api_endpoint=config.get("api_endpoint", "https://api.mycloud.com/v1"),
            region=config.get("region", "us-east-1"),
            timeout=config.get("timeout", 30),
            max_retries=config.get("max_retries", 3),
            verify_ssl=config.get("verify_ssl", True),
        )

        # Initialize API client
        self.api_client = httpx.AsyncClient(
            base_url=self.provider_config.api_endpoint,
            headers={
                "Authorization": f"Bearer {self.provider_config.api_key}",
                "User-Agent": f"terraform-provider-mycloud/{self.metadata.version}",
            },
            timeout=self.provider_config.timeout,
            verify=self.provider_config.verify_ssl,
        )

        # Test connection
        try:
            response = await self.api_client.get("/health")
            response.raise_for_status()
        except Exception as e:
            raise ProviderConfigurationError(f"Failed to connect to MyCloud API: {e}")
```

**Terraform usage:**

```hcl
terraform {
  required_providers {
    mycloud = {
      source  = "mycompany/mycloud"
      version = "~> 1.0"
    }
  }
}

provider "mycloud" {
  api_key      = var.mycloud_api_key
  region       = "us-west-2"
  timeout      = 60
  max_retries  = 5
  verify_ssl   = true
}
```

### Step 2: Add Provider Methods

Implement optional provider lifecycle methods:

```python
class MyCloudProvider(BaseProvider):
    # ... (previous code)

    async def validate_config(self, config: dict) -> list[str]:
        """
        Validate provider configuration before use.

        Returns list of validation error messages (empty if valid).
        """
        errors = []

        # Validate API key format
        api_key = config.get("api_key", "")
        if not api_key.startswith("mck_"):
            errors.append("API key must start with 'mck_'")

        if len(api_key) < 40:
            errors.append("API key appears invalid (too short)")

        # Validate endpoint URL
        endpoint = config.get("api_endpoint", "")
        if endpoint and not endpoint.startswith("https://"):
            errors.append("API endpoint must use HTTPS")

        return errors

    async def close(self) -> None:
        """
        Cleanup provider resources.

        Called when provider is being shut down.
        """
        if self.api_client:
            await self.api_client.aclose()
            self.api_client = None
```

### Step 3: Create Package Structure

Set up your provider package:

```python
# __init__.py
"""
MyCloud Terraform Provider

A Terraform provider for managing MyCloud infrastructure.
"""

from .provider import MyCloudProvider

__all__ = ["MyCloudProvider"]
__version__ = "1.0.0"
```

```python
# resources/__init__.py
"""MyCloud resources."""

from .server import Server
from .network import Network

__all__ = ["Server", "Network"]
```

```python
# data_sources/__init__.py
"""MyCloud data sources."""

from .image import ImageLookup

__all__ = ["ImageLookup"]
```

### Step 4: Add Resources

Create resource implementations:

```python
# resources/server.py
from pyvider.resources import register_resource, BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.schema import s_resource, a_str, a_num, PvsSchema
import attrs

@attrs.define
class ServerConfig:
    name: str
    size: str = "small"
    image: str | None = None

@attrs.define
class ServerState:
    id: str
    name: str
    size: str
    image: str
    ip_address: str
    status: str

@register_resource("server")
class Server(BaseResource):
    """Manages a compute server."""

    config_class = ServerConfig
    state_class = ServerState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource({
            "name": a_str(required=True, description="Server name"),
            "size": a_str(default="small", description="Server size"),
            "image": a_str(description="Image ID"),

            "id": a_str(computed=True, description="Server ID"),
            "ip_address": a_str(computed=True, description="IP address"),
            "status": a_str(computed=True, description="Server status"),
        })

    async def read(self, ctx: ResourceContext) -> ServerState | None:
        if not ctx.state:
            return None

        # Get provider instance
        from pyvider.hub import hub
        provider = hub.get_component("singleton", "provider")

        if provider is None:
            raise RuntimeError("Provider has not been registered in the hub yet.")

        # Fetch server from API
        response = await provider.api_client.get(f"/servers/{ctx.state.id}")
        if response.status_code == 404:
            return None

        data = response.json()
        return ServerState(
            id=ctx.state.id,
            name=data["name"],
            size=data["size"],
            image=data["image"],
            ip_address=data["ip_address"],
            status=data["status"],
        )

    async def _create_apply(self, ctx: ResourceContext) -> tuple[ServerState | None, None]:
        if not ctx.config:
            return None, None

        from pyvider.hub import hub
        provider = hub.get_component("singleton", "provider")

        # Create server via API
        response = await provider.api_client.post("/servers", json={
            "name": ctx.config.name,
            "size": ctx.config.size,
            "image": ctx.config.image or "ubuntu-22.04",
            "region": provider.provider_config.region,
        })
        response.raise_for_status()

        data = response.json()
        return ServerState(
            id=data["id"],
            name=data["name"],
            size=data["size"],
            image=data["image"],
            ip_address=data["ip_address"],
            status=data["status"],
        ), None

    async def _update_apply(self, ctx: ResourceContext) -> tuple[ServerState | None, None]:
        if not ctx.config or not ctx.state:
            return None, None

        from pyvider.hub import hub
        provider = hub.get_component("singleton", "provider")

        # Update server via API
        response = await provider.api_client.patch(
            f"/servers/{ctx.state.id}",
            json={
                "name": ctx.config.name,
                "size": ctx.config.size,
            }
        )
        response.raise_for_status()

        data = response.json()
        return ServerState(
            id=ctx.state.id,
            name=data["name"],
            size=data["size"],
            image=ctx.state.image,  # Image can't change
            ip_address=data["ip_address"],
            status=data["status"],
        ), None

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        if not ctx.state:
            return

        from pyvider.hub import hub
        provider = hub.get_component("singleton", "provider")

        # Delete server via API
        await provider.api_client.delete(f"/servers/{ctx.state.id}")
```

### Step 5: Add Data Sources

```python
# data_sources/image.py
from pyvider.data_sources import register_data_source, BaseDataSource
from pyvider.schema import s_data_source, a_str, PvsSchema
import attrs

@attrs.define
class ImageLookupConfig:
    name_filter: str
    os_type: str = "linux"

@attrs.define
class ImageLookupData:
    id: str
    image_id: str
    name: str
    os_type: str
    version: str

@register_data_source("image")
class ImageLookup(BaseDataSource):
    """Looks up operating system images."""

    config_class = ImageLookupConfig
    data_class = ImageLookupData

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_data_source({
            "name_filter": a_str(required=True, description="Image name filter"),
            "os_type": a_str(default="linux", description="OS type"),

            "id": a_str(computed=True, description="Data source ID"),
            "image_id": a_str(computed=True, description="Image ID"),
            "name": a_str(computed=True, description="Image name"),
            "version": a_str(computed=True, description="Image version"),
        })

    async def read(self, config: ImageLookupConfig) -> ImageLookupData:
        from pyvider.hub import hub
        provider = hub.get_component("singleton", "provider")

        # Search for images
        response = await provider.api_client.get("/images", params={
            "name": config.name_filter,
            "os_type": config.os_type,
        })
        response.raise_for_status()

        images = response.json()
        if not images:
            raise DataSourceError(f"No image found matching '{config.name_filter}'")

        # Return most recent
        image = images[0]
        return ImageLookupData(
            id=image["id"],
            image_id=image["id"],
            name=image["name"],
            os_type=image["os_type"],
            version=image["version"],
        )
```

### Step 6: Add Provider Functions

```python
# functions/validators.py
from pyvider.functions import register_function, BaseFunction
from pyvider.schema import s_function, a_str, a_bool, PvsSchema
import re

@register_function("validate_server_name")
class ValidateServerName(BaseFunction):
    """Validates server name format."""

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_function(
            parameters=[
                a_str(description="Server name to validate"),
            ],
            return_type=a_bool(description="Whether name is valid"),
        )

    async def call(self, name: str) -> bool:
        # Must be alphanumeric with hyphens, 3-63 chars
        pattern = r'^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$'
        return bool(re.match(pattern, name))
```

## Next Steps

You now have a complete, basic provider! For advanced features like error handling, retry logic, rate limiting, caching, and comprehensive testing, see the [Advanced Provider Features](../advanced/advanced-provider-features.md) guide.

## Complete Example

See the full example provider at:

- [GitHub: pyvider-components/providers/mycloud](https://github.com/provide-io/pyvider-components)

## See Also

- [Advanced Provider Features](../advanced/advanced-provider-features.md) - Error handling, retry logic, caching, and testing
- [Creating Resources](../building-components/creating-resources.md) - Resource implementation
- [Creating Data Sources](../building-components/creating-data-sources.md) - Data source implementation
- [Creating Functions](../building-components/creating-functions.md) - Function implementation
- [Best Practices](../production/best-practices.md) - Production patterns
