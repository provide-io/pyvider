#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for GetFunctions handler."""

from provide.testkit.mocking import MagicMock, patch
import pytest

from pyvider.protocols.tfprotov6.handlers.get_functions import (
    GetFunctionsHandler,
    _get_functions_impl,
)
import pyvider.protocols.tfprotov6.protobuf as pb


@pytest.fixture
def sample_request() -> pb.GetFunctions.Request:
    """Create sample GetFunctions request."""
    return pb.GetFunctions.Request()


@pytest.fixture
def sample_function_obj() -> MagicMock:
    """Create a sample function object for testing."""
    func_obj = MagicMock()
    func_obj.__name__ = "test_function"
    return func_obj


@pytest.fixture
def sample_function_dict() -> dict:
    """Create a sample function dictionary."""
    return {
        "name": "test_function",
        "description": "A test function",
        "parameters": [],
        "return_type": {"type": "string"},
    }


@pytest.fixture
def sample_proto_function() -> pb.Function:
    """Create a sample protocol buffer function."""
    func = pb.Function()
    func.description = "Test function"
    # Note: 'return' is a Python keyword, so we can't use return=...
    # The return field will be set by the handler if needed
    return func


# Pattern: Structure Tests
class TestGetFunctionsStructure:
    """Test handler structure and basic functionality."""

    @pytest.mark.asyncio
    async def test_handler_returns_response(self, sample_request: pb.GetFunctions.Request) -> None:
        """Test handler returns correct response type."""
        with patch("pyvider.hub.hub") as mock_hub:
            # Clear cache before test
            import pyvider.protocols.tfprotov6.handlers.get_functions as gf_module

            gf_module._cached_functions = None

            mock_hub.get_components.return_value = {}

            response = await GetFunctionsHandler(sample_request, context=None)

            assert isinstance(response, pb.GetFunctions.Response)

    @pytest.mark.asyncio
    async def test_handler_has_empty_functions_when_none_registered(
        self, sample_request: pb.GetFunctions.Request
    ) -> None:
        """Test handler returns empty dict when no functions registered."""
        with patch("pyvider.hub.hub") as mock_hub:
            # Clear cache before test
            import pyvider.protocols.tfprotov6.handlers.get_functions as gf_module

            gf_module._cached_functions = None

            mock_hub.get_components.return_value = {}

            response = await GetFunctionsHandler(sample_request, context=None)

            # Functions is a MessageMapContainer (dict-like)
            assert len(response.functions) == 0

    @pytest.mark.asyncio
    async def test_handler_returns_diagnostics_list(self, sample_request: pb.GetFunctions.Request) -> None:
        """Test handler returns diagnostics list."""
        with patch("pyvider.hub.hub") as mock_hub:
            # Clear cache before test
            import pyvider.protocols.tfprotov6.handlers.get_functions as gf_module

            gf_module._cached_functions = None

            mock_hub.get_components.return_value = {}

            response = await GetFunctionsHandler(sample_request, context=None)

            # Diagnostics is a RepeatedCompositeContainer (list-like)
            assert len(response.diagnostics) == 0


