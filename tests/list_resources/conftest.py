#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Shared components for list-resource tests."""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from typing import Any, ClassVar

import attrs
import pytest

from pyvider.hub import hub
from pyvider.list_resources import BaseListResource, ListResourceContext, ListResult
from pyvider.schema import PvsSchema, a_bool, a_num, a_str, s_identity, s_resource

RESOURCE_TYPE = "demo_widget"
# A list resource shares its name with the managed resource it lists: Terraform
# resolves results against the managed type of the same name and refuses to list
# when there is none (internal/plugin6/grpc_provider.go:1341-1345).
LIST_TYPE = RESOURCE_TYPE


@attrs.define
class WidgetListConfig:
    """Configuration block for the demo list resource."""

    region: str | None = None
    include_archived: bool | None = None


class DemoWidget:
    """A managed resource that supplies identity and state schemas."""

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(
            attributes={
                "id": a_str(required=True),
                "name": a_str(required=True),
                "size": a_num(),
            }
        )

    @classmethod
    def get_identity_schema(cls) -> PvsSchema:
        return s_identity(attributes={"id": a_str(required=True)})


class DemoWidgetList(BaseListResource[WidgetListConfig]):
    """Lists demo widgets, borrowing the managed resource's schemas."""

    config_class = WidgetListConfig
    resource_type = RESOURCE_TYPE

    #: Results the instance will yield; tests rewrite this per case.
    results: ClassVar[list[ListResult]] = []
    #: Validation errors returned by validate(); empty means valid.
    validation_errors: ClassVar[list[str]] = []
    #: Set by list() so tests can assert what the framework passed in.
    seen_contexts: ClassVar[list[ListResourceContext[WidgetListConfig]]] = []

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(
            attributes={
                "region": a_str(),
                "include_archived": a_bool(),
            }
        )

    async def validate(self, config: WidgetListConfig | None) -> list[str]:
        return list(type(self).validation_errors)

    async def list(self, ctx: ListResourceContext[WidgetListConfig]) -> AsyncIterator[ListResult]:
        type(self).seen_contexts.append(ctx)
        for result in type(self).results:
            yield result


def widget_result(identifier: str, **overrides: Any) -> ListResult:
    """Build a result for the demo widget resource."""
    payload: dict[str, Any] = {
        "identity": {"id": identifier},
        "display_name": f"widget {identifier}",
        "resource_object": {"id": identifier, "name": f"widget-{identifier}", "size": 1},
    }
    payload.update(overrides)
    return ListResult(**payload)


@pytest.fixture
def demo_widget() -> Iterator[type[DemoWidget]]:
    hub.register("resource", RESOURCE_TYPE, DemoWidget)
    yield DemoWidget
    hub.unregister("resource", RESOURCE_TYPE)


@pytest.fixture
def demo_list(demo_widget: type[DemoWidget]) -> Iterator[type[DemoWidgetList]]:
    DemoWidgetList.results = []
    DemoWidgetList.validation_errors = []
    DemoWidgetList.seen_contexts = []
    hub.register("list_resource", LIST_TYPE, DemoWidgetList)
    yield DemoWidgetList
    hub.unregister("list_resource", LIST_TYPE)
    DemoWidgetList.results = []
    DemoWidgetList.validation_errors = []
    DemoWidgetList.seen_contexts = []


# 🐍🏗️🔚
