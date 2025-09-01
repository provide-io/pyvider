# pyvider/exceptions/grpc.py
from pyvider.exceptions.base import PluginError


class GRPCError(PluginError):
    """Base class for gRPC-related errors."""

    pass


class GRPCConnectionError(GRPCError):  # Renamed
    """Raised when a gRPC connection fails."""

    pass


class NetworkError(GRPCError):
    """Raised for general gRPC network issues."""

    pass


class RateLimitError(GRPCError):
    """Raised when a gRPC operation is rate-limited."""

    pass
