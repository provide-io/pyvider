#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""The ListResource RPC: stream provider-registered listable resources.

Terraform consumes this RPC as a stream and stops reading once it has the
number of results it asked for, so results are forwarded one at a time as the
provider yields them rather than collected first.
"""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterable
from typing import Any

from provide.foundation import logger

from pyvider.conversion import marshal, marshal_identity
from pyvider.list_resources import ListResourceContext, ListResult
from pyvider.protocols.tfprotov6.handlers._component_config import decode_config
from pyvider.protocols.tfprotov6.handlers._diagnostics import (
    error_diagnostic,
    unknown_type_diagnostic,
    warning_diagnostic,
)
from pyvider.protocols.tfprotov6.handlers.utils import get_filtered_components
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.schema import PvsSchema


def _error_event(summary: str, detail: str = "") -> pb.ListResource.Event:
    """Report a failure through the stream, which has no response message."""
    return pb.ListResource.Event(diagnostic=[error_diagnostic(summary, detail)])


def _unknown_list_resource_event(type_name: str, registered: Iterable[str]) -> pb.ListResource.Event:
    return pb.ListResource.Event(
        diagnostic=[unknown_type_diagnostic("list resource", type_name, registered, "@register_list_resource")]
    )


def _build_event(
    result: ListResult,
    identity_schema: PvsSchema,
    resource_object_schema: PvsSchema | None,
    include_resource_object: bool,
) -> pb.ListResource.Event:
    """Convert one provider result into a protocol event."""
    event = pb.ListResource.Event(
        identity=marshal_identity(result.identity, identity_schema),
        display_name=result.display_name,
        diagnostic=[warning_diagnostic(warning) for warning in result.warnings],
    )

    if include_resource_object and result.resource_object is not None and resource_object_schema is not None:
        event.resource_object.CopyFrom(marshal(result.resource_object, schema=resource_object_schema.block))

    return event


async def stream_list_resource(
    request: pb.ListResource.Request, context: Any
) -> AsyncIterator[pb.ListResource.Event]:
    """Stream the results of a registered list resource."""
    registered = get_filtered_components("list_resource")

    if not registered:
        # A provider that registers no list resources is not in error; it simply
        # has nothing to list, and an empty stream is the correct answer.
        logger.info(
            "ListResource completed with no results; no list resources are registered",
            operation="list_resource",
            request_type=request.type_name,
        )
        return

    list_resource_class = registered.get(request.type_name)
    if list_resource_class is None:
        logger.error(
            "ListResource requested an unregistered list resource type",
            operation="list_resource",
            request_type=request.type_name,
            registered=sorted(registered),
        )
        yield _unknown_list_resource_event(request.type_name, registered)
        return

    identity_schema = list_resource_class.get_identity_schema()
    if identity_schema is None:
        # Terraform keys every listed instance by identity, so emitting results
        # without one would produce events it cannot use.
        yield _error_event(
            f"List resource '{request.type_name}' has no identity schema",
            "Set 'resource_type' to a managed resource that declares an identity schema, "
            "or override get_identity_schema().",
        )
        return

    try:
        config = decode_config(list_resource_class, request.config)
        instance = list_resource_class()
        errors = await instance.validate(config)
    except Exception as exc:
        logger.error(
            "ListResource configuration could not be prepared",
            operation="list_resource",
            request_type=request.type_name,
            error_type=type(exc).__name__,
            error_message=str(exc),
        )
        yield _error_event(f"Invalid configuration for list resource '{request.type_name}'", str(exc))
        return

    if errors:
        for message in errors:
            yield _error_event(message)
        return

    resource_object_schema = (
        list_resource_class.get_resource_object_schema() if request.include_resource_object else None
    )
    ctx: ListResourceContext[Any] = ListResourceContext(
        type_name=request.type_name,
        config=config,
        include_resource_object=request.include_resource_object,
        limit=request.limit,
    )

    emitted = 0
    try:
        async for result in instance.list(ctx):
            yield _build_event(
                result, identity_schema, resource_object_schema, request.include_resource_object
            )
            emitted += 1
            if request.limit > 0 and emitted >= request.limit:
                logger.debug(
                    "ListResource stopped at the requested limit",
                    operation="list_resource",
                    request_type=request.type_name,
                    limit=request.limit,
                )
                break
    except Exception as exc:
        logger.error(
            "ListResource implementation failed",
            operation="list_resource",
            request_type=request.type_name,
            emitted=emitted,
            error_type=type(exc).__name__,
            error_message=str(exc),
            exc_info=True,
        )
        yield _error_event(f"List resource '{request.type_name}' failed while listing", str(exc))
        return

    logger.info(
        "ListResource completed",
        operation="list_resource",
        request_type=request.type_name,
        result_count=emitted,
    )


# 🐍🏗️🔚
