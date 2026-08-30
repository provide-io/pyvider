#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""A contract violation must say which attribute broke it.

`is_valid_refinement` already walks objects and prefixes the offending
attribute name onto its reason, and `ResourceLifecycleContractError` carries it
as `detail`. But the error is a foundation `StateError` rather than a
`PyviderError`, so it missed the `except (CtyValidationError, PyviderError)`
clause that routes to `create_diagnostic_from_exception` and fell through to
the generic handler, which rebuilds the message from `str(e)` alone and drops
the detail.

The practitioner was then told only that "the final state is not a valid
refinement of the planned state", with nothing naming the attribute -- so the
only way to find it was to bisect the resource.
"""

from __future__ import annotations

from typing import Any

import attrs
import pytest

from pyvider.conversion import marshal
from pyvider.cty import CtyValue
from pyvider.hub import hub
from pyvider.protocols.tfprotov6.handlers.apply_resource_change import (
    ApplyResourceChangeHandler,
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.providers.base import BaseProvider, ProviderMetadata
from pyvider.resources.base import BaseResource
from pyvider.schema import PvsSchema, a_str, s_resource

RESOURCE = "contract_violator"


@attrs.define
class _State:
    name: str | None = None
    colour: str | None = None


class _ContractViolator(BaseResource[Any, _State, _State]):
    """Applies a value for `colour` that its plan did not promise."""

    config_class = _State
    state_class = _State

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(attributes={"name": a_str(required=True), "colour": a_str(optional=True)})

    async def _validate_config(self, config: _State) -> list[str]:
        return []

    async def read(self, ctx: Any) -> _State | None:
        return ctx.state

    async def _create_apply(self, ctx: Any) -> tuple[_State, None]:
        # The plan said "blue"; apply says otherwise. A concrete value may not
        # become a different concrete value.
        return _State(name=ctx.planned_state.name, colour="red"), None

    async def _delete_apply(self, ctx: Any) -> None:
        return None


@pytest.fixture
def violator() -> Any:
    previous = hub.get_component("singleton", "provider")
    hub.register(
        "singleton",
        "provider",
        BaseProvider(metadata=ProviderMetadata(name="test", version="0")),
    )
    hub.register("resource", RESOURCE, _ContractViolator)
    yield _ContractViolator
    hub.unregister("resource", RESOURCE)
    if previous is not None:
        hub.register("singleton", "provider", previous)


@pytest.mark.asyncio
async def test_the_diagnostic_names_the_offending_attribute(violator: Any) -> None:
    block = _ContractViolator.get_schema().block
    planned = marshal({"name": "x", "colour": "blue"}, schema=block)

    response = await ApplyResourceChangeHandler(
        pb.ApplyResourceChange.Request(
            type_name=RESOURCE,
            # A create: no prior state, so _create_apply runs.
            prior_state=marshal(CtyValue.null(block.to_cty_type()), schema=block),
            planned_state=planned,
            config=marshal({"name": "x", "colour": "blue"}, schema=block),
        ),
        context=None,
    )

    assert response.diagnostics, "a contract violation must be reported"
    text = "\n".join(d.summary + d.detail for d in response.diagnostics)
    assert "colour" in text, f"the diagnostic must name the attribute that broke the contract; got: {text}"


# 🐍🏗️🔚
