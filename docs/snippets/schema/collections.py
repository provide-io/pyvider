"""
Collection schema type examples.

This snippet demonstrates collection types:
- Lists
- Maps (dictionaries)
- Sets
- Nested collections
- Collection with defaults

Used in: schema documentation and guides.
"""

from pyvider.schema import PvsSchema, a_list, a_map, a_num, a_set, a_str, s_resource


# --8<-- [start:lists]
def list_examples() -> PvsSchema:
    """List attribute examples."""
    return s_resource(
        {
            # List of strings
            "tags": a_list(a_str(), default=[], description="Resource tags"),
            # List of numbers
            "ports": a_list(a_num(), required=True, description="Port numbers"),
            # Computed list
            "ip_addresses": a_list(a_str(), computed=True, description="IP addresses"),
        }
    )


# --8<-- [end:lists]


# --8<-- [start:maps]
def map_examples() -> PvsSchema:
    """Map (dictionary) attribute examples."""
    return s_resource(
        {
            # Map of string to string
            "labels": a_map(a_str(), default={}, description="Key-value labels"),
            # Map of string to number
            "quotas": a_map(a_num(), required=True, description="Resource quotas"),
            # Computed map
            "metadata": a_map(a_str(), computed=True, description="System metadata"),
        }
    )


# --8<-- [end:maps]


# --8<-- [start:sets]
def set_examples() -> PvsSchema:
    """Set attribute examples (unique values only)."""
    return s_resource(
        {
            # Set of strings (unique tags)
            "unique_tags": a_set(a_str(), default=set(), description="Unique tags"),
            # Set of numbers (unique ports)
            "allowed_ports": a_set(a_num(), required=True, description="Allowed ports"),
            # Computed set
            "active_regions": a_set(a_str(), computed=True, description="Active regions"),
        }
    )


# --8<-- [end:sets]


# --8<-- [start:nested]
def nested_collection_examples() -> PvsSchema:
    """Nested collection examples."""
    return s_resource(
        {
            # List of lists (matrix of strings)
            "matrix": a_list(a_list(a_str()), description="2D string matrix"),
            # Map of string to list
            "region_zones": a_map(
                a_list(a_str()),
                description="Regions mapped to availability zones",
            ),
            # List of maps
            "configurations": a_list(
                a_map(a_str()),
                description="List of configuration maps",
            ),
        }
    )


# --8<-- [end:nested]


# --8<-- [start:combined]
def combined_example() -> PvsSchema:
    """Real-world example with various collections."""
    return s_resource(
        {
            # User inputs
            "name": a_str(required=True),
            "tags": a_list(a_str(), default=[], description="Resource tags"),
            "labels": a_map(a_str(), default={}, description="Labels"),
            "allowed_ports": a_set(a_num(), required=True, description="Allowed ports"),
            "environment_vars": a_map(a_str(), default={}, description="Environment"),
            # Provider outputs
            "id": a_str(computed=True),
            "endpoints": a_list(a_str(), computed=True, description="Service endpoints"),
            "resource_metadata": a_map(a_str(), computed=True, description="Metadata"),
            "active_regions": a_set(a_str(), computed=True, description="Active regions"),
        }
    )


# --8<-- [end:combined]
