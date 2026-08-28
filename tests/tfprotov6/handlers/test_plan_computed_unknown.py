#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""A computed attribute the practitioner did not set is planned unknown.

Terraform calls it "known after apply". Planning it null instead promises Core a
null that apply then contradicts, and Core rejects the whole apply with
"Provider produced inconsistent result after apply".
"""

from __future__ import annotations

from pyvider.cty import CtyValue
from pyvider.protocols.tfprotov6.handlers.plan_resource_change import _handle_planned_state_dict
from pyvider.protocols.tfprotov6.protobuf import tfplugin6_pb2 as pb
from pyvider.schema import a_str, s_resource

SCHEMA = s_resource(
    attributes={
        "name": a_str(required=True),
        "id": a_str(computed=True),
        "arn": a_str(computed=True),
    }
)


def _plan(planned: dict[str, object]) -> CtyValue:
    return _handle_planned_state_dict(dict(planned), SCHEMA, pb.PlanResourceChange.Response())


def test_computed_is_unknown_when_the_config_is_wholly_known() -> None:
    """The case that was broken: nothing else unknown, so nothing forced the marking."""
    planned = _plan({"name": "foo"})
    assert planned.value["id"].is_unknown, "computed 'id' planned as null, not known-after-apply"
    assert planned.value["arn"].is_unknown


def test_computed_is_unknown_when_something_else_is_already_unknown() -> None:
    """The case that happened to work, and must keep working."""
    planned = _plan({"name": CtyValue.unknown(SCHEMA.block.attributes["name"].type)})
    assert planned.value["id"].is_unknown
    assert planned.value["arn"].is_unknown


def test_a_computed_value_the_provider_supplied_is_left_alone() -> None:
    """Marking unknown must not overwrite what the plan hook decided."""
    planned = _plan({"name": "foo", "id": "i-123"})
    assert not planned.value["id"].is_unknown
    assert planned.value["id"].value == "i-123"
    assert planned.value["arn"].is_unknown


def test_an_explicitly_null_computed_value_is_still_planned_unknown() -> None:
    """Null means "not set by the provider", which is precisely known-after-apply."""
    planned = _plan({"name": "foo", "id": None})
    assert planned.value["id"].is_unknown


# 🌊🪢🔚
