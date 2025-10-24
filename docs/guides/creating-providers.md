# Creating Providers

This comprehensive guide walks you through creating production-ready Terraform providers using Pyvider, from basic setup to advanced features.

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
        from pyvider.hub import ProviderHub
        provider = ProviderHub.get_provider()

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

        from pyvider.hub import ProviderHub
        provider = ProviderHub.get_provider()

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

        from pyvider.hub import ProviderHub
        provider = ProviderHub.get_provider()

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

        from pyvider.hub import ProviderHub
        provider = ProviderHub.get_provider()

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
        from pyvider.hub import ProviderHub
        provider = ProviderHub.get_provider()

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

## Advanced Provider Features

### Error Handling

Implement comprehensive error handling:

```python
from pyvider.exceptions import (
    ProviderError,
    ProviderConfigurationError,
    ResourceNotFoundError,
    APIError,
)

class MyCloudProvider(BaseProvider):
    async def configure(self, config: dict) -> None:
        try:
            await super().configure(config)

            # Validate API key
            if not await self._validate_api_key(config["api_key"]):
                raise ProviderConfigurationError("Invalid API key")

            # Initialize client
            self.api_client = self._create_client(config)

            # Test connection
            await self._test_connection()

        except httpx.HTTPError as e:
            raise ProviderConfigurationError(f"Failed to connect: {e}")
        except Exception as e:
            raise ProviderError(f"Provider configuration failed: {e}")

    async def _validate_api_key(self, api_key: str) -> bool:
        """Validate API key format and permissions."""
        if not api_key.startswith("mck_"):
            return False

        # Test API key
        try:
            response = await self.api_client.get("/auth/validate")
            return response.status_code == 200
        except Exception:
            return False

    async def _test_connection(self) -> None:
        """Test API connectivity."""
        try:
            response = await self.api_client.get("/health")
            response.raise_for_status()
        except httpx.HTTPError as e:
            raise ProviderConfigurationError(
                f"Health check failed: {e}. "
                f"Verify API endpoint and network connectivity."
            )
```

### Retry Logic

Add automatic retries for transient failures:

```python
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

class MyCloudProvider(BaseProvider):
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(httpx.HTTPStatusError),
    )
    async def _api_request(self, method: str, path: str, **kwargs):
        """Make API request with automatic retry."""
        response = await self.api_client.request(method, path, **kwargs)

        # Don't retry client errors (4xx)
        if 400 <= response.status_code < 500:
            response.raise_for_status()

        # Retry server errors (5xx) and network issues
        if response.status_code >= 500:
            response.raise_for_status()

        return response
```

### Rate Limiting

Implement rate limiting:

```python
import asyncio
from datetime import datetime, timedelta

class MyCloudProvider(BaseProvider):
    def __init__(self):
        super().__init__(...)
        self.rate_limiter = RateLimiter(
            max_requests=100,
            time_window=timedelta(minutes=1)
        )

    async def _api_request(self, method: str, path: str, **kwargs):
        """Make rate-limited API request."""
        await self.rate_limiter.acquire()
        return await self.api_client.request(method, path, **kwargs)

class RateLimiter:
    def __init__(self, max_requests: int, time_window: timedelta):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []

    async def acquire(self):
        """Wait if rate limit reached."""
        now = datetime.now()

        # Remove old requests
        self.requests = [
            req_time for req_time in self.requests
            if now - req_time < self.time_window
        ]

        # Wait if limit reached
        if len(self.requests) >= self.max_requests:
            oldest = min(self.requests)
            wait_time = (oldest + self.time_window - now).total_seconds()
            if wait_time > 0:
                await asyncio.sleep(wait_time)

        self.requests.append(now)
```

### Caching

Add response caching:

```python
from functools import lru_cache
import time

class MyCloudProvider(BaseProvider):
    def __init__(self):
        super().__init__(...)
        self.cache = {}

    async def get_with_cache(
        self,
        path: str,
        ttl: int = 300,
        **kwargs
    ):
        """Get resource with caching."""
        cache_key = f"{path}:{kwargs}"

        # Check cache
        if cache_key in self.cache:
            cached_at, data = self.cache[cache_key]
            if time.time() - cached_at < ttl:
                return data

        # Fetch fresh data
        response = await self.api_client.get(path, **kwargs)
        data = response.json()

        # Cache result
        self.cache[cache_key] = (time.time(), data)

        return data
```

