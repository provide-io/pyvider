# Data Sources API

Base classes and utilities for creating Terraform data sources (read-only resources).

## Overview

Data sources in Pyvider provide read-only access to external data that can be referenced in Terraform configurations.

### Key Components

- **`BaseDataSource`** - Base class for all data sources
- **`@register_data_source`** - Decorator for data source registration
- **Data Source Context** - Per-query context with provider access

### Usage

Data sources implement a single `read(ctx: ResourceContext)` method that:
- Reads configuration via `ctx.config`
- Queries external systems
- Returns data as computed attributes
- Does not modify any state

```python
from pyvider.resources.context import ResourceContext

async def read(self, ctx: ResourceContext) -> ImageState | None:
    if ctx.config is None:
        return None
    response = await self.client.get_image(ctx.config.image_id)
    return ImageState(**response)
```

## Usage Examples

### Basic Data Source

```python
import attrs
from pyvider.data_sources import register_data_source, BaseDataSource
from pyvider.resources.context import ResourceContext
from pyvider.schema import s_data_source, a_str, a_num, PvsSchema
from pyvider.exceptions import DataSourceError


@attrs.define
class UserConfig:
    """Data source lookup configuration."""
    user_id: int


@attrs.define
class UserData:
    """User data returned by data source."""
    id: int
    user_id: int
    name: str
    email: str
    username: str


@register_data_source("user")
class User(BaseDataSource):
    """
    Looks up user information by ID.

    This is a read-only data source that fetches user details
    from an external API.
    """

    config_class = UserConfig
    data_class = UserData

    @classmethod
    def get_schema(cls) -> PvsSchema:
        """Define data source schema."""
        return s_data_source({
            # Input (required)
            "user_id": a_num(
                required=True,
                description="User ID to lookup",
                validators=[
                    lambda x: x > 0 or "User ID must be positive",
                ],
            ),

            # Computed outputs
            "id": a_num(computed=True, description="User ID"),
            "name": a_str(computed=True, description="Full name"),
            "email": a_str(computed=True, description="Email address"),
            "username": a_str(computed=True, description="Username"),
        })

    async def read(self, ctx: ResourceContext) -> UserData | None:
        """Fetch user data from API."""
        if not ctx.config:
            return None

        from pyvider.hub import hub
        provider = hub.get_component("singleton", "provider")

        try:
            # Fetch from API
            user = await provider.api.get_user(ctx.config.user_id)

            return UserData(
                id=user.id,
                user_id=user.id,
                name=user.name,
                email=user.email,
                username=user.username,
            )

        except Exception as e:
            if "404" in str(e):
                raise DataSourceError(f"User {ctx.config.user_id} not found")
            raise
```

### Data Source with Filtering

```python
@attrs.define
class ServerFilterConfig:
    """Filter configuration."""
    region: str
    status: str | None = None
    tags: dict[str, str] | None = None


@attrs.define
class ServerListData:
    """Filtered server list."""
    servers: list[dict]
    count: int


@register_data_source("servers")
class Servers(BaseDataSource):
    """Fetch filtered list of servers."""

    config_class = ServerFilterConfig
    data_class = ServerListData

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_data_source({
            # Filter inputs
            "region": a_str(required=True, description="Filter by region"),
            "status": a_str(description="Filter by status"),
            "tags": a_map(a_str(), description="Filter by tags"),

            # Computed outputs
            "servers": a_list(
                a_obj({
                    "id": a_str(),
                    "name": a_str(),
                    "status": a_str(),
                }),
                computed=True,
                description="List of matching servers",
            ),
            "count": a_num(computed=True, description="Number of servers"),
        })

    async def read(self, ctx: ResourceContext) -> ServerListData | None:
        """Fetch and filter servers."""
        if not ctx.config:
            return None

        from pyvider.hub import hub
        provider = hub.get_component("singleton", "provider")

        # Build filter criteria
        filters = {"region": ctx.config.region}

        if ctx.config.status:
            filters["status"] = ctx.config.status

        if ctx.config.tags:
            filters["tags"] = ctx.config.tags

        # Fetch filtered servers
        servers = await provider.api.list_servers(filters)

        return ServerListData(
            servers=[
                {
                    "id": s.id,
                    "name": s.name,
                    "status": s.status,
                }
                for s in servers
            ],
            count=len(servers),
        )
```

### Data Source with Caching

```python
from datetime import datetime, timedelta


@register_data_source("region_info")
class RegionInfo(BaseDataSource):
    """Fetch region information with caching."""

    def __init__(self):
        super().__init__()
        self._cache = {}
        self._cache_expiry = {}

    async def read(self, ctx: ResourceContext) -> RegionData | None:
        """Fetch region info with caching."""
        if not ctx.config:
            return None

        region = ctx.config.region
        now = datetime.now()

        # Check cache
        if region in self._cache:
            expiry = self._cache_expiry.get(region)
            if expiry and now < expiry:
                return self._cache[region]

        # Fetch fresh data
        from pyvider.hub import hub
        provider = hub.get_component("singleton", "provider")

        region_data = await provider.api.get_region_info(region)

        # Cache for 5 minutes
        data = RegionData(
            name=region_data.name,
            zones=region_data.zones,
            available=region_data.available,
        )

        self._cache[region] = data
        self._cache_expiry[region] = now + timedelta(minutes=5)

        return data
```