# Pattern: Implementation Tests
class TestGetFunctionsImplementation:
    """Test handler implementation details."""

    @pytest.mark.asyncio
    async def test_successful_function_retrieval(
        self,
        sample_request: pb.GetFunctions.Request,
        sample_function_obj: MagicMock,
        sample_function_dict: dict,
        sample_proto_function: pb.Function,
    ) -> None:
        """Test successful retrieval of registered functions."""
        with (
            patch("pyvider.hub.hub") as mock_hub,
            patch("pyvider.protocols.tfprotov6.handlers.get_functions.function_to_dict") as mock_to_dict,
            patch(
                "pyvider.protocols.tfprotov6.handlers.get_functions.dict_to_proto_function"
            ) as mock_to_proto,
        ):
            # Clear cache before test
            import pyvider.protocols.tfprotov6.handlers.get_functions as gf_module

            gf_module._cached_functions = None

            mock_hub.get_components.return_value = {"test_func": sample_function_obj}
            mock_to_dict.return_value = sample_function_dict
            mock_to_proto.return_value = sample_proto_function

            response = await GetFunctionsHandler(sample_request, context=None)

            assert len(response.functions) == 1
            assert "test_func" in response.functions
            assert response.functions["test_func"] == sample_proto_function

    @pytest.mark.asyncio
    async def test_handles_function_to_dict_exception(
        self, sample_request: pb.GetFunctions.Request, sample_function_obj: MagicMock
    ) -> None:
        """Test handling of function_to_dict conversion errors."""
        with (
            patch("pyvider.hub.hub") as mock_hub,
            patch("pyvider.protocols.tfprotov6.handlers.get_functions.function_to_dict") as mock_to_dict,
        ):
            # Clear cache before test
            import pyvider.protocols.tfprotov6.handlers.get_functions as gf_module

            gf_module._cached_functions = None

            mock_hub.get_components.return_value = {"bad_func": sample_function_obj}
            mock_to_dict.side_effect = ValueError("Conversion error")

            response = await GetFunctionsHandler(sample_request, context=None)

            # Should still return a response, but without the failed function
            assert isinstance(response, pb.GetFunctions.Response)
            assert "bad_func" not in response.functions

    @pytest.mark.asyncio
    async def test_handles_dict_to_proto_exception(
        self,
        sample_request: pb.GetFunctions.Request,
        sample_function_obj: MagicMock,
        sample_function_dict: dict,
    ) -> None:
        """Test handling of dict_to_proto conversion errors."""
        with (
            patch("pyvider.hub.hub") as mock_hub,
            patch("pyvider.protocols.tfprotov6.handlers.get_functions.function_to_dict") as mock_to_dict,
            patch(
                "pyvider.protocols.tfprotov6.handlers.get_functions.dict_to_proto_function"
            ) as mock_to_proto,
        ):
            # Clear cache before test
            import pyvider.protocols.tfprotov6.handlers.get_functions as gf_module

            gf_module._cached_functions = None

            mock_hub.get_components.return_value = {"bad_func": sample_function_obj}
            mock_to_dict.return_value = sample_function_dict
            mock_to_proto.side_effect = RuntimeError("Proto conversion error")

            response = await GetFunctionsHandler(sample_request, context=None)

            # Should still return a response, but without the failed function
            assert isinstance(response, pb.GetFunctions.Response)
            assert "bad_func" not in response.functions

    @pytest.mark.asyncio
    async def test_handles_none_function_dict(
        self, sample_request: pb.GetFunctions.Request, sample_function_obj: MagicMock
    ) -> None:
        """Test handling when function_to_dict returns None."""
        with (
            patch("pyvider.hub.hub") as mock_hub,
            patch("pyvider.protocols.tfprotov6.handlers.get_functions.function_to_dict") as mock_to_dict,
        ):
            # Clear cache before test
            import pyvider.protocols.tfprotov6.handlers.get_functions as gf_module

            gf_module._cached_functions = None

            mock_hub.get_components.return_value = {"null_func": sample_function_obj}
            mock_to_dict.return_value = None

            response = await GetFunctionsHandler(sample_request, context=None)

            # Should skip the function when dict is None
            assert "null_func" not in response.functions

    @pytest.mark.asyncio
    async def test_handles_none_proto_function(
        self,
        sample_request: pb.GetFunctions.Request,
        sample_function_obj: MagicMock,
        sample_function_dict: dict,
    ) -> None:
        """Test handling when dict_to_proto_function returns None."""
        with (
            patch("pyvider.hub.hub") as mock_hub,
            patch("pyvider.protocols.tfprotov6.handlers.get_functions.function_to_dict") as mock_to_dict,
            patch(
                "pyvider.protocols.tfprotov6.handlers.get_functions.dict_to_proto_function"
            ) as mock_to_proto,
        ):
            # Clear cache before test
            import pyvider.protocols.tfprotov6.handlers.get_functions as gf_module

            gf_module._cached_functions = None

            mock_hub.get_components.return_value = {"null_func": sample_function_obj}
            mock_to_dict.return_value = sample_function_dict
            mock_to_proto.return_value = None

            response = await GetFunctionsHandler(sample_request, context=None)

            # Should skip the function when proto is None
            assert "null_func" not in response.functions

    @pytest.mark.asyncio
    async def test_impl_returns_error_diagnostic_on_exception(
        self, sample_request: pb.GetFunctions.Request
    ) -> None:
        """Test implementation returns error diagnostic on unhandled exception."""
        with patch("pyvider.protocols.tfprotov6.handlers.get_functions._get_functions_once") as mock_once:
            mock_once.side_effect = RuntimeError("Critical error")

            response = await _get_functions_impl(sample_request, context=None)

            assert len(response.diagnostics) == 1
            assert response.diagnostics[0].severity == pb.Diagnostic.ERROR
            assert "Function discovery failed" in response.diagnostics[0].summary
            assert "Critical error" in response.diagnostics[0].detail


