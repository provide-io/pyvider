"""
HTTP API resource example.

This snippet demonstrates managing resources via HTTP API:
- Async HTTP client usage with httpx
- Error handling for 404 responses
- Creating, reading, updating, and deleting via REST API
- Handling optional fields (labels)

Used in: guides showing real-world API integration patterns.
"""

import attrs
import httpx

from pyvider.resources import BaseResource, register_resource
from pyvider.resources.context import ResourceContext
from pyvider.schema import PvsSchema, a_bool, a_map, a_str, s_resource


@attrs.define
class APIObjectConfig:
    name: str
    enabled: bool = True
    labels: dict[str, str] | None = None


@attrs.define
class APIObjectState:
    id: str
    name: str
    enabled: bool
    labels: dict[str, str]
    created_at: str


@register_resource("api_object")
class APIObject(BaseResource):
    """Manages an API object."""

    config_class = APIObjectConfig
    state_class = APIObjectState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(
            {
                "name": a_str(required=True, description="Object name"),
                "enabled": a_bool(default=True, description="Whether enabled"),
                "labels": a_map(a_str(), default={}, description="Labels"),
                "id": a_str(computed=True, description="Object ID"),
                "created_at": a_str(computed=True, description="Creation timestamp"),
            }
        )

    async def _validate_config(self, config: APIObjectConfig) -> list[str]:
        errors = []
        if len(config.name) < 3:
            errors.append("Name must be at least 3 characters")
        return errors

    async def read(self, ctx: ResourceContext) -> APIObjectState | None:
        if not ctx.state:
            return None

        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://api.example.com/objects/{ctx.state.id}")

            if response.status_code == 404:
                return None

            data = response.json()
            return APIObjectState(
                id=ctx.state.id,
                name=data["name"],
                enabled=data["enabled"],
                labels=data.get("labels", {}),
                created_at=ctx.state.created_at,
            )

    async def _create_apply(self, ctx: ResourceContext) -> tuple[APIObjectState | None, None]:
        if not ctx.config:
            return None, None

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.example.com/objects",
                json={
                    "name": ctx.config.name,
                    "enabled": ctx.config.enabled,
                    "labels": ctx.config.labels or {},
                },
            )
            data = response.json()

            return APIObjectState(
                id=data["id"],
                name=data["name"],
                enabled=data["enabled"],
                labels=data.get("labels", {}),
                created_at=data["created_at"],
            ), None

    async def _update_apply(self, ctx: ResourceContext) -> tuple[APIObjectState | None, None]:
        if not ctx.config or not ctx.state:
            return None, None

        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"https://api.example.com/objects/{ctx.state.id}",
                json={
                    "name": ctx.config.name,
                    "enabled": ctx.config.enabled,
                    "labels": ctx.config.labels or {},
                },
            )
            data = response.json()

            return APIObjectState(
                id=ctx.state.id,
                name=data["name"],
                enabled=data["enabled"],
                labels=data.get("labels", {}),
                created_at=ctx.state.created_at,
            ), None

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        if not ctx.state:
            return

        async with httpx.AsyncClient() as client:
            await client.delete(f"https://api.example.com/objects/{ctx.state.id}")
