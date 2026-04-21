"""
Minimal file info data source example.

This snippet demonstrates the bare minimum needed for a working data source.
Used in: how-to guides for quick reference.
"""

from pathlib import Path

import attrs

from pyvider.data_sources import BaseDataSource, register_data_source
from pyvider.resources.context import ResourceContext
from pyvider.schema import PvsSchema, a_bool, a_num, a_str, s_data_source


@attrs.define
class FileInfoConfig:
    path: str


@attrs.define
class FileInfoData:
    id: str
    size: int
    exists: bool


@register_data_source("file_info")
class FileInfo(BaseDataSource):
    """Reads information about a local file."""

    config_class = FileInfoConfig
    state_class = FileInfoData

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_data_source(
            {
                "path": a_str(required=True),
                "id": a_str(computed=True),
                "size": a_num(computed=True),
                "exists": a_bool(computed=True),
            }
        )

    async def read(self, ctx: ResourceContext) -> FileInfoData | None:
        if not ctx.config:
            return None

        file_path = Path(ctx.config.path)

        if file_path.exists():
            return FileInfoData(
                id=str(file_path.absolute()),
                size=file_path.stat().st_size,
                exists=True,
            )
        else:
            return FileInfoData(
                id=str(file_path.absolute()),
                size=0,
                exists=False,
            )
