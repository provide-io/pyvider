# Capabilities Overview

Capabilities are a powerful composition mechanism in Pyvider that allows you to create reusable, modular components that extend the functionality of providers, resources, data sources, and functions.

## What are Capabilities?

Capabilities are compositional components that can:

- **Extend existing components** with new functionality
- **Share common patterns** across multiple providers
- **Encapsulate cross-cutting concerns** like authentication, caching, or logging
- **Be discovered and registered** automatically by Pyvider's hub system

Think of capabilities as mixins or plugins that you can attach to your components to enhance their behavior without modifying their core implementation.

## Why Use Capabilities?

### Reusability

Write once, use everywhere:

```python
# Define a caching capability once
@register_capability
class CachingCapability(BaseCapability):
    def setup(self):
        # Add caching logic
        pass

# Apply it to multiple resources
@register_resource("server")
@use_capability(CachingCapability)
class Server(BaseResource):
    pass

@register_resource("database")
@use_capability(CachingCapability)
class Database(BaseResource):
    pass
```

### Separation of Concerns

Keep your components focused on their core responsibility while capabilities handle cross-cutting concerns:

- **Authentication**: OAuth, API keys, token management
- **Retry Logic**: Exponential backoff, circuit breakers
- **Caching**: Response caching, state caching
- **Logging**: Structured logging, audit trails
- **Metrics**: Performance monitoring, usage tracking

### Modularity

Capabilities can be:

- Developed independently
- Tested in isolation
- Versioned separately
- Shared across projects
- Published as packages

## How Capabilities Work

### Discovery and Registration

Capabilities integrate with Pyvider's hub-based discovery system:

```python
from pyvider.capabilities import register_capability, BaseCapability

@register_capability
class MyCapability(BaseCapability):
    """A custom capability."""

    async def setup(self):
        """Called during provider initialization."""
        # Initialize capability
        pass

    async def teardown(self):
        """Called during provider shutdown."""
        # Cleanup capability
        pass
```

### Lifecycle Hooks

Capabilities have lifecycle hooks that integrate with component lifecycles:

- **`setup()`**: Called when the provider initializes
- **`teardown()`**: Called when the provider shuts down
- **`before_operation()`**: Called before resource operations
- **`after_operation()`**: Called after resource operations

### Applying Capabilities

Apply capabilities to components using decorators:

```python
from pyvider.resources import register_resource, BaseResource
from pyvider.capabilities import use_capability

@register_resource("server")
@use_capability(CachingCapability)
@use_capability(LoggingCapability)
class Server(BaseResource):
    """A server resource with caching and logging capabilities."""
    pass
```

## Common Use Cases

### Authentication Capability

Centralize authentication logic:

```python
@register_capability
class OAuth2Capability(BaseCapability):
    """OAuth2 authentication capability."""

    def __init__(self):
        self.token = None
        self.expires_at = None

    async def setup(self):
        """Initialize OAuth2 client."""
        await self.refresh_token()

    async def refresh_token(self):
        """Refresh OAuth2 token."""
        # Token refresh logic
        pass

    def get_headers(self):
        """Get authentication headers."""
        return {
            "Authorization": f"Bearer {self.token}"
        }
```

### Caching Capability

Add response caching:

```python
@register_capability
class CachingCapability(BaseCapability):
    """Response caching capability."""

    def __init__(self):
        self.cache = {}

    async def get(self, key: str):
        """Get from cache."""
        return self.cache.get(key)

    async def set(self, key: str, value: any, ttl: int = 300):
        """Set in cache with TTL."""
        self.cache[key] = {
            "value": value,
            "expires": time.time() + ttl
        }

    async def before_operation(self, ctx):
        """Check cache before operation."""
        cached = await self.get(ctx.cache_key)
        if cached:
            return cached["value"]
        return None
```

### Retry Capability

Add automatic retries with exponential backoff:

```python
@register_capability
class RetryCapability(BaseCapability):
    """Retry logic with exponential backoff."""

    def __init__(self, max_retries=3, base_delay=1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay

    async def execute_with_retry(self, operation):
        """Execute operation with retry logic."""
        for attempt in range(self.max_retries):
            try:
                return await operation()
            except RetryableError as e:
                if attempt == self.max_retries - 1:
                    raise
                delay = self.base_delay * (2 ** attempt)
                await asyncio.sleep(delay)
```

