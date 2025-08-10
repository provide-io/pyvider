import pytest

from pyvider.components.resources.private_state_verifier import (
    PrivateStateVerifierResource,
)
from pyvider.conversion import marshal, unmarshal
from pyvider.hub import hub
from pyvider.protocols.tfprotov6.handlers import (
    ApplyResourceChangeHandler,
    PlanResourceChangeHandler,
)
import pyvider.protocols.tfprotov6.protobuf as pb


@pytest.mark.asyncio
async def test_private_state_verifier_lifecycle(encryption_key_env, provider_in_hub):
    resource_name = "pyvider_private_state_verifier"
    hub.register("resource", resource_name, PrivateStateVerifierResource)
    try:
        schema = PrivateStateVerifierResource.get_schema()
        raw_config = {"input_value": "test-run"}
        config_dv = marshal(raw_config, schema=schema.block)
        plan_request = pb.PlanResourceChange.Request(
            type_name=resource_name,
            config=config_dv,
            proposed_new_state=config_dv
        )
        plan_response = await PlanResourceChangeHandler(plan_request, context=None)
        assert not plan_response.diagnostics, f"Plan phase returned diagnostics: {plan_response.diagnostics}"
        assert plan_response.planned_private, "Plan phase did not return a private state"
        apply_request = pb.ApplyResourceChange.Request(
            type_name=resource_name,
            config=plan_request.config,
            planned_state=plan_response.planned_state,
            planned_private=plan_response.planned_private
        )
        apply_response = await ApplyResourceChangeHandler(apply_request, context=None)
        assert not apply_response.diagnostics, f"Apply phase returned diagnostics: {apply_response.diagnostics[0].summary}"
        final_state = unmarshal(apply_response.new_state, schema=schema.block)
        assert final_state.value["input_value"].value == "test-run"
        assert final_state.value["decrypted_token"].value == "SECRET_FOR_TEST-RUN"
    finally:
        hub.unregister("resource", resource_name)
