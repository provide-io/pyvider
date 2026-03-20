#!/usr/bin/env python
"""Memray stress test for conversion/marshaling hot paths."""

import os

os.environ["PROVIDE_LOG_LEVEL"] = "ERROR"

import attrs

from pyvider.conversion.utils import unify_and_validate_list_of_objects
from pyvider.protocols.tfprotov6.handlers.utils import attrs_to_dict_for_cty


@attrs.define
class _StressModel:
    """Simple attrs model for stress testing attrs_to_dict_for_cty."""

    name: str = ""
    count: int = 0
    enabled: bool = True
    tags: dict[str, str] = attrs.Factory(dict)


@attrs.define
class _NestedModel:
    """Nested attrs model for deeper conversion paths."""

    label: str = ""
    inner: _StressModel = attrs.Factory(_StressModel)


def main() -> None:
    """Stress test conversion and marshaling functions."""

    # --- Warmup ---
    simple = _StressModel(name="warmup", count=1, tags={"env": "test"})
    for _ in range(100):
        attrs_to_dict_for_cty(simple)

    # --- Stress: attrs_to_dict_for_cty() with nested objects (10K cycles) ---
    models = [
        _NestedModel(
            label=f"item_{i}",
            inner=_StressModel(
                name=f"inner_{i}",
                count=i,
                enabled=i % 2 == 0,
                tags={"key": f"val_{i}", "env": "stress"},
            ),
        )
        for i in range(100)
    ]
    for i in range(10_000):
        attrs_to_dict_for_cty(models[i % len(models)])

    # --- Stress: unify_and_validate_list_of_objects() with varied dicts (10K cycles) ---
    dict_batches = [
        [{"name": f"a_{j}", "count": j, "active": True} for j in range(5)],
        [{"name": f"b_{j}", "value": j * 1.5} for j in range(5)],
        [{"name": f"c_{j}", "count": j, "value": j * 2.0, "active": False} for j in range(5)],
    ]
    for i in range(10_000):
        unify_and_validate_list_of_objects(dict_batches[i % len(dict_batches)])

    print("Conversion stress test complete: 20K+ total cycles")


if __name__ == "__main__":
    main()
