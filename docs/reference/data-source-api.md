# Data Source API Reference

Complete API reference for data sources and the BaseDataSource class.

---

## Base Data Source Class

```python
from pyvider.data_sources import BaseDataSource
```

### Class Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `config_class` | `Type[attrs.define]` | Yes | Configuration attrs class (inputs) |
| `state_class` | `Type[attrs.define]` | Yes | State attrs class (outputs) |

---

## Required Methods

### `read()`

```python
async def read(self, ctx: ResourceContext) -> StateType | None:
    """Execute query and return data."""
```

**Purpose:** Fetch data based on user configuration.

**Parameters:**
- `ctx`: ResourceContext containing configuration and context

**Returns:**
- `StateType | None`: Query results, or `None` if config unavailable

**When Called:** During every `terraform plan` and `terraform apply`

**Example:**
```python
async def read(self, ctx: ResourceContext) -> ServerQueryData | None:
    if not ctx.config:
        return None

    servers = await api.list_servers(
        filter=ctx.config.filter,
        limit=ctx.config.limit,
    )

    return ServerQueryData(
        id=f"{ctx.config.filter}:{ctx.config.limit}",
        servers=servers,
        count=len(servers),
    )
```

**Important:**
- Data sources use the same ResourceContext API as resources
- Access configuration via `ctx.config`
- Return `None` if config is unavailable
- Unlike resources, data sources re-fetch data on every Terraform operation

---

### `get_schema()`

```python
@classmethod
def get_schema(cls) -> PvsSchema:
    """Define Terraform schema."""
```

**Purpose:** Define input parameters and output attributes.

**Returns:** `PvsSchema` object

**Example:**
```python
from pyvider.schema import s_data_source, a_str, a_num, a_list

@classmethod
def get_schema(cls) -> PvsSchema:
    return s_data_source({
        # Inputs (from user)
        "filter": a_str(required=True, description="Filter expression"),
        "limit": a_num(default=10, description="Max results"),

        # Outputs (computed by data source)
        "id": a_str(computed=True, description="Query ID"),
        "servers": a_list(a_str(), computed=True, description="Server list"),
        "count": a_num(computed=True, description="Number of servers"),
    })
```

**Important:** All outputs MUST have `computed=True`.

---

## Type Signatures

### Configuration Class

Input parameters from user:

```python
import attrs

@attrs.define
class ServerQueryConfig:
    """User-provided query parameters."""
    filter: str
    limit: int = 10
    region: str | None = None
```

**Rules:**
- All fields represent Terraform inputs
- Use defaults for optional parameters
- Use `str | None` for nullable inputs

---

### Data Class

Query results returned to user:

```python
import attrs

@attrs.define
class ServerQueryData:
    """Query results."""
    id: str                    # Required: Stable query ID
    servers: list[dict]        # Query results
    count: int                 # Result metadata
    next_page: str | None      # Optional: Pagination token
```

**Rules:**
- `id` field is required (must be deterministic)
- All fields are outputs (returned to Terraform)
- Use appropriate types (list, dict, str, int, bool)

---

## Schema Attributes

### Input Attributes

```python
"filter": a_str(required=True, description="Filter expression")
"limit": a_num(default=10, description="Max results")
"region": a_str(description="AWS region")  # Optional (no default)
```

**Modifiers:**
- `required=True` - User must provide value
- `default=value` - Optional with default
- No `required` or `default` - Optional (null allowed)

---

### Output Attributes

```python
"id": a_str(computed=True, description="Query ID")
"results": a_list(a_map(a_str()), computed=True, description="Results")
"count": a_num(computed=True, description="Result count")
"error": a_str(computed=True, description="Error message if query failed")
```

