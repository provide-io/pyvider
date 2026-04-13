"""
Demo Provider - Resource Definitions

Contains:
- DemoServer: Virtual server management
- DemoDatabase: Database instance management
- DemoNetwork: Virtual private network management
"""

import time
from typing import Any, ClassVar

from attrs import define, field

from pyvider.resources import BaseResource, ResourceContext, register_resource
from pyvider.schema import PvsSchema, a_bool, a_list, a_map, a_num, a_str, s_resource


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
    _servers: ClassVar[dict[str, dict[str, Any]]] = {}
    _next_id: ClassVar[int] = 1

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
    def get_schema(cls) -> PvsSchema:
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
        DemoServer._next_id += 1

        # Simulate server creation
        server_data = {
            "id": server_id,
            "name": ctx.config.name,
            "instance_type": ctx.config.instance_type,
            "region": ctx.config.region,
            "tags": ctx.config.tags,
            "enable_monitoring": ctx.config.enable_monitoring,
            "public_ip": f"54.{DemoServer._next_id % 256}.{DemoServer._next_id % 256}.{DemoServer._next_id % 256}",
            "private_ip": f"10.0.{DemoServer._next_id % 256}.{DemoServer._next_id % 256}",
            "status": "running",
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }

        # Store in "backend"
        DemoServer._servers[server_id] = server_data

        # Return state
        state = self.State(**server_data)
        return state, None

    async def read(self, ctx: ResourceContext) -> Any:
        """Read current server state"""
        server_id = ctx.state.id

        # Check if server exists
        if server_id not in DemoServer._servers:
            return None  # Server doesn't exist (deleted outside Terraform)

        # Return current state
        server_data = DemoServer._servers[server_id]
        return self.State(**server_data)

    async def _update_apply(self, ctx: ResourceContext) -> tuple[Any, Any]:
        """Update server configuration"""
        server_id = ctx.state.id

        # Update server data
        server_data = DemoServer._servers[server_id]
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

    async def _validate_config(self, config: Any) -> list[str]:
        """Validate server configuration"""
        errors = []
        if config and config.name and len(config.name) > 255:
            errors.append("name must be 255 characters or less")
        return errors

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        """Delete server"""
        server_id = ctx.state.id

        # Remove from "backend"
        if server_id in DemoServer._servers:
            del DemoServer._servers[server_id]


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
    _databases: ClassVar[dict[str, dict[str, Any]]] = {}
    _next_db_id: ClassVar[int] = 1

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
    def get_schema(cls) -> PvsSchema:
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
        db_id = f"db-{DemoDatabase._next_db_id:06d}"
        DemoDatabase._next_db_id += 1

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

        DemoDatabase._databases[db_id] = db_data
        state = self.State(**db_data)
        return state, None

    async def read(self, ctx: ResourceContext) -> Any:
        """Read database state"""
        db_id = ctx.state.id
        if db_id not in DemoDatabase._databases:
            return None
        db_data = DemoDatabase._databases[db_id]
        return self.State(**db_data)

    async def _update_apply(self, ctx: ResourceContext) -> tuple[Any, Any]:
        """Update database configuration"""
        db_id = ctx.state.id
        db_data = DemoDatabase._databases[db_id]

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

    async def _validate_config(self, config: Any) -> list[str]:
        """Validate database configuration"""
        return []

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        """Delete database"""
        db_id = ctx.state.id
        if db_id in DemoDatabase._databases:
            del DemoDatabase._databases[db_id]


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
    _networks: ClassVar[dict[str, dict[str, Any]]] = {}
    _next_net_id: ClassVar[int] = 1

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
    def get_schema(cls) -> PvsSchema:
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
        net_id = f"net-{DemoNetwork._next_net_id:06d}"
        DemoNetwork._next_net_id += 1

        net_data = {
            "id": net_id,
            "name": ctx.config.name,
            "cidr_block": ctx.config.cidr_block,
            "enable_dns": ctx.config.enable_dns,
            "enable_dns_hostnames": ctx.config.enable_dns_hostnames,
            "subnets": ctx.config.subnets,
            "tags": ctx.config.tags,
            "vpc_id": f"vpc-{DemoNetwork._next_net_id:08x}",
            "default_route_table_id": f"rtb-{DemoNetwork._next_net_id:08x}",
            "default_security_group_id": f"sg-{DemoNetwork._next_net_id:08x}",
            "status": "available",
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }

        DemoNetwork._networks[net_id] = net_data
        state = self.State(**net_data)
        return state, None

    async def read(self, ctx: ResourceContext) -> Any:
        """Read network state"""
        net_id = ctx.state.id
        if net_id not in DemoNetwork._networks:
            return None
        net_data = DemoNetwork._networks[net_id]
        return self.State(**net_data)

    async def _update_apply(self, ctx: ResourceContext) -> tuple[Any, Any]:
        """Update network configuration"""
        net_id = ctx.state.id
        net_data = DemoNetwork._networks[net_id]

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

    async def _validate_config(self, config: Any) -> list[str]:
        """Validate network configuration"""
        return []

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        """Delete network"""
        net_id = ctx.state.id
        if net_id in DemoNetwork._networks:
            del DemoNetwork._networks[net_id]
