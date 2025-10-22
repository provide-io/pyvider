"""Tests for pyvider/ephemerals/base.py - ephemeral resource base class."""

from datetime import datetime, timedelta, timezone

import pytest

from pyvider.ephemerals.base import BaseEphemeralResource
from pyvider.ephemerals.context import EphemeralResourceContext
from pyvider.resources.private_state import PrivateState
from pyvider.schema import s_ephemeral, a_str, a_num


class MockPrivateState(PrivateState):
    """Mock private state for testing."""

    def __init__(self, token: str = "test-token"):
        self.token = token


class TestEphemeralResource(BaseEphemeralResource):
    """Concrete test ephemeral resource."""

    @classmethod
    def get_schema(cls):
        return s_ephemeral(
            attributes={
                "name": a_str(required=True),
                "ttl": a_num(optional=True),
            }
        )

    async def open(self, ctx):
        """Open the ephemeral resource."""
        result = {"name": "test-resource", "token": "abc123"}
        private_state = MockPrivateState(token="abc123")
        renew_at = datetime.now(timezone.utc) + timedelta(hours=1)
        return result, private_state, renew_at

    async def renew(self, ctx):
        """Renew the ephemeral resource."""
        # Renew by creating new private state
        new_private_state = MockPrivateState(token="renewed-token")
        new_renew_at = datetime.now(timezone.utc) + timedelta(hours=1)
        return new_private_state, new_renew_at

    async def close(self, ctx):
        """Close the ephemeral resource."""
        # Cleanup logic here
        pass


class PartialEphemeralResource(BaseEphemeralResource):
    """Incomplete ephemeral resource for testing abstract enforcement."""

    @classmethod
    def get_schema(cls):
        return s_ephemeral(attributes={"id": a_str()})

    # Missing open, renew, close methods


class TestBaseEphemeralResource:
    """Tests for BaseEphemeralResource abstract base class."""

    def test_ephemeral_resource_has_class_attributes(self):
        """Test that ephemeral resource has expected class attributes."""
        assert hasattr(BaseEphemeralResource, "config_class")
        assert hasattr(BaseEphemeralResource, "result_class")
        assert hasattr(BaseEphemeralResource, "private_state_class")

    def test_ephemeral_resource_get_schema_is_abstract(self):
        """Test that get_schema is abstract and must be implemented."""
        # Can't instantiate without implementing abstract methods
        with pytest.raises(TypeError, match="abstract"):
            BaseEphemeralResource()

    def test_concrete_ephemeral_resource_can_be_instantiated(self):
        """Test that concrete implementation can be instantiated."""
        resource = TestEphemeralResource()
        assert resource is not None
        assert isinstance(resource, BaseEphemeralResource)

    def test_partial_ephemeral_resource_cannot_be_instantiated(self):
        """Test that partial implementations cannot be instantiated."""
        with pytest.raises(TypeError, match="abstract"):
            PartialEphemeralResource()

    def test_get_schema_returns_schema(self):
        """Test that get_schema returns a valid schema."""
        schema = TestEphemeralResource.get_schema()
        assert schema is not None
        assert hasattr(schema, "block")

    async def test_validate_default_implementation(self):
        """Test that default validate returns empty list."""
        resource = TestEphemeralResource()
        errors = await resource.validate({"name": "test"})
        assert errors == []


class TestEphemeralResourceLifecycle:
    """Tests for ephemeral resource lifecycle methods."""

    async def test_open_creates_resource(self):
        """Test that open creates the ephemeral resource."""
        resource = TestEphemeralResource()
        ctx = EphemeralResourceContext(
            config={"name": "test", "ttl": 3600}, private_state=None
        )

        result, private_state, renew_at = await resource.open(ctx)

        # Should return result data
        assert result is not None
        assert isinstance(result, dict)
        assert "token" in result

        # Should return private state
        assert private_state is not None
        assert isinstance(private_state, MockPrivateState)

        # Should return renewal time
        assert isinstance(renew_at, datetime)
        assert renew_at > datetime.now(timezone.utc)

    async def test_renew_extends_lifetime(self):
        """Test that renew extends the ephemeral resource lifetime."""
        resource = TestEphemeralResource()
        ctx = EphemeralResourceContext(
            config=None, private_state=MockPrivateState(token="old-token")
        )

        new_private_state, new_renew_at = await resource.renew(ctx)

        # Should return new private state
        assert new_private_state is not None
        assert isinstance(new_private_state, MockPrivateState)
        assert new_private_state.token == "renewed-token"

        # Should return new renewal time
        assert isinstance(new_renew_at, datetime)
        assert new_renew_at > datetime.now(timezone.utc)

    async def test_close_cleanup(self):
        """Test that close performs cleanup."""
        resource = TestEphemeralResource()
        ctx = EphemeralResourceContext(
            config=None, private_state=MockPrivateState(token="test-token")
        )

        # Should not raise
        await resource.close(ctx)


class TestEphemeralResourceValidation:
    """Tests for ephemeral resource validation."""

    async def test_custom_validation(self):
        """Test custom validation in ephemeral resource."""

        class ValidatingEphemeralResource(TestEphemeralResource):
            async def validate(self, config):
                errors = []
                if not config.get("name"):
                    errors.append("name is required")
                if config.get("ttl", 0) <= 0:
                    errors.append("ttl must be positive")
                return errors

        resource = ValidatingEphemeralResource()

        # Valid config
        errors = await resource.validate({"name": "test", "ttl": 3600})
        assert errors == []

        # Invalid config - missing name
        errors = await resource.validate({"ttl": 3600})
        assert "name is required" in errors

        # Invalid config - negative ttl
        errors = await resource.validate({"name": "test", "ttl": -1})
        assert "ttl must be positive" in errors


class TestEphemeralResourceContext:
    """Tests for EphemeralResourceContext usage."""

    async def test_open_context_has_config(self):
        """Test that open context provides config."""

        class ContextCheckingResource(TestEphemeralResource):
            async def open(self, ctx):
                # Verify context has config
                assert ctx.config is not None
                assert ctx.config["name"] == "test-name"
                assert ctx.private_state is None
                return await super().open(ctx)

        resource = ContextCheckingResource()
        ctx = EphemeralResourceContext(config={"name": "test-name"}, private_state=None)
        await resource.open(ctx)

    async def test_renew_context_has_private_state(self):
        """Test that renew context provides private state."""

        class ContextCheckingResource(TestEphemeralResource):
            async def renew(self, ctx):
                # Verify context has private state
                assert ctx.private_state is not None
                assert isinstance(ctx.private_state, MockPrivateState)
                assert ctx.config is None
                return await super().renew(ctx)

        resource = ContextCheckingResource()
        ctx = EphemeralResourceContext(
            config=None, private_state=MockPrivateState(token="test")
        )
        await resource.renew(ctx)

    async def test_close_context_has_private_state(self):
        """Test that close context provides private state."""

        class ContextCheckingResource(TestEphemeralResource):
            async def close(self, ctx):
                # Verify context has private state
                assert ctx.private_state is not None
                assert ctx.config is None
                await super().close(ctx)

        resource = ContextCheckingResource()
        ctx = EphemeralResourceContext(
            config=None, private_state=MockPrivateState(token="test")
        )
        await resource.close(ctx)
