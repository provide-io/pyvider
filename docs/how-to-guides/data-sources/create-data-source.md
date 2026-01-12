# How to Create a Data Source

Quick reference for creating Terraform data sources with pyvider. For a step-by-step tutorial, see [Building Your First Data Source](../../tutorials/building-your-first-data-source.md).

---

## Quick Steps

1. Define runtime types (config and data)
2. Create data source class with `@register_data_source()`
3. Define schema with `get_schema()`
4. Implement `read()` method
5. Test with Terraform

---

## Minimal Example

```python
import attrs
from pyvider.data_sources import register_data_source, BaseDataSource
from pyvider.schema import s_data_source, a_str, a_num, PvsSchema
from pathlib import Path

@attrs.define
class FileInfoConfig:
    path: str

@attrs.define
class FileInfoData:
    id: str
    size: int
    exists: bool

@register_data_source("file_info")
class FileInfo(BaseDataSource):
    config_class = FileInfoConfig
    state_class = FileInfoData

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_data_source({
            # Input
            "path": a_str(required=True, description="File to query"),
            # Outputs (all computed)
            "id": a_str(computed=True, description="File ID"),
            "size": a_num(computed=True, description="File size"),
            "exists": a_bool(computed=True, description="File exists"),
        })

    async def read(self, config: FileInfoConfig) -> FileInfoData:
        file_path = Path(config.path)
        if file_path.exists():
            return FileInfoData(
                id=str(file_path.absolute()),
                size=file_path.stat().st_size,
                exists=True,
            )
        return FileInfoData(
            id=str(file_path.absolute()),
            size=0,
            exists=False,
        )
```

---

## API Data Source Example

For data sources that query external APIs:

```python
import attrs
import httpx
from pyvider.data_sources import register_data_source, BaseDataSource
from pyvider.schema import s_data_source, a_str, a_num, a_list, PvsSchema

@attrs.define
class APIQueryConfig:
    endpoint: str
    filter: str | None = None
    limit: int = 10

@attrs.define
class APIQueryData:
    id: str
    results: list[str]
    count: int
    next_page: str | None

@register_data_source("api_query")
class APIQuery(BaseDataSource):
    config_class = APIQueryConfig
    state_class = APIQueryData

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_data_source({
            # Inputs
            "endpoint": a_str(required=True, description="API endpoint"),
            "filter": a_str(description="Filter expression"),
            "limit": a_num(default=10, description="Max results"),

            # Outputs
            "id": a_str(computed=True, description="Query ID"),
            "results": a_list(a_str(), computed=True, description="Results"),
            "count": a_num(computed=True, description="Result count"),
            "next_page": a_str(computed=True, description="Next page token"),
        })

    async def read(self, config: APIQueryConfig) -> APIQueryData:
        async with httpx.AsyncClient() as client:
            params = {"limit": config.limit}
            if config.filter:
                params["filter"] = config.filter

            response = await client.get(
                f"https://api.example.com{config.endpoint}",
                params=params
            )
            data = response.json()
            items = data.get("items", [])

            return APIQueryData(
                id=f"{config.endpoint}:{config.filter}:{config.limit}",
                results=items,
                count=len(items),
                next_page=data.get("next_page"),
            )
```

---

## Required Elements

| Element | Purpose | Notes |
|---------|---------|-------|
| `config_class` | Input configuration | What user provides |
| `data_class` | Output data | Query results |
| `get_schema()` | Terraform schema | All outputs `computed=True` |
| `read()` | Fetch data | Returns `Data` object |

---

## Common Patterns

### Handle Missing Data

Always return data, even if not found:

```python
async def read(self, config: Config) -> Data:
    result = await api.query(config.id)

    if not result:
        # Return empty data instead of raising error
        return Data(
            id=config.id,
            found=False,
            value=None,
        )

    return Data(
        id=result["id"],
        found=True,
        value=result["value"],
    )
```

### Generate Deterministic IDs

IDs should be stable across multiple reads:

```python
async def read(self, config: Config) -> Data:
    # Good: Same inputs = same ID
    query_id = f"{config.region}:{config.type}:{config.name}"

    results = await query(config)

    return Data(
        id=query_id,  # Deterministic
        results=results,
    )
```

### Error Handling

Return data with error fields instead of raising:

```python
@attrs.define
class QueryData:
    id: str
    results: list[str]
    error: str | None = None

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

### Caching

Cache expensive queries:

```python
from functools import lru_cache
import hashlib

class APIQuery(BaseDataSource):
    @lru_cache(maxsize=128)
    async def _cached_query(self, cache_key: str, endpoint: str) -> dict:
        """Cached API query."""
        async with httpx.AsyncClient() as client:
            response = await client.get(endpoint)
            return response.json()

    async def read(self, config: Config) -> Data:
        # Generate cache key from config
        cache_key = hashlib.md5(
            f"{config.endpoint}:{config.filter}".encode()
        ).hexdigest()

        result = await self._cached_query(cache_key, config.endpoint)

        return Data(
            id=cache_key,
            results=result["items"],
        )
```

---

## Best Practices

### 1. All Outputs Must Be Computed

```python
@classmethod
def get_schema(cls) -> PvsSchema:
    return s_data_source({
        # Inputs (no computed flag)
        "query": a_str(required=True),

        # Outputs (all computed)
        "id": a_str(computed=True),
        "results": a_list(a_str(), computed=True),
        "count": a_num(computed=True),
    })
```

### 2. Make Reads Idempotent

Multiple reads should return the same result:

```python
# Good: Deterministic
async def read(self, config: Config) -> Data:
    return await api.query(config.filter)  # Same filter = same result

# Bad: Non-deterministic
async def read(self, config: Config) -> Data:
    return Data(id=str(uuid.uuid4()))  # Different ID each time!
```

### 3. Return Empty Data on Errors

```python
# Good
async def read(self, config: Config) -> Data:
    try:
        result = await api.query()
    except:
        return Data(id=id, results=[])  # Empty data

# Bad
async def read(self, config: Config) -> Data:
    result = await api.query()  # Raises exception!
    return Data(id=id, results=result)
```

### 4. Use Typed Return Values

```python
# Good
@attrs.define
class QueryData:
    id: str
    results: list[str]
    count: int

async def read(self, config: Config) -> QueryData:  # Type safe
    ...

# Bad
async def read(self, config: Config) -> dict:  # No type safety
    return {"id": "123", "results": [...]}
```

---

## Testing

```python
import pytest
from my_provider.data_sources.api_query import APIQuery, APIQueryConfig

@pytest.mark.asyncio
async def test_api_query():
    ds = APIQuery()
    config = APIQueryConfig(endpoint="/users", limit=5)

    data = await ds.read(config)

    assert data.count <= 5
    assert len(data.results) == data.count
    assert data.id  # Has stable ID

@pytest.mark.asyncio
async def test_api_query_error_handling():
    ds = APIQuery()
    config = APIQueryConfig(endpoint="/invalid")

    data = await ds.read(config)

    # Should return data, not raise
    assert data.error is not None
    assert data.results == []
```

---

## See Also

- [Building Your First Data Source](../../tutorials/building-your-first-data-source.md) - Step-by-step tutorial
- [Handle Pagination](handle-pagination.md) - For large result sets
- [Data Source API Reference](../../reference/data-source-api.md) - Complete API
- [Testing Data Sources](../../guides/development/testing-providers.md) - Testing strategies