### Logging

Add structured logging:

```python
from provide.foundation import get_logger

class MyCloudProvider(BaseProvider):
    def __init__(self):
        super().__init__(...)
        self.logger = get_logger(__name__)

    async def configure(self, config: dict) -> None:
        self.logger.info(
            "Configuring MyCloud provider",
            region=config.get("region"),
            endpoint=config.get("api_endpoint"),
        )

        await super().configure(config)

        self.logger.info("Provider configured successfully")

    async def _api_request(self, method: str, path: str, **kwargs):
        self.logger.debug(
            "API request",
            method=method,
            path=path,
        )

        try:
            response = await self.api_client.request(method, path, **kwargs)

            self.logger.debug(
                "API response",
                method=method,
                path=path,
                status=response.status_code,
            )

            return response
        except Exception as e:
            self.logger.error(
                "API request failed",
                method=method,
                path=path,
                error=str(e),
            )
            raise
```

## Testing Your Provider

### Unit Tests

```python
# tests/test_provider.py
import pytest
from my_provider.provider import MyCloudProvider

@pytest.fixture
def provider():
    return MyCloudProvider()

@pytest.mark.asyncio
async def test_provider_configuration(provider):
    """Test provider configuration."""
    config = {
        "api_key": "mck_test_key_1234567890abcdefghijklmnop",
        "region": "us-east-1",
    }

    await provider.configure(config)

    assert provider.provider_config.api_key == config["api_key"]
    assert provider.provider_config.region == config["region"]
    assert provider.api_client is not None

@pytest.mark.asyncio
async def test_provider_validation():
    """Test configuration validation."""
    provider = MyCloudProvider()

    # Invalid API key
    errors = await provider.validate_config({
        "api_key": "invalid_key",
    })

    assert len(errors) > 0
    assert any("API key" in err for err in errors)
```

### Integration Tests

```python
# tests/test_integration.py
import pytest
import os

@pytest.mark.skipif(
    not os.getenv("MYCLOUD_API_KEY"),
    reason="Requires MYCLOUD_API_KEY environment variable"
)
@pytest.mark.asyncio
async def test_real_api_connection():
    """Test connection to real API."""
    provider = MyCloudProvider()

    config = {
        "api_key": os.getenv("MYCLOUD_API_KEY"),
        "region": "us-east-1",
    }

    await provider.configure(config)

    # Test health check
    response = await provider.api_client.get("/health")
    assert response.status_code == 200
```

## Best Practices

### 1. Version Your Provider

```python
metadata=ProviderMetadata(
    name="mycloud",
    version="1.0.0",  # Semantic versioning
    protocol_version="6",
)
```

### 2. Document Configuration Options

```python
"api_key": a_str(
    required=True,
    sensitive=True,
    description=(
        "API key for MyCloud authentication. "
        "Get your key from https://mycloud.com/settings/api"
    )
)
```

### 3. Validate Early

```python
async def validate_config(self, config: dict) -> list[str]:
    """Validate before attempting to use config."""
    errors = []

    # Check all requirements
    if not config.get("api_key"):
        errors.append("api_key is required")

    return errors
```

### 4. Handle Cleanup

```python
async def close(self) -> None:
    """Always cleanup resources."""
    if self.api_client:
        await self.api_client.aclose()
```

### 5. Use Type Hints

```python
async def configure(self, config: dict) -> None:
    self.provider_config: MyCloudConfig = MyCloudConfig(**config)
```

## Complete Example

See the full example provider at:
- [GitHub: pyvider-components/providers/mycloud](https://github.com/provide-io/pyvider-components)

## See Also

- [Creating Resources](creating-resources.md) - Resource implementation
- [Creating Data Sources](creating-data-sources.md) - Data source implementation
- [Creating Functions](creating-functions.md) - Function implementation
- [Testing Providers](testing-providers.md) - Testing strategies
- [Best Practices](best-practices.md) - Production patterns
