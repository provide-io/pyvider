# Providers API

Base classes and utilities for creating Terraform providers.

## Overview

Providers in Pyvider are the entry point for your Terraform provider implementation. They handle:
- **Configuration** and authentication
- **Metadata** (name, version, protocol)
- **Component discovery** and registration
- **Shared state** and resources

### Key Components

- **`BaseProvider`** - Base class for all providers
- **`@register_provider`** - Decorator for provider registration
- **`ProviderMetadata`** - Provider metadata definition
- **`ProviderContext`** - Provider runtime context
- **Provider capabilities** - Reusable provider behaviors

### Lifecycle

Providers implement:
- `setup()` - Initialize provider (called once)
- `configure()` - Configure with user settings
- `get_schema()` - Return provider configuration schema

## Usage Examples

### Basic Provider

```python
import httpx
from pyvider.providers import register_provider, BaseProvider, ProviderMetadata
from pyvider.schema import s_provider, a_str, a_num, a_bool, PvsSchema
from pyvider.exceptions import ProviderConfigurationError


@register_provider("mycloud")
class MyCloudProvider(BaseProvider):
    """Terraform provider for MyCloud API."""

    def __init__(self):
        super().__init__(
            metadata=ProviderMetadata(
                name="mycloud",
                version="1.0.0",
                protocol_version="6",
                description="MyCloud API provider",
            )
        )
        self.http_client = None
        self.api_endpoint = None

    def _build_schema(self) -> PvsSchema:
        """Define provider configuration schema."""
        return s_provider({
            "api_endpoint": a_str(
                required=True,
                description="API endpoint URL",
                validators=[
                    lambda x: x.startswith("https://") or "Must use HTTPS",
                ],
            ),
            "api_key": a_str(
                required=True,
                sensitive=True,
                description="API authentication key",
            ),
            "timeout": a_num(
                default=30,
                description="Request timeout in seconds",
            ),
            "verify_ssl": a_bool(
                default=True,
                description="Verify SSL certificates",
            ),
        })

    async def configure(self, config: dict) -> None:
        """Configure the provider with user settings."""
        await super().configure(config)

        self.api_endpoint = config["api_endpoint"]

        # Create HTTP client with connection pooling
        self.http_client = httpx.AsyncClient(
            base_url=self.api_endpoint,
            headers={"Authorization": f"Bearer {config['api_key']}"},
            timeout=config.get("timeout", 30),
            verify=config.get("verify_ssl", True),
            limits=httpx.Limits(
                max_connections=100,
                max_keepalive_connections=20,
            ),
        )

        # Test connectivity
        try:
            response = await self.http_client.get("/health")
            response.raise_for_status()
        except Exception as e:
            raise ProviderConfigurationError(f"Failed to connect: {e}")

    async def close(self) -> None:
        """Clean up resources."""
        if self.http_client:
            await self.http_client.aclose()
```

### Provider with Retry Logic

```python
import asyncio
from typing import Any
import httpx


@register_provider("resilient_provider")
class ResilientProvider(BaseProvider):
    """Provider with automatic retry logic."""

    async def configure(self, config: dict) -> None:
        await super().configure(config)

        self.max_retries = config.get("max_retries", 3)
        self.retry_delay = config.get("retry_delay", 1.0)

        self.http_client = httpx.AsyncClient(
            base_url=config["api_endpoint"],
            headers={"Authorization": f"Bearer {config['api_key']}"},
        )

    async def api_request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> httpx.Response:
        """Make API request with retry logic."""
        for attempt in range(self.max_retries + 1):
            try:
                response = await self.http_client.request(
                    method, path, **kwargs
                )
                response.raise_for_status()
                return response

            except httpx.HTTPStatusError as e:
                # Don't retry client errors (4xx)
                if 400 <= e.response.status_code < 500:
                    raise

                # Retry server errors (5xx)
                if attempt < self.max_retries:
                    await asyncio.sleep(self.retry_delay * (2 ** attempt))
                    continue
                raise

            except httpx.RequestError:
                if attempt < self.max_retries:
                    await asyncio.sleep(self.retry_delay * (2 ** attempt))
                    continue
                raise
```

