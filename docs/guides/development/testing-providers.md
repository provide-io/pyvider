# Testing Providers

This page documents Pyvider's testing utilities and best practices for testing providers.

## Overview

Pyvider provides testing utilities built on pytest to help you write comprehensive tests for your providers, resources, data sources, and functions.

## Test Fixtures

### Provider Test Fixture

Create a reusable provider fixture for your tests:

```python
import pytest
from my_provider import MyCloudProvider

@pytest.fixture
def provider():
    """Create a configured provider instance."""
    return MyCloudProvider()

@pytest.fixture
async def configured_provider(provider):
    """Create and configure a provider."""
    config = MyCloudProvider.Config(
        api_key="test-key",
        region="us-east-1"
    )
    await provider.configure(config)
    return provider
```

## Testing Resources

### Basic Resource Tests

Test the complete CRUD lifecycle:

```python
import pytest
import attrs
from pyvider.resources.context import ResourceContext
from my_provider.resources import Instance

# Example attrs classes for Instance resource
@attrs.define
class InstanceConfig:
    """Instance configuration."""
    name: str
    size: str
    ami: str

@attrs.define
class InstanceState:
    """Instance state."""
    id: str
    name: str
    size: str
    ami: str
    status: str


def make_context(
    *,
    config: InstanceConfig | None = None,
    state: InstanceState | None = None,
    planned_state: InstanceState | None = None,
):
    return ResourceContext(config=config, state=state, planned_state=planned_state)


@pytest.fixture
def instance_resource():
    """Create an instance resource."""
    return Instance()


@pytest.mark.asyncio
async def test_resource_create(instance_resource):
    """Test resource creation."""
    ctx = make_context(
        config=InstanceConfig(name="test-instance", size="t2.micro", ami="ami-12345678")
    )
    state, _ = await instance_resource._create_apply(ctx)

    assert state is not None
    assert state.id.startswith("i-")
    assert state.status == "running"


@pytest.mark.asyncio
async def test_resource_read(instance_resource):
    """Test resource read."""
    create_ctx = make_context(
        config=InstanceConfig(name="test-instance", size="t2.micro", ami="ami-12345678")
    )
    state, _ = await instance_resource._create_apply(create_ctx)

    read_ctx = ResourceContext(state=state)
    read_state = await instance_resource.read(read_ctx)

    assert read_state is not None
    assert read_state.id == state.id


@pytest.mark.asyncio
async def test_resource_update(instance_resource):
    """Test resource update."""
    create_ctx = make_context(
        config=InstanceConfig(name="test-instance", size="t2.micro", ami="ami-12345678")
    )
    state, _ = await instance_resource._create_apply(create_ctx)

    update_ctx = make_context(
        config=InstanceConfig(
            name="test-instance",
            size="t3.small",  # Changed size
            ami="ami-12345678",
        ),
        state=state,
        planned_state=state,
    )
    updated_state, _ = await instance_resource._update_apply(update_ctx)

    assert updated_state is not None
    assert updated_state.size == "t3.small"


@pytest.mark.asyncio
async def test_resource_delete(instance_resource):
    """Test resource deletion."""
    create_ctx = make_context(
        config=InstanceConfig(name="test-instance", size="t2.micro", ami="ami-12345678")
    )
    state, _ = await instance_resource._create_apply(create_ctx)

    await instance_resource._delete_apply(ResourceContext(state=state))

    read_ctx = ResourceContext(state=state)
    assert await instance_resource.read(read_ctx) is None
```

### Testing Resource Validation

Test configuration validation:

```python
import pytest
from pyvider.exceptions import ValidationError

@pytest.mark.asyncio
async def test_resource_validates_required_fields(instance_resource):
    """Test that required fields are validated."""
    # Note: In practice, attrs will raise TypeError for missing required fields
    # This example shows conceptual validation testing
    with pytest.raises((ValidationError, TypeError)):
        ctx = make_context(
            config=InstanceConfig(
                # Missing required 'name' field - this will fail at construction
                size="t2.micro",
                ami="ami-12345678",
            )
        )
        await instance_resource._create_apply(ctx)


@pytest.mark.asyncio
async def test_resource_validates_field_values(instance_resource):
    """Test that field values are validated."""
    ctx = make_context(
        config=InstanceConfig(
            name="test",
            size="invalid-size",  # Invalid size
            ami="ami-12345678",
        )
    )
    with pytest.raises(ValidationError):
        await instance_resource._create_apply(ctx)
```

## Testing Data Sources

### Basic Data Source Tests

