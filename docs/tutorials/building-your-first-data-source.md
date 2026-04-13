# Building Your First Data Source

Welcome! In this tutorial, you'll build your first Terraform data source using pyvider. Data sources are read-only queries that fetch information without creating infrastructure.

**What You'll Learn:**

- How data sources differ from resources
- Creating a data source class with Pyvider
- Defining input/output schemas
- Implementing read operations
- Using data sources in Terraform

**Time to Complete:** 10-15 minutes

**Prerequisites:**

- Python 3.11+ installed
- Pyvider installed ([installation guide](../getting-started/installation.md))
- Basic Python knowledge
- Basic Terraform knowledge

---

## What is a Data Source?

A data source is a **read-only query** that fetches information from external systems. Unlike resources (which manage infrastructure), data sources just read data.

**Examples:**

- Query file information
- Look up cloud resources
- Fetch API data
- Read database records

**Key Differences from Resources:**

| Data Source | Resource |
|-------------|----------|
| Read-only | Read-write |
| No lifecycle (just query) | Full CRUD lifecycle |
| No state management | Terraform tracks state |
| Quick queries | Manages infrastructure |

---

## Step 1: Create Your Package Structure

```bash
mkdir -p my_provider/data_sources
touch my_provider/__init__.py
touch my_provider/data_sources/__init__.py
touch my_provider/data_sources/file_info.py
```

Your structure:
```
my_provider/
├── __init__.py
└── data_sources/
    ├── __init__.py
    └── file_info.py    # We'll work here
```

---

## Step 2: Define Runtime Types

Data sources have two types:

- **Config** - Input from user (what to query)
- **Data** - Output to user (query results)

Open `my_provider/data_sources/file_info.py`:

```python
import attrs

# Configuration: User inputs
@attrs.define
class FileInfoConfig:
    """What the user wants to query."""
    path: str  # Which file to query

# Data: Query results
@attrs.define
class FileInfoData:
    """Information we return about the file."""
    id: str          # Unique identifier
    path: str        # File path
    size: int        # File size in bytes
    exists: bool     # Whether file exists
    content: str     # File content
```

**Why two types?**

- Config = what to query
- Data = query results

Simple and clean separation!

---

## Step 3: Create the Data Source Class

Now let's create the data source:

```python
from pyvider.data_sources import register_data_source, BaseDataSource
from pyvider.schema import s_data_source, a_str, a_num, a_bool, PvsSchema

@register_data_source("file_info")
class FileInfo(BaseDataSource):
    """Reads information about a local file."""

    # Link our runtime types
    config_class = FileInfoConfig
    state_class = FileInfoData

    @classmethod
    def get_schema(cls) -> PvsSchema:
        """Define what Terraform users see."""
        return s_data_source({
            # Input (from user)
            "path": a_str(required=True, description="File path to query"),

            # Outputs (we compute all of these)
            "id": a_str(computed=True, description="File path as ID"),
            "size": a_num(computed=True, description="File size in bytes"),
            "exists": a_bool(computed=True, description="Whether file exists"),
            "content": a_str(computed=True, description="File content"),
        })
```

**What's happening?**

- `@register_data_source("file_info")` - Registers as a Terraform data source
- `config_class` / `data_class` - Links our attrs classes
- All outputs are `computed=True` - We calculate them

---

## Step 4: Implement the Read Method

Data sources have ONE method: `read()`. It takes a ResourceContext and returns data:

```python
async def read(self, ctx: ResourceContext) -> FileInfoData | None:
    """Read file information."""
    if not ctx.config:
        return None

    from pathlib import Path

    file_path = Path(ctx.config.path)

    # Check if file exists
    if file_path.exists():
        # File exists - read information
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
        # File doesn't exist - return empty data
        return FileInfoData(
            id=str(file_path.absolute()),
            path=str(file_path),
            size=0,
            exists=False,
            content="",
        )
```

**Key points:**

