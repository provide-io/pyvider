#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for ApplyResourceChange handler - Advanced private state and context handling."""

from typing import ClassVar

from provide.testkit import mocking as mock
import pytest

import pyvider.protocols.tfprotov6.protobuf as pb


class TestProcessPrivateState:
    """Tests for _process_private_state helper function."""

    @pytest.mark.asyncio
    async def test_returns_none_when_no_private_state_class(self) -> None:
        """Test that returns None when resource has no private_state_class."""
        from pyvider.protocols.tfprotov6.handlers.apply_resource_change import _process_private_state

        class ResourceWithoutPrivateState:
            pass

        result = await _process_private_state(ResourceWithoutPrivateState(), b"some_data")
        assert result is None

    @pytest.mark.asyncio
    async def test_returns_none_when_private_state_class_is_none(self) -> None:
        """Test that returns None when private_state_class is None."""
        from pyvider.protocols.tfprotov6.handlers.apply_resource_change import _process_private_state

        class ResourceWithNonePrivateState:
            private_state_class = None

        result = await _process_private_state(ResourceWithNonePrivateState(), b"some_data")
        assert result is None

    @pytest.mark.asyncio
    async def test_returns_none_when_planned_private_is_empty(self) -> None:
        """Test that returns None when planned_private is empty."""
        import attrs

        from pyvider.protocols.tfprotov6.handlers.apply_resource_change import _process_private_state

        @attrs.define
        class PrivateState:
            data: str

        class ResourceWithPrivateState:
            private_state_class = PrivateState

        result = await _process_private_state(ResourceWithPrivateState(), b"")
        assert result is None

    @pytest.mark.asyncio
    async def test_deserializes_valid_private_state(self) -> None:
        """Test successful deserialization of private state."""
        import attrs
        import msgpack

        from pyvider.protocols.tfprotov6.handlers.apply_resource_change import _process_private_state

        @attrs.define
        class PrivateState:
            data: str
            count: int

        class ResourceWithPrivateState:
            private_state_class = PrivateState

        # Create encrypted private state
        private_data = {"data": "test", "count": 42}
        serialized = msgpack.packb(private_data, use_bin_type=True)
        fake_encrypted = b"fake_encrypted_" + serialized

        with mock.patch("pyvider.protocols.tfprotov6.handlers.apply_resource_change.decrypt") as mock_decrypt:
            mock_decrypt.return_value = serialized

            result = await _process_private_state(ResourceWithPrivateState(), fake_encrypted)

            assert result is not None
            assert result.data == "test"
            assert result.count == 42
            mock_decrypt.assert_called_once_with(fake_encrypted)

    @pytest.mark.asyncio
    async def test_raises_resource_error_on_deserialization_failure(self) -> None:
        """Test that raises ResourceError when deserialization fails."""
        import attrs

        from pyvider.exceptions import ResourceError
        from pyvider.protocols.tfprotov6.handlers.apply_resource_change import _process_private_state

        @attrs.define
        class PrivateState:
            data: str

        class ResourceWithPrivateState:
            private_state_class = PrivateState

        # Invalid encrypted data
        with pytest.raises(ResourceError, match="Failed to deserialize private state"):
            await _process_private_state(ResourceWithPrivateState(), b"invalid_data")


class TestCreateResourceContext:
    """Tests for _create_resource_context helper function."""

    def test_creates_context_with_all_fields(self) -> None:
        """Test creating resource context with all fields populated."""
        import attrs

        from pyvider.cty import CtyObject, CtyString, CtyValue
        from pyvider.protocols.tfprotov6.handlers.apply_resource_change import _create_resource_context

        @attrs.define
        class Config:
            name: str

        @attrs.define
        class State:
            value: str

        @attrs.define
        class PrivateState:
            token: str

        class MockResource:
            config_class = Config
            state_class = State

        class MockProvider:
            class Metadata:
                capabilities: ClassVar[dict] = {"test": True}

            metadata = Metadata()

        config_cty = CtyValue(
            vtype=CtyObject(attribute_types={"name": CtyString()}),
            value={"name": CtyValue(vtype=CtyString(), value="test")},
        )
        prior_cty = CtyValue(
            vtype=CtyObject(attribute_types={"value": CtyString()}),
            value={"value": CtyValue(vtype=CtyString(), value="old")},
        )
        planned_cty = CtyValue(
            vtype=CtyObject(attribute_types={"value": CtyString()}),
            value={"value": CtyValue(vtype=CtyString(), value="new")},
        )
        private_state = PrivateState(token="secret")

        with mock.patch(
            "pyvider.protocols.tfprotov6.handlers.apply_resource_change.cty_to_attrs_instance"
        ) as mock_convert:
            mock_convert.side_effect = [Config(name="test"), State(value="old"), State(value="new")]

            context = _create_resource_context(
                config_cty, prior_cty, planned_cty, private_state, MockResource(), MockProvider()
            )

            assert context.config is not None
            assert context.state is not None
            assert context.planned_state is not None
            assert context.private_state == private_state
            assert context.capabilities == {"test": True}


