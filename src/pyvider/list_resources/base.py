#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""The list-resource contract.

A list resource answers Terraform's ``ListResource`` RPC: given a filter
configuration, stream the resources that exist in the remote system. Each
result is keyed by resource identity, which is how Terraform ties a listed
instance back to a managed resource type.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator, Sequence
from typing import Generic, TypeVar

from pyvider.lint import LintContext, LintFinding
from pyvider.list_resources.types import ListResourceContext, ListResult
from pyvider.schema import PvsSchema

ConfigType = TypeVar("ConfigType")


class BaseListResource(ABC, Generic[ConfigType]):
    """Abstract base class for a listable resource type."""

    #: attrs class describing the list block's configuration.
    config_class: type[ConfigType] | None = None

    #: Name of the managed resource type these results describe. Setting it
    #: lets the framework borrow that resource's identity and state schemas
    #: instead of making every list resource restate them.
    resource_type: str | None = None

    @classmethod
    @abstractmethod
    def get_schema(cls) -> PvsSchema:
        """Return the schema of the list block's configuration."""

    @classmethod
    def get_identity_schema(cls) -> PvsSchema | None:
        """Return the identity schema used to encode results.

        The default defers to the managed resource named by ``resource_type``.
        Identity is mandatory for list resources, so a class that sets neither
        ``resource_type`` nor an override here cannot emit results -- the
        handler reports that as a diagnostic rather than emitting identityless
        events Terraform would reject.
        """
        if not cls.resource_type:
            return None

        from pyvider.hub import hub

        resource_class = hub.get_component("resource", cls.resource_type)
        if resource_class is None:
            return None
        getter = getattr(resource_class, "get_identity_schema", None)
        if getter is None:
            return None
        schema: PvsSchema | None = getter()
        return schema

    @classmethod
    def get_resource_object_schema(cls) -> PvsSchema | None:
        """Return the schema used to encode ``resource_object`` values.

        Defaults to the managed resource's own schema, which is what Terraform
        expects a listed resource object to conform to.
        """
        if not cls.resource_type:
            return None

        from pyvider.hub import hub

        resource_class = hub.get_component("resource", cls.resource_type)
        if resource_class is None:
            return None
        getter = getattr(resource_class, "get_schema", None)
        if getter is None:
            return None
        schema: PvsSchema | None = getter()
        return schema

    async def validate(self, config: ConfigType | None) -> list[str]:
        """Validate the list block's configuration.

        Returns human-readable error messages; empty means valid.
        """
        return []

    async def lint(self, ctx: LintContext[ConfigType]) -> Sequence[LintFinding]:
        """Return opt-in advisory findings for a semantically valid configuration."""
        return ()

    @abstractmethod
    def list(self, ctx: ListResourceContext[ConfigType]) -> AsyncIterator[ListResult]:
        """Stream the resources matching ``ctx``.

        Implemented as an async generator. Yielding lazily matters: Terraform
        consumes the RPC as a stream and may stop early once ``ctx.limit`` is
        reached, so building the whole list up front wastes work that will be
        discarded.
        """


# 🐍🏗️🔚
