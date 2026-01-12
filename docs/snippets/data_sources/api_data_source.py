"""
HTTP API data source example.

This snippet demonstrates querying data via HTTP API:
- Async HTTP client usage with httpx
- Error handling for failed requests
- Fetching data from REST API
- Handling optional fields

Used in: guides showing real-world API integration patterns.
"""

import attrs
import httpx

from pyvider.data_sources import BaseDataSource, register_data_source
from pyvider.resources.context import ResourceContext
from pyvider.schema import PvsSchema, a_map, a_str, s_data_source


@attrs.define
class UserConfig:
    """Configuration for user lookup."""

    user_id: str


@attrs.define
class UserData:
    """User information from API."""

    id: str
    name: str
    email: str
    role: str
    metadata: dict[str, str]


@register_data_source("user")
class User(BaseDataSource):
    """Fetches user information from API."""

    config_class = UserConfig
    state_class = UserData

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_data_source(
            {
                # Input
                "user_id": a_str(required=True, description="User ID to query"),
                # Outputs
                "id": a_str(computed=True, description="User ID"),
                "name": a_str(computed=True, description="User name"),
                "email": a_str(computed=True, description="User email"),
                "role": a_str(computed=True, description="User role"),
                "metadata": a_map(a_str(), computed=True, description="User metadata"),
            }
        )

    async def read(self, ctx: ResourceContext) -> UserData | None:
        """Fetch user information from API."""
        if not ctx.config:
            return None

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"https://api.example.com/users/{ctx.config.user_id}",
                    timeout=10.0,
                )
                response.raise_for_status()

                data = response.json()
                return UserData(
                    id=data["id"],
                    name=data["name"],
                    email=data["email"],
                    role=data.get("role", "user"),
                    metadata=data.get("metadata", {}),
                )

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    # User not found - return None or raise error
                    ctx.add_error(f"User {ctx.config.user_id} not found")
                    return None
                raise

            except httpx.RequestError as e:
                ctx.add_error(f"Failed to fetch user: {e}")
                return None
