#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from typing import Any

import pytest

from pyvider.cty.exceptions import CtyValidationError
from pyvider.protocols.tfprotov6.handlers.utils import (
    create_diagnostic_from_exception,
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.schema import (
    PvsSchema,
    a_list,
    a_map,
    a_num,
    a_obj,
    a_str,
    a_tuple,
    b_list,
    b_map,
    s_resource,
)


async def assert_deep_diagnostic(
    schema: PvsSchema,
    invalid_config: dict[str, Any],
    expected_path_str: str,
    expected_summary_contains: str,
) -> None:
    """
    Helper to assert that validating a config against a schema produces a
    diagnostic with a specific, correctly formatted deep path.
    """
    validator_cty_type = schema.block.to_cty_type()

    with pytest.raises(CtyValidationError) as exc_info:
        validator_cty_type.validate(invalid_config)

    # This is the core function we are testing the behavior of.
    diag = await create_diagnostic_from_exception(exc_info.value)

    assert diag.severity == pb.Diagnostic.ERROR
    assert expected_summary_contains in diag.summary

    # Reconstruct the path string from the protobuf message for comparison.
    actual_path_parts = []
    if diag.attribute and diag.attribute.steps:
        for i, step in enumerate(diag.attribute.steps):
            if step.HasField("attribute_name"):
                # Add a dot only if it's not the first step.
                if i > 0:
                    actual_path_parts.append(".")
                actual_path_parts.append(step.attribute_name)
            elif step.HasField("element_key_int"):
                actual_path_parts.append(f"[{step.element_key_int}]")
            elif step.HasField("element_key_string"):
                actual_path_parts.append(f"['{step.element_key_string}']")

    actual_path_str = "".join(actual_path_parts)

    assert actual_path_str == expected_path_str, (
        f"Path mismatch: expected '{expected_path_str}', got '{actual_path_str}'"
    )


@pytest.mark.asyncio
class TestDeepDiagnosticPaths:
    """
    TDD Test Suite for ensuring clear and accurate diagnostic messages
    for errors in deeply nested data structures.
    """

    async def test_error_in_nested_object(self) -> None:
        """TDD: Verifies pathing for an object nested within another object."""
        schema = s_resource(
            attributes={"config": a_obj(attributes={"retries": a_num(required=True)}, required=True)}
        )
        invalid_config = {"config": {"retries": "five"}}
        await assert_deep_diagnostic(
            schema,
            invalid_config,
            expected_path_str="config.retries",
            expected_summary_contains="Number validation error",
        )

    async def test_error_in_list_of_objects(self) -> None:
        """TDD: Verifies pathing for an error in the nth element of a list of objects."""
        schema = s_resource(
            attributes={"users": a_list(a_obj(attributes={"name": a_str(required=True)}), required=True)}
        )
        invalid_config = {"users": [{"name": "Alice"}, {"name": 123}]}
        await assert_deep_diagnostic(
            schema,
            invalid_config,
            expected_path_str="users[1].name",
            expected_summary_contains="String validation error",
        )

    async def test_error_in_map_of_objects(self) -> None:
        """TDD: Verifies pathing for an error in an object inside a map."""
        schema = s_resource(
            attributes={"services": a_map(a_obj(attributes={"port": a_num(required=True)}), required=True)}
        )
        invalid_config = {"services": {"api": {"port": 80}, "db": {"port": "invalid"}}}
        await assert_deep_diagnostic(
            schema,
            invalid_config,
            expected_path_str="services['db'].port",
            expected_summary_contains="Number validation error",
        )

    async def test_error_in_tuple_with_nested_list(self) -> None:
        """TDD: Verifies pathing for an error in a list inside a tuple."""
        schema = s_resource(
            attributes={"endpoint": a_tuple([a_str(), a_list(a_num(required=True))], required=True)}
        )
        invalid_config = {"endpoint": ("host.com", [80, 443, "not-a-port"])}
        await assert_deep_diagnostic(
            schema,
            invalid_config,
            expected_path_str="endpoint[1][2]",
            expected_summary_contains="Number validation error",
        )

    async def test_error_in_nested_block_list(self) -> None:
        """TDD: Verifies pathing for an error within a nested block list."""
        schema = s_resource(
            block_types=[
                b_list(
                    "ingress_rule",
                    attributes={"port": a_num(required=True), "proto": a_str()},
                )
            ]
        )
        invalid_config = {"ingress_rule": [{"port": 443, "proto": "tcp"}, {"port": "invalid"}]}
        await assert_deep_diagnostic(
            schema,
            invalid_config,
            expected_path_str="ingress_rule[1].port",
            expected_summary_contains="Number validation error",
        )

    async def test_deeply_nested_block_in_map_in_list(self) -> None:
        """TDD: A stress test for deeply nested path generation."""
        schema = s_resource(
            block_types=[
                b_list(
                    "environments",
                    attributes={"name": a_str()},
                    block_types=[
                        b_map(
                            "services",
                            attributes={"image": a_str()},
                            block_types=[
                                b_list(
                                    "volumes",
                                    attributes={"mount_path": a_str(required=True)},
                                )
                            ],
                        )
                    ],
                )
            ]
        )
        invalid_config = {
            "environments": [
                {
                    "name": "prod",
                    "services": {
                        "api": {
                            "image": "api:v1",
                            "volumes": [
                                {"mount_path": "/data"},
                                {"mount_path": None},  # The invalid value
                            ],
                        }
                    },
                }
            ]
        }
        await assert_deep_diagnostic(
            schema,
            invalid_config,
            expected_path_str="environments[0].services['api'].volumes[1].mount_path",
            expected_summary_contains="Attribute cannot be null",
        )


# 🐍🏗️🔚
