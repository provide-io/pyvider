# Creating Data Sources

This guide shows you how to create data sources for your Pyvider provider. Data sources are read-only queries that fetch information from external systems.

## What is a Data Source?

A data source in Terraform:
- **Reads data** from external systems (APIs, databases, files)
- **Does not manage** infrastructure (read-only)
- **Returns computed values** to be used by resources

## Basic Data Source Example

Here's a complete, working data source:

```python
from pyvider.data_sources import register_data_source, BaseDataSource
from pyvider.schema import s_data_source, a_str, a_num, a_bool, PvsSchema
import attrs

# Configuration (input from user)
@attrs.define
class FileInfoConfig:
    path: str

# Data (output to user)
@attrs.define
class FileInfoData:
    id: str
    path: str
    size: int
    exists: bool
    content: str

@register_data_source("file_info")
class FileInfo(BaseDataSource):
    """Reads information about a local file."""

    config_class = FileInfoConfig
    data_class = FileInfoData

    @classmethod
    def get_schema(cls) -> PvsSchema:
        """Define Terraform schema."""
        return s_data_source({
            # Input (from user)
            "path": a_str(required=True, description="File path to query"),

            # Outputs (computed by provider)
            "id": a_str(computed=True, description="File path as ID"),
            "size": a_num(computed=True, description="File size in bytes"),
            "exists": a_bool(computed=True, description="Whether file exists"),
            "content": a_str(computed=True, description="File content"),
        })

    async def read(self, config: FileInfoConfig) -> FileInfoData:
        """Read file information."""
        from pathlib import Path

        file_path = Path(config.path)

        if file_path.exists():
            content = file_path.read_text()
            size = file_path.stat().st_size
            return FileInfoData(
                id=str(file_path.absolute()),
                path=str(file_path),
                size=size,
                exists=True,
                content=content,
            )
        else:
            return FileInfoData(
                id=str(file_path.absolute()),
                path=str(file_path),
                size=0,
                exists=False,
                content="",
            )
```

## Data Source Components

### 1. Schema Definition

Define inputs and outputs:

```python
@classmethod
def get_schema(cls) -> PvsSchema:
    return s_data_source({
        # Inputs (required or with defaults)
        "filter": a_str(required=True, description="Filter expression"),
        "limit": a_num(default=10, description="Max results"),

        # Outputs (all computed=True)
        "id": a_str(computed=True, description="Data source ID"),
        "results": a_list(a_str(), computed=True, description="Query results"),
        "count": a_num(computed=True, description="Result count"),
    })
```

### 2. Runtime Classes

Separate configuration and data:

```python
@attrs.define
class QueryConfig:
    """Input from user."""
    filter: str
    limit: int = 10

@attrs.define
class QueryData:
    """Output to user."""
    id: str
    results: list[str]
    count: int
```

### 3. Read Method

Implement the data fetching logic:

```python
async def read(self, config: QueryConfig) -> QueryData:
    """Fetch data based on configuration."""
    # Query your API/database
    results = await self.fetch_data(config.filter, config.limit)

    return QueryData(
        id=generate_id(config),
        results=results,
        count=len(results),
    )
```

## Complete Example: API Data Source

Here's a data source that queries an external API:

```python
from pyvider.data_sources import register_data_source, BaseDataSource
from pyvider.schema import s_data_source, a_str, a_num, a_list, a_map, PvsSchema
import attrs
import httpx

@attrs.define
class APIQueryConfig:
    endpoint: str
    filter: str | None = None
    limit: int = 10

@attrs.define
class APIQueryData:
    id: str
    endpoint: str
    results: list[dict[str, str]]
    count: int
    metadata: dict[str, str]

@register_data_source("api_query")
class APIQuery(BaseDataSource):
    """Queries an external API."""

    config_class = APIQueryConfig
    data_class = APIQueryData

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_data_source({
            # Inputs
            "endpoint": a_str(required=True, description="API endpoint path"),
            "filter": a_str(description="Optional filter expression"),
            "limit": a_num(default=10, description="Maximum results"),

            # Outputs
            "id": a_str(computed=True, description="Query ID"),
            "results": a_list(
                a_map(a_str()),
                computed=True,
                description="Query results"
            ),
            "count": a_num(computed=True, description="Result count"),
            "metadata": a_map(a_str(), computed=True, description="Response metadata"),
        })

    async def read(self, config: APIQueryConfig) -> APIQueryData:
        """Execute API query."""
        async with httpx.AsyncClient() as client:
            params = {"limit": config.limit}
            if config.filter:
                params["filter"] = config.filter

            response = await client.get(
                f"https://api.example.com{config.endpoint}",
                params=params
            )
            data = response.json()

            return APIQueryData(
                id=f"{config.endpoint}:{config.filter}:{config.limit}",
                endpoint=config.endpoint,
                results=data.get("items", []),
                count=len(data.get("items", [])),
                metadata=data.get("metadata", {}),
            )
```

## Using Data Sources in Terraform

After creating a data source, users can query it:

```hcl
# Query file information
data "local_file_info" "readme" {
  path = "../README.md"
}

# Use the data in a resource
resource "local_file" "summary" {
  path    = "summary.txt"
  content = <<EOT
README size: ${data.local_file_info.readme.size} bytes
Exists: ${data.local_file_info.readme.exists}
EOT
}

# Query API
data "mycloud_api_query" "servers" {
  endpoint = "/servers"
  filter   = "status=running"
  limit    = 50
}

output "server_count" {
  value = data.mycloud_api_query.servers.count
}
```

## Data Source vs Resource

**Data Source** (read-only):
- Queries existing data
- Does not create/modify infrastructure
- Can be refreshed on every plan
- No state management

**Resource** (read-write):
- Manages infrastructure lifecycle
- Creates, updates, deletes resources
- Maintains state between runs
- Uses ResourceContext API

## Best Practices

1. **Make read idempotent** - Multiple reads should return same result
2. **Generate stable IDs** - Use deterministic ID generation
3. **Handle errors gracefully** - Return empty/null data on failures
4. **Add caching** - Cache API responses if appropriate
5. **Use computed outputs** - All outputs should be `computed=True`
6. **Validate inputs** - Check configuration in `read()`

## Advanced: Conditional Data

Handle missing or conditional data:

```python
async def read(self, config: QueryConfig) -> QueryData:
    """Read with error handling."""
    try:
        results = await self.api.query(config.filter)

        return QueryData(
            id=generate_id(config),
            results=results,
            found=True,
            error=None,
        )
    except APIError as e:
        # Return empty data on error
        return QueryData(
            id=generate_id(config),
            results=[],
            found=False,
            error=str(e),
        )
```

## Advanced: Paginated Queries

Handle pagination:

```python
async def read(self, config: QueryConfig) -> QueryData:
    """Read with pagination."""
    all_results = []
    page = 1
    max_pages = config.limit // 100 + 1

    async with httpx.AsyncClient() as client:
        while page <= max_pages:
            response = await client.get(
                config.endpoint,
                params={"page": page, "per_page": 100}
            )
            data = response.json()

            all_results.extend(data["items"])

            if not data.get("has_more"):
                break

            page += 1

    return QueryData(
        id=generate_id(config),
        results=all_results[:config.limit],
        count=len(all_results[:config.limit]),
        total_available=len(all_results),
    )
```

## See Also

- [Schema System](../../explanation/schema-system.md) - Understanding schemas
- [Data Source API](../../api/data_sources.md) - BaseDataSource reference
- [Creating Resources](../building-components/creating-resources.md) - For comparison
- [Best Practices](../production/best-practices.md) - Production patterns
