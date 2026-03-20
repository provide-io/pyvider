#!/usr/bin/env python
"""Memray stress test for schema processing hot paths."""

import os

os.environ["PROVIDE_LOG_LEVEL"] = "ERROR"

from pyvider.schema.factory import a_num, a_obj, a_str, b_list, s_resource
from pyvider.schema.types.attribute import PvsAttribute
from pyvider.schema.types.object import PvsObjectType

from pyvider.cty import CtyNumber, CtyString


def main() -> None:
    """Stress test schema creation and type conversion."""

    # --- Warmup ---
    for _ in range(100):
        s_resource(attributes={"name": a_str("A name")})

    # --- Stress: s_resource() with mixed attributes (10K cycles) ---
    for i in range(10_000):
        s_resource(
            attributes={
                "name": a_str("Resource name", required=True),
                "count": a_num("Instance count", optional=True),
                "metadata": a_obj(
                    {"key": a_str("Key"), "value": a_str("Value")},
                    description="Metadata object",
                    optional=True,
                ),
            },
            block_types=[
                b_list(
                    "tags",
                    attributes={
                        "tag_key": a_str("Tag key", required=True),
                        "tag_value": a_str("Tag value", required=True),
                    },
                ),
            ],
        )

    # --- Stress: PvsObjectType.to_cty_type() on complex schemas (10K cycles) ---
    complex_obj = PvsObjectType(
        attributes={
            "id": PvsAttribute(name="id", type=CtyString(), computed=True),
            "name": PvsAttribute(name="name", type=CtyString(), required=True),
            "port": PvsAttribute(name="port", type=CtyNumber(), optional=True),
        },
    )
    for _ in range(10_000):
        complex_obj.to_cty_type()

    # --- Stress: PvsAttribute creation with validation (5K cycles) ---
    for i in range(5_000):
        PvsAttribute(name=f"attr_{i}", type=CtyString(), required=True)
        PvsAttribute(name=f"opt_{i}", type=CtyNumber(), optional=True)
        PvsAttribute(name=f"comp_{i}", type=CtyString(), computed=True)

    print("Schema stress test complete: 25K+ total cycles")


if __name__ == "__main__":
    main()
