#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for ConfigureProvider handler."""

from typing import Any

import attrs
from provide.testkit.mocking import patch
import pytest

from pyvider.hub import hub
from pyvider.protocols.tfprotov6.handlers.configure_provider import (
    ConfigureProviderHandler,
    _configure_provider_impl,
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.providers.base import BaseProvider


@attrs.define
class SampleProviderConfig:
    region: str = "us-west-2"
    api_key: str = ""


class TestConfigureProviderHandler:
    """Tests for ConfigureProviderHandler function."""

    @pytest.mark.asyncio
    async def test_handler_returns_response_object(self, provider_in_hub: Any) -> None:
        """Test that handler returns proper response object."""
        provider = hub.get_component("singleton", "provider")
        schema = provider.schema
        cty_type = schema.block.to_cty_type()
        config_cty = cty_type.validate({})

        from pyvider.conversion import marshal

        config_dv = marshal(config_cty, schema=schema.block)

        request = pb.ConfigureProvider.Request(config=config_dv)
        response = await ConfigureProviderHandler(request, context=None)

        assert isinstance(response, pb.ConfigureProvider.Response)

    @pytest.mark.asyncio
    async def test_handler_configures_provider_successfully(self, provider_in_hub: Any) -> None:
        """Test handler configures provider with valid config."""
        provider = hub.get_component("singleton", "provider")
        schema = provider.schema
        cty_type = schema.block.to_cty_type()
        config_cty = cty_type.validate({})

        from pyvider.conversion import marshal

        config_dv = marshal(config_cty, schema=schema.block)

        request = pb.ConfigureProvider.Request(config=config_dv)
        response = await ConfigureProviderHandler(request, context=None)

        assert len(response.diagnostics) == 0
        # Provider context should be registered
        provider_context = hub.get_component("singleton", "provider_context")
        assert provider_context is not None

    @pytest.mark.asyncio
    async def test_handler_handles_unknown_config(self, provider_in_hub: Any) -> None:
        """Test handler handles unknown configuration during planning."""
        provider = hub.get_component("singleton", "provider")
        schema = provider.schema
        cty_type = schema.block.to_cty_type()

        from pyvider.cty import CtyValue

        unknown_config = CtyValue.unknown(cty_type)

        from pyvider.conversion import marshal

        config_dv = marshal(unknown_config, schema=schema.block)

        request = pb.ConfigureProvider.Request(config=config_dv)
        response = await ConfigureProviderHandler(request, context=None)

        # Should return without error, deferring configuration
        assert isinstance(response, pb.ConfigureProvider.Response)

    @pytest.mark.asyncio
    async def test_handler_handles_missing_provider(self, provider_in_hub: Any) -> None:
        """Test handler handles missing provider instance."""
        # Temporarily remove provider
        provider = hub.get_component("singleton", "provider")
        hub.unregister("singleton", "provider")

        try:
            request = pb.ConfigureProvider.Request(config=pb.DynamicValue(msgpack=b"\x80"))
            response = await ConfigureProviderHandler(request, context=None)

            assert len(response.diagnostics) > 0
        finally:
            # Restore provider
            hub.register("singleton", "provider", provider)

    @pytest.mark.asyncio
    async def test_impl_creates_provider_context(self, provider_in_hub: Any) -> None:
        """Test implementation creates and stores provider context."""
        # Clear any existing provider context
        if hub.get_component("singleton", "provider_context"):
            hub.unregister("singleton", "provider_context")

        provider = hub.get_component("singleton", "provider")
        schema = provider.schema
        cty_type = schema.block.to_cty_type()
        config_cty = cty_type.validate({})

        from pyvider.conversion import marshal

        config_dv = marshal(config_cty, schema=schema.block)

        request = pb.ConfigureProvider.Request(config=config_dv)
        await _configure_provider_impl(request, context=None)

        # Provider context should be created
        provider_context_factory = hub.get_component("singleton", "provider_context")
        assert provider_context_factory is not None
        # Call the factory to get the actual context instance
        provider_context = (
            provider_context_factory() if callable(provider_context_factory) else provider_context_factory
        )
        assert provider_context.config is not None

    @pytest.mark.asyncio
    async def test_handler_metrics_recorded(self, provider_in_hub: Any) -> None:
        """Test that handler records metrics."""
        provider = hub.get_component("singleton", "provider")
        schema = provider.schema
        cty_type = schema.block.to_cty_type()
        config_cty = cty_type.validate({})

        from pyvider.conversion import marshal

        config_dv = marshal(config_cty, schema=schema.block)

        request = pb.ConfigureProvider.Request(config=config_dv)

        # Just verify handler completes successfully (metrics recorded internally)
        response = await ConfigureProviderHandler(request, context=None)
        assert isinstance(response, pb.ConfigureProvider.Response)

    @pytest.mark.asyncio
    async def test_handler_records_error_on_exception(self, provider_in_hub: Any) -> None:
        """Test that handler increments error counter on exceptions."""
        from provide.testkit.mocking import patch

        with (
            patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_errors") as mock_errors,
            patch(
                "pyvider.protocols.tfprotov6.handlers.configure_provider._configure_provider_impl"
            ) as mock_impl,
        ):
            # Make implementation raise an exception
            mock_impl.side_effect = RuntimeError("Test error")
            request = pb.ConfigureProvider.Request()

            # @resilient() decorator catches the exception
            with pytest.raises(RuntimeError):
                await ConfigureProviderHandler(request, context=None)

            # Error metric should be incremented
            mock_errors.inc.assert_called_once_with(handler="ConfigureProvider")

    @pytest.mark.asyncio
    async def test_impl_handles_null_config_instance(self, provider_in_hub: Any) -> None:
        """Test handling when config_instance is None."""
        from unittest.mock import patch

        provider = hub.get_component("singleton", "provider")
        schema = provider.schema
        cty_type = schema.block.to_cty_type()
        config_cty = cty_type.validate({})

        from pyvider.conversion import marshal

        config_dv = marshal(config_cty, schema=schema.block)

        request = pb.ConfigureProvider.Request(config=config_dv)

        # Mock the shared configuration conversion to return None.
        with patch(
            "pyvider.protocols.tfprotov6.handlers.configure_provider.config_to_attrs_instance"
        ) as mock_config_to_attrs:
            mock_config_to_attrs.return_value = None

            response = await _configure_provider_impl(request, context=None)

            # Should have diagnostic
            assert len(response.diagnostics) > 0
            assert "Invalid provider configuration" in response.diagnostics[0].summary

    @pytest.mark.asyncio
    async def test_impl_logs_warning_for_unknown_config(self, provider_in_hub: Any) -> None:
        """Test that unknown config triggers warning log."""
        from provide.testkit.mocking import patch

        hub.get_component("singleton", "provider")

        # Create request and mock config decoding to return unknown CtyValue
        request = pb.ConfigureProvider.Request()
        request.config.msgpack = b"\x80"  # Empty dict in msgpack

        from pyvider.cty import CtyObject, CtyValue

        unknown_config = CtyValue.unknown(CtyObject(attribute_types={}))

        # Patch logger and the shared wire-config decoder.
        with (
            patch("pyvider.protocols.tfprotov6.handlers.configure_provider.logger") as mock_logger,
            patch(
                "pyvider.protocols.tfprotov6.handlers.configure_provider.unmarshal_config"
            ) as mock_unmarshal_config,
        ):
            mock_unmarshal_config.return_value = unknown_config

            response = await _configure_provider_impl(request, context=None)

            # Should log warning about unknown config
            mock_logger.warning.assert_called_once()
            assert "unknown" in mock_logger.warning.call_args[0][0].lower()

            # Should return empty response (early return)
            assert len(response.diagnostics) == 0


# 🐍🏗️🔚


class TestConfigureHookIsInvoked:
    """The provider's own configure() hook.

    Registering the ProviderContext is not enough: a provider that overrides
    configure() to build a client from its configuration gets nothing, and every
    request afterwards runs on defaults — with no error to say so.
    """

    @pytest.mark.asyncio
    async def test_configure_hook_receives_the_config(self, provider_in_hub: Any) -> None:
        from provide.testkit.mocking import patch

        from pyvider.conversion import marshal

        provider = hub.get_component("singleton", "provider")
        seen: list[Any] = []

        async def spy(_self: Any, config: Any) -> None:
            seen.append(config)

        # BaseProvider is an attrs class with slots, so the method is patched on the
        # CLASS rather than the instance.
        with patch.object(type(provider), "configure", spy):
            schema = provider.schema
            config_cty = schema.block.to_cty_type().validate({})
            request = pb.ConfigureProvider.Request(config=marshal(config_cty, schema=schema.block))

            response = await ConfigureProviderHandler(request, context=None)

        assert len(seen) == 1, "the provider's configure() hook was not called"
        assert not [d for d in response.diagnostics if d.severity == pb.Diagnostic.ERROR]

        # WHAT the hook receives is the part that breaks providers, so assert it.
        # The framework passes an attrs instance built by BaseResource.from_cty();
        # a provider written against a dict (`config.get(...)`) fails on first use,
        # and a test that only counts calls cannot tell the difference.
        received = seen[0]
        assert attrs.has(type(received)), f"expected an attrs instance, got {type(received).__name__}"
        assert not isinstance(received, dict)

    @pytest.mark.asyncio
    async def test_configuring_twice_is_not_an_error(self, provider_in_hub: Any) -> None:
        """Terraform may configure a provider more than once in a session.

        The "configure once" rule is about multiple provider BLOCKS; a repeated RPC
        must not fail the operation.
        """
        from pyvider.conversion import marshal

        provider = hub.get_component("singleton", "provider")
        schema = provider.schema
        config_cty = schema.block.to_cty_type().validate({})
        request = pb.ConfigureProvider.Request(config=marshal(config_cty, schema=schema.block))

        first = await ConfigureProviderHandler(request, context=None)
        after_first = hub.get_component("singleton", "provider_context")
        second = await ConfigureProviderHandler(request, context=None)

        for response in (first, second):
            assert not [d for d in response.diagnostics if d.severity == pb.Diagnostic.ERROR]

        # The repeat must not republish a context. The live provider refused the
        # second configuration, so a context describing it would describe a state
        # the provider never adopted.
        assert hub.get_component("singleton", "provider_context") is after_first

    @pytest.mark.asyncio
    async def test_hook_failing_after_super_is_reported(self, provider_in_hub: Any) -> None:
        """A configure() hook that fails after calling super() must be reported.

        This is the ordinary shape — `await super().configure(config)` and then
        build the client — and BaseProvider.configure() marks the provider
        configured before the second half runs. Deciding "this is just a repeated
        RPC" from that flag therefore swallowed genuine failures: Terraform was
        told configuration succeeded, no diagnostic was emitted, and no
        ProviderContext was ever published, so every later handler read None.
        """
        from pyvider.conversion import marshal
        from pyvider.exceptions import ProviderError

        provider = hub.get_component("singleton", "provider")
        hub.unregister("singleton", "provider_context")

        async def failing(self: Any, config: Any) -> None:
            await BaseProvider.configure(self, config)
            raise ProviderError("upstream endpoint unreachable")

        schema = provider.schema
        config_cty = schema.block.to_cty_type().validate({})
        request = pb.ConfigureProvider.Request(config=marshal(config_cty, schema=schema.block))

        with patch.object(type(provider), "configure", failing):
            response = await ConfigureProviderHandler(request, context=None)

        assert [d for d in response.diagnostics if d.severity == pb.Diagnostic.ERROR], (
            "a failed configure() hook was reported to Terraform as success"
        )
        assert hub.get_component("singleton", "provider_context") is None
