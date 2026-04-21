# Advanced Provider Features

This guide covers advanced features and patterns for building production-focused Pyvider providers, including error handling, retry logic, rate limiting, caching, and testing.

For basic provider creation, see [Creating Providers](../building-components/creating-providers.md).

## Table of Contents

- [Error Handling](#error-handling)
- [Retry Logic](#retry-logic)
- [Rate Limiting](#rate-limiting)
- [Caching](#caching)
- [Logging](#logging)
- [Testing Your Provider](#testing-your-provider)
- [Best Practices](#best-practices)

---

## Error Handling

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

## Retry Logic

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

## Rate Limiting

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

## Caching

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

## Logging

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

## Related Documentation

- [Creating Providers](../building-components/creating-providers.md) - Provider basics
- [Creating Resources](../building-components/creating-resources.md) - Resource implementation
- [Creating Data Sources](../building-components/creating-data-sources.md) - Data source implementation
- [Creating Functions](../building-components/creating-functions.md) - Function implementation
- [Testing Providers](../development/testing-providers.md) - Comprehensive testing strategies
- [Production Readiness](../production/production-readiness.md) - Production best practices
- [Best Practices](../production/best-practices.md) - General best practices

---

**Remember**: These advanced features help you build robust, production-focused providers that can handle real-world challenges like network failures, rate limits, and scale requirements.