### Data Source with Validation

```python
@register_data_source("image")
class Image(BaseDataSource):
    """Lookup image with validation."""

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_data_source({
            "image_name": a_str(
                required=True,
                validators=[
                    lambda x: len(x) >= 3 or "Image name too short",
                    lambda x: not x.startswith("_") or "Invalid image name",
                ],
            ),
            "architecture": a_str(
                validators=[
                    lambda x: x in ["amd64", "arm64"] or "Invalid architecture",
                ],
            ),

            # Computed
            "id": a_str(computed=True),
            "version": a_str(computed=True),
            "created_at": a_str(computed=True),
        })

    async def read(self, ctx: ResourceContext) -> ImageData | None:
        """Fetch image with validation."""
        if not ctx.config:
            return None

        from pyvider.hub import hub
        provider = hub.get_component("singleton", "provider")

        # Fetch image
        image = await provider.api.get_image(
            name=ctx.config.image_name,
            architecture=ctx.config.architecture or "amd64",
        )

        if not image:
            raise DataSourceError(
                f"Image '{ctx.config.image_name}' not found"
            )

        return ImageData(
            id=image.id,
            version=image.version,
            created_at=image.created_at.isoformat(),
        )
```

### Data Source in Terraform

```hcl
# Use data source to look up user
data "mycloud_user" "admin" {
  user_id = 1
}

# Use data source output in resource
resource "mycloud_server" "web" {
  name     = "web-server"
  owner_id = data.mycloud_user.admin.id
}

# Filter servers
data "mycloud_servers" "production" {
  region = "us-east-1"
  status = "running"

  tags = {
    environment = "production"
  }
}

output "production_server_count" {
  value = data.mycloud_servers.production.count
}
```

### Testing Data Sources

```python
import pytest
from pyvider.resources.context import ResourceContext


@pytest.mark.asyncio
async def test_user_data_source():
    """Test user lookup."""
    data_source = User()

    ctx = ResourceContext(
        config=UserConfig(user_id=1)
    )

    data = await data_source.read(ctx)

    assert data is not None
    assert data.user_id == 1
    assert data.email
    assert data.username


@pytest.mark.asyncio
async def test_data_source_not_found():
    """Test handling of missing data."""
    data_source = User()

    ctx = ResourceContext(
        config=UserConfig(user_id=99999)
    )

    with pytest.raises(DataSourceError, match="not found"):
        await data_source.read(ctx)


@pytest.mark.asyncio
async def test_data_source_filtering():
    """Test data source with filters."""
    data_source = Servers()

    ctx = ResourceContext(
        config=ServerFilterConfig(
            region="us-east-1",
            status="running",
            tags={"env": "prod"},
        )
    )

    data = await data_source.read(ctx)

    assert data is not None
    assert data.count > 0
    assert all(s["status"] == "running" for s in data.servers)
```

## Best Practices

### 1. Keep Data Sources Read-Only

Data sources should never modify state:

```python
# Good - Read-only
async def read(self, ctx):
    data = await provider.api.get_user(ctx.config.user_id)
    return UserData(**data)

# Bad - Modifying state
async def read(self, ctx):
    # Don't create/update/delete in data sources!
    user = await provider.api.create_user(...)  # ❌
    return UserData(**user)
```

### 2. Handle Missing Data

Return None or raise clear errors:

```python
async def read(self, ctx):
    try:
        data = await provider.api.get_item(ctx.config.id)
        return ItemData(**data)
    except NotFoundError:
        # Option 1: Return None
        return None

        # Option 2: Raise descriptive error
        raise DataSourceError(f"Item {ctx.config.id} not found")
```

### 3. Use Caching When Appropriate

Cache expensive or frequently accessed data:

```python
# Cache data that changes infrequently
async def read(self, ctx):
    cache_key = f"region:{ctx.config.region}"

    if cached := self._get_from_cache(cache_key):
        return cached

    data = await provider.api.get_region(ctx.config.region)
    self._cache(cache_key, data, ttl=300)

    return data
```

### 4. Validate Inputs

Validate configuration before querying:

```python
@classmethod
def get_schema(cls):
    return s_data_source({
        "id": a_str(
            required=True,
            validators=[
                lambda x: x.isalnum() or "ID must be alphanumeric",
                lambda x: len(x) <= 64 or "ID too long",
            ],
        ),
    })
```

## Related Guides

- [Creating Data Sources](../guides/building-components/creating-data-sources.md) - Complete data source guide
- [Best Practices](../guides/production/best-practices.md) - Data source patterns
- [Testing Providers](../guides/development/testing-providers.md) - Testing data sources
- [Performance Optimization](../guides/production/performance-optimization.md) - Caching strategies
- [Tutorials](../tutorials/intermediate-provider.md) - Real-world examples

## Module Reference
