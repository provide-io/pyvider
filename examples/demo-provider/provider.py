"""
Demo Provider for Pyvider

This is a complete example provider demonstrating all major features:
- Provider configuration
- Resource management (CRUD operations)
- Data sources (read-only queries)
- Provider functions
- State management with private state
"""

import json
import time
from typing import Any

from attrs import define, field

from pyvider.cty import CtyBool, CtyNumber, CtyString
from pyvider.data_sources import register_data_source
from pyvider.data_sources.base import BaseDataSource
from pyvider.functions import BaseFunction, FunctionParameter, FunctionReturnType, register_function
from pyvider.providers import BaseProvider, ProviderMetadata, register_provider
from pyvider.resources import BaseResource, ResourceContext, register_resource
from pyvider.schema import (
    a_bool,
    a_list,
    a_map,
    a_num,
    a_str,
    s_data_source,
    s_function,
    s_provider,
    s_resource,
)

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
        return s_provider(
            {
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
            }
        )


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
        return s_resource(
            {
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
            }
        )

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
        server_data.update(
            {
                "name": ctx.config.name,
                "instance_type": ctx.config.instance_type,
                "region": ctx.config.region,
                "tags": ctx.config.tags,
                "enable_monitoring": ctx.config.enable_monitoring,
            }
        )

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
        return s_data_source(
            {
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
            }
        )

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
            parameters=[
                a_map(a_str(), description="Tag map to format"),
                a_bool(description="Pretty print the JSON"),
            ],
            return_type=a_str(description="Formatted JSON string"),
        )

    def get_parameters(self) -> list[FunctionParameter]:
        return [
            FunctionParameter(name="tags", type=CtyMap(CtyString()), description="Tag map to format"),
            FunctionParameter(name="pretty", type=CtyBool(), description="Pretty print the JSON"),
        ]

    def get_return_type(self) -> FunctionReturnType:
        return FunctionReturnType(type=CtyString())

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
            parameters=[
                a_str(description="Instance type"),
                a_num(description="Expected hours per month"),
            ],
            return_type=a_num(description="Estimated monthly cost"),
        )

    def get_parameters(self) -> list[FunctionParameter]:
        return [
            FunctionParameter(name="instance_type", type=CtyString(), description="Instance type"),
            FunctionParameter(
                name="hours_per_month", type=CtyNumber(), description="Expected hours per month"
            ),
        ]

    def get_return_type(self) -> FunctionReturnType:
        return FunctionReturnType(type=CtyNumber())

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


# ============================================================================
# Resource: demo_database
# ============================================================================