# Pattern: Caching Tests
class TestGetFunctionsCaching:
    """Test function caching behavior."""

    @pytest.mark.asyncio
    async def test_caches_function_definitions(
        self,
        sample_request: pb.GetFunctions.Request,
        sample_function_obj: MagicMock,
        sample_function_dict: dict,
        sample_proto_function: pb.Function,
    ) -> None:
        """Test that function definitions are cached after first call."""
        with (
            patch("pyvider.hub.hub") as mock_hub,
            patch("pyvider.protocols.tfprotov6.handlers.get_functions.function_to_dict") as mock_to_dict,
            patch(
                "pyvider.protocols.tfprotov6.handlers.get_functions.dict_to_proto_function"
            ) as mock_to_proto,
        ):
            # Clear cache before test
            import pyvider.protocols.tfprotov6.handlers.get_functions as gf_module

            gf_module._cached_functions = None

            mock_hub.get_components.return_value = {"test_func": sample_function_obj}
            mock_to_dict.return_value = sample_function_dict
            mock_to_proto.return_value = sample_proto_function

            # First call
            await GetFunctionsHandler(sample_request, context=None)
            assert mock_hub.get_components.call_count == 1

            # Second call - should use cache
            await GetFunctionsHandler(sample_request, context=None)
            assert mock_hub.get_components.call_count == 1  # Not called again

    @pytest.mark.asyncio
    async def test_returns_cached_result_on_subsequent_calls(
        self,
        sample_request: pb.GetFunctions.Request,
        sample_function_obj: MagicMock,
        sample_function_dict: dict,
        sample_proto_function: pb.Function,
    ) -> None:
        """Test that cached results are returned on subsequent calls."""
        with (
            patch("pyvider.hub.hub") as mock_hub,
            patch("pyvider.protocols.tfprotov6.handlers.get_functions.function_to_dict") as mock_to_dict,
            patch(
                "pyvider.protocols.tfprotov6.handlers.get_functions.dict_to_proto_function"
            ) as mock_to_proto,
        ):
            # Clear cache before test
            import pyvider.protocols.tfprotov6.handlers.get_functions as gf_module

            gf_module._cached_functions = None

            mock_hub.get_components.return_value = {"test_func": sample_function_obj}
            mock_to_dict.return_value = sample_function_dict
            mock_to_proto.return_value = sample_proto_function

            response1 = await GetFunctionsHandler(sample_request, context=None)
            response2 = await GetFunctionsHandler(sample_request, context=None)

            # Both responses should have the same functions
            assert response1.functions == response2.functions


# Pattern: Metrics Tests
class TestGetFunctionsMetrics:
    """Test metrics recording."""

    @pytest.mark.asyncio
    async def test_records_request_metric(self, sample_request: pb.GetFunctions.Request) -> None:
        """Test request counter incremented."""
        with (
            patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_requests") as mock_requests,
            patch("pyvider.hub.hub") as mock_hub,
        ):
            mock_hub.get_components.return_value = {}

            await GetFunctionsHandler(sample_request, context=None)

            mock_requests.inc.assert_called_once_with(handler="GetFunctions")

    @pytest.mark.asyncio
    async def test_records_duration_metric(self, sample_request: pb.GetFunctions.Request) -> None:
        """Test duration observer called."""
        with (
            patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_duration") as mock_duration,
            patch("pyvider.hub.hub") as mock_hub,
        ):
            mock_hub.get_components.return_value = {}

            await GetFunctionsHandler(sample_request, context=None)

            assert mock_duration.observe.call_count == 1
            call_args = mock_duration.observe.call_args
            assert call_args[1]["handler"] == "GetFunctions"
            assert isinstance(call_args[0][0], float)

    @pytest.mark.asyncio
    async def test_records_error_metric_on_exception(self, sample_request: pb.GetFunctions.Request) -> None:
        """Test error counter incremented on exception."""
        with (
            patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_errors") as mock_errors,
            patch("pyvider.protocols.tfprotov6.handlers.get_functions._get_functions_impl") as mock_impl,
        ):
            mock_impl.side_effect = RuntimeError("Test error")

            with pytest.raises(RuntimeError):
                await GetFunctionsHandler(sample_request, context=None)

            mock_errors.inc.assert_called_once_with(handler="GetFunctions")


