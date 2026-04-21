"""
Minimal file resource example.

This snippet demonstrates the bare minimum needed for a working resource.
Used in: how-to guides for quick reference.
"""

from pathlib import Path

import attrs

from pyvider.resources import BaseResource, register_resource
from pyvider.resources.context import ResourceContext
from pyvider.schema import PvsSchema, a_num, a_str, s_resource


@attrs.define
class FileConfig:
    path: str
    content: str


@attrs.define
class FileState:
    id: str
    path: str
    content: str
    size: int


@register_resource("file")
class File(BaseResource):
    """Manages a local file."""

    config_class = FileConfig
    state_class = FileState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(
            {
                "path": a_str(required=True),
                "content": a_str(required=True),
                "id": a_str(computed=True),
                "size": a_num(computed=True),
            }
        )

    async def read(self, ctx: ResourceContext) -> FileState | None:
        if not ctx.state:
            return None

        file_path = Path(ctx.state.path)
        if not file_path.exists():
            return None

        content = file_path.read_text()
        return FileState(
            id=ctx.state.id,
            path=str(file_path),
            content=content,
            size=len(content),
        )

    async def _create_apply(self, ctx: ResourceContext) -> tuple[FileState | None, None]:
        if not ctx.config:
            return None, None

        file_path = Path(ctx.config.path)
        file_path.write_text(ctx.config.content)

        return FileState(
            id=str(file_path.absolute()),
            path=str(file_path),
            content=ctx.config.content,
            size=len(ctx.config.content),
        ), None

    async def _update_apply(self, ctx: ResourceContext) -> tuple[FileState | None, None]:
        if not ctx.config or not ctx.state:
            return None, None

        file_path = Path(ctx.state.path)
        file_path.write_text(ctx.config.content)

        return FileState(
            id=ctx.state.id,
            path=ctx.state.path,
            content=ctx.config.content,
            size=len(ctx.config.content),
        ), None

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        if not ctx.state:
            return

        file_path = Path(ctx.state.path)
        if file_path.exists():
            file_path.unlink()