- Takes `ctx: ResourceContext` parameter (same as resources)
- Access configuration via `ctx.config`
- Return `None` if config is unavailable
- Always return data (even if file doesn't exist)
- Generate a stable, deterministic ID
- Handle missing data gracefully

---

## Complete Code

Here's your complete `file_info.py`:

```python
import attrs
from pyvider.data_sources import register_data_source, BaseDataSource
from pyvider.resources.context import ResourceContext
from pyvider.schema import s_data_source, a_str, a_num, a_bool, PvsSchema
from pathlib import Path

# Configuration (input)
@attrs.define
class FileInfoConfig:
    path: str

# Data (output)
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
    state_class = FileInfoData

    @classmethod
    def get_schema(cls) -> PvsSchema:
        """Define Terraform schema."""
        return s_data_source({
            # Input
            "path": a_str(required=True, description="File path to query"),

            # Outputs (all computed)
            "id": a_str(computed=True, description="File path as ID"),
            "size": a_num(computed=True, description="File size in bytes"),
            "exists": a_bool(computed=True, description="Whether file exists"),
            "content": a_str(computed=True, description="File content"),
        })

    async def read(self, ctx: ResourceContext) -> FileInfoData | None:
        """Read file information."""
        if not ctx.config:
            return None

        file_path = Path(ctx.config.path)

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

---

## Step 5: Test with Terraform

Create a Terraform configuration `test.tf`:

```hcl
terraform {
  required_providers {
    local = {
      source = "mycompany/local"
    }
  }
}

# Query file information
data "local_file_info" "readme" {
  path = "../README.md"
}

# Use the data in outputs
output "readme_exists" {
  value = data.local_file_info.readme.exists
}

output "readme_size" {
  value = data.local_file_info.readme.size
}

# Use data in a resource
resource "local_file" "summary" {
  path    = "summary.txt"
  content = <<EOT
README Information:
- Exists: ${data.local_file_info.readme.exists}
- Size: ${data.local_file_info.readme.size} bytes
EOT
}
```

Run it:

```bash
terraform init
terraform plan
terraform apply
```

You should see:

- Data source queries the file
- Outputs show file existence and size
- Resource uses the data

---

## Advanced Example: API Data Source

Here's a more realistic example that queries an API:

```python
import attrs
from pyvider.data_sources import register_data_source, BaseDataSource
from pyvider.resources.context import ResourceContext
from pyvider.schema import s_data_source, a_str, a_num, a_list, PvsSchema
import httpx

@attrs.define
class APIQueryConfig:
    endpoint: str
    limit: int = 10

@attrs.define
class APIQueryData:
    id: str
    endpoint: str
    results: list[str]
    count: int

@register_data_source("api_query")
class APIQuery(BaseDataSource):
    """Queries an external API."""

    config_class = APIQueryConfig
    state_class = APIQueryData

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_data_source({
            # Inputs
            "endpoint": a_str(required=True, description="API endpoint"),
            "limit": a_num(default=10, description="Max results"),

            # Outputs
            "id": a_str(computed=True, description="Query ID"),
            "results": a_list(a_str(), computed=True, description="Results"),
            "count": a_num(computed=True, description="Result count"),
        })

    async def read(self, ctx: ResourceContext) -> APIQueryData | None:
        """Execute API query."""
        if not ctx.config:
            return None

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.example.com{ctx.config.endpoint}",
                params={"limit": ctx.config.limit}
            )
            data = response.json()
            items = data.get("items", [])

            return APIQueryData(
                id=f"{ctx.config.endpoint}:{ctx.config.limit}",
                endpoint=ctx.config.endpoint,
                results=items,
                count=len(items),
            )
```

---

## Best Practices

1. **Generate Stable IDs** - Use deterministic ID generation so repeated queries return the same ID
   ```python
   id = f"{config.param1}:{config.param2}"
   ```

2. **Handle Missing Data** - Return empty values instead of raising errors
   ```python
   if not found:
       return Data(id=id, results=[], count=0)
   ```

3. **Make Reads Idempotent** - Multiple reads should return the same result
   ```python
   # Good: Same query always returns same result
   async def read(self, config):
       return query_api(config.endpoint)  # Deterministic
   ```

4. **Use Computed Outputs** - All outputs should be `computed=True`
   ```python
   "result": a_str(computed=True, description="Query result")
   ```

5. **Add Error Handling** - Handle API failures gracefully
   ```python
   try:
       result = await api.query()
   except APIError:
       return Data(id=id, results=[], error="API unavailable")
   ```

---

## What You've Learned

Congratulations! You've built your first Pyvider data source. You now understand:

✅ **Data Sources vs Resources** - Read-only queries vs managed infrastructure
✅ **Simple Read Pattern** - One method that returns data
✅ **Input/Output Separation** - Config for inputs, Data for outputs
✅ **Deterministic IDs** - Stable identification for query results
✅ **Error Handling** - Graceful handling of missing data

---

## Next Steps

Now that you understand data sources, explore:

- **[Building Your First Resource](building-your-first-resource.md)** - For comparison
- **[How to Create a Data Source](../how-to-guides/data-sources/create-data-source.md)** - Quick reference
- **[Handle Pagination](../how-to-guides/data-sources/handle-pagination.md)** - For large result sets
- **[Data Source API Reference](../reference/data-source-api.md)** - Complete API documentation
- **[Intermediate Provider Tutorial](intermediate-provider.md)** - Build a complete HTTP API provider

---

## Troubleshooting

**Q: My data source isn't being registered**

Make sure you're using `register_data_source()` as a decorator and importing the module.

**Q: Terraform says "computed values can't be configured"**

All outputs in data sources must be `computed=True`. Inputs should not be computed.

**Q: Data isn't refreshing**

Data sources are refreshed on every `terraform plan`. Make sure your `read()` method is actually querying fresh data.

**Q: How do I handle errors?**

Return data with error fields instead of raising exceptions:

```python
@attrs.define
class QueryData:
    id: str
    results: list[str]
    error: str | None = None  # Add error field

async def read(self, config):
    try:
        results = await query()
        return QueryData(id=id, results=results, error=None)
    except Exception as e:
        return QueryData(id=id, results=[], error=str(e))
```

For more help, see [Troubleshooting Guide](../troubleshooting.md).