@register_resource("database")
class DemoDatabase(BaseResource):
    """
    Manages a database instance.

    This resource demonstrates:
    - Database-specific attributes
    - Storage configuration
    - Backup settings
    - Connection endpoint management
    """

    # In-memory storage
    _databases = {}
    _next_db_id = 1

    @define
    class Config:
        """Database configuration"""

        name: str
        engine: str = "postgresql"
        engine_version: str = "14.0"
        storage_gb: int = 20
        instance_class: str = "db.t3.micro"
        backup_retention_days: int = 7
        multi_az: bool = False
        tags: dict[str, str] = field(factory=dict)

    @define
    class State:
        """Database state"""

        id: str
        name: str
        engine: str
        engine_version: str
        storage_gb: int
        instance_class: str
        backup_retention_days: int
        multi_az: bool
        tags: dict[str, str]
        # Computed
        endpoint: str
        port: int
        status: str
        created_at: str

    @classmethod
    def get_schema(cls):
        """Define database schema"""
        return s_resource(
            {
                "id": a_str(computed=True, description="Database identifier"),
                "name": a_str(required=True, description="Database name"),
                "engine": a_str(optional=True, description="Database engine (postgresql, mysql, mariadb)"),
                "engine_version": a_str(optional=True, description="Engine version"),
                "storage_gb": a_num(optional=True, description="Storage size in GB"),
                "instance_class": a_str(optional=True, description="Instance class"),
                "backup_retention_days": a_num(optional=True, description="Backup retention in days"),
                "multi_az": a_bool(optional=True, description="Enable multi-AZ deployment"),
                "tags": a_map(a_str(), optional=True, description="Resource tags"),
                # Computed
                "endpoint": a_str(computed=True, description="Connection endpoint"),
                "port": a_num(computed=True, description="Connection port"),
                "status": a_str(computed=True, description="Database status"),
                "created_at": a_str(computed=True, description="Creation timestamp"),
            }
        )

    async def _create_apply(self, ctx: ResourceContext) -> tuple[Any, Any]:
        """Create a new database"""
        db_id = f"db-{self._next_db_id:06d}"
        self._next_db_id += 1

        # Determine port based on engine
        port_map = {"postgresql": 5432, "mysql": 3306, "mariadb": 3306}
        port = port_map.get(ctx.config.engine, 5432)

        db_data = {
            "id": db_id,
            "name": ctx.config.name,
            "engine": ctx.config.engine,
            "engine_version": ctx.config.engine_version,
            "storage_gb": ctx.config.storage_gb,
            "instance_class": ctx.config.instance_class,
            "backup_retention_days": ctx.config.backup_retention_days,
            "multi_az": ctx.config.multi_az,
            "tags": ctx.config.tags,
            "endpoint": f"{db_id}.demo-rds.amazonaws.com",
            "port": port,
            "status": "available",
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }

        self._databases[db_id] = db_data
        state = self.State(**db_data)
        return state, None

    async def read(self, ctx: ResourceContext) -> Any:
        """Read database state"""
        db_id = ctx.state.id
        if db_id not in self._databases:
            return None
        db_data = self._databases[db_id]
        return self.State(**db_data)

    async def _update_apply(self, ctx: ResourceContext) -> tuple[Any, Any]:
        """Update database configuration"""
        db_id = ctx.state.id
        db_data = self._databases[db_id]

        # Update mutable fields
        db_data.update(
            {
                "storage_gb": ctx.config.storage_gb,
                "backup_retention_days": ctx.config.backup_retention_days,
                "multi_az": ctx.config.multi_az,
                "tags": ctx.config.tags,
            }
        )

        state = self.State(**db_data)
        return state, None

    async def delete(self, ctx: ResourceContext) -> None:
        """Delete database"""
        db_id = ctx.state.id
        if db_id in self._databases:
            del self._databases[db_id]


# ============================================================================
# Resource: demo_network
# ============================================================================


@register_resource("network")
class DemoNetwork(BaseResource):
    """
    Manages a virtual private network (VPC).

    This resource demonstrates:
    - Network configuration
    - CIDR block management
    - Subnet allocation
    - List attributes
    """

    # In-memory storage
    _networks = {}
    _next_net_id = 1

    @define
    class Config:
        """Network configuration"""

        name: str
        cidr_block: str
        enable_dns: bool = True
        enable_dns_hostnames: bool = True
        subnets: list[str] = field(factory=list)
        tags: dict[str, str] = field(factory=dict)

    @define
    class State:
        """Network state"""

        id: str
        name: str
        cidr_block: str
        enable_dns: bool
        enable_dns_hostnames: bool
        subnets: list[str]
        tags: dict[str, str]
        # Computed
        vpc_id: str
        default_route_table_id: str
        default_security_group_id: str
        status: str
        created_at: str

    @classmethod
    def get_schema(cls):
        """Define network schema"""
        return s_resource(
            {
                "id": a_str(computed=True, description="Network identifier"),
                "name": a_str(required=True, description="Network name"),
                "cidr_block": a_str(required=True, description="CIDR block (e.g., 10.0.0.0/16)"),
                "enable_dns": a_bool(optional=True, description="Enable DNS resolution"),
                "enable_dns_hostnames": a_bool(optional=True, description="Enable DNS hostnames"),
                "subnets": a_list(a_str(), optional=True, description="List of subnet CIDR blocks"),
                "tags": a_map(a_str(), optional=True, description="Resource tags"),
                # Computed
                "vpc_id": a_str(computed=True, description="VPC ID"),
                "default_route_table_id": a_str(computed=True, description="Default route table ID"),
                "default_security_group_id": a_str(computed=True, description="Default security group ID"),
                "status": a_str(computed=True, description="Network status"),
                "created_at": a_str(computed=True, description="Creation timestamp"),
            }
        )

    async def _create_apply(self, ctx: ResourceContext) -> tuple[Any, Any]:
        """Create a new network"""
        net_id = f"net-{self._next_net_id:06d}"
        self._next_net_id += 1

        net_data = {
            "id": net_id,
            "name": ctx.config.name,
            "cidr_block": ctx.config.cidr_block,
            "enable_dns": ctx.config.enable_dns,
            "enable_dns_hostnames": ctx.config.enable_dns_hostnames,
            "subnets": ctx.config.subnets,
            "tags": ctx.config.tags,
            "vpc_id": f"vpc-{self._next_net_id:08x}",
            "default_route_table_id": f"rtb-{self._next_net_id:08x}",
            "default_security_group_id": f"sg-{self._next_net_id:08x}",
            "status": "available",
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }

        self._networks[net_id] = net_data
        state = self.State(**net_data)
        return state, None

    async def read(self, ctx: ResourceContext) -> Any:
        """Read network state"""
        net_id = ctx.state.id
        if net_id not in self._networks:
            return None
        net_data = self._networks[net_id]
        return self.State(**net_data)

    async def _update_apply(self, ctx: ResourceContext) -> tuple[Any, Any]:
        """Update network configuration"""
        net_id = ctx.state.id
        net_data = self._networks[net_id]

        # Update mutable fields
        net_data.update(
            {
                "enable_dns": ctx.config.enable_dns,
                "enable_dns_hostnames": ctx.config.enable_dns_hostnames,
                "subnets": ctx.config.subnets,
                "tags": ctx.config.tags,
            }
        )

        state = self.State(**net_data)
        return state, None

    async def delete(self, ctx: ResourceContext) -> None:
        """Delete network"""
        net_id = ctx.state.id
        if net_id in self._networks:
            del self._networks[net_id]


