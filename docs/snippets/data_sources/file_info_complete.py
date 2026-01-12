"""
Complete file info data source example.

This snippet demonstrates a full-featured data source implementation including:
- Runtime type definitions with attrs
- Schema definition
- Read operation that handles both existing and non-existing files
- Proper error handling and data return

Used in: tutorials, guides
"""

from pathlib import Path

import attrs

from pyvider.data_sources import BaseDataSource, register_data_source
from pyvider.resources.context import ResourceContext
from pyvider.schema import PvsSchema, a_bool, a_num, a_str, s_data_source


# --8<-- [start:types]
# Configuration (input from user)
@attrs.define
class FileInfoConfig:
    """What the user wants to query."""

    path: str  # Which file to query


# Data (output to user - query results)
@attrs.define
class FileInfoData:
    """Information we return about the file."""

    id: str  # Unique identifier
    path: str  # File path
    size: int  # File size in bytes
    exists: bool  # Whether file exists
    content: str  # File content


# --8<-- [end:types]


# --8<-- [start:schema]
@register_data_source("file_info")
class FileInfo(BaseDataSource):
    """Reads information about a local file."""

    # Link our runtime types
    config_class = FileInfoConfig
    state_class = FileInfoData

    @classmethod
    def get_schema(cls) -> PvsSchema:
        """Define what Terraform users see."""
        return s_data_source(
            {
                # Input (from user)
                "path": a_str(required=True, description="File path to query"),
                # Outputs (we compute all of these)
                "id": a_str(computed=True, description="File path as ID"),
                "size": a_num(computed=True, description="File size in bytes"),
                "exists": a_bool(computed=True, description="Whether file exists"),
                "content": a_str(computed=True, description="File content"),
            }
        )

    # --8<-- [end:schema]

    # --8<-- [start:read]
    async def read(self, ctx: ResourceContext) -> FileInfoData | None:
        """Read file information."""
        if not ctx.config:
            return None

        file_path = Path(ctx.config.path)

        # Check if file exists
        if file_path.exists():
            # File exists - read information
            content = file_path.read_text()
            size = file_path.stat().st_size

            return FileInfoData(
                id=str(file_path.absolute()),
                path=str(file_path),
                size=size,
                exists=True,
                content=content,
            )
        else:
            # File doesn't exist - return empty data
            return FileInfoData(
                id=str(file_path.absolute()),
                path=str(file_path),
                size=0,
                exists=False,
                content="",
            )

    # --8<-- [end:read]