### Provider with Caching

```python
from datetime import datetime, timedelta
from functools import lru_cache


@register_provider("caching_provider")
class CachingProvider(BaseProvider):
    """Provider with response caching."""

    def __init__(self):
        super().__init__(...)
        self._cache = {}
        self._cache_expiry = {}

    async def get_with_cache(
        self,
        key: str,
        fetcher: callable,
        ttl: int = 300,
    ) -> Any:
        """Get data with time-based caching."""
        now = datetime.now()

        # Check cache
        if key in self._cache:
            expiry = self._cache_expiry.get(key)
            if expiry and now < expiry:
                return self._cache[key]

        # Fetch fresh data
        data = await fetcher()

        # Update cache
        self._cache[key] = data
        self._cache_expiry[key] = now + timedelta(seconds=ttl)

        return data

    def invalidate_cache(self, key: str = None):
        """Invalidate cache entry or entire cache."""
        if key:
            self._cache.pop(key, None)
            self._cache_expiry.pop(key, None)
        else:
            self._cache.clear()
            self._cache_expiry.clear()
```

### Provider with OAuth 2.0

```python
from datetime import datetime, timedelta


@register_provider("oauth_provider")
class OAuthProvider(BaseProvider):
    """Provider with OAuth 2.0 authentication."""

    async def configure(self, config: dict) -> None:
        await super().configure(config)

        self.client_id = config["client_id"]
        self.client_secret = config["client_secret"]
        self.token_url = config["token_url"]

        # Get initial access token
        self.access_token = await self._fetch_token()
        self.token_expiry = datetime.now() + timedelta(hours=1)

        # Create client with token
        self.http_client = httpx.AsyncClient(
            base_url=config["api_endpoint"],
        )

    async def _fetch_token(self) -> str:
        """Fetch OAuth access token."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.token_url,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
            )
            response.raise_for_status()
            data = response.json()
            return data["access_token"]

    async def api_request(self, method: str, path: str, **kwargs):
        """Make authenticated request with token refresh."""
        # Refresh token if expired
        if datetime.now() >= self.token_expiry:
            self.access_token = await self._fetch_token()
            self.token_expiry = datetime.now() + timedelta(hours=1)

        # Add auth header
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self.access_token}"

        response = await self.http_client.request(
            method, path, headers=headers, **kwargs
        )
        response.raise_for_status()
        return response
```

### Testing Providers

```python
import pytest


@pytest.mark.asyncio
async def test_provider_configure():
    """Test provider configuration."""
    provider = MyCloudProvider()

    config = {
        "api_endpoint": "https://api.example.com",
        "api_key": "test_key",
        "timeout": 60,
        "verify_ssl": True,
    }

    await provider.configure(config)

    assert provider.api_endpoint == "https://api.example.com"
    assert provider.http_client is not None


@pytest.mark.asyncio
async def test_provider_schema():
    """Test provider schema."""
    schema = MyCloudProvider().get_schema()

    assert "api_endpoint" in schema.main_block.attributes
    assert "api_key" in schema.main_block.attributes
    assert schema.main_block.attributes["api_key"].sensitive is True


@pytest.mark.asyncio
async def test_provider_api_request():
    """Test provider API requests."""
    provider = MyCloudProvider()

    await provider.configure({
        "api_endpoint": "https://api.example.com",
        "api_key": "test_key",
    })

    # Mock API call
    response = await provider.http_client.get("/test")
    assert response.status_code == 200
```

## Related Guides

- [Creating Providers](../../guides/building-components/creating-providers.md) - Complete provider development guide
- [Best Practices](../../guides/production/best-practices.md) - Provider best practices
- [Security Best Practices](../../guides/production/security-best-practices.md) - Secure providers
- [Performance Optimization](../../guides/production/performance-optimization.md) - Fast providers
- [Testing Providers](../../guides/development/testing-providers.md) - Testing strategies

## Module Reference
