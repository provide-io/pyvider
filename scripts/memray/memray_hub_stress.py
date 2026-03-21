#!/usr/bin/env python
"""Memray stress test for hub/discovery and schema-to-proto hot paths."""

import os

os.environ["PROVIDE_LOG_LEVEL"] = "ERROR"

import asyncio

from pyvider.conversion.schema_adapter import pvs_schema_to_proto
from pyvider.hub.components import ComponentRegistry
from pyvider.schema.factory import a_num, a_str, s_resource


def main() -> None:
    """Stress test hub registry lookups and schema-to-proto conversion."""

    # --- Setup: populate a registry with test components ---
    reg = ComponentRegistry()
    component_types = ["resource", "data_source", "function", "capability"]
    for ctype in component_types:
        for j in range(20):
            reg.register(ctype, f"test_{ctype}_{j}", object())

    # --- Warmup ---
    for _ in range(100):
        reg.get_components("resource")

    # --- Stress: get_components() for each type (10K cycles) ---
    for i in range(10_000):
        ctype = component_types[i % len(component_types)]
        reg.get_components(ctype)

    # --- Stress: pvs_schema_to_proto() schema conversion (5K cycles) ---
    schemas = [
        s_resource(attributes={
            "id": a_str("Resource ID", computed=True),
            "name": a_str("Resource name", required=True),
            "count": a_num("Count", optional=True),
        })
        for _ in range(10)
    ]

    async def _run_schema_conversion() -> None:
        for i in range(5_000):
            await pvs_schema_to_proto(schemas[i % len(schemas)])

    asyncio.run(_run_schema_conversion())

    print("Hub stress test complete: 15K+ total cycles")


if __name__ == "__main__":
    main()
