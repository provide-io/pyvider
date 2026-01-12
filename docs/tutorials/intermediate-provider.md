# Tutorial: Building an HTTP API Provider

This tutorial walks you through building a real Terraform provider for a REST API service. You'll learn production patterns for authentication, error handling, caching, and testing.

## What We'll Build

A provider for the **JSONPlaceholder API** (a fake REST API for testing):
- **Provider**: Authentication and configuration
- **Resources**: Posts and Comments (CRUD operations)
- **Data Sources**: User lookups
- **Functions**: Text validation

**API Documentation**: [https://jsonplaceholder.typicode.com/](https://jsonplaceholder.typicode.com/)

## Prerequisites

- Python 3.11+
- Basic understanding of Pyvider (complete [Quick Start](../getting-started/quick-start.md) first)
- Familiarity with REST APIs
- Knowledge of async/await in Python

## Project Setup

### 1. Create Project Structure

```bash
# Create project directory
mkdir jsonplaceholder-provider
cd jsonplaceholder-provider

# Create package structure
mkdir -p jsonplaceholder_provider/{provider,resources,data_sources,functions,tests}

# Create __init__.py files
touch jsonplaceholder_provider/__init__.py
touch jsonplaceholder_provider/provider/__init__.py
touch jsonplaceholder_provider/resources/__init__.py
touch jsonplaceholder_provider/data_sources/__init__.py
touch jsonplaceholder_provider/functions/__init__.py
touch jsonplaceholder_provider/tests/__init__.py

# Create main files
touch jsonplaceholder_provider/provider/provider.py
touch jsonplaceholder_provider/resources/post.py
touch jsonplaceholder_provider/resources/comment.py
touch jsonplaceholder_provider/data_sources/user.py
touch jsonplaceholder_provider/functions/validate_text.py
```

### 2. Create pyproject.toml

```toml
[project]
name = "terraform-provider-jsonplaceholder"
version = "0.1.0"
description = "Terraform provider for JSONPlaceholder API"
requires-python = ">=3.11"
dependencies = [
    "pyvider>=0.0.3",
    "httpx>=0.24.0",
]

[dependency-groups]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.0.0",
    "mypy>=1.0.0",
    "ruff>=0.1.0",
]

[build-system]
requires = ["setuptools>=65", "wheel"]
build-backend = "setuptools.build_meta"

[tool.pyvider]
provider_name = "jsonplaceholder"
```

### 3. Install Dependencies

```bash
uv sync --group dev
```

---

## Step 1: Build the Provider

Create `jsonplaceholder_provider/provider/provider.py`:

```python
"""JSONPlaceholder Terraform Provider."""

from typing import Any
import attrs
import httpx
from provide.foundation import logger

from pyvider.providers import register_provider, BaseProvider, ProviderMetadata
from pyvider.schema import s_provider, a_str, a_num, a_bool, PvsSchema
from pyvider.exceptions import ProviderConfigurationError


@attrs.define
class JSONPlaceholderConfig:
    """Provider configuration."""
    api_endpoint: str = "https://jsonplaceholder.typicode.com"
    timeout: int = 30
    max_retries: int = 3
    verify_ssl: bool = True


@register_provider("jsonplaceholder")
class JSONPlaceholderProvider(BaseProvider):
    """
    Terraform provider for JSONPlaceholder API.

    Provides resources and data sources for interacting with the
    JSONPlaceholder fake REST API service.
    """

    def __init__(self):
        super().__init__(
            metadata=ProviderMetadata(
                name="jsonplaceholder",
                version="0.1.0",
                protocol_version="6",
                description="JSONPlaceholder API provider",
            )
        )
        self.config: JSONPlaceholderConfig | None = None
        self.http_client: httpx.AsyncClient | None = None

    def _build_schema(self) -> PvsSchema:
        """Define provider configuration schema."""
        return s_provider({
            "api_endpoint": a_str(
                default="https://jsonplaceholder.typicode.com",
                description="JSONPlaceholder API endpoint URL",
            ),
            "timeout": a_num(
                default=30,
                description="API request timeout in seconds",
                validators=[
                    lambda x: 5 <= x <= 300 or "Timeout must be 5-300 seconds"
                ],
            ),
            "max_retries": a_num(
                default=3,
                description="Maximum retry attempts for failed requests",
                validators=[
                    lambda x: 0 <= x <= 10 or "Max retries must be 0-10"
                ],
            ),
            "verify_ssl": a_bool(
                default=True,
                description="Verify SSL certificates",
            ),
        })

    async def configure(self, config: dict[str, Any]) -> None:
        """Configure the provider with user settings."""
        await super().configure(config)

        # Store configuration
        self.config = JSONPlaceholderConfig(
            api_endpoint=config.get("api_endpoint", "https://jsonplaceholder.typicode.com"),
            timeout=config.get("timeout", 30),
            max_retries=config.get("max_retries", 3),
            verify_ssl=config.get("verify_ssl", True),
        )

        # Create HTTP client with connection pooling
        self.http_client = httpx.AsyncClient(
            base_url=self.config.api_endpoint,
            timeout=httpx.Timeout(self.config.timeout),
            verify=self.config.verify_ssl,
            limits=httpx.Limits(
                max_connections=100,
                max_keepalive_connections=20,
            ),
        )

        # Test connectivity
        try:
            response = await self.http_client.get("/posts/1")
            response.raise_for_status()
            logger.info(
                "Successfully connected to JSONPlaceholder API",
                endpoint=self.config.api_endpoint,
            )
        except Exception as e:
            raise ProviderConfigurationError(
                f"Failed to connect to JSONPlaceholder API: {e}"
            )

    async def close(self) -> None:
        """Clean up resources."""
        if self.http_client:
            await self.http_client.aclose()
            self.http_client = None

    async def api_request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> httpx.Response:
        """
        Make an authenticated API request with retries.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            path: API path
            **kwargs: Additional arguments for httpx

        Returns:
            HTTP response

        Raises:
            Exception: If request fails after retries
        """
        for attempt in range(self.config.max_retries + 1):
            try:
                response = await self.http_client.request(method, path, **kwargs)
                response.raise_for_status()

                logger.debug(
                    "API request successful",
                    method=method,
                    path=path,
                    status=response.status_code,
                    attempt=attempt + 1,
                )

                return response

            except httpx.HTTPStatusError as e:
                # Don't retry client errors (4xx)
                if 400 <= e.response.status_code < 500:
                    logger.warning(
                        "Client error - not retrying",
                        method=method,
                        path=path,
                        status=e.response.status_code,
                    )
                    raise

                # Retry server errors (5xx) and network issues
                if attempt < self.config.max_retries:
                    logger.warning(
                        "Request failed - retrying",
                        method=method,
                        path=path,
                        attempt=attempt + 1,
                        error=str(e),
                    )
                    continue
                raise

            except httpx.RequestError as e:
                if attempt < self.config.max_retries:
                    logger.warning(
                        "Request error - retrying",
                        method=method,
                        path=path,
                        attempt=attempt + 1,
                        error=str(e),
                    )
                    continue
                raise
```

---

## Step 2: Create Post Resource

Create `jsonplaceholder_provider/resources/post.py`:

```python
"""Post resource for managing blog posts."""

import attrs
from provide.foundation import logger

from pyvider.resources import register_resource, BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.schema import s_resource, a_str, a_num, PvsSchema
from pyvider.exceptions import ResourceError
from pyvider.hub import hub


@attrs.define
class PostConfig:
    """Post configuration."""
    title: str
    body: str
    user_id: int


@attrs.define
class PostState:
    """Post state."""
    id: int
    title: str
    body: str
    user_id: int


@register_resource("post")
class Post(BaseResource):
    """
    Manages a blog post on JSONPlaceholder.

    This resource allows creation, reading, updating, and deletion of posts.
    Note: JSONPlaceholder is a fake API, so changes don't persist.
    """

    config_class = PostConfig
    state_class = PostState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        """Define post schema."""
        return s_resource({
            # Configuration attributes
            "title": a_str(
                required=True,
                description="Post title",
                validators=[
                    lambda x: len(x) >= 3 or "Title must be at least 3 characters",
                    lambda x: len(x) <= 200 or "Title must be 200 characters or less",
                ],
            ),
            "body": a_str(
                required=True,
                description="Post content",
                validators=[
                    lambda x: len(x) >= 10 or "Body must be at least 10 characters",
                ],
            ),
            "user_id": a_num(
                required=True,
                description="User ID who owns the post",
                validators=[
                    lambda x: x > 0 or "User ID must be positive",
                ],
            ),

            # Computed attributes
            "id": a_num(
                computed=True,
                description="Post ID",
            ),
        })

    async def _create_apply(
        self,
        ctx: ResourceContext,
    ) -> tuple[PostState | None, None]:
        """Create a new post."""
        if not ctx.config:
            return None, None

        provider = hub.get_component("singleton", "provider")

        logger.info(
            "Creating post",
            title=ctx.config.title,
            user_id=ctx.config.user_id,
        )

        # Create post via API
        response = await provider.api_request(
            "POST",
            "/posts",
            json={
                "title": ctx.config.title,
                "body": ctx.config.body,
                "userId": ctx.config.user_id,
            },
        )

        data = response.json()

        state = PostState(
            id=data["id"],
            title=data["title"],
            body=data["body"],
            user_id=data["userId"],
        )

        logger.info("Post created successfully", post_id=state.id)

        return state, None

    async def read(self, ctx: ResourceContext) -> PostState | None:
        """Read current post state."""
        if not ctx.state:
            return None

        provider = hub.get_component("singleton", "provider")

        try:
            response = await provider.api_request("GET", f"/posts/{ctx.state.id}")
            data = response.json()

            return PostState(
                id=data["id"],
                title=data["title"],
                body=data["body"],
                user_id=data["userId"],
            )

        except Exception as e:
            if "404" in str(e):
                logger.debug(
                    "Post not found - assuming deleted",
                    post_id=ctx.state.id,
                )
                return None
            raise

    async def _update_apply(
        self,
        ctx: ResourceContext,
    ) -> tuple[PostState | None, None]:
        """Update an existing post."""
        if not ctx.config or not ctx.state:
            return None, None

        provider = hub.get_component("singleton", "provider")

        logger.info(
            "Updating post",
            post_id=ctx.state.id,
            title=ctx.config.title,
        )

        response = await provider.api_request(
            "PUT",
            f"/posts/{ctx.state.id}",
            json={
                "id": ctx.state.id,
                "title": ctx.config.title,
                "body": ctx.config.body,
                "userId": ctx.config.user_id,
            },
        )

        data = response.json()

        state = PostState(
            id=ctx.state.id,
            title=data["title"],
            body=data["body"],
            user_id=data["userId"],
        )

        logger.info("Post updated successfully", post_id=state.id)

        return state, None

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        """Delete a post."""
        if not ctx.state:
            return

        provider = hub.get_component("singleton", "provider")

        logger.info("Deleting post", post_id=ctx.state.id)

        try:
            await provider.api_request("DELETE", f"/posts/{ctx.state.id}")
            logger.info("Post deleted successfully", post_id=ctx.state.id)
        except Exception as e:
            if "404" in str(e):
                # Already deleted
                logger.debug("Post already deleted", post_id=ctx.state.id)
                return
            raise
```

---

## Step 3: Create User Data Source

Create `jsonplaceholder_provider/data_sources/user.py`:

```python
"""User data source for looking up user information."""

import attrs
from provide.foundation import logger

from pyvider.data_sources import register_data_source, BaseDataSource
from pyvider.resources.context import ResourceContext
from pyvider.schema import s_data_source, a_str, a_num, PvsSchema
from pyvider.exceptions import DataSourceError
from pyvider.hub import hub


@attrs.define
class UserConfig:
    """User lookup configuration."""
    user_id: int


@attrs.define
class UserData:
    """User data."""
    id: int
    user_id: int  # For compatibility
    name: str
    email: str
    username: str
    website: str


@register_data_source("user")
class User(BaseDataSource):
    """
    Looks up user information from JSONPlaceholder.

    This data source retrieves user details by ID.
    """

    config_class = UserConfig
    data_class = UserData

    @classmethod
    def get_schema(cls) -> PvsSchema:
        """Define user data source schema."""
        return s_data_source({
            # Input
            "user_id": a_num(
                required=True,
                description="User ID to lookup",
                validators=[
                    lambda x: x > 0 or "User ID must be positive",
                ],
            ),

            # Computed outputs
            "id": a_num(computed=True, description="User ID"),
            "name": a_str(computed=True, description="User full name"),
            "email": a_str(computed=True, description="User email"),
            "username": a_str(computed=True, description="Username"),
            "website": a_str(computed=True, description="User website"),
        })

    async def read(self, ctx: ResourceContext) -> UserData | None:
        """Fetch user data."""
        if not ctx.config:
            return None

        provider = hub.get_component("singleton", "provider")

        logger.debug("Fetching user", user_id=ctx.config.user_id)

        try:
            response = await provider.api_request(
                "GET",
                f"/users/{ctx.config.user_id}",
            )
            data = response.json()

            user_data = UserData(
                id=data["id"],
                user_id=data["id"],
                name=data["name"],
                email=data["email"],
                username=data["username"],
                website=data.get("website", ""),
            )

            logger.debug(
                "User fetched successfully",
                user_id=user_data.id,
                username=user_data.username,
            )

            return user_data

        except Exception as e:
            if "404" in str(e):
                raise DataSourceError(f"User {ctx.config.user_id} not found")
            raise
```

---

## Step 4: Test the Provider

Create `jsonplaceholder_provider/tests/test_post.py`:

```python
"""Tests for post resource."""

import pytest
from pyvider.resources.context import ResourceContext
from jsonplaceholder_provider.resources.post import Post, PostConfig, PostState


@pytest.mark.asyncio
async def test_post_schema():
    """Test post schema is defined."""
    schema = Post.get_schema()
    assert schema is not None
    assert "title" in schema.main_block.attributes
    assert "body" in schema.main_block.attributes
    assert "user_id" in schema.main_block.attributes


@pytest.mark.asyncio
async def test_post_create():
    """Test creating a post."""
    post = Post()

    ctx = ResourceContext(
        config=PostConfig(
            title="Test Post",
            body="This is a test post body with enough content",
            user_id=1,
        )
    )

    state, private = await post._create_apply(ctx)

    assert state is not None
    assert state.title == "Test Post"
    assert state.body == "This is a test post body with enough content"
    assert state.user_id == 1
    assert state.id > 0


@pytest.mark.asyncio
async def test_post_read():
    """Test reading a post."""
    post = Post()

    # First create a post
    create_ctx = ResourceContext(
        config=PostConfig(
            title="Test Post",
            body="Test body content here",
            user_id=1,
        )
    )

    state, _ = await post._create_apply(create_ctx)

    # Now read it
    read_ctx = ResourceContext(state=state)
    read_state = await post.read(read_ctx)

    assert read_state is not None
    assert read_state.id == state.id
    assert read_state.title == state.title


@pytest.mark.asyncio
async def test_post_update():
    """Test updating a post."""
    post = Post()

    # Create post
    create_ctx = ResourceContext(
        config=PostConfig(
            title="Original Title",
            body="Original body content",
            user_id=1,
        )
    )

    state, _ = await post._create_apply(create_ctx)

    # Update post
    update_ctx = ResourceContext(
        config=PostConfig(
            title="Updated Title",
            body="Updated body content",
            user_id=1,
        ),
        state=state,
    )

    updated_state, _ = await post._update_apply(update_ctx)

    assert updated_state is not None
    assert updated_state.title == "Updated Title"
    assert updated_state.body == "Updated body content"


@pytest.mark.asyncio
async def test_post_delete():
    """Test deleting a post."""
    post = Post()

    # Create post
    create_ctx = ResourceContext(
        config=PostConfig(
            title="Test Post",
            body="Test body",
            user_id=1,
        )
    )

    state, _ = await post._create_apply(create_ctx)

    # Delete post
    delete_ctx = ResourceContext(state=state)
    await post._delete_apply(delete_ctx)

    # Verify deletion (read should return None)
    read_ctx = ResourceContext(state=state)
    read_state = await post.read(read_ctx)

    # Note: JSONPlaceholder doesn't actually delete, but we test the pattern
    # In a real API, this would return None
```

Run tests:

```bash
uv run pytest -v
```

---

## Step 5: Use with Terraform

Create `main.tf`:

```hcl
terraform {
  required_providers {
    jsonplaceholder = {
      source = "example.com/tutorials/jsonplaceholder"
      version = "0.1.0"
    }
  }
}

provider "jsonplaceholder" {
  api_endpoint = "https://jsonplaceholder.typicode.com"
  timeout      = 30
  max_retries  = 3
}

# Look up a user
data "jsonplaceholder_user" "author" {
  user_id = 1
}

# Create a post
resource "jsonplaceholder_post" "tutorial" {
  title   = "Learning Pyvider"
  body    = "This post demonstrates building a Terraform provider with Pyvider."
  user_id = data.jsonplaceholder_user.author.id
}

output "post_id" {
  value = jsonplaceholder_post.tutorial.id
}

output "author_email" {
  value = data.jsonplaceholder_user.author.email
}
```

Install and run:

```bash
# Install provider
pyvider install

# Initialize Terraform
terraform init

# Plan changes
terraform plan

# Apply changes
terraform apply
```

---

## Key Takeaways

### Patterns You Learned

1. **Provider Configuration**
   - Schema definition with validation
   - HTTP client setup with connection pooling
   - Retry logic for resilience

2. **Resource Implementation**
   - Full CRUD lifecycle
   - Error handling
   - Logging

3. **Data Source Implementation**
   - Read-only data fetching
   - Error handling for missing data

4. **Testing**
   - Async test patterns
   - Resource lifecycle testing
   - Schema validation

### Production Considerations

For a real provider, also implement:

- **Caching** - Cache frequently accessed data
- **Rate Limiting** - Respect API rate limits
- **Pagination** - Handle paginated responses
- **Authentication** - OAuth, API keys, etc.
- **Private State** - For sensitive data
- **Import Support** - Allow importing existing resources

---

## Next Steps

- Add the comment resource (similar to post)
- Add a validate_text function
- Implement caching for user lookups
- Add comprehensive error handling
- Write integration tests
- Add more data sources (posts by user, etc.)

---

## Related Documentation

- [Creating Providers](../guides/building-components/creating-providers.md) - Complete provider guide
- [Creating Resources](../guides/building-components/creating-resources.md) - Resource patterns
- [Creating Data Sources](../guides/building-components/creating-data-sources.md) - Data source patterns
- [Testing Providers](../guides/development/testing-providers.md) - Testing strategies
- [Error Handling](../guides/development/error-handling.md) - Error patterns
- [Security Best Practices](../guides/production/security-best-practices.md) - Security guidance
- [Performance Optimization](../guides/production/performance-optimization.md) - Performance tips
