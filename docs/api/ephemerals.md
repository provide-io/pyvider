# Ephemeral Resources API Reference

This page documents the ephemeral resources API for creating short-lived, stateless resources in Terraform providers.

## Overview

Ephemeral resources are a special type of resource that manage temporary connections, sessions, or other short-lived infrastructure. Unlike regular resources, ephemeral resources:

- Have a different lifecycle: `open`, `renew`, and `close` instead of CRUD operations
- Are not persisted in Terraform state
- Are recreated on every Terraform run
- Perfect for database connections, API sessions, temporary credentials, etc.

## Core Components

### `@register_ephemeral_resource` Decorator

Register a class as an ephemeral resource component:

```python
from pyvider.ephemerals import register_ephemeral_resource

@register_ephemeral_resource("database_session")
class DatabaseSession:
    """Manages a temporary database session."""
    pass
```

**Parameters:**
- `name` (str): The resource name as it appears in Terraform configurations

### `BaseEphemeral` Class

Base class for all ephemeral resource implementations:

```python
from pyvider.ephemerals import BaseEphemeral
from pyvider.schema import a_str, a_num
import attrs

class MyEphemeral(BaseEphemeral):
    """Base class for ephemeral resources."""

    @attrs.define
    class Config:
        """Configuration from Terraform."""
        host: str = a_str(required=True)
        port: int = a_num(default=5432)

    @attrs.define
    class State:
        """Ephemeral state (not persisted)."""
        session_id: str = a_str(computed=True)
        expires_at: str = a_str(computed=True)
```

## Lifecycle Methods

Ephemeral resources implement a different lifecycle than regular resources:

### `open(config: Config) -> State`

Opens/creates the ephemeral resource:

```python
async def open(self, config: Config) -> State:
    """
    Open a new ephemeral resource instance.

    Args:
        config: User-provided configuration

    Returns:
        State object representing the opened resource
    """
    session = await self.provider.create_session(
        host=config.host,
        port=config.port
    )
    return self.State(
        session_id=session.id,
        expires_at=session.expires_at
    )
```

### `renew(state: State) -> State`

Renews/refreshes the ephemeral resource lease:

```python
async def renew(self, state: State) -> State:
    """
    Renew the ephemeral resource lease.

    Args:
        state: Current ephemeral state

    Returns:
        Updated state with renewed lease
    """
    renewed = await self.provider.renew_session(state.session_id)
    return self.State(
        session_id=state.session_id,
        expires_at=renewed.expires_at
    )
```

### `close(state: State) -> None`

Closes/destroys the ephemeral resource:

```python
async def close(self, state: State) -> None:
    """
    Close the ephemeral resource.

    Args:
        state: Current ephemeral state
    """
    await self.provider.close_session(state.session_id)
```

## Complete Example

```python
from pyvider.ephemerals import register_ephemeral_resource, BaseEphemeral
from pyvider.schema import a_str, a_num, a_bool
from datetime import datetime, timedelta
import attrs
import uuid

@register_ephemeral_resource("api_token")
class ApiToken(BaseEphemeral):
    """
    Manages temporary API tokens with automatic expiration.
    """

    @attrs.define
    class Config:
        """Token configuration."""
        scopes: list[str] = a_list(a_str(), required=True)
        ttl_seconds: int = a_num(default=3600)
        auto_renew: bool = a_bool(default=True)

    @attrs.define
    class State:
        """Token state."""
        token: str = a_str(computed=True, sensitive=True)
        token_id: str = a_str(computed=True)
        expires_at: str = a_str(computed=True)
        scopes: list[str] = a_list(a_str(), computed=True)

    async def open(self, config: Config) -> State:
        """Generate a new API token."""
        # Create token with requested scopes
        response = await self.provider.api_client.create_token(
            scopes=config.scopes,
            ttl=config.ttl_seconds
        )

        return self.State(
            token=response.token,
            token_id=response.token_id,
            expires_at=response.expires_at.isoformat(),
            scopes=config.scopes
        )

    async def renew(self, state: State) -> State:
        """Renew token before expiration."""
        # Check if token needs renewal
        expires_at = datetime.fromisoformat(state.expires_at)
        if datetime.utcnow() > expires_at - timedelta(minutes=5):
            # Renew the token
            response = await self.provider.api_client.renew_token(
                token_id=state.token_id
            )
            return self.State(
                token=response.token,
                token_id=state.token_id,
                expires_at=response.expires_at.isoformat(),
                scopes=state.scopes
            )
        return state

    async def close(self, state: State) -> None:
        """Revoke the API token."""
        await self.provider.api_client.revoke_token(state.token_id)
```

## Usage in Terraform

```hcl
# Ephemeral resource for temporary database connection
ephemeral "mycloud_database_session" "main" {
  host     = "db.example.com"
  port     = 5432
  database = "myapp"
}

# Use in another resource
resource "mycloud_data_import" "import" {
  session_id = ephemeral.mycloud_database_session.main.session_id
  source     = "s3://bucket/data.csv"
}
```

## Context Access

Ephemeral resources have access to context information:

```python
from pyvider.ephemerals.context import EphemeralContext

async def open(self, config: Config) -> State:
    # Access context
    ctx: EphemeralContext = self.context

    # Log with context
    self.logger.info(
        "Opening ephemeral resource",
        resource_type=ctx.resource_type,
        resource_name=ctx.resource_name
    )

    # Continue with implementation...
```

## Error Handling

```python
from pyvider.exceptions import ResourceError

async def open(self, config: Config) -> State:
    try:
        session = await self.provider.create_session(...)
    except ConnectionError as e:
        raise ResourceError(
            f"Failed to open session: {e}",
            details={"host": config.host, "port": config.port}
        )
    return self.State(...)
```

## Best Practices

1. **Idempotency**: Ensure `open` can be called multiple times safely
2. **Cleanup**: Always implement proper cleanup in `close`
3. **Renewal Logic**: Implement smart renewal to avoid unnecessary API calls
4. **Error Recovery**: Handle transient failures gracefully
5. **Sensitive Data**: Mark tokens/passwords as `sensitive=True`
6. **Expiration Tracking**: Include expiration timestamps in state

## Testing Ephemeral Resources

```python
import pytest
from my_provider.ephemerals import ApiToken

@pytest.fixture
def api_token():
    return ApiToken()

@pytest.mark.asyncio
async def test_token_lifecycle(api_token, mock_provider):
    # Setup
    api_token.provider = mock_provider

    # Test open
    config = ApiToken.Config(scopes=["read", "write"])
    state = await api_token.open(config)
    assert state.token_id is not None
    assert state.scopes == ["read", "write"]

    # Test renew
    renewed_state = await api_token.renew(state)
    assert renewed_state.token_id == state.token_id

    # Test close
    await api_token.close(renewed_state)
    # Verify cleanup happened
```

## Related Documentation

- [Component Model](../core-concepts/component-model.md) - Understanding components
- [Creating Resources](../guides/creating-resources.md) - Regular resources
- [Error Handling](../guides/error-handling.md) - Error management

## Auto-Generated API Documentation

::: pyvider.ephemerals
    options:
      show_source: true
      show_bases: true
      members:
        - register_ephemeral_resource
        - BaseEphemeral
        - EphemeralContext