```python
import pytest
import attrs
from my_provider.data_sources import Image

# Example attrs classes for Image data source
@attrs.define
class ImageConfig:
    """Image lookup configuration."""
    name_filter: str
    most_recent: bool = True

@attrs.define
class ImageData:
    """Image data."""
    id: str
    name: str
    created_at: str

@pytest.fixture
def image_data_source():
    """Create an image data source."""
    return Image()

@pytest.mark.asyncio
async def test_data_source_read(image_data_source):
    """Test data source read."""
    config = ImageConfig(
        name_filter="ubuntu-22.04",
        most_recent=True
    )

    data = await image_data_source.read(config)

    assert data.id is not None
    assert "ubuntu" in data.name.lower()
    assert data.created_at is not None

@pytest.mark.asyncio
async def test_data_source_filters(image_data_source):
    """Test data source filtering."""
    config = ImageConfig(
        name_filter="ubuntu*",
        most_recent=True
    )

    data = await image_data_source.read(config)

    assert data.id is not None
    assert "ubuntu" in data.name.lower()
```

## Testing Functions

### Basic Function Tests

```python
import pytest
import attrs
from my_provider.functions import HashFunction

# Example attrs classes for HashFunction
@attrs.define
class HashParameters:
    """Hash function parameters."""
    input: str
    algorithm: str = "sha256"

@attrs.define
class HashResult:
    """Hash function result."""
    output: str

@pytest.fixture
def hash_function():
    """Create a hash function."""
    return HashFunction()

@pytest.mark.asyncio
async def test_function_call(hash_function):
    """Test function execution."""
    params = HashParameters(
        input="hello world",
        algorithm="sha256"
    )

    result = await hash_function.call(params)

    assert result.output is not None
    assert len(result.output) == 64  # SHA256 produces 64 hex chars

@pytest.mark.asyncio
async def test_function_algorithms(hash_function):
    """Test different hash algorithms."""
    params_sha256 = HashParameters(
        input="test",
        algorithm="sha256"
    )
    result_sha256 = await hash_function.call(params_sha256)
    assert len(result_sha256.output) == 64

    params_md5 = HashParameters(
        input="test",
        algorithm="md5"
    )
    result_md5 = await hash_function.call(params_md5)
    assert len(result_md5.output) == 32  # MD5 produces 32 hex chars
```

## Testing Ephemeral Resources

### Ephemeral Resource Lifecycle Tests

```python
import pytest
import attrs
from my_provider.ephemerals import Token

# Example attrs classes for Token ephemeral resource
@attrs.define
class TokenConfig:
    """Token configuration."""
    scope: str
    ttl: int = 3600

@attrs.define
class TokenData:
    """Token data."""
    token: str
    expires_at: str

@pytest.fixture
def token_ephemeral():
    """Create a token ephemeral resource."""
    return Token()

@pytest.mark.asyncio
async def test_ephemeral_open(token_ephemeral):
    """Test ephemeral resource open."""
    config = TokenConfig(
        scope="read:write",
        ttl=3600
    )

    data = await token_ephemeral.open(config)

    assert data.token is not None
    assert data.expires_at is not None

@pytest.mark.asyncio
async def test_ephemeral_renew(token_ephemeral):
    """Test ephemeral resource renewal."""
    config = TokenConfig(
        scope="read:write",
        ttl=3600
    )

    # Open
    original_data = await token_ephemeral.open(config)

    # Renew
    renewed_data = await token_ephemeral.renew(config, original_data)

    assert renewed_data.token == original_data.token
    # Expiration time should be extended
    assert renewed_data.expires_at >= original_data.expires_at

@pytest.mark.asyncio
async def test_ephemeral_close(token_ephemeral):
    """Test ephemeral resource close."""
    config = Token.Config(
        scope="read:write",
        ttl=3600
    )

    # Open
    data = await token_ephemeral.open(config)

    # Close (should not raise)
    await token_ephemeral.close(data)
```

## Mocking External APIs

### Using pytest-mock

```python
import pytest
from unittest.mock import AsyncMock, MagicMock

@pytest.mark.asyncio
async def test_resource_with_mocked_api(instance_resource, mocker):
    """Test resource with mocked API calls."""
    # Mock the API client
    mock_client = AsyncMock()
    mock_client.create_instance.return_value = {
        "id": "i-12345",
        "public_ip": "203.0.113.42",
        "status": "running"
    }

    # Inject mock into resource
    instance_resource.client = mock_client

    # Test create
    ctx = make_context(
        config=Instance.Config(
            name="test-instance",
            size="t2.micro",
            ami="ami-12345678",
        )
    )
    state, _ = await instance_resource._create_apply(ctx)

    # Verify mock was called
    mock_client.create_instance.assert_called_once()
    assert state and state.id == "i-12345"
```

### Using responses for HTTP APIs