# ============================================================================
# Data Source: demo_regions
# ============================================================================


@register_data_source("regions")
class DemoRegions(BaseDataSource):
    """
    Query available cloud regions.

    This data source demonstrates:
    - Listing data
    - Filter parameters
    - Complex return types
    """

    @define
    class Config:
        """Query configuration"""

        filter_prefix: str = ""

    @define
    class State:
        """Query results"""

        regions: list[str]
        count: int

    @classmethod
    def get_schema(cls):
        """Define data source schema"""
        return s_data_source(
            {
                "filter_prefix": a_str(optional=True, description="Filter regions by prefix"),
                # Results
                "regions": a_list(a_str(), computed=True, description="List of region codes"),
                "count": a_num(computed=True, description="Number of regions"),
            }
        )

    async def read(self, ctx) -> Any:
        """Read available regions"""
        all_regions = [
            "us-east-1",
            "us-east-2",
            "us-west-1",
            "us-west-2",
            "eu-west-1",
            "eu-west-2",
            "eu-central-1",
            "ap-southeast-1",
            "ap-southeast-2",
            "ap-northeast-1",
            "sa-east-1",
            "ca-central-1",
        ]

        # Filter if prefix provided
        filter_prefix = ctx.config.filter_prefix
        regions = [r for r in all_regions if r.startswith(filter_prefix)] if filter_prefix else all_regions

        return self.State(
            regions=regions,
            count=len(regions),
        )

    async def _validate_config(self, config) -> list[str]:
        """Validate configuration"""
        return []


# ============================================================================
# Data Source: demo_instance_types
# ============================================================================


@register_data_source("instance_types")
class DemoInstanceTypes(BaseDataSource):
    """
    Query available instance types and their specifications.

    This data source demonstrates:
    - Complex nested data structures
    - Computed pricing information
    - Filter capabilities
    """

    @define
    class Config:
        """Query configuration"""

        family: str = ""
        min_vcpus: int = 0

    @define
    class State:
        """Query results"""

        instance_types: dict[str, dict[str, Any]]
        count: int

    @classmethod
    def get_schema(cls):
        """Define data source schema"""
        return s_data_source(
            {
                "family": a_str(optional=True, description="Filter by instance family (t2, t3, m5, etc)"),
                "min_vcpus": a_num(optional=True, description="Minimum vCPUs required"),
                # Results
                "instance_types": a_map(
                    a_map(a_str()),  # map of maps
                    computed=True,
                    description="Instance type specifications",
                ),
                "count": a_num(computed=True, description="Number of instance types"),
            }
        )

    async def read(self, ctx) -> Any:
        """Read available instance types"""
        all_types = {
            "t2.micro": {"vcpus": "1", "memory_gb": "1", "price_per_hour": "0.0116"},
            "t2.small": {"vcpus": "1", "memory_gb": "2", "price_per_hour": "0.023"},
            "t2.medium": {"vcpus": "2", "memory_gb": "4", "price_per_hour": "0.0464"},
            "t3.micro": {"vcpus": "2", "memory_gb": "1", "price_per_hour": "0.0104"},
            "t3.small": {"vcpus": "2", "memory_gb": "2", "price_per_hour": "0.0208"},
            "t3.medium": {"vcpus": "2", "memory_gb": "4", "price_per_hour": "0.0416"},
            "m5.large": {"vcpus": "2", "memory_gb": "8", "price_per_hour": "0.096"},
            "m5.xlarge": {"vcpus": "4", "memory_gb": "16", "price_per_hour": "0.192"},
        }

        # Filter by family
        family = ctx.config.family
        filtered = {k: v for k, v in all_types.items() if k.startswith(family)} if family else all_types

        # Filter by min vCPUs
        min_vcpus = ctx.config.min_vcpus
        if min_vcpus > 0:
            filtered = {k: v for k, v in filtered.items() if int(v["vcpus"]) >= min_vcpus}

        return self.State(
            instance_types=filtered,
            count=len(filtered),
        )

    async def _validate_config(self, config) -> list[str]:
        """Validate configuration"""
        return []