# Pattern: Edge Cases
class TestGetFunctionsEdgeCases:
    """Test edge cases."""

    @pytest.mark.asyncio
    async def test_with_none_context(self, sample_request: pb.GetFunctions.Request) -> None:
        """Test with None context."""
        with patch("pyvider.hub.hub") as mock_hub:
            mock_hub.get_components.return_value = {}

            response = await GetFunctionsHandler(sample_request, context=None)

            assert isinstance(response, pb.GetFunctions.Response)

    @pytest.mark.asyncio
    async def test_with_multiple_functions(
        self,
        sample_request: pb.GetFunctions.Request,
        sample_function_obj: MagicMock,
        sample_function_dict: dict,
        sample_proto_function: pb.Function,
    ) -> None:
        """Test with multiple registered functions."""
        with (
            patch("pyvider.hub.hub") as mock_hub,
            patch("pyvider.protocols.tfprotov6.handlers.get_functions.function_to_dict") as mock_to_dict,
            patch(
                "pyvider.protocols.tfprotov6.handlers.get_functions.dict_to_proto_function"
            ) as mock_to_proto,
        ):
            # Clear cache before test
            import pyvider.protocols.tfprotov6.handlers.get_functions as gf_module

            gf_module._cached_functions = None

            mock_hub.get_components.return_value = {
                "func1": sample_function_obj,
                "func2": sample_function_obj,
                "func3": sample_function_obj,
            }
            mock_to_dict.return_value = sample_function_dict
            mock_to_proto.return_value = sample_proto_function

            response = await GetFunctionsHandler(sample_request, context=None)

            assert len(response.functions) == 3
            assert "func1" in response.functions
            assert "func2" in response.functions
            assert "func3" in response.functions

    @pytest.mark.asyncio
    async def test_mixed_success_and_failure(
        self,
        sample_request: pb.GetFunctions.Request,
        sample_function_obj: MagicMock,
        sample_function_dict: dict,
        sample_proto_function: pb.Function,
    ) -> None:
        """Test with mix of successful and failed function conversions."""
        with (
            patch("pyvider.hub.hub") as mock_hub,
            patch("pyvider.protocols.tfprotov6.handlers.get_functions.function_to_dict") as mock_to_dict,
            patch(
                "pyvider.protocols.tfprotov6.handlers.get_functions.dict_to_proto_function"
            ) as mock_to_proto,
        ):
            # Clear cache before test
            import pyvider.protocols.tfprotov6.handlers.get_functions as gf_module

            gf_module._cached_functions = None

            mock_hub.get_components.return_value = {
                "good_func": sample_function_obj,
                "bad_func": sample_function_obj,
            }

            def to_dict_side_effect(func_obj: MagicMock) -> dict | None:
                if func_obj == sample_function_obj:
                    # Alternate between success and failure
                    if not hasattr(to_dict_side_effect, "count"):
                        to_dict_side_effect.count = 0
                    to_dict_side_effect.count += 1
                    if to_dict_side_effect.count == 1:
                        return sample_function_dict
                    raise ValueError("Conversion failed")
                return None

            mock_to_dict.side_effect = to_dict_side_effect
            mock_to_proto.return_value = sample_proto_function

            response = await GetFunctionsHandler(sample_request, context=None)

            # Only the successful function should be in the response
            assert len(response.functions) == 1
            assert "good_func" in response.functions


# 🐍🏗️🔚
