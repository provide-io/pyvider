#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Shared decoding of wire configurations."""

from __future__ import annotations

from typing import Any

from pyvider.conversion import unmarshal
from pyvider.protocols.tfprotov6.handlers.utils import cty_to_attrs_instance
import pyvider.protocols.tfprotov6.protobuf as pb


def decode_config(component_class: Any, config: pb.DynamicValue, *, validate: bool = False) -> Any:
    """Decode a component's configuration into the type its hooks expect.

    ``component_class`` is any component class exposing ``get_schema()`` and a
    ``config_class`` attribute.

    Returns None when the component declares no schema or the caller sent no
    configuration, so a hook can treat "nothing configured" uniformly. When the
    component declares a ``config_class`` the result is an instance of it;
    otherwise the raw ``CtyValue`` is passed through, which keeps components
    that prefer to read values directly from having to define an attrs class.
    """
    schema = component_class.get_schema()
    if schema is None or not config.ByteSize():
        return None

    config_cty = unmarshal(config, schema=schema.block, apply_defaults=True)
    if validate:
        schema.validate_config(config_cty.value)
    if component_class.config_class is None:
        return config_cty
    return cty_to_attrs_instance(config_cty, component_class.config_class, apply_defaults=True)


# 🐍🏗️🔚