# ============================================================================
# Function: demo_validate_cidr
# ============================================================================


@register_function("validate_cidr")
class ValidateCIDRFunction(BaseFunction):
    """
    Validate CIDR block notation.

    This function demonstrates:
    - Input validation
    - Boolean return type
    - Network calculations
    """

    @classmethod
    def get_schema(cls):
        """Define function schema"""
        return s_function(
            parameters=[
                a_str(description="CIDR block to validate (e.g., 10.0.0.0/16)"),
            ],
            return_type=a_bool(description="Whether CIDR is valid"),
        )

    def get_parameters(self) -> list[FunctionParameter]:
        return [
            FunctionParameter(name="cidr", type=CtyString(), description="CIDR block to validate"),
        ]

    def get_return_type(self) -> FunctionReturnType:
        return FunctionReturnType(type=CtyBool())

    async def call(self, cidr: str) -> bool:
        """Validate CIDR block"""
        try:
            # Split into IP and prefix
            if "/" not in cidr:
                return False

            ip_part, prefix_part = cidr.split("/")

            # Validate IP address parts
            octets = ip_part.split(".")
            if len(octets) != 4:
                return False

            for octet in octets:
                num = int(octet)
                if num < 0 or num > 255:
                    return False

            # Validate prefix length
            prefix = int(prefix_part)
            return not (prefix < 0 or prefix > 32)
        except (ValueError, AttributeError):
            return False


# ============================================================================
# Function: demo_generate_name
# ============================================================================


@register_function("generate_name")
class GenerateNameFunction(BaseFunction):
    """
    Generate a standardized resource name.

    This function demonstrates:
    - String formatting
    - Multiple parameters
    - Naming conventions
    """

    @classmethod
    def get_schema(cls):
        """Define function schema"""
        return s_function(
            parameters=[
                a_str(description="Name prefix (e.g., 'web', 'db', 'app')"),
                a_str(description="Environment (e.g., 'prod', 'staging', 'dev')"),
                a_str(description="Region code (e.g., 'us-east-1')"),
                a_num(description="Sequence number"),
            ],
            return_type=a_str(description="Standardized resource name"),
        )

    def get_parameters(self) -> list[FunctionParameter]:
        return [
            FunctionParameter(name="prefix", type=CtyString(), description="Name prefix"),
            FunctionParameter(name="environment", type=CtyString(), description="Environment"),
            FunctionParameter(name="region", type=CtyString(), description="Region code"),
            FunctionParameter(name="sequence", type=CtyNumber(), description="Sequence number"),
        ]

    def get_return_type(self) -> FunctionReturnType:
        return FunctionReturnType(type=CtyString())

    async def call(self, prefix: str, environment: str, region: str, sequence: float) -> str:
        """Generate standardized name"""
        # Extract region abbreviation (first letters of each part)
        region_parts = region.split("-")
        region_abbr = "".join([p[0] for p in region_parts])

        # Format: prefix-environment-region-sequence
        # Example: web-prod-use1-001
        return f"{prefix}-{environment}-{region_abbr}{region_parts[-1]}-{int(sequence):03d}"


# Note: CtyMap import needed for format_tags function
from pyvider.cty import CtyMap
