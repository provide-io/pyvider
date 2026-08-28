#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""`is_valid_refinement` decides whether apply's result is consistent with the plan.

A `False` here becomes `ResourceLifecycleContractError` and fails the apply, so a
refinement wrongly called invalid makes a resource unusable rather than merely
noisy.
"""

from __future__ import annotations

import pytest

from pyvider.cty import (
    CtyList,
    CtyMap,
    CtyNumber,
    CtyObject,
    CtySet,
    CtyString,
    CtyValue,
)
from pyvider.protocols.tfprotov6.handlers.utils import is_valid_refinement


class TestUnknownRefinesToAnything:
    """The docstring's own promise: "refined from unknown to null/concrete"."""

    def test_unknown_to_concrete(self) -> None:
        assert is_valid_refinement(CtyValue.unknown(CtyString()), CtyString().validate("x")) == (True, "")

    def test_unknown_to_null(self) -> None:
        """An optional+computed attribute planned unknown may resolve to null."""
        valid, reason = is_valid_refinement(CtyValue.unknown(CtyString()), CtyValue.null(CtyString()))
        assert valid, reason

    def test_unknown_object_to_concrete(self) -> None:
        t = CtyObject({"a": CtyString()})
        valid, reason = is_valid_refinement(CtyValue.unknown(t), t.validate({"a": "x"}))
        assert valid, reason

    def test_unknown_list_to_concrete(self) -> None:
        t = CtyList(element_type=CtyString())
        valid, reason = is_valid_refinement(CtyValue.unknown(t), t.validate(["x"]))
        assert valid, reason

    def test_unknown_map_to_concrete(self) -> None:
        t = CtyMap(element_type=CtyString())
        valid, reason = is_valid_refinement(CtyValue.unknown(t), t.validate({"k": "v"}))
        assert valid, reason


class TestContainersHoldingUnknownElements:
    """`tags = { name = random_pet.x.id }` is a known map with an unknown value."""

    def test_map_with_unknown_value_resolves(self) -> None:
        t = CtyMap(element_type=CtyString())
        plan = t.validate({"name": CtyValue.unknown(CtyString())})
        valid, reason = is_valid_refinement(plan, t.validate({"name": "abc"}))
        assert valid, reason

    def test_set_with_unknown_element_resolves(self) -> None:
        t = CtySet(element_type=CtyString())
        plan = t.validate([CtyValue.unknown(CtyString())])
        valid, reason = is_valid_refinement(plan, t.validate(["abc"]))
        assert valid, reason

    def test_object_with_unknown_attribute_resolves(self) -> None:
        t = CtyObject({"id": CtyString(), "name": CtyString()})
        plan = t.validate({"id": CtyValue.unknown(CtyString()), "name": "n"})
        valid, reason = is_valid_refinement(plan, t.validate({"id": "i-1", "name": "n"}))
        assert valid, reason


class TestRealViolationsAreStillCaught:
    """The check has to keep failing what it exists to fail."""

    def test_known_to_different_value(self) -> None:
        valid, _ = is_valid_refinement(CtyString().validate("a"), CtyString().validate("b"))
        assert not valid

    def test_known_to_null(self) -> None:
        valid, reason = is_valid_refinement(CtyString().validate("a"), CtyValue.null(CtyString()))
        assert not valid
        assert "null" in reason

    def test_known_to_unknown(self) -> None:
        valid, reason = is_valid_refinement(CtyString().validate("a"), CtyValue.unknown(CtyString()))
        assert not valid
        assert "unknown" in reason

    def test_type_mismatch(self) -> None:
        valid, reason = is_valid_refinement(CtyString().validate("a"), CtyNumber().validate(1))
        assert not valid
        assert "Type mismatch" in reason

    def test_map_value_changed(self) -> None:
        t = CtyMap(element_type=CtyString())
        valid, _ = is_valid_refinement(t.validate({"k": "a"}), t.validate({"k": "b"}))
        assert not valid

    def test_map_keys_changed(self) -> None:
        t = CtyMap(element_type=CtyString())
        valid, _ = is_valid_refinement(t.validate({"k": "a"}), t.validate({"other": "a"}))
        assert not valid

    def test_object_attribute_changed(self) -> None:
        t = CtyObject({"a": CtyString()})
        valid, reason = is_valid_refinement(t.validate({"a": "x"}), t.validate({"a": "y"}))
        assert not valid
        assert "a" in reason

    def test_list_length_changed(self) -> None:
        t = CtyList(element_type=CtyString())
        valid, _ = is_valid_refinement(t.validate(["a"]), t.validate(["a", "b"]))
        assert not valid


class TestUnchangedValuesPass:
    @pytest.mark.parametrize(
        "value",
        [
            CtyString().validate("a"),
            CtyNumber().validate(1),
            CtyList(element_type=CtyString()).validate(["a", "b"]),
            CtyMap(element_type=CtyString()).validate({"k": "v"}),
            CtySet(element_type=CtyString()).validate(["a"]),
            CtyObject({"a": CtyString()}).validate({"a": "x"}),
        ],
        ids=lambda v: str(v.type),
    )
    def test_identical_value_is_a_valid_refinement(self, value: CtyValue) -> None:
        valid, reason = is_valid_refinement(value, value)
        assert valid, reason

    def test_null_to_null(self) -> None:
        valid, reason = is_valid_refinement(CtyValue.null(CtyString()), CtyValue.null(CtyString()))
        assert valid, reason


# 🌊🪢🔚
