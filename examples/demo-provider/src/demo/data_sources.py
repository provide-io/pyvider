"""
Demo Provider - Data Source Definitions

Contains:
- DemoServerInfo: Query server information
- DemoRegions: Query available regions
- DemoInstanceTypes: Query instance type specifications
"""

import time
from typing import Any

from attrs import define

from pyvider.data_sources import register_data_source
from pyvider.data_sources.base import BaseDataSource
from pyvider.resources.context import ResourceContext
from pyvider.schema import PvsSchema, a_list, a_map, a_num, a_str, s_data_source

from .resources import DemoServer


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
    def get_schema(cls) -> PvsSchema:
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

    async def read(self, ctx: ResourceContext) -> Any:
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
    def get_schema(cls) -> PvsSchema:
        """Define data source schema"""
        return s_data_source(
            {
                "filter_prefix": a_str(optional=True, description="Filter regions by prefix"),
                # Results
                "regions": a_list(a_str(), computed=True, description="List of region codes"),
                "count": a_num(computed=True, description="Number of regions"),
            }
        )

    async def read(self, ctx: ResourceContext) -> Any:
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

    async def _validate_config(self, config: Any) -> list[str]:
        """Validate configuration"""
        return []


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
    def get_schema(cls) -> PvsSchema:
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

    async def read(self, ctx: ResourceContext) -> Any:
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

    async def _validate_config(self, config: Any) -> list[str]:
        """Validate configuration"""
        return []
