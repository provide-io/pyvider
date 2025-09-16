from typing import Any

import attrs
import msgpack
import pytest

from pyvider.common.encryption import CONFIG_KEY_NAME, decrypt, encrypt
from pyvider.conversion import marshal
from pyvider.exceptions import FrameworkConfigurationError
from pyvider.hub import hub
from pyvider.protocols.tfprotov6.handlers import (
    ApplyResourceChangeHandler,
    PlanResourceChangeHandler,
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.resources.base import BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.resources.private_state import PrivateState
from pyvider.schema import a_str, s_resource


@attrs.define(frozen=True)
class MockPrivateState(PrivateState):
    session_id: str
    version: int


@attrs.define(frozen=True)
class MockConfig:
    name: str


class EncryptionTestResource(BaseResource):
    config_class = MockConfig
    private_state_class = MockPrivateState

    @classmethod
    def get_schema(cls):
        return s_resource({"name": a_str()})

    async def _validate_config(self, config: Any) -> list[str]:
        return []

    async def _create(self, ctx: ResourceContext, base_plan: dict[str, Any]):
        private = MockPrivateState(session_id="abc-123", version=1)
        return base_plan, private

    async def _create_apply(self, ctx: ResourceContext):
        assert ctx.private_state == MockPrivateState(session_id="abc-123", version=1)
        return ctx.planned_state, ctx.private_state

    async def read(self, ctx):
        pass

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        pass


def test_encryption_raises_error_when_secret_is_missing(monkeypatch):
    env_var_name = f"PYVIDER_{CONFIG_KEY_NAME.upper()}"
    monkeypatch.delenv(env_var_name, raising=False)
    monkeypatch.setattr("pyvider.common.config.PyviderConfig.get", lambda self, key, default=None: None)
    from pyvider.common import encryption

    encryption._ENCRYPTION_KEY = None
    with pytest.raises(FrameworkConfigurationError, match="Private state shared secret not found"):
        encrypt(b"some data")


def test_encryption_decryption_roundtrip(encryption_key_env):
    original_plaintext = b"this is a very secret message"
    encrypted = encrypt(original_plaintext)
    decrypted = decrypt(encrypted)
    assert decrypted == original_plaintext


@pytest.mark.asyncio
async def test_full_lifecycle_with_encryption(encryption_key_env, provider_in_hub):
    resource_name = "encryption_test_resource"
    hub.register("resource", resource_name, EncryptionTestResource)
    try:
        schema = EncryptionTestResource.get_schema()
        raw_config = {"name": "test"}
        config_dv = marshal(raw_config, schema=schema.block)
        plan_request = pb.PlanResourceChange.Request(
            type_name=resource_name, config=config_dv, proposed_new_state=config_dv
        )
        plan_response = await PlanResourceChangeHandler(plan_request, context=None)
        assert not plan_response.diagnostics, f"Plan phase returned diagnostics: {plan_response.diagnostics}"
        assert plan_response.planned_private
        raw_private_bytes = msgpack.packb(attrs.asdict(MockPrivateState(session_id="abc-123", version=1)))
        assert decrypt(plan_response.planned_private) == raw_private_bytes
        apply_request = pb.ApplyResourceChange.Request(
            type_name=resource_name,
            config=plan_request.config,
            planned_state=plan_response.planned_state,
            planned_private=plan_response.planned_private,
        )
        apply_response = await ApplyResourceChangeHandler(apply_request, context=None)
        assert not apply_response.diagnostics
    finally:
        hub.unregister("resource", resource_name)
