#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""A full v6.11 session driven through ProviderHandler.

The per-RPC tests exercise each handler in isolation. This walks the sequence a
Terraform run actually performs -- discover, configure the state store, take a
lock, write and read state back, release, list, then validate/plan/invoke an
action -- against a durable filesystem backend and a provider that registers a
resource, a list resource, and an action. Its job is to catch the failures that
only appear when the pieces are wired together: a lock that does not survive
between two RPCs, state that a second provider process cannot see, a component
advertised in metadata that the RPC then cannot resolve.
"""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from pathlib import Path
from typing import Any, ClassVar

import attrs
import pytest

from pyvider.actions import ActionContext, ActionPlan, ActionProgress, BaseAction, register_action
from pyvider.conversion import marshal, unmarshal_identity
from pyvider.handler import ProviderHandler
from pyvider.hub import hub
from pyvider.list_resources import (
    BaseListResource,
    ListResourceContext,
    ListResult,
    register_list_resource,
)
from pyvider.protocols.tfprotov6.handlers.get_metadata import GetMetadataHandler
from pyvider.protocols.tfprotov6.handlers.state_store_handlers import reset_state_stores
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.providers.base import BaseProvider, ProviderMetadata
from pyvider.resources.base import BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.schema import PvsSchema, a_bool, a_num, a_str, s_identity, s_resource
from pyvider.state_stores import FileSystemStateStore, state_store_manager

pytestmark = pytest.mark.integration

RESOURCE_TYPE = "e2e_widget"
# A list resource is registered under the managed resource's own name: Terraform
# looks its results up against the managed resource type with the same name and
# refuses to list at all when there is no such type
# (internal/plugin6/grpc_provider.go:1341-1345). This fixture used to use
# "e2e_widget_list", which passes in-process and fails against real Terraform.
LIST_TYPE = RESOURCE_TYPE
ACTION_TYPE = "e2e_widget_reboot"
STORE_TYPE = "e2e_store"
STATE_ID = "production"

WIDGETS = [
    {"id": "w-1", "name": "alpha", "size": 1},
    {"id": "w-2", "name": "beta", "size": 2},
    {"id": "w-3", "name": "gamma", "size": 3},
]


@attrs.define
class WidgetState:
    id: str | None = None
    name: str | None = None
    size: int | None = None


@attrs.define
class WidgetListConfig:
    name_prefix: str | None = None
    include_archived: bool | None = None


@attrs.define
class RebootConfig:
    target: str | None = None


class E2EWidget(BaseResource[Any, WidgetState, WidgetState]):
    config_class = WidgetState
    state_class = WidgetState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(
            {"id": a_str(required=True), "name": a_str(required=True), "size": a_num(computed=True)}
        )

    @classmethod
    def get_identity_schema(cls) -> PvsSchema:
        return s_identity(attributes={"id": a_str(required=True)})

    async def generate_config(self, state: Any) -> Any:
        # Drop the computed attribute so the result is a configuration a
        # practitioner could have written by hand.
        return WidgetState(id=state.id, name=state.name, size=None)

    async def _validate_config(self, config: Any) -> list[str]:  # pragma: no cover - unused here
        return []

    async def read(self, ctx: ResourceContext) -> WidgetState | None:  # pragma: no cover - unused here
        return None

    async def _delete_apply(self, ctx: ResourceContext) -> None:  # pragma: no cover - unused here
        return None


class E2EWidgetList(BaseListResource[WidgetListConfig]):
    config_class = WidgetListConfig
    resource_type = RESOURCE_TYPE

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(attributes={"name_prefix": a_str(), "include_archived": a_bool()})

    async def validate(self, config: WidgetListConfig | None) -> list[str]:
        if config is not None and config.name_prefix == "":
            return ["name_prefix must not be empty"]
        return []

    async def list(self, ctx: ListResourceContext[WidgetListConfig]) -> AsyncIterator[ListResult]:
        prefix = ctx.config.name_prefix if ctx.config and ctx.config.name_prefix else ""
        for widget in WIDGETS:
            if not str(widget["name"]).startswith(prefix):
                continue
            yield ListResult(
                identity={"id": widget["id"]},
                display_name=str(widget["name"]),
                resource_object=WidgetState(**widget),  # type: ignore[arg-type]
            )


class E2EReboot(BaseAction[RebootConfig]):
    config_class = RebootConfig

    invoked: ClassVar[list[str]] = []

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(attributes={"target": a_str(required=True)})

    async def validate(self, config: RebootConfig | None) -> list[str]:
        if config is None or not config.target:
            return ["target is required"]
        return []

    async def plan(self, ctx: ActionContext[RebootConfig]) -> ActionPlan:
        return ActionPlan(warnings=("reboot is disruptive",))

    async def invoke(self, ctx: ActionContext[RebootConfig]) -> AsyncIterator[ActionProgress]:
        target = ctx.config.target if ctx.config else ""
        type(self).invoked.append(str(target))
        yield ActionProgress(message=f"draining {target}")
        yield ActionProgress(message=f"rebooting {target}")


@pytest.fixture
def provider(tmp_path: Path) -> Iterator[FileSystemStateStore]:
    """Register the components and bind a durable store, then tear it all down."""
    E2EReboot.invoked = []
    reset_state_stores()

    # The unary RPCs resolve the provider from the hub before dispatching, so a
    # session test needs one registered even though these RPCs never read it.
    previous_provider = hub.get_component("singleton", "provider")
    hub.register(
        "singleton",
        "provider",
        BaseProvider(metadata=ProviderMetadata(name="e2e", version="0.0.0")),
    )

    hub.register("resource", RESOURCE_TYPE, E2EWidget)
    register_list_resource(LIST_TYPE)(E2EWidgetList)
    register_action(ACTION_TYPE)(E2EReboot)

    backend = FileSystemStateStore(root=tmp_path / "state")
    state_store_manager.register_instance(STORE_TYPE, backend)

    yield backend

    hub.unregister("resource", RESOURCE_TYPE)
    hub.unregister("list_resource", LIST_TYPE)
    hub.unregister("action", ACTION_TYPE)
    if previous_provider is None:
        hub.unregister("singleton", "provider")
    else:
        hub.register("singleton", "provider", previous_provider)
    reset_state_stores()
    E2EReboot.invoked = []


async def _write_state(handler: ProviderHandler, payload: bytes) -> pb.WriteStateBytes.Response:
    async def chunks() -> AsyncIterator[pb.WriteStateBytes.RequestChunk]:
        yield pb.WriteStateBytes.RequestChunk(
            meta=pb.RequestChunkMeta(type_name=STORE_TYPE, state_id=STATE_ID),
            bytes=payload,
            total_length=len(payload),
            range=pb.StateRange(start=0, end=len(payload)),
        )

    return await handler.WriteStateBytes(chunks(), context=None)


def _no_errors(diagnostics: Any) -> bool:
    return not [d for d in diagnostics if d.severity == pb.Diagnostic.ERROR]


@pytest.mark.asyncio
async def test_a_full_v6_11_session(provider: FileSystemStateStore) -> None:
    handler = ProviderHandler()
    payload = b'{"version": 4, "resources": []}'

    # 1. Discovery: everything registered is advertised.
    metadata = await GetMetadataHandler(pb.GetMetadata.Request(), context=None)
    assert {entry.type_name for entry in metadata.resources} >= {RESOURCE_TYPE}
    assert {entry.type_name for entry in metadata.list_resources} == {LIST_TYPE}
    assert {entry.type_name for entry in metadata.actions} == {ACTION_TYPE}

    # 2. Configure the state store and negotiate a chunk size.
    configure = pb.ConfigureStateStore.Request(type_name=STORE_TYPE)
    configure.capabilities.chunk_size = 8
    configured = await handler.ConfigureStateStore(configure, context=None)
    assert configured.capabilities.chunk_size == 8
    assert _no_errors(configured.diagnostics)

    # 3. Take the lock, then confirm a competing request is refused while it is held.
    lock_request = pb.LockState.Request(type_name=STORE_TYPE, state_id=STATE_ID, operation="apply")
    lock = await handler.LockState(lock_request, context=None)
    assert lock.lock_id
    contender = await handler.LockState(lock_request, context=None)
    assert contender.lock_id == ""
    assert contender.diagnostics[0].summary == "State is already locked"

    # 4. Write state and read it back through the negotiated chunking.
    assert _no_errors((await _write_state(handler, payload)).diagnostics)
    read_request = pb.ReadStateBytes.Request(type_name=STORE_TYPE, state_id=STATE_ID)
    chunks = [chunk async for chunk in handler.ReadStateBytes(read_request, context=None)]
    assert b"".join(chunk.bytes for chunk in chunks) == payload
    assert all(len(chunk.bytes) <= 8 for chunk in chunks)

    # 5. The state is on disk, so a separate backend instance -- a restarted or
    #    second provider process -- sees the same bytes.
    assert await FileSystemStateStore(root=provider.root).read_state(STORE_TYPE, STATE_ID) == payload

    # 6. Release the lock; the next acquisition succeeds.
    unlock = await handler.UnlockState(
        pb.UnlockState.Request(type_name=STORE_TYPE, state_id=STATE_ID, lock_id=lock.lock_id),
        context=None,
    )
    assert _no_errors(unlock.diagnostics)
    assert (await handler.LockState(lock_request, context=None)).lock_id

    # 7. The state is enumerable and deletable.
    states = await handler.GetStates(pb.GetStates.Request(type_name=STORE_TYPE), context=None)
    assert list(states.state_id) == [STATE_ID]

    # 8. Validate and run a list, filtered by the list block's own configuration.
    list_config = marshal(
        {"name_prefix": "b", "include_archived": False}, schema=E2EWidgetList.get_schema().block
    )
    validated = await handler.ValidateListResourceConfig(
        pb.ValidateListResourceConfig.Request(type_name=LIST_TYPE, config=list_config), context=None
    )
    assert _no_errors(validated.diagnostics)

    list_request = pb.ListResource.Request(
        type_name=LIST_TYPE, config=list_config, include_resource_object=True
    )
    events = [event async for event in handler.ListResource(list_request, context=None)]
    assert [event.display_name for event in events] == ["beta"]
    identity = unmarshal_identity(events[0].identity, E2EWidget.get_identity_schema())
    assert identity == {"id": "w-2"}
    assert events[0].HasField("resource_object")

    # 9. Validate, plan, and invoke the action.
    action_config = marshal({"target": "w-2"}, schema=E2EReboot.get_schema().block)
    action_validated = await handler.ValidateActionConfig(
        pb.ValidateActionConfig.Request(type_name=ACTION_TYPE, config=action_config), context=None
    )
    assert _no_errors(action_validated.diagnostics)

    planned = await handler.PlanAction(
        pb.PlanAction.Request(action_type=ACTION_TYPE, config=action_config), context=None
    )
    assert [d.summary for d in planned.diagnostics] == ["reboot is disruptive"]
    assert _no_errors(planned.diagnostics)

    invoke_request = pb.InvokeAction.Request(action_type=ACTION_TYPE, config=action_config)
    action_events = [event async for event in handler.InvokeAction(invoke_request, context=None)]
    assert [event.WhichOneof("type") for event in action_events] == [
        "progress",
        "progress",
        "completed",
    ]
    assert [event.progress.message for event in action_events[:2]] == [
        "draining w-2",
        "rebooting w-2",
    ]
    assert _no_errors(action_events[-1].completed.diagnostics)
    assert E2EReboot.invoked == ["w-2"]

    # 10. GenerateResourceConfig reaches the resource's hook.
    state = marshal({"id": "w-2", "name": "beta", "size": 2}, schema=E2EWidget.get_schema().block)
    generated = await handler.GenerateResourceConfig(
        pb.GenerateResourceConfig.Request(type_name=RESOURCE_TYPE, state=state), context=None
    )
    assert _no_errors(generated.diagnostics)
    assert generated.config != state

    # 11. Deleting the state leaves the store empty.
    deleted = await handler.DeleteState(
        pb.DeleteState.Request(type_name=STORE_TYPE, state_id=STATE_ID), context=None
    )
    assert _no_errors(deleted.diagnostics)
    remaining = await handler.GetStates(pb.GetStates.Request(type_name=STORE_TYPE), context=None)
    assert list(remaining.state_id) == []


@pytest.mark.asyncio
async def test_invalid_input_is_rejected_at_every_boundary(provider: FileSystemStateStore) -> None:
    """Each validation hook actually refuses bad input rather than accepting it."""
    handler = ProviderHandler()

    empty_prefix = marshal({"name_prefix": ""}, schema=E2EWidgetList.get_schema().block)
    list_result = await handler.ValidateListResourceConfig(
        pb.ValidateListResourceConfig.Request(type_name=LIST_TYPE, config=empty_prefix), context=None
    )
    assert [d.summary for d in list_result.diagnostics] == ["name_prefix must not be empty"]

    action_result = await handler.ValidateActionConfig(
        pb.ValidateActionConfig.Request(type_name=ACTION_TYPE), context=None
    )
    assert [d.summary for d in action_result.diagnostics] == ["target is required"]

    unknown_action = await handler.PlanAction(
        pb.PlanAction.Request(action_type="not_registered"), context=None
    )
    assert not _no_errors(unknown_action.diagnostics)


@pytest.mark.asyncio
async def test_state_locked_by_one_handler_is_visible_to_another(
    provider: FileSystemStateStore,
) -> None:
    """A lock is a property of the store, not of the handler that took it.

    Two ProviderHandler instances stand in for two gRPC connections into the
    same provider: the lock one takes must block the other and be releasable
    by the lock id, not by identity of the caller.
    """
    first = ProviderHandler()
    second = ProviderHandler()
    request = pb.LockState.Request(type_name=STORE_TYPE, state_id=STATE_ID, operation="apply")

    lock = await first.LockState(request, context=None)
    blocked = await second.LockState(request, context=None)
    assert lock.lock_id
    assert blocked.lock_id == ""

    released = await second.UnlockState(
        pb.UnlockState.Request(type_name=STORE_TYPE, state_id=STATE_ID, lock_id=lock.lock_id),
        context=None,
    )
    assert _no_errors(released.diagnostics)
    assert (await second.LockState(request, context=None)).lock_id


# 🐍🏗️🔚
