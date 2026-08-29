#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""`resolve_schema_defaults` puts a schema default into the configuration itself.

Resolving a default on the plan alone is not enough. `ctx.config` is what a
resource's own apply hook reads, so a default that never reaches it produces a
final state that does not match the state Terraform planned -- pyvider rejects
that as `ResourceLifecycleContractError`, and Terraform as a provider-produced
inconsistency.
"""

import attrs
import pytest

from pyvider.cty import CtyBool, CtyNumber, CtyString, CtyValue
from pyvider.resources.base import BaseResource
from pyvider.schema import (
    a_bool,
    a_num,
    a_obj,
    a_str,
    b_list,
    b_map,
    b_set,
    b_single,
    merge_schema_defaults_into_plan,
    resolve_schema_defaults,
    resolves_from_configuration,
    s_resource,
)

SCHEMA = s_resource(
    attributes={
        "name": a_str(required=True),
        "size": a_str(default="small"),
        "learning": a_bool(default=True),
        "explicit_null": a_str(),
        "secret": a_str(write_only=True),
        "mandatory": a_str(required=True),
    }
)

BLOCK_TYPE = SCHEMA.block.to_cty_type()


def _config(**overrides: object) -> CtyValue:
    values: dict[str, object] = {
        "name": "example",
        "size": CtyValue.null(CtyString()),
        "learning": CtyValue.null(CtyBool()),
        "explicit_null": CtyValue.null(CtyString()),
        "secret": CtyValue.null(CtyString()),
        "mandatory": CtyValue.null(CtyString()),
    }
    values.update(overrides)
    return BLOCK_TYPE.validate(values)


class TestAttributeResolution:
    def test_null_attribute_takes_the_schema_default(self) -> None:
        resolved = resolve_schema_defaults(_config(), SCHEMA.block)

        assert resolved.value["size"].value == "small"
        assert resolved.value["learning"].value is True

    def test_configured_value_is_left_alone(self) -> None:
        resolved = resolve_schema_defaults(_config(size="large"), SCHEMA.block)

        assert resolved.value["size"].value == "large"

    def test_unknown_value_is_left_unknown(self) -> None:
        resolved = resolve_schema_defaults(_config(size=CtyValue.unknown(CtyString())), SCHEMA.block)

        assert resolved.value["size"].is_unknown

    def test_attribute_without_a_default_stays_null(self) -> None:
        resolved = resolve_schema_defaults(_config(), SCHEMA.block)

        assert resolved.value["explicit_null"].is_null

    def test_write_only_attribute_is_not_filled(self) -> None:
        # A write-only attribute cannot declare a default at all, so nothing
        # ever fills one in.
        resolved = resolve_schema_defaults(_config(), SCHEMA.block)

        assert resolved.value["secret"].is_null

    def test_required_attribute_is_not_filled(self) -> None:
        # A required attribute cannot declare a default at all, so a missing
        # required value stays null for the required-attribute check to catch.
        resolved = resolve_schema_defaults(_config(), SCHEMA.block)

        assert resolved.value["mandatory"].is_null

    def test_value_is_returned_unchanged_when_nothing_needs_resolving(self) -> None:
        already = resolve_schema_defaults(_config(), SCHEMA.block)

        assert resolve_schema_defaults(already, SCHEMA.block) is already

    def test_null_and_unknown_configurations_pass_through(self) -> None:
        null_config = CtyValue.null(BLOCK_TYPE)
        unknown_config = CtyValue.unknown(BLOCK_TYPE)

        assert resolve_schema_defaults(null_config, SCHEMA.block) is null_config
        assert resolve_schema_defaults(unknown_config, SCHEMA.block) is unknown_config
        assert resolve_schema_defaults(None, SCHEMA.block) is None


NESTED_SCHEMA = s_resource(
    attributes={"name": a_str(required=True)},
    block_types=[
        b_single("options", attributes={"mode": a_str(default="fast")}),
        b_list("port", attributes={"enabled": a_bool(default=True)}),
    ],
)

NESTED_TYPE = NESTED_SCHEMA.block.to_cty_type()


class TestNestedBlockResolution:
    def test_single_nested_block_gets_its_defaults(self) -> None:
        config = NESTED_TYPE.validate(
            {"name": "n", "options": {"mode": CtyValue.null(CtyString())}, "port": []}
        )

        resolved = resolve_schema_defaults(config, NESTED_SCHEMA.block)

        assert resolved.value["options"].value["mode"].value == "fast"

    def test_every_element_of_a_list_block_gets_its_defaults(self) -> None:
        config = NESTED_TYPE.validate(
            {
                "name": "n",
                "options": CtyValue.null(NESTED_SCHEMA.block.block_types[0].block.to_cty_type()),
                "port": [{"enabled": CtyValue.null(CtyBool())}, {"enabled": False}],
            }
        )

        resolved = resolve_schema_defaults(config, NESTED_SCHEMA.block)

        ports = resolved.value["port"].value
        assert ports[0].value["enabled"].value is True
        assert ports[1].value["enabled"].value is False


@attrs.define
class SwitchConfig:
    """A config class that declares no default of its own.

    This is the shape that made the plan-only fix insufficient: attrs has
    nothing to fall back on, so the default has to already be in the cty value.
    """

    name: str
    learning: bool | None = None


class TestDecodingWithoutAnAttrsDefault:
    def test_default_reaches_a_config_class_that_declares_none(self) -> None:
        resolved = resolve_schema_defaults(_config(), SCHEMA.block)

        config = BaseResource.from_cty(resolved, SwitchConfig)

        assert config is not None
        assert config.learning is True


MERGE_SCHEMA = s_resource(
    attributes={"name": a_str(required=True)},
    block_types=[
        b_single(
            "options",
            attributes={"mode": a_str(default="fast"), "label": a_str()},
            block_types=[b_single("tuning", attributes={"level": a_str(default="low")})],
        ),
        b_list("port", attributes={"enabled": a_bool(default=True)}),
        b_map("zone", attributes={"enabled": a_bool(default=True)}),
        b_set("tag", attributes={"enabled": a_bool(default=True)}),
    ],
)

MERGE_TYPE = MERGE_SCHEMA.block.to_cty_type()


def _merge_config(**overrides: object) -> CtyValue:
    values: dict[str, object] = {
        "name": "example",
        "options": {"mode": "fast", "label": "primary", "tuning": {"level": "low"}},
        "port": [{"enabled": True}],
        "zone": {"a": {"enabled": True}},
        "tag": [{"enabled": True}],
    }
    values.update(overrides)
    return MERGE_TYPE.validate(values)


class TestNestedPlanMerge:
    """`merge_schema_defaults_into_plan` corrects a plan that retained prior state.

    Terraform's proposed new state keeps the prior value of an attribute the
    practitioner omitted, because the protocol never told it there was a
    default. Only attributes that declare one may be overridden.
    """

    def test_retained_single_block_value_is_corrected(self) -> None:
        plan = {"options": {"mode": "slow", "label": "primary", "tuning": {"level": "low"}}}

        merge_schema_defaults_into_plan(plan, _merge_config(), MERGE_SCHEMA.block)

        assert plan["options"]["mode"] == "fast"

    def test_attribute_without_a_default_keeps_the_proposed_value(self) -> None:
        plan = {"options": {"mode": "slow", "label": "stale", "tuning": {"level": "low"}}}

        merge_schema_defaults_into_plan(plan, _merge_config(), MERGE_SCHEMA.block)

        assert plan["options"]["label"] == "stale"

    def test_blocks_nested_inside_blocks_are_corrected(self) -> None:
        plan = {"options": {"mode": "fast", "label": "primary", "tuning": {"level": "high"}}}

        merge_schema_defaults_into_plan(plan, _merge_config(), MERGE_SCHEMA.block)

        assert plan["options"]["tuning"]["level"] == "low"

    def test_list_elements_are_corrected_by_position(self) -> None:
        plan = {"port": [{"enabled": False}]}

        merge_schema_defaults_into_plan(plan, _merge_config(), MERGE_SCHEMA.block)

        assert plan["port"][0]["enabled"] is True

    def test_list_of_a_different_length_is_left_alone(self) -> None:
        # Nothing pairs a planned element with the configuration it came from
        # once the counts differ.
        plan = {"port": [{"enabled": False}, {"enabled": False}]}

        merge_schema_defaults_into_plan(plan, _merge_config(), MERGE_SCHEMA.block)

        assert [element["enabled"] for element in plan["port"]] == [False, False]

    def test_map_elements_are_corrected_by_key(self) -> None:
        plan = {"zone": {"a": {"enabled": False}, "b": {"enabled": False}}}

        merge_schema_defaults_into_plan(plan, _merge_config(), MERGE_SCHEMA.block)

        assert plan["zone"]["a"]["enabled"] is True
        # "b" is not in the configuration, so there is no default to follow.
        assert plan["zone"]["b"]["enabled"] is False

    def test_single_element_set_is_corrected(self) -> None:
        plan = {"tag": [{"enabled": False}]}

        merge_schema_defaults_into_plan(plan, _merge_config(), MERGE_SCHEMA.block)

        assert plan["tag"][0]["enabled"] is True

    def test_multi_element_set_is_left_alone(self) -> None:
        # Set elements have no stable order to pair on -- a default that differs
        # from prior state is itself what reorders them.
        config = _merge_config(tag=[{"enabled": True}, {"enabled": False}])
        plan = {"tag": [{"enabled": False}, {"enabled": False}]}

        merge_schema_defaults_into_plan(plan, config, MERGE_SCHEMA.block)

        assert [element["enabled"] for element in plan["tag"]] == [False, False]

    def test_unconfigured_block_is_left_alone(self) -> None:
        config = _merge_config(options=CtyValue.null(MERGE_SCHEMA.block.block_types[0].block.to_cty_type()))
        plan = {"options": {"mode": "slow", "label": "primary", "tuning": {"level": "low"}}}

        merge_schema_defaults_into_plan(plan, config, MERGE_SCHEMA.block)

        assert plan["options"]["mode"] == "slow"

    def test_null_and_unknown_configurations_change_nothing(self) -> None:
        for config in (CtyValue.null(MERGE_TYPE), CtyValue.unknown(MERGE_TYPE), None):
            plan = {"port": [{"enabled": False}]}

            merge_schema_defaults_into_plan(plan, config, MERGE_SCHEMA.block)

            assert plan["port"][0]["enabled"] is False

    def test_block_absent_from_the_plan_is_not_invented(self) -> None:
        plan: dict[str, object] = {"name": "example"}

        merge_schema_defaults_into_plan(plan, _merge_config(), MERGE_SCHEMA.block)

        assert plan == {"name": "example"}


OBJECT_SCHEMA = s_resource(
    attributes={
        "name": a_str(required=True),
        "config": a_obj(
            {
                "timeout": a_num(default=30),
                "retries": a_num(default=3),
                "label": a_str(),
                "tls": a_obj({"enabled": a_bool(default=True)}),
            }
        ),
        "secret": a_obj({"token": a_str(default="hunter2")}, write_only=True),
    },
    block_types=[b_single("options", attributes={"limits": a_obj({"max": a_num(default=5)})})],
)

OBJECT_TYPE = OBJECT_SCHEMA.block.to_cty_type()
CONFIG_TYPE = OBJECT_SCHEMA.block.attributes["config"].type
SECRET_TYPE = OBJECT_SCHEMA.block.attributes["secret"].type
TLS_TYPE = OBJECT_SCHEMA.block.attributes["config"].object_type.attributes["tls"].type


def _object_config(**overrides: object) -> CtyValue:
    config: dict[str, object] = {
        "timeout": CtyValue.null(CtyNumber()),
        "retries": CtyValue.null(CtyNumber()),
        "label": CtyValue.null(CtyString()),
        "tls": {"enabled": CtyValue.null(CtyBool())},
    }
    config.update(overrides)
    values: dict[str, object] = {
        "name": "example",
        "config": config,
        "secret": {"token": CtyValue.null(CtyString())},
        "options": {"limits": {"max": CtyValue.null(CtyNumber())}},
    }
    return OBJECT_TYPE.validate(values)


class TestObjectAttributeResolution:
    """An `a_obj()` attribute is a block written as a value.

    Its members declare defaults exactly as a block's attributes do, so the
    resolution walk has to descend into `PvsAttribute.object_type` too --
    otherwise the documented `a_obj({"timeout": a_num(default=30)})` example
    leaves the practitioner with a null.
    """

    def test_omitted_object_member_takes_the_schema_default(self) -> None:
        resolved = resolve_schema_defaults(_object_config(), OBJECT_SCHEMA.block)

        assert resolved.value["config"].value["timeout"].value == 30
        assert resolved.value["config"].value["retries"].value == 3

    def test_configured_object_member_is_left_alone(self) -> None:
        resolved = resolve_schema_defaults(_object_config(timeout=60), OBJECT_SCHEMA.block)

        assert resolved.value["config"].value["timeout"].value == 60

    def test_unknown_object_member_is_left_unknown(self) -> None:
        resolved = resolve_schema_defaults(
            _object_config(timeout=CtyValue.unknown(CtyNumber())), OBJECT_SCHEMA.block
        )

        assert resolved.value["config"].value["timeout"].is_unknown

    def test_object_member_without_a_default_stays_null(self) -> None:
        resolved = resolve_schema_defaults(_object_config(), OBJECT_SCHEMA.block)

        assert resolved.value["config"].value["label"].is_null

    def test_objects_nested_inside_objects_are_resolved(self) -> None:
        resolved = resolve_schema_defaults(_object_config(), OBJECT_SCHEMA.block)

        assert resolved.value["config"].value["tls"].value["enabled"].value is True

    def test_object_inside_a_nested_block_is_resolved(self) -> None:
        resolved = resolve_schema_defaults(_object_config(), OBJECT_SCHEMA.block)

        assert resolved.value["options"].value["limits"].value["max"].value == 5

    def test_write_only_object_is_not_filled(self) -> None:
        # A write-only value is never stored, so nothing inside it may be
        # filled in either.
        resolved = resolve_schema_defaults(_object_config(), OBJECT_SCHEMA.block)

        assert resolved.value["secret"].value["token"].is_null

    def test_null_object_is_not_invented(self) -> None:
        # The attribute itself declares no default, and an absent object is not
        # an object whose members were omitted.
        config = OBJECT_TYPE.validate(
            {
                "name": "example",
                "config": CtyValue.null(CONFIG_TYPE),
                "secret": CtyValue.null(SECRET_TYPE),
                "options": {"limits": {"max": CtyValue.null(CtyNumber())}},
            }
        )

        resolved = resolve_schema_defaults(config, OBJECT_SCHEMA.block)

        assert resolved.value["config"].is_null

    def test_object_default_is_completed_by_its_members(self) -> None:
        # The object attribute's own default supplies the object; the members it
        # leaves null are then resolved like any other.
        schema = s_resource(
            attributes={
                "config": a_obj(
                    {"timeout": a_num(default=30), "retries": a_num(default=3)},
                    default={"timeout": 60, "retries": None},
                )
            }
        )
        config = schema.block.to_cty_type().validate(
            {"config": CtyValue.null(schema.block.attributes["config"].type)}
        )

        resolved = resolve_schema_defaults(config, schema.block)

        assert resolved.value["config"].value["timeout"].value == 60
        assert resolved.value["config"].value["retries"].value == 3


class TestObjectPlanMerge:
    """A plan that retained a prior object member is corrected too.

    Terraform's proposed new state carries the prior value of an omitted object
    member forward, just as it does for a nested block's attribute, so the plan
    merge has to descend into `object_type` as well.
    """

    def _resolved_config(self, **overrides: object) -> CtyValue:
        resolved = resolve_schema_defaults(_object_config(**overrides), OBJECT_SCHEMA.block)
        assert resolved is not None
        return resolved

    def test_retained_object_member_is_corrected(self) -> None:
        plan = {"config": {"timeout": 60, "retries": 3, "label": "primary", "tls": {"enabled": True}}}

        merge_schema_defaults_into_plan(plan, self._resolved_config(), OBJECT_SCHEMA.block)

        assert plan["config"]["timeout"] == 30

    def test_member_without_a_default_keeps_the_proposed_value(self) -> None:
        plan = {"config": {"timeout": 30, "retries": 3, "label": "stale", "tls": {"enabled": True}}}

        merge_schema_defaults_into_plan(plan, self._resolved_config(), OBJECT_SCHEMA.block)

        assert plan["config"]["label"] == "stale"

    def test_objects_nested_inside_objects_are_corrected(self) -> None:
        plan = {"config": {"timeout": 30, "retries": 3, "label": None, "tls": {"enabled": False}}}

        merge_schema_defaults_into_plan(plan, self._resolved_config(), OBJECT_SCHEMA.block)

        assert plan["config"]["tls"]["enabled"] is True

    def test_object_inside_a_nested_block_is_corrected(self) -> None:
        plan = {"options": {"limits": {"max": 99}}}

        merge_schema_defaults_into_plan(plan, self._resolved_config(), OBJECT_SCHEMA.block)

        assert plan["options"]["limits"]["max"] == 5

    def test_unknown_member_leaves_the_plan_alone(self) -> None:
        config = self._resolved_config(timeout=CtyValue.unknown(CtyNumber()))
        plan = {"config": {"timeout": 60, "retries": 3, "label": None, "tls": {"enabled": True}}}

        merge_schema_defaults_into_plan(plan, config, OBJECT_SCHEMA.block)

        assert plan["config"]["timeout"] == 60

    def test_write_only_object_is_not_filled(self) -> None:
        plan = {"secret": None}

        merge_schema_defaults_into_plan(plan, self._resolved_config(), OBJECT_SCHEMA.block)

        assert plan["secret"] is None

    def test_object_absent_from_the_plan_is_not_invented(self) -> None:
        plan: dict[str, object] = {"name": "example"}

        merge_schema_defaults_into_plan(plan, self._resolved_config(), OBJECT_SCHEMA.block)

        assert plan == {"name": "example"}

    def test_null_object_in_the_plan_is_left_alone(self) -> None:
        # There is no object to correct members inside, and the attribute
        # declares no default of its own to fall back on.
        plan: dict[str, object] = {"config": None}

        merge_schema_defaults_into_plan(plan, self._resolved_config(), OBJECT_SCHEMA.block)

        assert plan["config"] is None


class TestComputedOnlyDefaults:
    """A computed-only attribute cannot declare a default.

    A default is the value used when the practitioner omits something they could
    have written, and `computed=True` without `optional=True` means they cannot
    write it at all. The provider's fallback for a value it computes belongs in
    the resource, not the schema.
    """

    def test_computed_only_default_is_rejected(self) -> None:
        with pytest.raises(ValueError, match="computed-only attribute cannot declare a default"):
            a_str(computed=True, default="x")

    def test_optional_and_computed_default_is_allowed(self) -> None:
        # The flag combination `a_str(default=...)` produces on its own, and the
        # one to reach for when a practitioner may set the value.
        attribute = a_str(optional=True, computed=True, default="small")

        assert attribute.optional is True
        assert attribute.computed is True

    def test_computed_only_without_a_default_is_allowed(self) -> None:
        attribute = a_str(computed=True)

        assert attribute.computed is True
        assert attribute.optional is False

    def test_optional_and_computed_default_is_resolved(self) -> None:
        schema = s_resource(attributes={"size": a_str(default="small")})
        config = schema.block.to_cty_type().validate({"size": CtyValue.null(CtyString())})

        resolved = resolve_schema_defaults(config, schema.block)

        assert resolved.value["size"].value == "small"

    def test_explicit_none_default_is_no_default(self) -> None:
        # `default=None` is indistinguishable from declaring no default; there is
        # no way to spell "defaults to null", which is what a null already is.
        # It is also why `computed=True, default=None` is accepted rather than
        # rejected: there is no default there to contradict the flag.
        attribute = a_str(computed=True, default=None)

        assert attribute.default is None
        assert resolves_from_configuration(attribute) is False


# 🐍🏗️🔚
