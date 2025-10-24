# 🏗️ Creating Providers

This comprehensive guide walks you through creating production-ready Terraform providers using Pyvider. We'll cover everything from basic setup to advanced features.

## 📋 Prerequisites

Before creating a provider, ensure you understand:
- Basic Terraform concepts (providers, resources, state)
- Python async/await programming
- attrs for class definitions
- Type hints in Python

## 🎯 Provider Anatomy

A complete provider consists of several components:

```
my_provider/
├── __init__.py           # Package initialization
├── provider.py           # Provider definition
├── resources/           # Resource implementations
│   ├── __init__.py
│   ├── server.py
│   └── network.py
├── data_sources/        # Data source implementations
│   ├── __init__.py
│   └── images.py
├── functions/           # Provider functions
│   ├── __init__.py
│   └── validators.py
└── tests/              # Test suite
    ├── __init__.py
    └── test_provider.py
```

## 🚀 Step-by-Step Provider Creation

### Step 1: Define the Provider Class

```python
# provider.py
from pyvider.providers import register_provider, BaseProvider, ProviderMetadata
from pyvider.schema import Attribute
import attrs
import httpx

@register_provider("mycloud")
class MyCloudProvider(BaseProvider):
    """
    MyCloud Infrastructure Provider
    
    This provider manages resources in the MyCloud platform.
    """
    
    def __init__(self):
        """Initialize provider with metadata."""
        super().__init__(
            metadata=ProviderMetadata(
                name="mycloud",
                version="1.0.0",
                protocol_version="6"
            )
        )
        self.client = None
    
    @attrs.define
    class Config:
        """Provider configuration schema."""
        
        # Required authentication
        api_key: str = Attribute(
            required=True,
            sensitive=True,
            description="API key for MyCloud authentication"
        )
        
        # Optional configuration
        api_endpoint: str = Attribute(
            default="https://api.mycloud.com/v1",
            description="MyCloud API endpoint"
        )
        
        region: str = Attribute(
            default="us-east-1",
            description="Default region for resources",
            validators=[
                OneOf(["us-east-1", "us-west-2", "eu-central-1"])
            ]
        )
        
        timeout: int = Attribute(
            default=30,
            description="API request timeout in seconds",
            validators=[Range(min=5, max=300)]
        )
        
        max_retries: int = Attribute(
            default=3,
            description="Maximum API retry attempts",
            validators=[Range(min=0, max=10)]
        )
    
    async def configure(self, config: Config) -> None:
        """
        Configure the provider with validated configuration.
        
        This method is called once after provider initialization
        with the configuration from Terraform.
        """
        # Create HTTP client with configuration
        self.client = httpx.AsyncClient(
            base_url=config.api_endpoint,
            headers={
                "Authorization": f"Bearer {config.api_key}",
                "X-Region": config.region,
                "User-Agent": f"terraform-provider-mycloud/{self.metadata.version}"
            },
            timeout=config.timeout,
            follow_redirects=True
        )
        
        # Store configuration for resource access
        self.config = config
        
        # Validate authentication
        try:
            response = await self.client.get("/auth/validate")
            response.raise_for_status()
        except httpx.HTTPError as e:
            raise ProviderError(f"Authentication failed: {e}")
        
        logger.info("MyCloud provider configured successfully", region=config.region)
    
    async def close(self) -> None:
        """Clean up provider resources."""
        if self.client:
            await self.client.aclose()
```

### Step 2: Implement Resources

