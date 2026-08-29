#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for handlers/utils.py utility functions."""

import attrs
import pytest

from pyvider.cty import CtyList, CtyMap, CtyNumber, CtyObject, CtySet, CtyString
from pyvider.cty.path import CtyPath, GetAttrStep, IndexStep, KeyStep
from pyvider.cty.values import CtyValue
from pyvider.cty.values.markers import UNREFINED_UNKNOWN
from pyvider.protocols.tfprotov6.handlers.utils import (
    attrs_to_dict_for_cty,
    cty_path_to_proto_path,
    is_valid_refinement,
    str_path_to_proto_path,
)


class TestAttrsToDictForCty:
    """Tests for attrs_to_dict_for_cty function."""

    def test_converts_simple_attrs_instance(self) -> None:
        """Test converting simple attrs instance to dict."""

        @attrs.define
        class SimpleConfig:
            name: str
            count: int

        config = SimpleConfig(name="test", count=42)
        result = attrs_to_dict_for_cty(config)

        assert result == {"name": "test", "count": 42}

    def test_converts_nested_attrs_instances(self) -> None:
        """Test converting nested attrs instances."""

        @attrs.define
        class Inner:
            value: int

        @attrs.define
        class Outer:
            inner: Inner
            name: str

        config = Outer(inner=Inner(value=10), name="test")
        result = attrs_to_dict_for_cty(config)

        assert result == {"inner": {"value": 10}, "name": "test"}

    def test_preserves_tuples(self) -> None:
        """Test that tuples are preserved in conversion."""

        @attrs.define
        class Config:
            data: tuple

        config = Config(data=("a", "b", "c"))
        result = attrs_to_dict_for_cty(config)

        assert result == {"data": ("a", "b", "c")}
        assert isinstance(result["data"], tuple)

    def test_converts_lists(self) -> None:
        """Test that lists are converted recursively."""

        @attrs.define
        class Inner:
            val: int

        @attrs.define
        class Outer:
            items: list

        config = Outer(items=[Inner(val=1), Inner(val=2)])
        result = attrs_to_dict_for_cty(config)

        assert result == {"items": [{"val": 1}, {"val": 2}]}

    def test_converts_nested_dicts(self) -> None:
        """Test that nested dicts are converted."""

        @attrs.define
        class Inner:
            value: int

        @attrs.define
        class Outer:
            data: dict

        config = Outer(data={"key": Inner(value=5)})
        result = attrs_to_dict_for_cty(config)

        assert result == {"data": {"key": {"value": 5}}}

    def test_passes_through_primitives(self) -> None:
        """Test that primitives are passed through unchanged."""
        assert attrs_to_dict_for_cty("string") == "string"
        assert attrs_to_dict_for_cty(42) == 42
        assert attrs_to_dict_for_cty(3.14) == 3.14
        assert attrs_to_dict_for_cty(True) is True
        assert attrs_to_dict_for_cty(None) is None

    def test_passes_through_cty_values(self) -> None:
        """Test that CtyValue instances are passed through."""
        cty_val = CtyValue(vtype=CtyString(), value="test")
        result = attrs_to_dict_for_cty(cty_val)
        assert result is cty_val

    def test_handles_circular_references(self) -> None:
        """Test that circular references are detected."""

        @attrs.define
        class Node:
            name: str
            next: object = None

        # Create circular reference
        node1 = Node(name="first")
        node2 = Node(name="second", next=node1)
        node1.next = node2

        result = attrs_to_dict_for_cty(node1)

        # Should detect circular reference
        assert result["name"] == "first"
        assert "next" in result
        assert result["next"]["name"] == "second"
        # Circular ref should be marked
        assert "__circular_ref__" in result["next"]["next"]