**Rules:**
- ALL outputs must have `computed=True`
- Cannot have `required` or `default` (they're outputs)
- Use descriptive descriptions

---

## ID Generation

Data source IDs must be deterministic (same inputs = same ID):

### Good: Deterministic

```python
async def read(self, config: Config) -> Data:
    # Generate stable ID from inputs
    query_id = f"{config.endpoint}:{config.filter}:{config.limit}"

    results = await api.query(...)

    return Data(
        id=query_id,  # Same config always = same ID
        results=results,
    )
```

### Bad: Non-Deterministic

```python
import uuid

async def read(self, config: Config) -> Data:
    return Data(
        id=str(uuid.uuid4()),  # Different ID every time!
        results=results,
    )
```

### Hash-Based IDs

For complex configurations:

```python
import hashlib
import json

async def read(self, config: Config) -> Data:
    # Create hash of all config values
    config_str = json.dumps({
        "endpoint": config.endpoint,
        "filter": config.filter,
        "limit": config.limit,
    }, sort_keys=True)

    query_id = hashlib.md5(config_str.encode()).hexdigest()

    return Data(id=query_id, ...)
```

---

## Error Handling

### Return Data With Error Field

```python
@attrs.define
class QueryData:
    id: str
    results: list[dict]
    error: str | None = None  # Error field

async def read(self, config: Config) -> QueryData:
    try:
        results = await api.query(config.endpoint)
        return QueryData(
            id=config.endpoint,
            results=results,
            error=None,
        )
    except APIError as e:
        return QueryData(
            id=config.endpoint,
            results=[],
            error=str(e),
        )
```

### Don't Raise Exceptions

```python
# Good: Return data with error
async def read(self, config: Config) -> Data:
    try:
        return await query(config)
    except Exception as e:
        return Data(id=id, results=[], error=str(e))

# Bad: Raise exception
async def read(self, config: Config) -> Data:
    result = await api.query()  # Might raise!
    return Data(id=id, results=result)
```

---

## Common Patterns

### Handle Missing Data

```python
async def read(self, config: Config) -> Data:
    result = await api.get(config.resource_id)

    if not result:
        # Return empty data instead of None
        return Data(
            id=config.resource_id,
            found=False,
            value=None,
        )

    return Data(
        id=result["id"],
        found=True,
        value=result["value"],
    )
```

### Boolean Outputs

```python
@attrs.define
class FileInfoData:
    id: str
    exists: bool      # Use bool for yes/no outputs
    readable: bool
    size: int | None  # None if doesn't exist

async def read(self, config: Config) -> FileInfoData:
    from pathlib import Path
    path = Path(config.path)

    return FileInfoData(
        id=str(path.absolute()),
        exists=path.exists(),
        readable=path.exists() and os.access(path, os.R_OK),
        size=path.stat().st_size if path.exists() else None,
    )
```

### List Outputs

```python
from pyvider.schema import s_data_source, a_list, a_map, a_str

@classmethod
def get_schema(cls) -> PvsSchema:
    return s_data_source({
        "query": a_str(required=True),
        "id": a_str(computed=True),
        # List of strings
        "tags": a_list(a_str(), computed=True),
        # List of objects
        "servers": a_list(
            a_map(a_str()),  # Each server is a map
            computed=True
        ),
    })
```

---

## Caching

Cache expensive queries:

```python
from functools import lru_cache

class ServerQuery(BaseDataSource):
    @lru_cache(maxsize=128)
    async def _fetch_servers(self, filter_str: str, limit: int) -> list[dict]:
        """Cached query."""
        return await api.list_servers(filter=filter_str, limit=limit)

    async def read(self, config: Config) -> Data:
        # Query is cached by filter+limit
        servers = await self._fetch_servers(config.filter, config.limit)

        return Data(
            id=f"{config.filter}:{config.limit}",
            servers=servers,
            count=len(servers),
        )
```

---

## Validation

Data sources don't have `_validate_config()`. Validate in `read()`:

```python
async def read(self, config: Config) -> Data:
    # Validate inputs
    errors = []

    if not config.endpoint.startswith("/"):
        errors.append("Endpoint must start with /")

    if config.limit < 1 or config.limit > 1000:
        errors.append("Limit must be between 1 and 1000")

    if errors:
        return Data(
            id="error",
            results=[],
            error="; ".join(errors),
        )

    # Proceed with query
    ...
```

---

## Performance Considerations

### Idempotency

Reads should be idempotent (same result every time for same inputs):

```python
# Good: Idempotent
async def read(self, config: Config) -> Data:
    # Same query always returns same results
    servers = await api.list_servers(filter=config.filter)
    return Data(id=config.filter, servers=servers)

# Bad: Not idempotent
async def read(self, config: Config) -> Data:
    # Returns different results each time!
    servers = await api.list_recent_servers()
    return Data(id=str(uuid.uuid4()), servers=servers)
```

### Minimize API Calls

```python
# Good: Single API call
async def read(self, config: Config) -> Data:
    response = await api.get_user_with_posts(config.user_id)
    return Data(
        id=config.user_id,
        user=response["user"],
        posts=response["posts"],
    )

# Bad: Multiple API calls
async def read(self, config: Config) -> Data:
    user = await api.get_user(config.user_id)
    posts = await api.get_posts(config.user_id)  # Separate call
    return Data(id=config.user_id, user=user, posts=posts)
```

---

## Testing

```python
import pytest
from my_provider.data_sources.server_query import ServerQuery, ServerQueryConfig

@pytest.mark.asyncio
async def test_server_query():
    ds = ServerQuery()
    config = ServerQueryConfig(filter="status=running", limit=5)

    data = await ds.read(config)

    assert data.count <= 5
    assert len(data.servers) == data.count
    assert data.id == "status=running:5"  # Deterministic ID

@pytest.mark.asyncio
async def test_server_query_error_handling():
    ds = ServerQuery()
    config = ServerQueryConfig(filter="invalid!", limit=5)

    data = await ds.read(config)

    # Should return data with error, not raise
    assert data.error is not None
    assert data.servers == []
```

---

## Complete Example

```python
import attrs
import httpx
from pyvider.data_sources import register_data_source, BaseDataSource
from pyvider.resources.context import ResourceContext
from pyvider.schema import s_data_source, a_str, a_num, a_list, a_map, PvsSchema

@attrs.define
class ServerQueryConfig:
    region: str
    limit: int = 10

@attrs.define
class ServerQueryData:
    id: str
    servers: list[dict[str, str]]
    count: int

@register_data_source("servers")
class ServerQuery(BaseDataSource):
    config_class = ServerQueryConfig
    state_class = ServerQueryData

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_data_source({
            # Inputs
            "region": a_str(required=True, description="AWS region"),
            "limit": a_num(default=10, description="Max servers"),

            # Outputs
            "id": a_str(computed=True, description="Query ID"),
            "servers": a_list(
                a_map(a_str()),
                computed=True,
                description="Server list"
            ),
            "count": a_num(computed=True, description="Server count"),
        })

    async def read(self, ctx: ResourceContext) -> ServerQueryData | None:
        if not ctx.config:
            return None

        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.example.com/servers",
                params={"region": ctx.config.region, "limit": ctx.config.limit}
            )
            servers = response.json()["servers"]

            return ServerQueryData(
                id=f"{ctx.config.region}:{ctx.config.limit}",
                servers=servers,
                count=len(servers),
            )
```

---

## See Also

- [Create a Data Source](../how-to-guides/data-sources/create-data-source.md) - How-to guide
- [Building Your First Data Source](../tutorials/building-your-first-data-source.md) - Tutorial
- [Handle Pagination](../how-to-guides/data-sources/handle-pagination.md) - Pagination patterns
- [API Reference](../api/data_sources.md) - Auto-generated API docs
