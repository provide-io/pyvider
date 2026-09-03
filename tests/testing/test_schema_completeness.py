#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for pyvider.testing.schema_completeness.

The dev-time complement to `complete_state_dict` (issue #50's runtime fix,
generalized): catches a schema/state-class mismatch statically, the way a Go
provider's compiler would, instead of at a real `terraform apply`.
"""

from typing import Any

from attrs import define
import pytest

from pyvider.exceptions import FrameworkConfigurationError
from pyvider.schema import a_str, s_resource
from pyvider.testing import assert_schema_state_parity, find_missing_state_fields

SCHEMA = s_resource(
    {
        "id": a_str(computed=True),
        "name": a_str(required=True),
        "secret": a_str(required=True, write_only=True),
    }
)


@define
class CompleteState:
    id: str = ""
    name: str = ""
    secret: str | None = None


@define
class IdiomaticState:
    """Omits the write-only field entirely -- the recommended pattern."""

    id: str = ""
    name: str = ""


@define
class MissingNameState:
    id: str = ""


class NotAttrs:
    pass


def _resource_class(for_state_class: type[Any]) -> type[Any]:
    class Resource:
        state_class = for_state_class

        @classmethod
        def get_schema(cls) -> Any:
            return SCHEMA

    return Resource


def test_no_mismatch_when_every_attribute_has_a_field() -> None:
    assert find_missing_state_fields(_resource_class(CompleteState)) == []
    assert_schema_state_parity(_resource_class(CompleteState))


def test_write_only_field_is_exempt_when_omitted() -> None:
    assert find_missing_state_fields(_resource_class(IdiomaticState)) == []
    assert_schema_state_parity(_resource_class(IdiomaticState))


def test_missing_non_write_only_field_is_reported() -> None:
    assert find_missing_state_fields(_resource_class(MissingNameState)) == ["name"]


def test_assert_raises_with_actionable_message() -> None:
    with pytest.raises(AssertionError, match="name"):
        assert_schema_state_parity(_resource_class(MissingNameState))


def test_no_state_class_raises_configuration_error() -> None:
    class Resource:
        state_class = None

        @classmethod
        def get_schema(cls) -> Any:
            return SCHEMA

    with pytest.raises(FrameworkConfigurationError, match="state_class"):
        find_missing_state_fields(Resource)


def test_non_attrs_state_class_raises_configuration_error() -> None:
    with pytest.raises(FrameworkConfigurationError, match="attrs"):
        find_missing_state_fields(_resource_class(NotAttrs))