class TestIsValidRefinement:
    """Tests for is_valid_refinement function."""

    def test_type_mismatch_returns_false(self) -> None:
        """Test that type mismatch is detected."""
        plan = CtyValue(vtype=CtyString(), value="test")
        result = CtyValue(vtype=CtyNumber(), value=42)

        is_valid, reason = is_valid_refinement(plan, result)

        assert not is_valid
        assert "Type mismatch" in reason

    def test_unknown_to_concrete_is_valid(self) -> None:
        """Test that unknown can be refined to concrete."""
        plan = CtyValue(vtype=CtyString(), value="test", is_unknown=True)
        result = CtyValue(vtype=CtyString(), value="concrete")

        is_valid, reason = is_valid_refinement(plan, result)

        assert is_valid
        assert reason == ""

    def test_unrefined_unknown_can_refine_to_any(self) -> None:
        """Test that UNREFINED_UNKNOWN can refine to any concrete value."""
        plan = CtyValue(vtype=CtyString(), value=UNREFINED_UNKNOWN, is_unknown=True)
        result = CtyValue(vtype=CtyString(), value="anything")

        is_valid, _reason = is_valid_refinement(plan, result)

        assert is_valid

    def test_null_to_concrete_is_valid(self) -> None:
        """Test that null can be refined to concrete."""
        plan = CtyValue(vtype=CtyString(), value=None, is_null=True)
        result = CtyValue(vtype=CtyString(), value="concrete")

        is_valid, _reason = is_valid_refinement(plan, result)

        assert is_valid

    def test_concrete_to_null_is_invalid(self) -> None:
        """Test that concrete cannot be refined to null."""
        plan = CtyValue(vtype=CtyString(), value="concrete")
        result = CtyValue(vtype=CtyString(), value=None, is_null=True)

        is_valid, reason = is_valid_refinement(plan, result)

        assert not is_valid
        assert "became null" in reason

    def test_known_to_unknown_is_invalid(self) -> None:
        """Test that known cannot become unknown."""
        plan = CtyValue(vtype=CtyString(), value="known")
        result = CtyValue(vtype=CtyString(), value="test", is_unknown=True)

        is_valid, reason = is_valid_refinement(plan, result)

        assert not is_valid
        assert "became unknown" in reason

    def test_concrete_value_change_is_invalid(self) -> None:
        """Test that concrete values cannot change."""
        plan = CtyValue(vtype=CtyString(), value="original")
        result = CtyValue(vtype=CtyString(), value="changed")

        is_valid, reason = is_valid_refinement(plan, result)

        assert not is_valid
        assert "Value mismatch" in reason

    def test_object_refinement_key_mismatch(self) -> None:
        """Test object refinement detects key mismatches."""
        plan_obj = CtyValue(
            vtype=CtyObject(attribute_types={"a": CtyString()}),
            value={"a": CtyValue(vtype=CtyString(), value="test")},
        )
        result_obj = CtyValue(
            vtype=CtyObject(attribute_types={"b": CtyString()}),
            value={"b": CtyValue(vtype=CtyString(), value="test")},
        )

        is_valid, reason = is_valid_refinement(plan_obj, result_obj)

        assert not is_valid
        assert "attribute mismatch" in reason.lower() or "type mismatch" in reason.lower()

    def test_list_refinement_length_change(self) -> None:
        """Test list refinement detects length changes."""
        plan_list = CtyValue(
            vtype=CtyList(element_type=CtyString()), value=[CtyValue(vtype=CtyString(), value="a")]
        )
        result_list = CtyValue(
            vtype=CtyList(element_type=CtyString()),
            value=[CtyValue(vtype=CtyString(), value="a"), CtyValue(vtype=CtyString(), value="b")],
        )

        is_valid, reason = is_valid_refinement(plan_list, result_list)

        assert not is_valid
        assert "length changed" in reason.lower()


