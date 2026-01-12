"""
Basic schema type examples.

This snippet demonstrates common schema types:
- String attributes
- Number attributes
- Boolean attributes
- Required vs optional fields
- Default values
- Descriptions

Used in: schema documentation and guides.
"""

from pyvider.schema import PvsSchema, a_bool, a_num, a_str, s_resource


# --8<-- [start:strings]
def string_examples() -> PvsSchema:
    """String attribute examples."""
    return s_resource(
        {
            # Required string
            "name": a_str(required=True, description="Resource name"),
            # Optional string with default
            "region": a_str(default="us-east-1", description="AWS region"),
            # Computed string (provider generates)
            "id": a_str(computed=True, description="Unique identifier"),
            # String with validation (see validators.py)
            "email": a_str(
                required=True,
                description="User email address",
            ),
        }
    )


# --8<-- [end:strings]


# --8<-- [start:numbers]
def number_examples() -> PvsSchema:
    """Number attribute examples."""
    return s_resource(
        {
            # Required integer
            "count": a_num(required=True, description="Instance count"),
            # Optional number with default
            "port": a_num(default=8080, description="Port number"),
            # Computed number (provider generates)
            "size_bytes": a_num(computed=True, description="Size in bytes"),
            # Float number
            "timeout": a_num(default=30.5, description="Timeout in seconds"),
        }
    )


# --8<-- [end:numbers]


# --8<-- [start:booleans]
def boolean_examples() -> PvsSchema:
    """Boolean attribute examples."""
    return s_resource(
        {
            # Required boolean
            "enabled": a_bool(required=True, description="Whether enabled"),
            # Optional boolean with default
            "debug": a_bool(default=False, description="Debug mode"),
            # Computed boolean (provider generates)
            "is_active": a_bool(computed=True, description="Active status"),
        }
    )


# --8<-- [end:booleans]


# --8<-- [start:combined]
def combined_example() -> PvsSchema:
    """Real-world example combining all basic types."""
    return s_resource(
        {
            # User inputs
            "name": a_str(required=True, description="Server name"),
            "region": a_str(default="us-east-1", description="Deployment region"),
            "instance_count": a_num(default=1, description="Number of instances"),
            "enabled": a_bool(default=True, description="Whether server is enabled"),
            "timeout_seconds": a_num(default=30.0, description="Request timeout"),
            # Provider outputs
            "id": a_str(computed=True, description="Unique server ID"),
            "total_size_bytes": a_num(computed=True, description="Total size"),
            "is_running": a_bool(computed=True, description="Running status"),
            "public_url": a_str(computed=True, description="Public URL"),
        }
    )


# --8<-- [end:combined]