```python
# resources/server.py
from pyvider.resources import register_resource, BaseResource
from pyvider.schema import Attribute
from pyvider.exceptions import ResourceError
import attrs
from datetime import datetime

@register_resource("server")
class Server(BaseResource):
    """
    Manages MyCloud server instances.
    
    Example:
        resource "mycloud_server" "web" {
          name = "web-server-01"
          type = "t3.medium"
          image = "ubuntu-22.04"
          
          network {
            vpc_id = mycloud_vpc.main.id
            subnet_id = mycloud_subnet.public.id
          }
          
          tags = {
            Environment = "production"
            Team = "platform"
          }
        }
    """
    
    @attrs.define
    class Config:
        """Server configuration."""
        
        # Required attributes
        name: str = Attribute(
            required=True,
            description="Server name",
            validators=[
                Length(min=1, max=63),
                Regex(r"^[a-z0-9-]+$")
            ]
        )
        
        type: str = Attribute(
            required=True,
            description="Instance type",
            validators=[
                OneOf(["t3.micro", "t3.small", "t3.medium", "t3.large"])
            ]
        )
        
        image: str = Attribute(
            required=True,
            description="Operating system image"
        )
        
        # Optional attributes
        ssh_key: str = Attribute(
            description="SSH public key for access"
        )
        
        user_data: str = Attribute(
            description="Cloud-init user data script"
        )
        
        # Nested block for network configuration
        network: NetworkConfig = Attribute(
            required=True,
            description="Network configuration"
        )
        
        # Complex types
        tags: dict[str, str] = Attribute(
            default_factory=dict,
            description="Resource tags"
        )
        
        security_groups: list[str] = Attribute(
            default_factory=list,
            description="Security group IDs"
        )
    
    @attrs.define
    class NetworkConfig:
        """Nested network configuration."""
        vpc_id: str = Attribute(required=True)
        subnet_id: str = Attribute(required=True)
        assign_public_ip: bool = Attribute(default=True)
    
    @attrs.define
    class State:
        """Server state."""
        
        # Identifiers
        id: str = Attribute(
            computed=True,
            description="Server ID"
        )
        
        # Configuration echo
        name: str = Attribute()
        type: str = Attribute()
        image: str = Attribute()
        network: NetworkConfig = Attribute()
        tags: dict[str, str] = Attribute()
        security_groups: list[str] = Attribute()
        
        # Computed attributes
        public_ip: str = Attribute(
            computed=True,
            description="Public IP address"
        )
        
        private_ip: str = Attribute(
            computed=True,
            description="Private IP address"
        )
        
        status: str = Attribute(
            computed=True,
            description="Server status"
        )
        
        created_at: str = Attribute(
            computed=True,
            description="Creation timestamp"
        )
    
    async def create(self, config: Config) -> State:
        """Create a new server."""
        logger.info("Creating server", name=config.name, type=config.type)
        
        # Prepare API request
        request_data = {
            "name": config.name,
            "type": config.type,
            "image": config.image,
            "vpc_id": config.network.vpc_id,
            "subnet_id": config.network.subnet_id,
            "assign_public_ip": config.network.assign_public_ip,
            "tags": config.tags,
            "security_groups": config.security_groups
        }
        
        if config.ssh_key:
            request_data["ssh_key"] = config.ssh_key
        
        if config.user_data:
            request_data["user_data"] = config.user_data
        
        try:
            # Create server via API
            response = await self.provider.client.post(
                "/servers",
                json=request_data
            )
            response.raise_for_status()
            server_data = response.json()
            
            # Wait for server to be ready
            server_id = server_data["id"]
            server = await self._wait_for_status(server_id, "running")
            
            # Return state
            return State(
                id=server["id"],
                name=server["name"],
                type=server["type"],
                image=server["image"],
                network=config.network,
                tags=server.get("tags", {}),
                security_groups=server.get("security_groups", []),
                public_ip=server.get("public_ip", ""),
                private_ip=server["private_ip"],
                status=server["status"],
                created_at=server["created_at"]
            )
            
        except httpx.HTTPError as e:
            raise ResourceError(f"Failed to create server: {e}")
    
    async def read(self, state: State) -> State | None:
        """Read current server state."""
        try:
            response = await self.provider.client.get(f"/servers/{state.id}")
            
            if response.status_code == 404:
                return None  # Server no longer exists
            
            response.raise_for_status()
            server = response.json()
            
            # Update state with current values
            return State(
                id=server["id"],
                name=server["name"],
                type=server["type"],
                image=server["image"],
                network=state.network,  # Preserve network config
                tags=server.get("tags", {}),
                security_groups=server.get("security_groups", []),
                public_ip=server.get("public_ip", ""),
                private_ip=server["private_ip"],
                status=server["status"],
                created_at=server["created_at"]
            )
            
        except httpx.HTTPError as e:
            raise ResourceError(f"Failed to read server: {e}")
    
    async def update(self, config: Config, state: State) -> State:
        """Update server configuration."""
        updates = {}
        
        # Check what needs updating
        if config.tags != state.tags:
            updates["tags"] = config.tags
        
        if config.security_groups != state.security_groups:
            updates["security_groups"] = config.security_groups
        
        if config.type != state.type:
            # Instance type change requires stop/modify/start
            await self._resize_instance(state.id, config.type)
        
        if updates:
            try:
                response = await self.provider.client.patch(
                    f"/servers/{state.id}",
                    json=updates
                )
                response.raise_for_status()
            except httpx.HTTPError as e:
                raise ResourceError(f"Failed to update server: {e}")
        
        # Read and return current state
        return await self.read(state)
    
    async def delete(self, state: State) -> None:
        """Delete the server."""
        try:
            response = await self.provider.client.delete(f"/servers/{state.id}")
            
            if response.status_code == 404:
                return  # Already deleted
            
            response.raise_for_status()
            
            # Wait for deletion to complete
            await self._wait_for_deletion(state.id)
            
        except httpx.HTTPError as e:
            raise ResourceError(f"Failed to delete server: {e}")
    
    async def import_resource(self, resource_id: str) -> State:
        """Import existing server into Terraform state."""
        try:
            response = await self.provider.client.get(f"/servers/{resource_id}")
            response.raise_for_status()
            server = response.json()
            
            # Reconstruct state from API data
            return State(
                id=server["id"],
                name=server["name"],
                type=server["type"],
                image=server["image"],
                network=NetworkConfig(
                    vpc_id=server["vpc_id"],
                    subnet_id=server["subnet_id"],
                    assign_public_ip=bool(server.get("public_ip"))
                ),
                tags=server.get("tags", {}),
                security_groups=server.get("security_groups", []),
                public_ip=server.get("public_ip", ""),
                private_ip=server["private_ip"],
                status=server["status"],
                created_at=server["created_at"]
            )
            
        except httpx.HTTPError as e:
            raise ResourceError(f"Failed to import server {resource_id}: {e}")
    
    # Helper methods
    async def _wait_for_status(self, server_id: str, target_status: str, timeout: int = 300):
        """Wait for server to reach target status."""
        start_time = datetime.now()
        
        while (datetime.now() - start_time).total_seconds() < timeout:
            response = await self.provider.client.get(f"/servers/{server_id}")
            response.raise_for_status()
            server = response.json()
            
            if server["status"] == target_status:
                return server
            
            if server["status"] == "error":
                raise ResourceError(f"Server entered error state: {server.get('error_message')}")
            
            await asyncio.sleep(5)
        
        raise ResourceError(f"Timeout waiting for server to reach {target_status} status")
    
    async def _wait_for_deletion(self, server_id: str, timeout: int = 120):
        """Wait for server deletion to complete."""
        start_time = datetime.now()
        
        while (datetime.now() - start_time).total_seconds() < timeout:
            response = await self.provider.client.get(f"/servers/{server_id}")
            
            if response.status_code == 404:
                return  # Successfully deleted
            
            await asyncio.sleep(5)
        
        raise ResourceError("Timeout waiting for server deletion")
    
    async def _resize_instance(self, server_id: str, new_type: str):
        """Resize instance type."""
        # Stop instance
        await self.provider.client.post(f"/servers/{server_id}/stop")
        await self._wait_for_status(server_id, "stopped")
        
        # Change type
        response = await self.provider.client.patch(
            f"/servers/{server_id}",
            json={"type": new_type}
        )
        response.raise_for_status()
        
        # Start instance
        await self.provider.client.post(f"/servers/{server_id}/start")
        await self._wait_for_status(server_id, "running")
```