class TestStrPathToProtoPath:
    """Tests for str_path_to_proto_path function."""

    def test_simple_attribute_path(self) -> None:
        """Test converting simple attribute path."""
        result = str_path_to_proto_path("name")

        assert len(result.steps) == 1
        assert result.steps[0].attribute_name == "name"

    def test_nested_attribute_path(self) -> None:
        """Test converting nested attribute path."""
        result = str_path_to_proto_path("config.database.host")

        assert len(result.steps) == 3
        assert result.steps[0].attribute_name == "config"
        assert result.steps[1].attribute_name == "database"
        assert result.steps[2].attribute_name == "host"

    def test_index_path(self) -> None:
        """Test converting index path."""
        result = str_path_to_proto_path("items[0]")

        assert len(result.steps) == 2
        assert result.steps[0].attribute_name == "items"
        assert result.steps[1].element_key_int == 0

    def test_key_path(self) -> None:
        """Test converting key path."""
        result = str_path_to_proto_path("data['key']")

        assert len(result.steps) == 2
        assert result.steps[0].attribute_name == "data"
        assert result.steps[1].element_key_string == "key"

    def test_complex_nested_path(self) -> None:
        """Test converting complex nested path."""
        result = str_path_to_proto_path("config.servers[0].endpoints['primary']")

        assert len(result.steps) == 5
        assert result.steps[0].attribute_name == "config"
        assert result.steps[1].attribute_name == "servers"
        assert result.steps[2].element_key_int == 0
        assert result.steps[3].attribute_name == "endpoints"
        assert result.steps[4].element_key_string == "primary"

    def test_empty_path_returns_none(self) -> None:
        """Test that empty path returns None."""
        assert str_path_to_proto_path("") is None
        assert str_path_to_proto_path(None) is None

    def test_attribute_name_containing_a_dash_stays_one_step(self) -> None:
        """go-cty allows a dash in an attribute name; the old `\\w+` regex did not.

        It matched either side of the dash separately, so a single attribute
        became a two-step path naming two attributes that do not exist.
        """
        result = str_path_to_proto_path("retention-days")

        assert [step.attribute_name for step in result.steps] == ["retention-days"]

    def test_nested_attribute_name_containing_a_dash(self) -> None:
        result = str_path_to_proto_path("config.retention-days")

        assert [step.attribute_name for step in result.steps] == ["config", "retention-days"]

    def test_within_resolves_a_bracket_by_what_the_type_accepts(self) -> None:
        """`['a']` is both a set element and a map key; only the type can say which."""
        within = CtyObject(
            {
                "items": CtyList(element_type=CtyString()),
                "meta": CtyMap(element_type=CtyString()),
            }
        )

        indexed = str_path_to_proto_path("items[0]", within=within)
        keyed = str_path_to_proto_path("meta['k']", within=within)

        assert indexed.steps[1].element_key_int == 0
        assert keyed.steps[1].element_key_string == "k"

    @pytest.mark.parametrize(
        "unresolvable",
        ["nope", "items['a']", "name.deeper"],
    )
    def test_within_drops_a_path_the_type_cannot_answer(self, unresolvable: str) -> None:
        """A misspelt attribute, a list keyed by string, a scalar descended into."""
        within = CtyObject({"name": CtyString(), "items": CtyList(element_type=CtyString())})

        assert str_path_to_proto_path(unresolvable, within=within) is None

    def test_without_within_an_unknown_attribute_is_still_accepted(self) -> None:
        """Only the syntax is checked when there is no type to resolve against."""
        result = str_path_to_proto_path("nope")

        assert [step.attribute_name for step in result.steps] == ["nope"]

    @pytest.mark.parametrize(
        "malformed",
        ["tags[0", "tags[]", "tags['a", "items[0]extra"],
    )
    def test_a_malformed_path_yields_no_path_rather_than_a_wrong_one(self, malformed: str) -> None:
        """A path that cannot be read points at nothing, not at the wrong attribute.

        The old regex used `finditer`, which skips what it cannot match, so
        `tags[0` silently became `tags[0]`-looking steps and `items[0]extra`
        grew a third step. A diagnostic aimed at the wrong attribute is worse
        than one aimed at nothing.
        """
        assert str_path_to_proto_path(malformed) is None


