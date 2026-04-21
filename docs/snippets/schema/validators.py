"""
Schema validation examples.

This snippet demonstrates common validation patterns:
- String length validation
- Number range validation
- Pattern matching (regex)
- Custom validators
- Multiple validators

Used in: schema documentation and guides.
"""

from pyvider.schema import (
    PvsSchema,
    a_num,
    a_str,
    s_resource,
    v_max_length,
    v_max_value,
    v_min_length,
    v_min_value,
    v_pattern,
)


# --8<-- [start:string_validation]
def string_validation_examples() -> PvsSchema:
    """String validation examples."""
    return s_resource(
        {
            # Minimum length
            "username": a_str(
                required=True,
                validators=[v_min_length(3)],
                description="Username (min 3 chars)",
            ),
            # Maximum length
            "description": a_str(
                validators=[v_max_length(500)],
                description="Description (max 500 chars)",
            ),
            # Min and max length combined
            "password": a_str(
                required=True,
                validators=[v_min_length(8), v_max_length(128)],
                description="Password (8-128 chars)",
            ),
            # Pattern matching (regex)
            "email": a_str(
                required=True,
                validators=[v_pattern(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")],
                description="Email address",
            ),
            # Identifier pattern (alphanumeric + hyphens)
            "resource_id": a_str(
                required=True,
                validators=[v_pattern(r"^[a-z0-9-]+$")],
                description="Resource ID (lowercase, numbers, hyphens)",
            ),
        }
    )


# --8<-- [end:string_validation]


# --8<-- [start:number_validation]
def number_validation_examples() -> PvsSchema:
    """Number validation examples."""
    return s_resource(
        {
            # Minimum value
            "count": a_num(
                required=True,
                validators=[v_min_value(1)],
                description="Instance count (min 1)",
            ),
            # Maximum value
            "port": a_num(
                required=True,
                validators=[v_max_value(65535)],
                description="Port number (max 65535)",
            ),
            # Range validation (min and max)
            "timeout_seconds": a_num(
                default=30,
                validators=[v_min_value(1), v_max_value(3600)],
                description="Timeout (1-3600 seconds)",
            ),
            # Percentage (0-100)
            "cpu_threshold": a_num(
                required=True,
                validators=[v_min_value(0), v_max_value(100)],
                description="CPU threshold percentage (0-100)",
            ),
        }
    )


# --8<-- [end:number_validation]


# --8<-- [start:combined]
def combined_validation_example() -> PvsSchema:
    """Real-world example with multiple validations."""
    return s_resource(
        {
            # User inputs with validation
            "name": a_str(
                required=True,
                validators=[v_min_length(3), v_max_length(50), v_pattern(r"^[a-z0-9-]+$")],
                description="Resource name (3-50 chars, lowercase, numbers, hyphens)",
            ),
            "email": a_str(
                required=True,
                validators=[v_pattern(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")],
                description="Contact email",
            ),
            "instance_count": a_num(
                default=1,
                validators=[v_min_value(1), v_max_value(100)],
                description="Number of instances (1-100)",
            ),
            "timeout_seconds": a_num(
                default=30,
                validators=[v_min_value(1), v_max_value(3600)],
                description="Request timeout (1-3600 seconds)",
            ),
            # Outputs (no validation needed)
            "id": a_str(computed=True),
            "status": a_str(computed=True),
        }
    )


# --8<-- [end:combined]


# --8<-- [start:custom_validation]
# Note: For custom validation beyond these built-in validators,
# use the _validate_config() method in your resource class.
# Example from resource implementation:
#
# async def _validate_config(self, config: ConfigClass) -> list[str]:
#     """Custom configuration validation."""
#     errors = []
#
#     # Custom business logic validation
#     if config.name.startswith("test-") and config.environment == "production":
#         errors.append("Test resources cannot be deployed to production")
#
#     # Cross-field validation
#     if config.min_instances > config.max_instances:
#         errors.append("min_instances cannot exceed max_instances")
#
#     return errors
# --8<-- [end:custom_validation]
