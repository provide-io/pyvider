# Ephemeral Resources API Reference

This page documents the ephemeral resources API for creating short-lived, stateless resources in Terraform providers.

## Overview

Ephemeral resources are a special type of resource that manage temporary connections, sessions, or other short-lived infrastructure. Unlike regular resources, ephemeral resources:

- Have a different lifecycle: `open`, `renew`, and `close` (each receives an `EphemeralResourceContext`)
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

### `BaseEphemeralResource` Class

Base class for all ephemeral resource implementations:

```python
from pyvider.ephemerals import BaseEphemeralResource
from pyvider.resources.private_state import PrivateState
from pyvider.schema import a_str, a_num
import attrs

class MyEphemeral(BaseEphemeralResource):
    """Base class for ephemeral resources."""

    @attrs.define
    class Config:
        """Configuration from Terraform."""
        host: str = a_str(required=True)
        port: int = a_num(default=5432)

    @attrs.define
    class Result:
        """Data returned to Terraform callers."""
        session_id: str = a_str(computed=True)
        expires_at: str = a_str(computed=True)

    @attrs.define
    class SessionState(PrivateState):
        token: str = a_str(sensitive=True)
```

## Lifecycle Methods

Ephemeral resources implement a different lifecycle than regular resources:

### `open(ctx: EphemeralResourceContext) -> tuple[Result, PrivateState, datetime]`

Opens/creates the ephemeral resource. The context gives you strongly typed config and capability access.

```python
async def open(
    self, ctx: EphemeralResourceContext[Config, None]
) -> tuple[Result, PrivateState, datetime]:
    """
    Open a new ephemeral resource instance.

    Returns:
        (result, private_state, renew_at_utc)
    """
    session = await self.provider.create_session(
        host=ctx.config.host,
        port=ctx.config.port,
    )
    return (
        self.Result(session_id=session.id, expires_at=session.expires_at.isoformat()),
        self.PrivateState(token=session.token),
        session.expires_at,
    )
```

### `renew(ctx: EphemeralResourceContext) -> tuple[PrivateState, datetime]`

Renews/refreshes the ephemeral resource lease using the stored private state:

```python
async def renew(
    self, ctx: EphemeralResourceContext[None, PrivateState]
) -> tuple[PrivateState, datetime]:
    """
    Renew the ephemeral resource lease.
    """
    renewed = await self.provider.renew_session(ctx.private_state.token)
    return self.PrivateState(token=renewed.token), renewed.expires_at
```

### `close(ctx: EphemeralResourceContext) -> None`

Closes/destroys the ephemeral resource:

```python
async def close(self, ctx: EphemeralResourceContext[None, PrivateState]) -> None:
    """
    Close the ephemeral resource and clean up server-side state.
    """
    await self.provider.close_session(ctx.private_state.token)
```

## Complete Example

```python
from pyvider.ephemerals import register_ephemeral_resource, BaseEphemeralResource, EphemeralResourceContext
from pyvider.resources.private_state import PrivateState
from pyvider.schema import a_str, a_num, a_bool, a_list
from datetime import datetime, timedelta
import attrs
import uuid

@register_ephemeral_resource("api_token")
class ApiToken(BaseEphemeralResource):
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
    class Result:
        token: str = a_str(computed=True, sensitive=True)
        token_id: str = a_str(computed=True)
        expires_at: str = a_str(computed=True)
        scopes: list[str] = a_list(a_str(), computed=True)

    @attrs.define
    class TokenPrivateState(PrivateState):
        token: str = a_str(sensitive=True)

    async def open(
        self, ctx: EphemeralResourceContext[Config, None]
    ) -> tuple[Result, PrivateState, datetime]:
        """Generate a new API token."""
        response = await self.provider.api_client.create_token(
            scopes=ctx.config.scopes, ttl=ctx.config.ttl_seconds
        )

        expires_at = response.expires_at or datetime.utcnow() + timedelta(hours=1)
        return (
            self.Result(
                token=response.token,
                token_id=response.token_id,
                expires_at=expires_at.isoformat(),
                scopes=ctx.config.scopes,
            ),
            self.TokenPrivateState(token=response.token),
            expires_at,
        )

    async def renew(
        self, ctx: EphemeralResourceContext[None, TokenPrivateState]
    ) -> tuple[TokenPrivateState, datetime]:
        """Renew token before expiration."""
        response = await self.provider.api_client.renew_token(token=ctx.private_state.token)
        expires_at = response.expires_at or datetime.utcnow() + timedelta(hours=1)
        return self.TokenPrivateState(token=response.token), expires_at

    async def close(self, ctx: EphemeralResourceContext[None, TokenPrivateState]) -> None:
        """Revoke the API token."""
        await self.provider.api_client.revoke_token(ctx.private_state.token)
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
from pyvider.ephemerals.context import EphemeralResourceContext

async def open(self, ctx: EphemeralResourceContext[Config, None]) -> tuple[Result, TokenPrivateState, datetime]:
    # Context provides: config, private_state, and diagnostic methods
    self.logger.info(
        "Opening ephemeral resource",
        scopes=ctx.config.scopes if ctx.config else [],
        ttl=ctx.config.ttl_seconds if ctx.config else None,
    )
    ...
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
from pyvider.ephemerals.context import EphemeralResourceContext
from my_provider.ephemerals import ApiToken

@pytest.fixture
def api_token():
    return ApiToken()

@pytest.mark.asyncio
async def test_token_lifecycle(api_token, mock_provider):
    # Setup
    api_token.provider = mock_provider

    # Test open
    config_ctx = EphemeralResourceContext(config=ApiToken.Config(scopes=["read", "write"]))
    result, private_state, renew_at = await api_token.open(config_ctx)
    assert result.token_id is not None
    assert result.scopes == ["read", "write"]

    # Test renew
    renew_ctx = EphemeralResourceContext(private_state=private_state)
    new_private_state, next_renew = await api_token.renew(renew_ctx)
    assert next_renew >= renew_at

    # Test close
    await api_token.close(EphemeralResourceContext(private_state=new_private_state))
    # Verify cleanup happened
```

## Related Documentation

- [Component Model](../explanation/component-model.md) - Understanding components
- [Creating Resources](../guides/building-components/creating-resources.md) - Regular resources
- [Error Handling](../guides/development/error-handling.md) - Error management

## Auto-Generated API Documentation
