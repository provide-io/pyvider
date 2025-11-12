"""
Demo Provider for Pyvider

This is a complete example provider demonstrating all major features:
- Provider configuration
- Resource management (CRUD operations)
- Data sources (read-only queries)
- Provider functions
- State management with private state
"""

from pyvider.providers import BaseProvider, ProviderMetadata, register_provider
from pyvider.resources import BaseResource, ResourceContext, register_resource
from pyvider.data_sources import register_data_source
from pyvider.data_sources.base import BaseDataSource
from pyvider.functions import BaseFunction, FunctionParameter, FunctionReturnType, register_function
from pyvider.schema import (
    s_provider,
    s_resource,
    s_data_source,
    s_function,
    a_str,
    a_num,
    a_bool,
    a_list,
    a_map,
    PvsStringKind,
)
from pyvider.cty import CtyString, CtyNumber, CtyBool, CtyList
from attrs import define, field
from typing import Any
import json
import time


# ============================================================================
# Provider Definition
# ============================================================================

@register_provider("demo")
class DemoProvider(BaseProvider):
    """
    Demo infrastructure provider showcasing Pyvider capabilities.

    This provider simulates managing servers and demonstrates:
    - Configuration management
    - Resource lifecycle
    - Data source queries
    - Custom functions
    """

    def __init__(self) -> None:
        super().__init__(
            metadata=ProviderMetadata(
                name="demo",
                version="1.0.0",
                protocol_version="6",
            )
        )

    @classmethod
    def get_schema(cls):
        """Define provider configuration schema"""
        return s_provider({
            "api_url": a_str(
                required=False,
                description="API endpoint URL for the demo service",
            ),
            "api_token": a_str(
                required=False,
                sensitive=True,
                description="API authentication token",
            ),
            "timeout": a_num(
                required=False,
                description="Request timeout in seconds",
            ),
            "debug": a_bool(
                required=False,
                description="Enable debug logging",
            ),
        })


# ============================================================================
# Resource: demo_server
# ============================================================================

@register_resource("server")
class DemoServer(BaseResource):
    """
    Manages a virtual server resource.

    This resource demonstrates:
    - Required and optional attributes
    - Computed attributes
    - Sensitive data handling
    - Private state management
    - Full CRUD lifecycle
    """

    # In-memory storage simulating a backend API
    _servers = {}
    _next_id = 1

    @define
    class Config:
        """Resource configuration (user input)"""
        name: str
        instance_type: str = "t2.micro"
        region: str = "us-east-1"
        tags: dict[str, str] = field(factory=dict)
        enable_monitoring: bool = False

    @define
    class State:
        """Resource state (computed values)"""
        id: str
        name: str
        instance_type: str
        region: str
        tags: dict[str, str]
        enable_monitoring: bool
        # Computed attributes
        public_ip: str
        private_ip: str
        status: str
        created_at: str

    @classmethod
    def get_schema(cls):
        """Define resource schema"""
        return s_resource({
            # Required attributes
            "id": a_str(computed=True, description="Unique server identifier"),
            "name": a_str(required=True, description="Server name"),

            # Optional attributes with defaults
            "instance_type": a_str(
                optional=True,
                description="Instance type (t2.micro, t2.small, t2.medium)",
            ),
            "region": a_str(
                optional=True,
                description="AWS region",
            ),
            "tags": a_map(a_str(), optional=True, description="Resource tags"),
            "enable_monitoring": a_bool(
                optional=True,
                description="Enable CloudWatch monitoring",
            ),

            # Computed attributes
            "public_ip": a_str(computed=True, description="Public IP address"),
            "private_ip": a_str(computed=True, description="Private IP address"),
            "status": a_str(computed=True, description="Server status"),
            "created_at": a_str(computed=True, description="Creation timestamp"),
        })

    async def _create_apply(self, ctx: ResourceContext) -> tuple[Any, Any]:
        """Create a new server"""
        # Generate server ID
        server_id = f"srv-{self._next_id:06d}"
        self._next_id += 1

        # Simulate server creation
        server_data = {
            "id": server_id,
            "name": ctx.config.name,
            "instance_type": ctx.config.instance_type,
            "region": ctx.config.region,
            "tags": ctx.config.tags,
            "enable_monitoring": ctx.config.enable_monitoring,
            "public_ip": f"54.{self._next_id % 256}.{self._next_id % 256}.{self._next_id % 256}",
            "private_ip": f"10.0.{self._next_id % 256}.{self._next_id % 256}",
            "status": "running",
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }

        # Store in "backend"
        self._servers[server_id] = server_data

        # Return state
        state = self.State(**server_data)
        return state, None

    async def read(self, ctx: ResourceContext) -> Any:
        """Read current server state"""
        server_id = ctx.state.id

        # Check if server exists
        if server_id not in self._servers:
            return None  # Server doesn't exist (deleted outside Terraform)

        # Return current state
        server_data = self._servers[server_id]
        return self.State(**server_data)

    async def _update_apply(self, ctx: ResourceContext) -> tuple[Any, Any]:
        """Update server configuration"""
        server_id = ctx.state.id

        # Update server data
        server_data = self._servers[server_id]
        server_data.update({
            "name": ctx.config.name,
            "instance_type": ctx.config.instance_type,
            "region": ctx.config.region,
            "tags": ctx.config.tags,
            "enable_monitoring": ctx.config.enable_monitoring,
        })

        # Return updated state
        state = self.State(**server_data)
        return state, None

    async def delete(self, ctx: ResourceContext) -> None:
        """Delete server"""
        server_id = ctx.state.id

        # Remove from "backend"
        if server_id in self._servers:
            del self._servers[server_id]


