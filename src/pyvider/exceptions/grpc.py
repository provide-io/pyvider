#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from provide.foundation.errors import NetworkError as FoundationNetworkError

from pyvider.exceptions.base import PluginError


class GRPCError(PluginError):
    """Base class for gRPC-related errors."""

    def _default_code(self) -> str:
        return "GRPC_ERROR"


class GRPCConnectionError(GRPCError):
    """Raised when a gRPC connection fails."""

    def _default_code(self) -> str:
        return "GRPC_CONNECTION_ERROR"


class NetworkError(FoundationNetworkError):
    """Raised for general gRPC network issues.

    Inherits directly from foundation's NetworkError for
    automatic retry and circuit breaker support.
    """

    def _default_code(self) -> str:
        return "NETWORK_ERROR"


class RateLimitError(NetworkError):
    """Raised when a gRPC operation is rate-limited."""

    def _default_code(self) -> str:
        return "RATE_LIMIT_ERROR"


# 🐍🏗️🔚
