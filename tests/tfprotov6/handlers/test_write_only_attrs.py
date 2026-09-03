from typing import Any

from attrs import define
import pytest

from pyvider.conversion import marshal
from pyvider.hub import hub
from pyvider.protocols.tfprotov6.handlers.apply_resource_change import _apply_resource_change_impl
from pyvider.protocols.tfprotov6.handlers.plan_resource_change import _plan_resource_change_impl
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.resources.base import BaseResource
from pyvider.schema import a_str, s_resource


@define
class SecretConfig:
    my_secret: str = ""
    id: str = ""


@define
class SecretConfigNoSecretField:
    id: str = ""


@pytest.mark.asyncio
async def test_write_only_end_to_end(provider_in_hub: Any) -> None:
    class SecretResource(BaseResource):
        config_class = SecretConfig
        state_class = SecretConfig

        @classmethod
        def get_schema(cls) -> Any:
            return s_resource(
                attributes={
                    "id": a_str(computed=True),
                    "my_secret": a_str(required=True, write_only=True),
                }
            )

        async def _validate_config(self, config):
            return []

        async def _create(self, ctx, plan):
            plan["id"] = "test-id"
            return plan, None

        async def _create_apply(self, ctx):
            assert ctx.config.my_secret == "super-secret-value"
            return ctx.planned_state, ctx.private_state

        async def read(self, ctx):
            return ctx.state

        async def _delete_apply(self, ctx):
            pass

    hub.register("resource", "e2e_secret", SecretResource)
    try:
        schema = SecretResource.get_schema()
        cty_type = schema.block.to_cty_type()
        config_cty = cty_type.validate({"my_secret": "super-secret-value"})
        config_dv = marshal(config_cty, schema=schema.block)

        plan_req = pb.PlanResourceChange.Request(
            type_name="e2e_secret",
            config=config_dv,
            proposed_new_state=config_dv,
        )
        plan_res = await _plan_resource_change_impl(plan_req, context=None)
        assert len(plan_res.diagnostics) == 0

        from pyvider.conversion import unmarshal

        planned_state = unmarshal(plan_res.planned_state, schema=schema.block)
        assert (
            "my_secret" not in planned_state.value
            or planned_state.value["my_secret"] is None
            or planned_state.value["my_secret"].is_null
        )

        apply_req = pb.ApplyResourceChange.Request(
            type_name="e2e_secret",
            config=config_dv,
            planned_state=plan_res.planned_state,
        )
        apply_res = await _apply_resource_change_impl(apply_req, context=None)
        assert len(apply_res.diagnostics) == 0

        new_state = unmarshal(apply_res.new_state, schema=schema.block)
        assert (
            "my_secret" not in new_state.value
            or new_state.value["my_secret"] is None
            or new_state.value["my_secret"].is_null
        )
    finally:
        hub.unregister("resource", "e2e_secret")


@pytest.mark.asyncio
async def test_write_only_required_attr_omitted_from_state_class(provider_in_hub: Any) -> None:
    """Regression test for issue #50: a required+write_only attribute must not
    need to be declared on the state class just to satisfy apply-time validation.
    """

    class SecretResourceNoField(BaseResource):
        config_class = SecretConfig
        state_class = SecretConfigNoSecretField

        @classmethod
        def get_schema(cls) -> Any:
            return s_resource(
                attributes={
                    "id": a_str(computed=True),
                    "my_secret": a_str(required=True, write_only=True),
                }
            )

        async def _validate_config(self, config):
            return []

        async def _create(self, ctx, plan):
            plan["id"] = "test-id"
            return plan, None

        async def _create_apply(self, ctx):
            assert ctx.config.my_secret == "super-secret-value"
            return ctx.planned_state, ctx.private_state

        async def read(self, ctx):
            return ctx.state

        async def _delete_apply(self, ctx):
            pass

    hub.register("resource", "e2e_secret_no_field", SecretResourceNoField)
    try:
        schema = SecretResourceNoField.get_schema()
        cty_type = schema.block.to_cty_type()
        config_cty = cty_type.validate({"my_secret": "super-secret-value"})
        config_dv = marshal(config_cty, schema=schema.block)

        plan_req = pb.PlanResourceChange.Request(
            type_name="e2e_secret_no_field",
            config=config_dv,
            proposed_new_state=config_dv,
        )
        plan_res = await _plan_resource_change_impl(plan_req, context=None)
        assert len(plan_res.diagnostics) == 0

        from pyvider.conversion import unmarshal

        apply_req = pb.ApplyResourceChange.Request(
            type_name="e2e_secret_no_field",
            config=config_dv,
            planned_state=plan_res.planned_state,
        )
        apply_res = await _apply_resource_change_impl(apply_req, context=None)
        assert len(apply_res.diagnostics) == 0, apply_res.diagnostics

        new_state = unmarshal(apply_res.new_state, schema=schema.block)
        assert (
            "my_secret" not in new_state.value
            or new_state.value["my_secret"] is None
            or new_state.value["my_secret"].is_null
        )
        assert new_state.value["id"].value == "test-id"
    finally:
        hub.unregister("resource", "e2e_secret_no_field")