### Step 3: Add Data Sources

```python
# data_sources/images.py
from pyvider.data_sources import register_data_source, BaseDataSource
from pyvider.schema import Attribute
import attrs

@register_data_source("images")
class Images(BaseDataSource):
    """
    Data source for available server images.
    
    Example:
        data "mycloud_images" "ubuntu" {
          filter = "ubuntu-*"
          architecture = "x86_64"
          most_recent = true
        }
    """
    
    @attrs.define
    class Config:
        """Query configuration."""
        filter: str = Attribute(
            default="*",
            description="Name filter pattern"
        )
        
        architecture: str = Attribute(
            default="x86_64",
            description="CPU architecture",
            validators=[OneOf(["x86_64", "arm64"])]
        )
        
        most_recent: bool = Attribute(
            default=False,
            description="Return only the most recent image"
        )
    
    @attrs.define
    class State:
        """Query results."""
        images: list[dict] = Attribute(
            computed=True,
            description="List of matching images"
        )
        
        total: int = Attribute(
            computed=True,
            description="Total number of matching images"
        )
    
    async def read(self, config: Config) -> State:
        """Fetch image data."""
        params = {
            "filter": config.filter,
            "architecture": config.architecture
        }
        
        response = await self.provider.client.get("/images", params=params)
        response.raise_for_status()
        
        images = response.json()["images"]
        
        if config.most_recent and images:
            # Sort by creation date and take the most recent
            images = sorted(
                images,
                key=lambda x: x["created_at"],
                reverse=True
            )[:1]
        
        return State(
            images=[
                {
                    "id": img["id"],
                    "name": img["name"],
                    "version": img["version"],
                    "architecture": img["architecture"],
                    "created_at": img["created_at"]
                }
                for img in images
            ],
            total=len(images)
        )
```

## 🧪 Testing Your Provider