# ============================================================================
# Data Source: demo_server_info
# ============================================================================

@register_data_source("server_info")
class DemoServerInfo(BaseDataSource):
    """
    Query information about existing servers.

    This data source demonstrates:
    - Read-only operations
    - Query by attributes
    - Computed values
    """

    @define
    class Config:
        """Data source configuration (query parameters)"""
        server_id: str

    @define
    class State:
        """Data source state (query results)"""
        id: str
        name: str
        instance_type: str
        region: str
        status: str
        public_ip: str
        private_ip: str
        uptime_seconds: int  # Computed

    @classmethod
    def get_schema(cls):
        """Define data source schema"""
        return s_data_source({
            # Query parameters
            "server_id": a_str(required=True, description="Server ID to query"),

            # Results
            "id": a_str(computed=True, description="Server ID"),
            "name": a_str(computed=True, description="Server name"),
            "instance_type": a_str(computed=True, description="Instance type"),
            "region": a_str(computed=True, description="Region"),
            "status": a_str(computed=True, description="Server status"),
            "public_ip": a_str(computed=True, description="Public IP"),
            "private_ip": a_str(computed=True, description="Private IP"),
            "uptime_seconds": a_num(computed=True, description="Server uptime in seconds"),
        })

    async def read(self, ctx) -> Any:
        """Read server information"""
        server_id = ctx.config.server_id

        # Look up server
        if server_id not in DemoServer._servers:
            raise ValueError(f"Server {server_id} not found")

        server_data = DemoServer._servers[server_id]

        # Calculate uptime (simulated)
        created_time = time.mktime(time.strptime(server_data["created_at"], "%Y-%m-%dT%H:%M:%SZ"))
        uptime = int(time.time() - created_time)

        # Return state
        return self.State(
            id=server_data["id"],
            name=server_data["name"],
            instance_type=server_data["instance_type"],
            region=server_data["region"],
            status=server_data["status"],
            public_ip=server_data["public_ip"],
            private_ip=server_data["private_ip"],
            uptime_seconds=uptime,
        )


# ============================================================================
# Function: demo_format_tags
# ============================================================================

@register_function("format_tags")
class FormatTagsFunction(BaseFunction):
    """
    Format a map of tags into a JSON string.

    This function demonstrates:
    - Custom Terraform functions
    - Type-safe parameters
    - String manipulation
    """

    @classmethod
    def get_schema(cls):
        """Define function schema"""
        return s_function(
            description="Format tags as JSON string",
            parameters=[
                FunctionParameter(
                    name="tags",
                    description="Tag map to format",
                    type=CtyMap(CtyString()),
                ),
                FunctionParameter(
                    name="pretty",
                    description="Pretty print the JSON",
                    type=CtyBool(),
                ),
            ],
            return_type=FunctionReturnType(
                type=CtyString(),
            ),
        )

    async def call(self, tags: dict[str, str], pretty: bool = False) -> str:
        """Execute the function"""
        if pretty:
            return json.dumps(tags, indent=2, sort_keys=True)
        return json.dumps(tags, sort_keys=True)


# ============================================================================
# Function: demo_calculate_cost
# ============================================================================

@register_function("calculate_cost")
class CalculateCostFunction(BaseFunction):
    """
    Calculate estimated monthly cost for a server.

    Demonstrates numeric calculations and multiple parameters.
    """

    @classmethod
    def get_schema(cls):
        """Define function schema"""
        return s_function(
            description="Calculate estimated monthly cost",
            parameters=[
                FunctionParameter(
                    name="instance_type",
                    description="Instance type",
                    type=CtyString(),
                ),
                FunctionParameter(
                    name="hours_per_month",
                    description="Expected hours per month",
                    type=CtyNumber(),
                ),
            ],
            return_type=FunctionReturnType(
                type=CtyNumber(),
            ),
        )

    async def call(self, instance_type: str, hours_per_month: float) -> float:
        """Calculate cost"""
        # Simplified pricing ($/hour)
        pricing = {
            "t2.micro": 0.0116,
            "t2.small": 0.023,
            "t2.medium": 0.0464,
        }

        hourly_rate = pricing.get(instance_type, 0.05)
        return hourly_rate * hours_per_month


# Note: CtyMap import needed for format_tags function
from pyvider.cty import CtyMap
