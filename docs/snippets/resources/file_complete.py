"""
Complete file resource example with validation.

This snippet demonstrates a full-featured resource implementation including:
- Runtime type definitions with attrs
- Schema definition with validation
- All CRUD operations (create, read, update, delete)
- Configuration validation

Used in: tutorials, guides
"""

from pathlib import Path

import attrs

from pyvider.resources import BaseResource, register_resource
from pyvider.resources.context import ResourceContext
from pyvider.schema import PvsSchema, a_num, a_str, s_resource


# --8<-- [start:types]
# Runtime configuration class (Python type safety)
@attrs.define
class FileConfig:
    """What the user configures."""

    path: str  # Where to create the file
    content: str  # What to write in the file
    mode: str = "644"  # File permissions (optional, defaults to 644)


# Runtime state class (Python type safety)
@attrs.define
class FileState:
    """What Terraform tracks about the file."""

    id: str  # Unique identifier
    path: str  # File path
    content: str  # Current content
    mode: str  # Current permissions
    size: int  # File size in bytes (computed by us)


# --8<-- [end:types]


# --8<-- [start:schema]
@register_resource("file")
class File(BaseResource):
    """Manages a local file."""

    # Link our runtime types
    config_class = FileConfig
    state_class = FileState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        """Define what Terraform users see."""
        return s_resource(
            {
                # User inputs
                "path": a_str(required=True, description="File path"),
                "content": a_str(required=True, description="File content"),
                "mode": a_str(default="644", description="File permissions"),
                # Provider outputs (we compute these)
                "id": a_str(computed=True, description="File ID"),
                "size": a_num(computed=True, description="File size in bytes"),
            }
        )

    # --8<-- [end:schema]

    # --8<-- [start:validation]
    async def _validate_config(self, config: FileConfig) -> list[str]:
        """Validate configuration."""
        errors = []

        # Prevent path traversal attacks
        if ".." in config.path:
            errors.append("Path cannot contain '..'")

        # Validate file mode format
        if not config.mode.isdigit() or len(config.mode) != 3:
            errors.append("Mode must be 3 digits (e.g., '644')")

        return errors

    # --8<-- [end:validation]

    # --8<-- [start:read]
    async def read(self, ctx: ResourceContext) -> FileState | None:
        """Refresh state from filesystem."""
        # If no existing state, nothing to read
        if not ctx.state:
            return None

        file_path = Path(ctx.state.path)

        # Check if file still exists
        if not file_path.exists():
            return None  # File was deleted outside Terraform

        # File exists! Return current state
        content = file_path.read_text()
        return FileState(
            id=ctx.state.id,
            path=str(file_path),
            content=content,
            mode=ctx.state.mode,
            size=len(content),
        )

    # --8<-- [end:read]

    # --8<-- [start:create]
    async def _create_apply(self, ctx: ResourceContext) -> tuple[FileState | None, None]:
        """Create file."""
        if not ctx.config:
            return None, None

        file_path = Path(ctx.config.path)

        # Write the file
        file_path.write_text(ctx.config.content)

        # Return new state
        return FileState(
            id=str(file_path.absolute()),
            path=str(file_path),
            content=ctx.config.content,
            mode=ctx.config.mode,
            size=len(ctx.config.content),
        ), None

    # --8<-- [end:create]

    # --8<-- [start:update]
    async def _update_apply(self, ctx: ResourceContext) -> tuple[FileState | None, None]:
        """Update file."""
        if not ctx.config or not ctx.state:
            return None, None

        file_path = Path(ctx.state.path)

        # Update the file content
        file_path.write_text(ctx.config.content)

        # Return updated state
        return FileState(
            id=ctx.state.id,
            path=ctx.state.path,
            content=ctx.config.content,
            mode=ctx.config.mode,
            size=len(ctx.config.content),
        ), None

    # --8<-- [end:update]

    # --8<-- [start:delete]
    async def _delete_apply(self, ctx: ResourceContext) -> None:
        """Delete file."""
        if not ctx.state:
            return

        file_path = Path(ctx.state.path)

        # Delete file if it exists
        if file_path.exists():
            file_path.unlink()

    # --8<-- [end:delete]