```python
# tests/test_provider.py
import pytest
from pyvider.testing import ProviderTestCase
import httpx
from unittest.mock import AsyncMock, patch

class TestMyCloudProvider(ProviderTestCase):
    """Test suite for MyCloud provider."""
    
    @pytest.fixture
    async def configured_provider(self):
        """Provide a configured provider instance."""
        from my_provider.provider import MyCloudProvider
        
        provider = MyCloudProvider()
        
        # Mock HTTP client
        with patch.object(provider, 'client', new=AsyncMock(spec=httpx.AsyncClient)):
            # Mock auth validation
            provider.client.get.return_value.raise_for_status = AsyncMock()
            
            await provider.configure(
                MyCloudProvider.Config(
                    api_key="test-key",
                    region="us-east-1"
                )
            )
            
            yield provider
    
    async def test_provider_configuration(self, configured_provider):
        """Test provider configures correctly."""
        assert configured_provider.config.api_key == "test-key"
        assert configured_provider.config.region == "us-east-1"
        assert configured_provider.client is not None
    
    async def test_server_create(self, configured_provider):
        """Test server resource creation."""
        from my_provider.resources.server import Server
        
        server = Server()
        server.provider = configured_provider
        
        # Mock API responses
        configured_provider.client.post.return_value.json.return_value = {
            "id": "srv-123",
            "status": "pending"
        }
        
        configured_provider.client.get.return_value.json.return_value = {
            "id": "srv-123",
            "name": "test-server",
            "type": "t3.medium",
            "image": "ubuntu-22.04",
            "status": "running",
            "private_ip": "10.0.1.5",
            "public_ip": "203.0.113.42",
            "created_at": "2024-01-15T10:00:00Z"
        }
        
        # Create server
        config = Server.Config(
            name="test-server",
            type="t3.medium",
            image="ubuntu-22.04",
            network=Server.NetworkConfig(
                vpc_id="vpc-123",
                subnet_id="subnet-456"
            )
        )
        
        state = await server.create(config)
        
        # Verify state
        assert state.id == "srv-123"
        assert state.status == "running"
        assert state.public_ip == "203.0.113.42"
```

## 🎨 Best Practices

### 1. Provider Design

- **Single Responsibility**: Provider handles authentication and configuration only
- **Shared Client**: Create reusable API client for all resources
- **Configuration Validation**: Validate all inputs in the schema
- **Graceful Degradation**: Handle API failures gracefully

### 2. Resource Implementation

- **Idempotency**: All operations must be idempotent
- **Drift Detection**: Implement proper `read()` to detect changes
- **Partial Updates**: Only update changed attributes
- **Error Context**: Provide detailed error messages

### 3. State Management

- **Minimal State**: Store only essential information
- **Computed Attributes**: Mark generated values as computed
- **Sensitive Data**: Use private state for secrets
- **Import Support**: Always implement import functionality

### 4. Performance

- **Async Operations**: Use async/await for all I/O
- **Connection Pooling**: Reuse HTTP connections
- **Retries**: Implement exponential backoff
- **Timeouts**: Set reasonable timeouts

## 🔐 Security Considerations

### Handling Sensitive Data

```python
@attrs.define
class Config:
    # Mark sensitive attributes
    api_key: str = Attribute(
        required=True,
        sensitive=True  # Won't be logged
    )
    
    # Use private state for runtime secrets
    _session_token: str = field(default=None, init=False)
```

### Input Validation

```python
@attrs.define
class Config:
    email: str = Attribute(
        required=True,
        validators=[
            Email(),  # Validate email format
            NoSQLInjection(),  # Prevent injection
        ]
    )
```

## 📚 Advanced Features

### Custom Validators

```python
def validate_cidr(value: str) -> None:
    """Validate CIDR notation."""
    import ipaddress
    try:
        ipaddress.ip_network(value)
    except ValueError as e:
        raise ValueError(f"Invalid CIDR: {e}")

@attrs.define
class Config:
    cidr_block: str = Attribute(
        required=True,
        validators=[validate_cidr]
    )
```

### Dynamic Schema

```python
@register_resource("dynamic_table")
class DynamicTable(BaseResource):
    @classmethod
    def get_schema(cls) -> PvsSchema:
        """Generate schema dynamically."""
        # Load schema from external source
        schema_def = load_schema_from_api()
        return build_schema(schema_def)
```

### Provider Capabilities

```python
@register_provider("advanced")
class AdvancedProvider(BaseProvider):
    def __init__(self):
        super().__init__(
            metadata=ProviderMetadata(
                name="advanced",
                version="1.0.0",
                capabilities=ProviderCapabilities(
                    plan_destroy=True,
                    move_resource_state=True,
                    get_provider_schema_optional=False
                )
            )
        )
```

## 🚀 Next Steps

- [Creating Resources](creating-resources.md) - Deep dive into resources
- [Creating Data Sources](creating-data-sources.md) - Implementing data sources
- [Testing Providers](testing-providers.md) - Comprehensive testing
- [Debugging](debugging.md) - Troubleshooting providers

---

<p align="center">
  Ready to build? Check out <a href="https://github.com/provide-io/pyvider-components/tree/main/examples">100+ Working Examples →</a>
</p>