### Metrics Capability

Track performance metrics:

```python
@register_capability
class MetricsCapability(BaseCapability):
    """Performance metrics collection."""

    def __init__(self):
        self.metrics = {}

    async def before_operation(self, ctx):
        """Start timing."""
        ctx.start_time = time.time()

    async def after_operation(self, ctx):
        """Record duration."""
        duration = time.time() - ctx.start_time
        self.record_metric(ctx.operation, duration)

    def record_metric(self, operation: str, duration: float):
        """Record metric."""
        if operation not in self.metrics:
            self.metrics[operation] = []
        self.metrics[operation].append(duration)
```

## Capability Composition

Capabilities can build on each other:

```python
@register_capability
class AdvancedAuthCapability(BaseCapability):
    """Advanced auth combining multiple capabilities."""

    def __init__(self):
        # Compose with other capabilities
        self.oauth = OAuth2Capability()
        self.caching = CachingCapability()
        self.retry = RetryCapability()

    async def setup(self):
        """Initialize all sub-capabilities."""
        await self.oauth.setup()
        await self.caching.setup()
        await self.retry.setup()

    async def get_authenticated_headers(self):
        """Get headers with caching and retry."""
        cache_key = "auth_headers"

        # Try cache first
        cached = await self.caching.get(cache_key)
        if cached:
            return cached

        # Get fresh token with retry
        headers = await self.retry.execute_with_retry(
            lambda: self.oauth.get_headers()
        )

        # Cache result
        await self.caching.set(cache_key, headers, ttl=300)

        return headers
```

## Best Practices

### 1. Keep Capabilities Focused

Each capability should have a single, well-defined responsibility:

```python
# Good: Focused on one concern
@register_capability
class CachingCapability(BaseCapability):
    """Handles caching only."""
    pass

# Bad: Too many responsibilities
@register_capability
class EveryThingCapability(BaseCapability):
    """Handles caching, auth, retry, logging, metrics..."""
    pass
```

### 2. Make Capabilities Configurable

Allow users to configure capability behavior:

```python
@register_capability
class CachingCapability(BaseCapability):
    def __init__(self, ttl=300, max_size=1000):
        self.ttl = ttl
        self.max_size = max_size
```

### 3. Document Capabilities

Provide clear documentation:

```python
@register_capability
class OAuth2Capability(BaseCapability):
    """
    OAuth2 authentication capability.

    Provides automatic token management including:
    - Initial token acquisition
    - Automatic token refresh before expiration
    - Thread-safe token access
    - Error handling and retry logic

    Configuration:
        client_id (str): OAuth2 client ID
        client_secret (str): OAuth2 client secret
        token_url (str): Token endpoint URL
        scopes (list[str]): Requested OAuth2 scopes

    Example:
        @use_capability(OAuth2Capability(
            client_id="my-client",
            client_secret="secret",
            token_url="https://oauth.example.com/token",
            scopes=["read", "write"]
        ))
        class MyResource(BaseResource):
            pass
    """
    pass
```

### 4. Test Capabilities Independently

Write unit tests for capabilities:

```python
async def test_caching_capability():
    """Test caching capability."""
    cache = CachingCapability(ttl=10)

    # Test set and get
    await cache.set("key", "value")
    assert await cache.get("key") == "value"

    # Test expiration
    await asyncio.sleep(11)
    assert await cache.get("key") is None
```

### 5. Handle Errors Gracefully

Capabilities should not break the host component:

```python
@register_capability
class MetricsCapability(BaseCapability):
    async def after_operation(self, ctx):
        try:
            # Record metrics
            self.record_metric(ctx.operation, ctx.duration)
        except Exception as e:
            # Log error but don't fail the operation
            logger.warning(f"Failed to record metrics: {e}")
```

## See Also

- **[Using Capabilities](using-capabilities.md)** - How to apply capabilities to components
- **[Creating Capabilities](creating-capabilities.md)** - Building custom capabilities
- **[Capability Lifecycle](capability-lifecycle.md)** - Lifecycle hooks and events
- **[Capability Composition](capability-composition.md)** - Composing capabilities together
- **[Bundling Components](bundling-components.md)** - Packaging capabilities for distribution