class TestHandleApplyResult:
    """Tests for _handle_apply_result helper function."""

    def test_handles_none_new_state(self) -> None:
        """Test handling None new state (delete operation)."""
        from pyvider.cty import CtyString, CtyValue
        from pyvider.protocols.tfprotov6.handlers.apply_resource_change import _handle_apply_result

        response = pb.ApplyResourceChange.Response()

        class MockSchema:
            class Block:
                pass

            block = Block()

        planned_cty = CtyValue(vtype=CtyString(), value="test")

        _handle_apply_result(None, None, MockSchema(), planned_cty, response)

        assert response.new_state.msgpack == b"\xc0"

    def test_raises_error_on_invalid_refinement(self) -> None:
        """Test that raises error when new state is not valid refinement of planned state."""
        import attrs

        from pyvider.cty import CtyString, CtyType, CtyValue
        from pyvider.exceptions import ResourceLifecycleContractError
        from pyvider.protocols.tfprotov6.handlers.apply_resource_change import _handle_apply_result

        @attrs.define
        class NewState:
            name: str

        response = pb.ApplyResourceChange.Response()

        class MockType:
            def validate(self, data: CtyValue) -> CtyValue:
                return CtyValue(vtype=CtyString(), value="different")

        class MockBlock:
            def to_cty_type(self) -> CtyType:
                return MockType()

        class MockSchema:
            name = "test_resource"
            block = MockBlock()

        new_state = NewState(name="test")
        planned_cty = CtyValue(vtype=CtyString(), value="planned")

        with (
            mock.patch(
                "pyvider.protocols.tfprotov6.handlers.apply_resource_change.attrs_to_dict_for_cty"
            ) as mock_to_dict,
            mock.patch(
                "pyvider.protocols.tfprotov6.handlers.apply_resource_change.is_valid_refinement"
            ) as mock_refine,
        ):
            mock_to_dict.return_value = {"name": "test"}
            mock_refine.return_value = (False, "Values don't match")

            with pytest.raises(ResourceLifecycleContractError, match="not a valid refinement"):
                _handle_apply_result(new_state, None, MockSchema(), planned_cty, response)

    def test_encrypts_and_sets_private_state(self) -> None:
        """Test that private state is serialized and encrypted."""
        import attrs

        from pyvider.cty import CtyString, CtyType, CtyValue
        from pyvider.protocols.tfprotov6.handlers.apply_resource_change import _handle_apply_result

        @attrs.define
        class NewState:
            name: str

        @attrs.define
        class NewPrivateState:
            token: str

        response = pb.ApplyResourceChange.Response()

        class MockType:
            def validate(self, data: CtyValue) -> CtyValue:
                return CtyValue(vtype=CtyString(), value="validated")

        class MockBlock:
            def to_cty_type(self) -> CtyType:
                return MockType()

        class MockSchema:
            block = MockBlock()

        new_state = NewState(name="test")
        new_private = NewPrivateState(token="secret")

        with (
            mock.patch(
                "pyvider.protocols.tfprotov6.handlers.apply_resource_change.attrs_to_dict_for_cty"
            ) as mock_to_dict,
            mock.patch("pyvider.protocols.tfprotov6.handlers.apply_resource_change.marshal") as mock_marshal,
            mock.patch("pyvider.protocols.tfprotov6.handlers.apply_resource_change.encrypt") as mock_encrypt,
        ):
            mock_to_dict.return_value = {"name": "test"}
            mock_marshal.return_value = pb.DynamicValue(msgpack=b"marshaled")
            mock_encrypt.return_value = b"encrypted_private"

            _handle_apply_result(new_state, new_private, MockSchema(), None, response)

            assert response.private == b"encrypted_private"
            mock_encrypt.assert_called_once()


# 🐍🏗️🔚