```python
import pytest
import responses

@responses.activate
@pytest.mark.asyncio
async def test_data_source_with_http_mock(image_data_source):
    """Test data source with mocked HTTP responses."""
    # Mock HTTP response
    responses.add(
        responses.GET,
        "https://api.mycloud.com/v1/images",
        json={
            "images": [{
                "id": "ami-12345678",
                "name": "ubuntu-22.04",
                "created_at": "2024-01-01T00:00:00Z"
            }]
        },
        status=200
    )

    config = Image.Config(
        name_filter="ubuntu-22.04",
        most_recent=True
    )

    data = await image_data_source.read(config)

    assert data.id == "ami-12345678"
    assert data.name == "ubuntu-22.04"
```

## Property-Based Testing

### Using Hypothesis

```python
import pytest
from hypothesis import given, strategies as st

@given(
    name=st.text(min_size=1, max_size=50),
    size=st.sampled_from(["t2.micro", "t2.small", "t3.medium"])
)
@pytest.mark.asyncio
async def test_resource_handles_various_inputs(instance_resource, name, size):
    """Test resource with property-based testing."""
    ctx = make_context(
        config=Instance.Config(
            name=name,
            size=size,
            ami="ami-12345678",
        )
    )
    state, _ = await instance_resource._create_apply(ctx)

    assert state is not None
    assert state.status == "running"
```

## Integration Tests

### Testing Provider Configuration

```python
import pytest

@pytest.mark.asyncio
@pytest.mark.integration
async def test_provider_configuration():
    """Test provider configuration flow."""
    provider = MyCloudProvider()

    config = MyCloudProvider.Config(
        api_key="test-key",
        region="us-east-1"
    )

    await provider.configure(config)

    # Verify provider is configured
    assert provider.configured is True
```

### Testing Complete Workflows

```python
@pytest.mark.asyncio
@pytest.mark.integration
async def test_complete_resource_lifecycle(configured_provider):
    """Test complete resource lifecycle integration."""
    instance = Instance()

    # Create
    create_ctx = ResourceContext(
        config=Instance.Config(
            name="integration-test",
            size="t2.micro",
            ami="ami-12345678"
        )
    )
    created, _ = await instance._create_apply(create_ctx)
    assert created and created.id is not None

    # Read
    read = await instance.read(ResourceContext(state=created))
    assert read is not None
    assert read.id == created.id

    # Update
    update_ctx = ResourceContext(
        config=Instance.Config(
            name="integration-test",
            size="t3.small",
            ami="ami-12345678"
        ),
        state=created,
        planned_state=created,
    )
    updated, _ = await instance._update_apply(update_ctx)
    assert updated.id == created.id

    # Delete
    await instance._delete_apply(ResourceContext(state=updated))

    # Verify deleted
    deleted = await instance.read(ResourceContext(state=updated))
    assert deleted is None
```

## Test Organization

### Recommended Structure

```
tests/
├── conftest.py                 # Shared fixtures
├── unit/
│   ├── test_provider.py
│   ├── test_resources.py
│   ├── test_data_sources.py
│   └── test_functions.py
├── integration/
│   ├── test_provider_integration.py
│   └── test_resource_lifecycle.py
└── fixtures/
    ├── sample_configs.py
    └── mock_responses.py
```

### conftest.py Example

```python
import pytest
from my_provider import MyCloudProvider

@pytest.fixture(scope="session")
def provider_metadata():
    """Provider metadata for tests."""
    return {
        "name": "mycloud",
        "version": "1.0.0"
    }

@pytest.fixture
def provider():
    """Create a provider instance."""
    return MyCloudProvider()

@pytest.fixture
async def configured_provider(provider):
    """Create a configured provider."""
    config = MyCloudProvider.Config(
        api_key="test-key",
        region="us-east-1"
    )
    await provider.configure(config)
    return provider

def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
```

## Running Tests

### Basic Test Execution

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/unit/test_resources.py

# Run specific test
uv run pytest tests/unit/test_resources.py::test_resource_create

# Run with coverage
uv run pytest --cov=my_provider

# Run integration tests only
uv run pytest -m integration

# Run tests in parallel
uv run pytest -n auto
```

### Test Configuration (pytest.ini)

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
asyncio_mode = auto
markers =
    integration: Integration tests
    slow: Slow running tests
    unit: Unit tests
```

## Best Practices

1. **Use async tests**: Always mark async tests with `@pytest.mark.asyncio`
2. **Mock external dependencies**: Use mocks for API calls in unit tests
3. **Test error cases**: Don't just test happy paths
4. **Use fixtures**: Create reusable fixtures in `conftest.py`
5. **Organize tests**: Separate unit and integration tests
6. **Test validation**: Verify configuration validation works
7. **Property-based testing**: Use Hypothesis for comprehensive coverage
8. **Coverage**: Aim for >80% code coverage

## See Also

- [Creating Providers](../building-components/creating-providers.md) - Provider development guide
- [Creating Resources](../building-components/creating-resources.md) - Resource implementation
- [Best Practices](../production/best-practices.md) - Production best practices
