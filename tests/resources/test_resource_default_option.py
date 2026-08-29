#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""`PvsAttribute.default` has to be resolved by the provider.

The plugin protocol schema carries no default-value field, so Terraform sends an
omitted optional attribute as null and never learns what the provider considers
the default. Unless the framework resolves it while decoding config and building
the plan, `a_str(default=...)` is inert and apply can return a value Terraform
never planned.
"""

from typing import Any

import attrs
import pytest

from pyvider.cty import CtyObject, CtyString, CtyValue
from pyvider.resources.base import BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.schema import PvsSchema, a_obj, a_str, b_list, b_single, resolve_schema_defaults, s_resource

DEFAULT_SIZE = "small"


@attrs.define
class WidgetConfig:
    name: str
    size: str | None = DEFAULT_SIZE


@attrs.define
class WidgetState:
    name: str
    size: str | None = DEFAULT_SIZE
    id: str | None = None


class Widget(BaseResource[Any, WidgetState, WidgetConfig]):
    config_class = WidgetConfig
    state_class = WidgetState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(
            attributes={
                "name": a_str(required=True),
                "size": a_str(default=DEFAULT_SIZE),
                "id": a_str(computed=True),
            }
        )

    async def _validate_config(self, config: WidgetConfig) -> list[str]:
        return []

    async def read(self, ctx: ResourceContext) -> WidgetState | None:
        return ctx.state

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        return None


CONFIG_TYPE = CtyObject({"name": CtyString(), "size": CtyString(), "id": CtyString()})


def _config_cty(size: CtyValue | str) -> CtyValue:
    return CONFIG_TYPE.validate({"name": "example", "size": size, "id": CtyValue.unknown(CtyString())})


class TestSchemaFlags:
    """An attribute with a default has to be Optional + Computed.

    Terraform rejects a planned value on an attribute that is not computed
    ("planned value ... for a non-computed attribute"), so a schema default is
    unusable unless the attribute is also computed.
    """

    def test_default_marks_the_attribute_optional_and_computed(self) -> None:
        attribute = a_str(default=DEFAULT_SIZE)

        assert attribute.optional is True
        assert attribute.computed is True
        assert attribute.required is False

    def test_attribute_without_a_default_is_not_computed(self) -> None:
        attribute = a_str()

        assert attribute.optional is True
        assert attribute.computed is False

    def test_required_attribute_rejects_a_default(self) -> None:
        # Required and Computed is a contradiction the schema rejects outright,
        # and a default on a required attribute could never be reached, so the
        # combination is refused rather than silently ignored.
        with pytest.raises(ValueError, match="required attribute cannot declare a default"):
            a_str(required=True, default=DEFAULT_SIZE)

    def test_write_only_attribute_rejects_a_default(self) -> None:
        # A write-only value is never stored, so it cannot be computed and a
        # default would plan the value that must show null.
        with pytest.raises(ValueError, match="write-only attribute cannot declare a default"):
            a_str(optional=True, write_only=True, default=DEFAULT_SIZE)


class TestConfigDecoding:
    """`from_cty(apply_defaults=True)` applies the *class* default.

    This is the attrs field default declared on the config class, and it is a
    different thing from `PvsAttribute.default` in the schema: the schema
    default is resolved one layer earlier, into the cty value itself, so it
    never arrives here as a null. The flag decides only what a null means, and
    that answer differs between a configuration and state.
    """

    def test_omitted_attribute_decodes_to_its_default(self) -> None:
        config = Widget.from_cty(_config_cty(CtyValue.null(CtyString())), WidgetConfig, apply_defaults=True)

        assert config is not None
        assert config.size == DEFAULT_SIZE

    def test_state_is_decoded_without_defaults(self) -> None:
        """A null in state is a recorded absence, not an omission.

        `WidgetState` declares the same class default as `WidgetConfig`, so if
        state were decoded the way a configuration is, a null the provider
        deliberately stored would come back as "small" and the resource would
        read a value its own state never held.
        """
        state_cty = CONFIG_TYPE.validate({"name": "example", "size": CtyValue.null(CtyString()), "id": "w-1"})

        state = Widget.from_cty(state_cty, WidgetState)

        assert state is not None
        assert state.size is None

    def test_configured_value_overrides_the_default(self) -> None:
        config = Widget.from_cty(_config_cty("large"), WidgetConfig, apply_defaults=True)

        assert config is not None
        assert config.size == "large"

    def test_unknown_value_does_not_become_the_default(self) -> None:
        config = Widget.from_cty(_config_cty(CtyValue.unknown(CtyString())), WidgetConfig, apply_defaults=True)

        assert config is not None
        assert config.size is None


class TestPlanning:
    @pytest.mark.asyncio
    async def test_create_plan_contains_the_default(self) -> None:
        config_cty = _config_cty(CtyValue.null(CtyString()))
        ctx = ResourceContext(
            config=Widget.from_cty(config_cty, WidgetConfig, apply_defaults=True),
            state=None,
            config_cty=config_cty,
        )

        planned_state, _ = await Widget().plan(ctx)

        assert planned_state is not None
        assert planned_state["size"] == DEFAULT_SIZE

    @pytest.mark.asyncio
    async def test_update_plan_contains_the_default(self) -> None:
        config_cty = _config_cty(CtyValue.null(CtyString()))
        ctx = ResourceContext(
            config=Widget.from_cty(config_cty, WidgetConfig, apply_defaults=True),
            state=WidgetState(name="example", size="large", id="w-1"),
            config_cty=config_cty,
        )

        planned_state, _ = await Widget().plan(ctx)

        assert planned_state is not None
        assert planned_state["size"] == DEFAULT_SIZE

    @pytest.mark.asyncio
    async def test_configured_value_wins_over_the_default_in_the_plan(self) -> None:
        config_cty = _config_cty("large")
        ctx = ResourceContext(
            config=Widget.from_cty(config_cty, WidgetConfig, apply_defaults=True),
            state=None,
            config_cty=config_cty,
        )

        planned_state, _ = await Widget().plan(ctx)

        assert planned_state is not None
        assert planned_state["size"] == "large"

    @pytest.mark.asyncio
    async def test_stale_state_value_loses_to_the_default_once_the_config_omits_it(self) -> None:
        """An omitted attribute plans the default, even when state holds another value.

        This mirrors the real pipeline: the configuration reaching `plan()` has
        already had its defaults resolved, and Terraform's proposed new state
        carries the prior value forward. If the plan kept that prior value while
        `ctx.config` reported the default, apply would return a state the plan
        did not contain and fail the refinement check.
        """
        config_cty = resolve_schema_defaults(
            _config_cty(CtyValue.null(CtyString())), Widget.get_schema().block
        )
        assert config_cty is not None
        ctx = ResourceContext(
            config=Widget.from_cty(config_cty, WidgetConfig, apply_defaults=True),
            state=WidgetState(name="example", size="large", id="w-1"),
            planned_state=WidgetState(name="example", size="large", id="w-1"),
            planned_state_cty=CONFIG_TYPE.validate({"name": "example", "size": "large", "id": "w-1"}),
            config_cty=config_cty,
        )

        planned_state, _ = await Widget().plan(ctx)

        assert planned_state is not None
        assert planned_state["size"] == DEFAULT_SIZE

    @pytest.mark.asyncio
    async def test_unknown_value_stays_unknown_in_the_plan(self) -> None:
        config_cty = _config_cty(CtyValue.unknown(CtyString()))
        ctx = ResourceContext(
            config=Widget.from_cty(config_cty, WidgetConfig, apply_defaults=True),
            state=None,
            config_cty=config_cty,
        )

        planned_state, _ = await Widget().plan(ctx)

        assert planned_state is not None
        planned_size = planned_state["size"]
        assert isinstance(planned_size, CtyValue)
        assert planned_size.is_unknown


@attrs.define
class GadgetSettings:
    label: str | None = None
    size: str | None = DEFAULT_SIZE


@attrs.define
class GadgetConfig:
    name: str
    settings: GadgetSettings | None = None
    tier: list[GadgetSettings] | None = None


@attrs.define
class GadgetState:
    name: str
    settings: GadgetSettings | None = None
    tier: list[GadgetSettings] | None = None
    id: str | None = None


class Gadget(BaseResource[Any, GadgetState, GadgetConfig]):
    """A resource whose defaulted attributes live inside nested blocks."""

    config_class = GadgetConfig
    state_class = GadgetState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(
            attributes={
                "name": a_str(required=True),
                "id": a_str(computed=True),
            },
            block_types=[
                b_single(
                    "settings",
                    attributes={"label": a_str(), "size": a_str(default=DEFAULT_SIZE)},
                ),
                b_list(
                    "tier",
                    attributes={"label": a_str(), "size": a_str(default=DEFAULT_SIZE)},
                ),
            ],
        )

    async def _validate_config(self, config: GadgetConfig) -> list[str]:
        return []

    async def read(self, ctx: ResourceContext) -> GadgetState | None:
        return ctx.state

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        return None


GADGET_TYPE = Gadget.get_schema().block.to_cty_type()


def _gadget_cty(size: CtyValue | str) -> CtyValue:
    return GADGET_TYPE.validate(
        {
            "name": "example",
            "id": CtyValue.unknown(CtyString()),
            "settings": {"label": "primary", "size": size},
            "tier": [{"label": "hot", "size": size}],
        }
    )


class TestNestedBlockDefaults:
    """A default inside a nested block has to reach the plan too.

    Terraform knows nothing about provider-side defaults, so an attribute the
    practitioner omitted inside a block that already exists in prior state comes
    back in the proposed new state carrying the *prior* value. The plan has to
    be corrected to the resolved configuration, or apply -- which reads the
    default from `ctx.config` -- returns a state Terraform did not plan.
    """

    def test_omitted_nested_attribute_decodes_to_its_default(self) -> None:
        config_cty = resolve_schema_defaults(
            _gadget_cty(CtyValue.null(CtyString())), Gadget.get_schema().block
        )
        assert config_cty is not None
        config = Gadget.from_cty(config_cty, GadgetConfig, apply_defaults=True)

        assert config is not None
        assert config.settings is not None
        assert config.settings.size == DEFAULT_SIZE

    @pytest.mark.asyncio
    async def test_retained_nested_state_loses_to_the_default_on_update(self) -> None:
        config_cty = resolve_schema_defaults(
            _gadget_cty(CtyValue.null(CtyString())), Gadget.get_schema().block
        )
        assert config_cty is not None
        prior = GadgetState(
            name="example",
            settings=GadgetSettings(label="primary", size="large"),
            tier=[GadgetSettings(label="hot", size="large")],
            id="g-1",
        )
        ctx = ResourceContext(
            config=Gadget.from_cty(config_cty, GadgetConfig, apply_defaults=True),
            state=prior,
            planned_state=prior,
            # Terraform's proposed new state: the block is still configured, so
            # the value it held in prior state is carried forward.
            planned_state_cty=_gadget_cty("large"),
            config_cty=config_cty,
        )

        planned_state, _ = await Gadget().plan(ctx)

        assert planned_state is not None
        assert planned_state["settings"]["size"] == DEFAULT_SIZE
        assert planned_state["tier"][0]["size"] == DEFAULT_SIZE

    @pytest.mark.asyncio
    async def test_configured_nested_value_survives_the_merge(self) -> None:
        config_cty = resolve_schema_defaults(_gadget_cty("large"), Gadget.get_schema().block)
        assert config_cty is not None
        prior = GadgetState(
            name="example",
            settings=GadgetSettings(label="primary", size="large"),
            tier=[GadgetSettings(label="hot", size="large")],
            id="g-1",
        )
        ctx = ResourceContext(
            config=Gadget.from_cty(config_cty, GadgetConfig, apply_defaults=True),
            state=prior,
            planned_state=prior,
            planned_state_cty=_gadget_cty("large"),
            config_cty=config_cty,
        )

        planned_state, _ = await Gadget().plan(ctx)

        assert planned_state is not None
        assert planned_state["settings"]["size"] == "large"
        assert planned_state["settings"]["label"] == "primary"
        assert planned_state["tier"][0]["size"] == "large"

    @pytest.mark.asyncio
    async def test_unknown_nested_value_does_not_become_the_default(self) -> None:
        # An unknown value is one that is not yet known, not an omitted one, so
        # the default must not be substituted for it -- Terraform is about to
        # compute that value and planning "small" would contradict it.
        config_cty = resolve_schema_defaults(
            _gadget_cty(CtyValue.unknown(CtyString())), Gadget.get_schema().block
        )
        assert config_cty is not None
        prior = GadgetState(
            name="example",
            settings=GadgetSettings(label="primary", size="large"),
            id="g-1",
        )
        ctx = ResourceContext(
            config=Gadget.from_cty(config_cty, GadgetConfig, apply_defaults=True),
            state=prior,
            planned_state=prior,
            planned_state_cty=_gadget_cty(CtyValue.unknown(CtyString())),
            config_cty=config_cty,
        )

        planned_state, _ = await Gadget().plan(ctx)

        assert planned_state is not None
        assert planned_state["settings"]["size"] != DEFAULT_SIZE


@attrs.define
class DialSettings:
    label: str | None = None
    size: str | None = None


@attrs.define
class DialConfig:
    name: str
    config: DialSettings | None = None


@attrs.define
class DialState:
    name: str
    config: DialSettings | None = None
    id: str | None = None


class Dial(BaseResource[Any, DialState, DialConfig]):
    """A resource whose defaulted attribute lives inside an `a_obj()` value."""

    config_class = DialConfig
    state_class = DialState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(
            attributes={
                "name": a_str(required=True),
                "config": a_obj({"label": a_str(), "size": a_str(default=DEFAULT_SIZE)}),
                "id": a_str(computed=True),
            }
        )

    async def _validate_config(self, config: DialConfig) -> list[str]:
        return []

    async def read(self, ctx: ResourceContext) -> DialState | None:
        return ctx.state

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        return None


DIAL_TYPE = Dial.get_schema().block.to_cty_type()


def _dial_cty(size: CtyValue | str) -> CtyValue:
    return DIAL_TYPE.validate(
        {
            "name": "example",
            "id": CtyValue.unknown(CtyString()),
            "config": {"label": "primary", "size": size},
        }
    )


class TestObjectAttributeDefaults:
    """A default inside `a_obj()` has to behave like one inside a block.

    An object-typed attribute is a block written as a value, so its members
    declare defaults the same way -- and both the configuration decode and the
    plan have to carry them, or apply returns a state Terraform did not plan.
    """

    def test_omitted_object_member_decodes_to_its_default(self) -> None:
        config_cty = resolve_schema_defaults(_dial_cty(CtyValue.null(CtyString())), Dial.get_schema().block)
        assert config_cty is not None
        config = Dial.from_cty(config_cty, DialConfig, apply_defaults=True)

        assert config is not None
        assert config.config is not None
        assert config.config.size == DEFAULT_SIZE

    @pytest.mark.asyncio
    async def test_retained_object_member_loses_to_the_default_on_update(self) -> None:
        config_cty = resolve_schema_defaults(_dial_cty(CtyValue.null(CtyString())), Dial.get_schema().block)
        assert config_cty is not None
        prior = DialState(name="example", config=DialSettings(label="primary", size="large"), id="d-1")
        ctx = ResourceContext(
            config=Dial.from_cty(config_cty, DialConfig, apply_defaults=True),
            state=prior,
            planned_state=prior,
            planned_state_cty=_dial_cty("large"),
            config_cty=config_cty,
        )

        planned_state, _ = await Dial().plan(ctx)

        assert planned_state is not None
        assert planned_state["config"]["size"] == DEFAULT_SIZE
        assert planned_state["config"]["label"] == "primary"

    @pytest.mark.asyncio
    async def test_configured_object_member_survives_the_merge(self) -> None:
        config_cty = resolve_schema_defaults(_dial_cty("large"), Dial.get_schema().block)
        assert config_cty is not None
        prior = DialState(name="example", config=DialSettings(label="primary", size="large"), id="d-1")
        ctx = ResourceContext(
            config=Dial.from_cty(config_cty, DialConfig, apply_defaults=True),
            state=prior,
            planned_state=prior,
            planned_state_cty=_dial_cty("large"),
            config_cty=config_cty,
        )

        planned_state, _ = await Dial().plan(ctx)

        assert planned_state is not None
        assert planned_state["config"]["size"] == "large"


@attrs.define
class TokenConfig:
    name: str


@attrs.define
class TokenState:
    name: str
    token: str | None = None


class Tokened(BaseResource[Any, TokenState, TokenConfig]):
    """The supported way to give a computed-only attribute a fallback.

    `a_str(computed=True, default=...)` is refused by the schema, so the
    fallback lives in the resource's own create logic, where the provider's
    other computed values are produced.
    """

    config_class = TokenConfig
    state_class = TokenState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(
            attributes={
                "name": a_str(required=True),
                "token": a_str(computed=True),
            }
        )

    async def _validate_config(self, config: TokenConfig) -> list[str]:
        return []

    async def _create(self, ctx: ResourceContext, base_plan: dict[str, Any]) -> tuple[dict[str, Any], None]:
        base_plan["token"] = "unset"
        return base_plan, None

    async def read(self, ctx: ResourceContext) -> TokenState | None:
        return ctx.state

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        return None


TOKEN_TYPE = Tokened.get_schema().block.to_cty_type()


class TestComputedOnlyAttributes:
    """A computed-only attribute is the provider's alone, defaults included."""

    def test_schema_refuses_a_computed_only_default(self) -> None:
        with pytest.raises(ValueError, match="computed-only attribute cannot declare a default"):
            s_resource(attributes={"token": a_str(computed=True, default="unset")})

    @pytest.mark.asyncio
    async def test_resource_supplies_the_fallback_on_create(self) -> None:
        config_cty = TOKEN_TYPE.validate({"name": "example", "token": CtyValue.null(CtyString())})
        ctx = ResourceContext(
            config=Tokened.from_cty(config_cty, TokenConfig, apply_defaults=True),
            state=None,
            config_cty=config_cty,
        )

        planned_state, _ = await Tokened().plan(ctx)

        assert planned_state is not None
        assert planned_state["token"] == "unset"

    @pytest.mark.asyncio
    async def test_computed_value_is_retained_on_update(self) -> None:
        # Nothing in the configuration can contradict a computed-only attribute,
        # so Terraform's proposed new state carries the previous value forward
        # and the plan leaves it alone. This is the retention that a schema
        # default would have silently overridden.
        config_cty = TOKEN_TYPE.validate({"name": "example", "token": CtyValue.null(CtyString())})
        prior = TokenState(name="example", token="computed-last-run")
        ctx = ResourceContext(
            config=Tokened.from_cty(config_cty, TokenConfig, apply_defaults=True),
            state=prior,
            planned_state=prior,
            planned_state_cty=TOKEN_TYPE.validate({"name": "example", "token": "computed-last-run"}),
            config_cty=config_cty,
        )

        planned_state, _ = await Tokened().plan(ctx)

        assert planned_state is not None
        assert planned_state["token"] == "computed-last-run"


# 🐍🏗️🔚