class TestCtyPathToProtoPath:
    """Tests for cty_path_to_proto_path function."""

    def test_getattr_step(self) -> None:
        """Test converting GetAttrStep."""
        cty_path = CtyPath(steps=[GetAttrStep(name="field")])
        result = cty_path_to_proto_path(cty_path)

        assert len(result.steps) == 1
        assert result.steps[0].attribute_name == "field"

    def test_index_step(self) -> None:
        """Test converting IndexStep."""
        cty_path = CtyPath(steps=[IndexStep(index=5)])
        result = cty_path_to_proto_path(cty_path)

        assert len(result.steps) == 1
        assert result.steps[0].element_key_int == 5

    def test_key_step(self) -> None:
        """Test converting KeyStep."""
        cty_path = CtyPath(steps=[KeyStep(key="mykey")])
        result = cty_path_to_proto_path(cty_path)

        assert len(result.steps) == 1
        assert result.steps[0].element_key_string == "mykey"

    def test_mixed_steps(self) -> None:
        """Test converting mixed step types."""
        cty_path = CtyPath(
            steps=[
                GetAttrStep(name="root"),
                IndexStep(index=0),
                KeyStep(key="item"),
            ]
        )
        result = cty_path_to_proto_path(cty_path)

        assert len(result.steps) == 3
        assert result.steps[0].attribute_name == "root"
        assert result.steps[1].element_key_int == 0
        assert result.steps[2].element_key_string == "item"

    def test_empty_path_returns_none(self) -> None:
        """Test that empty path returns None."""
        assert cty_path_to_proto_path(None) is None
        assert cty_path_to_proto_path(CtyPath(steps=[])) is None

    def test_map_key_step_renders_as_element_key_string(self) -> None:
        """A map's KeyStep carries a plain string key (see map.py's
        `KeyStep(normalized_key)`, and walk.py's `KeyStep(key) for key in
        sorted(payload)`). This is the live, already-shipping case and must
        keep rendering as element_key_string, not be affected by the set
        handling below.
        """
        cty_path = CtyPath(steps=[GetAttrStep(name="tags"), KeyStep(key="env")])
        result = cty_path_to_proto_path(cty_path)

        assert result is not None
        assert len(result.steps) == 2
        assert result.steps[0].attribute_name == "tags"
        assert result.steps[1].element_key_string == "env"

    def test_set_element_key_step_at_root_truncates_to_none(self) -> None:
        """A set element's KeyStep carries a whole CtyValue (walk.py's
        `_child_steps`: `KeyStep(element)` where `element` is a set member).
        There is no tfplugin6 AttributePath.Step that can honestly address a
        set element -- attribute_name/element_key_string/element_key_int only
        cover attributes and *indexable* collections, and go-cty documents a
        set element as "acting as its own key" rather than having one. A path
        that is nothing but a set-element step therefore has nothing more
        specific to point at than the root, matching the empty-path contract.
        """
        element = CtyValue(vtype=CtyString(), value="a")
        cty_path = CtyPath(steps=[KeyStep(key=element)])

        assert cty_path_to_proto_path(cty_path) is None

    def test_set_element_key_step_truncates_remaining_path(self) -> None:
        """A set element mid-path stops the proto path at the set itself
        rather than inventing a position past it -- the same choice
        required.py's block-nesting check makes for SET-nested blocks
        ("an index here would be an invented position. Report the block.").
        Steps after the set-element step (however they were produced) must
        not appear in the output: there is no honest way to say "inside this
        particular element."
        """
        element = CtyValue(vtype=CtyString(), value="prod")
        cty_path = CtyPath(
            steps=[
                GetAttrStep(name="environments"),
                KeyStep(key=element),
                GetAttrStep(name="name"),
            ]
        )
        result = cty_path_to_proto_path(cty_path)

        assert result is not None
        assert len(result.steps) == 1
        assert result.steps[0].attribute_name == "environments"

    def test_set_element_from_real_walk_path_truncates(self) -> None:
        """End-to-end: a KeyStep produced by actually walking a CtySet value
        (not a hand-built CtyValue) still truncates cleanly. This is the
        exact shape `deep_values`/`walk` hand to a caller once they feed
        paths into diagnostics.
        """
        from pyvider.cty.walk import deep_values

        set_type = CtySet(element_type=CtyString())
        set_value = set_type.validate({"a", "b"})

        set_element_paths = [
            path
            for path, _value in deep_values(set_value)
            if path.steps and isinstance(path.steps[-1], KeyStep)
        ]
        assert set_element_paths, "expected at least one KeyStep path from walking a set"

        for path in set_element_paths:
            key = path.steps[-1].key
            assert isinstance(key, CtyValue)  # confirms this is the set-element shape, not a map key
            assert cty_path_to_proto_path(path) is None

    def test_nested_map_index_and_set_combination(self) -> None:
        """A path that mixes an attribute, a list index, a map key, and a
        trailing set-element step: everything up to the set renders
        normally, and the set-element step truncates the rest.
        """
        element = CtyValue(vtype=CtyString(), value="x")
        cty_path = CtyPath(
            steps=[
                GetAttrStep(name="clusters"),
                IndexStep(index=2),
                KeyStep(key="labels"),
                KeyStep(key=element),
            ]
        )
        result = cty_path_to_proto_path(cty_path)

        assert result is not None
        assert len(result.steps) == 3
        assert result.steps[0].attribute_name == "clusters"
        assert result.steps[1].element_key_int == 2
        assert result.steps[2].element_key_string == "labels"


# 🐍🏗️🔚
