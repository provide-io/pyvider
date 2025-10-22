import asyncio
import os
from pathlib import Path
import sys
from typing import Any

import click

from pyvider.cli.main import cli

# Terraform's magic cookie value - this must match what Terraform sends
# See: https://github.com/hashicorp/go-plugin
TERRAFORM_PLUGIN_MAGIC_COOKIE = "d602bf8f470bc67ca7faa0386276bbdd4330efaf76d1a219cb4d6991ca9872b2"
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


async def x__run_provider_server__mutmut_orig(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_1(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = None
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_2(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get(None, "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_3(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", None)
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_4(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_5(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", )
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_6(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("XXlogging.levelXX", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_7(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("LOGGING.LEVEL", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_8(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "XXINFOXX")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_9(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "info")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_10(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = None
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_11(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get(None, "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_12(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", None)
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_13(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_14(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", )
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_15(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("XXlogging.formatXX", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_16(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("LOGGING.FORMAT", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_17(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "XXkey_valueXX")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_18(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "KEY_VALUE")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_19(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = None
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_20(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["XXPYVIDER_LOG_LEVELXX"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_21(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["pyvider_log_level"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_22(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = None
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_23(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["XXPYVIDER_LOG_CONSOLE_FORMATTERXX"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_24(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["pyvider_log_console_formatter"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_25(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info(None, domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_26(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain=None)

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_27(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info(domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_28(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", )

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_29(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("XXTelemetry configured for provider server mode.XX", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_30(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_31(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("TELEMETRY CONFIGURED FOR PROVIDER SERVER MODE.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_32(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="XXsystemXX")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_33(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="SYSTEM")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_34(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(None, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_35(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, None):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_36(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr("done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_37(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, ):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_38(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "XXdoneXX"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_39(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "DONE"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_40(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = None
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_41(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(None)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_42(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = None

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_43(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = False

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_44(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = None
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_45(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(None)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_46(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = None
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_47(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(None)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_48(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(None, domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_49(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain=None)

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_50(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_51(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", )

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_52(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="XXsystemXX")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_53(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="SYSTEM")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_54(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = None
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_55(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register(None, "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_56(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", None, provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_57(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", None)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_58(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_59(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_60(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", )
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_61(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("XXsingletonXX", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_62(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("SINGLETON", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_63(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "XXproviderXX", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_64(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "PROVIDER", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_65(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = None
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_66(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = None

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_67(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(None)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_68(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = None

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_69(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "XXPLUGIN_MAGIC_COOKIE_KEYXX": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_70(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "plugin_magic_cookie_key": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_71(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "XXTF_PLUGIN_MAGIC_COOKIEXX",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_72(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "tf_plugin_magic_cookie",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_73(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "XXPLUGIN_MAGIC_COOKIE_VALUEXX": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_74(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "plugin_magic_cookie_value": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_75(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "XXPLUGIN_TIMEOUT_GRACEFUL_SHUTDOWNXX": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_76(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "plugin_timeout_graceful_shutdown": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_77(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get(None, 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_78(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", None),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_79(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get(5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_80(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", ),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_81(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("XXserver.timeout_graceful_shutdownXX", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_82(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("SERVER.TIMEOUT_GRACEFUL_SHUTDOWN", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_83(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 6),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_84(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = None
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_85(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=None, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_86(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=None, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_87(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=None)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_88(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_89(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_90(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, )
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_91(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info(None, domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_92(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain=None)
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_93(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info(domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_94(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", )
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_95(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("XXProvider server has shut down gracefully.XX", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_96(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_97(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("PROVIDER SERVER HAS SHUT DOWN GRACEFULLY.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_98(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="XXsystemXX")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_99(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="SYSTEM")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_100(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = None
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_101(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger(None)
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_102(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("XXpyvider.criticalXX")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_103(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("PYVIDER.CRITICAL")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_104(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(None, exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_105(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=None)
        sys.exit(1)


async def x__run_provider_server__mutmut_106(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(exc_info=True)
        sys.exit(1)


async def x__run_provider_server__mutmut_107(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", )
        sys.exit(1)


async def x__run_provider_server__mutmut_108(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=False)
        sys.exit(1)


async def x__run_provider_server__mutmut_109(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(None)


async def x__run_provider_server__mutmut_110(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from attrs import define, field
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.providers.provider import PyviderProvider
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

    def _configure_telemetry(config: PyviderConfig) -> None:
        log_level = config.get("logging.level", "INFO")
        log_format = config.get("logging.format", "key_value")
        os.environ["PYVIDER_LOG_LEVEL"] = log_level
        os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
        # Note: Foundation automatically sets up logging on import, no explicit setup needed
        logger.info("Telemetry configured for provider server mode.", domain="system")

    @define
    class PyviderProtocol(RPCPluginProtocol):
        _method_types: dict[str, str] = field(factory=dict)

        def __attrs_post_init__(self) -> None:
            self._method_types.update(
                {
                    "/plugin.GRPCStdio/StreamStdio": "stream_stream",
                    "/tfplugin6.Provider/StopProvider": "unary_unary",
                }
            )

        def get_method_type(self, method_name: str) -> str:
            return self._method_types.get(method_name, "unary_unary")

        async def get_grpc_descriptors(self) -> tuple[Any, str]:
            return pb.DESCRIPTOR, "tfplugin6.Provider"

        async def add_to_server(self, handler: Any, server: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)

    async def _discover_components_once() -> None:
        if hasattr(_discover_components_once, "done"):
            return
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        _discover_components_once.done = True

    try:
        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(f"Provider initialized with launch method: {launch_context.method.value}", domain="system")

        await _discover_components_once()
        provider_instance = PyviderProvider()
        await provider_instance.setup()
        hub.register("singleton", "provider", provider_instance)
        protocol = PyviderProtocol()
        handler = ProviderHandler(provider_instance)

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        server = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        await server.serve()
        logger.info("Provider server has shut down gracefully.", domain="system")
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(f"Provider server failed to start or crashed: {e}", exc_info=True)
        sys.exit(2)

x__run_provider_server__mutmut_mutants : ClassVar[MutantDict] = {
'x__run_provider_server__mutmut_1': x__run_provider_server__mutmut_1, 
    'x__run_provider_server__mutmut_2': x__run_provider_server__mutmut_2, 
    'x__run_provider_server__mutmut_3': x__run_provider_server__mutmut_3, 
    'x__run_provider_server__mutmut_4': x__run_provider_server__mutmut_4, 
    'x__run_provider_server__mutmut_5': x__run_provider_server__mutmut_5, 
    'x__run_provider_server__mutmut_6': x__run_provider_server__mutmut_6, 
    'x__run_provider_server__mutmut_7': x__run_provider_server__mutmut_7, 
    'x__run_provider_server__mutmut_8': x__run_provider_server__mutmut_8, 
    'x__run_provider_server__mutmut_9': x__run_provider_server__mutmut_9, 
    'x__run_provider_server__mutmut_10': x__run_provider_server__mutmut_10, 
    'x__run_provider_server__mutmut_11': x__run_provider_server__mutmut_11, 
    'x__run_provider_server__mutmut_12': x__run_provider_server__mutmut_12, 
    'x__run_provider_server__mutmut_13': x__run_provider_server__mutmut_13, 
    'x__run_provider_server__mutmut_14': x__run_provider_server__mutmut_14, 
    'x__run_provider_server__mutmut_15': x__run_provider_server__mutmut_15, 
    'x__run_provider_server__mutmut_16': x__run_provider_server__mutmut_16, 
    'x__run_provider_server__mutmut_17': x__run_provider_server__mutmut_17, 
    'x__run_provider_server__mutmut_18': x__run_provider_server__mutmut_18, 
    'x__run_provider_server__mutmut_19': x__run_provider_server__mutmut_19, 
    'x__run_provider_server__mutmut_20': x__run_provider_server__mutmut_20, 
    'x__run_provider_server__mutmut_21': x__run_provider_server__mutmut_21, 
    'x__run_provider_server__mutmut_22': x__run_provider_server__mutmut_22, 
    'x__run_provider_server__mutmut_23': x__run_provider_server__mutmut_23, 
    'x__run_provider_server__mutmut_24': x__run_provider_server__mutmut_24, 
    'x__run_provider_server__mutmut_25': x__run_provider_server__mutmut_25, 
    'x__run_provider_server__mutmut_26': x__run_provider_server__mutmut_26, 
    'x__run_provider_server__mutmut_27': x__run_provider_server__mutmut_27, 
    'x__run_provider_server__mutmut_28': x__run_provider_server__mutmut_28, 
    'x__run_provider_server__mutmut_29': x__run_provider_server__mutmut_29, 
    'x__run_provider_server__mutmut_30': x__run_provider_server__mutmut_30, 
    'x__run_provider_server__mutmut_31': x__run_provider_server__mutmut_31, 
    'x__run_provider_server__mutmut_32': x__run_provider_server__mutmut_32, 
    'x__run_provider_server__mutmut_33': x__run_provider_server__mutmut_33, 
    'x__run_provider_server__mutmut_34': x__run_provider_server__mutmut_34, 
    'x__run_provider_server__mutmut_35': x__run_provider_server__mutmut_35, 
    'x__run_provider_server__mutmut_36': x__run_provider_server__mutmut_36, 
    'x__run_provider_server__mutmut_37': x__run_provider_server__mutmut_37, 
    'x__run_provider_server__mutmut_38': x__run_provider_server__mutmut_38, 
    'x__run_provider_server__mutmut_39': x__run_provider_server__mutmut_39, 
    'x__run_provider_server__mutmut_40': x__run_provider_server__mutmut_40, 
    'x__run_provider_server__mutmut_41': x__run_provider_server__mutmut_41, 
    'x__run_provider_server__mutmut_42': x__run_provider_server__mutmut_42, 
    'x__run_provider_server__mutmut_43': x__run_provider_server__mutmut_43, 
    'x__run_provider_server__mutmut_44': x__run_provider_server__mutmut_44, 
    'x__run_provider_server__mutmut_45': x__run_provider_server__mutmut_45, 
    'x__run_provider_server__mutmut_46': x__run_provider_server__mutmut_46, 
    'x__run_provider_server__mutmut_47': x__run_provider_server__mutmut_47, 
    'x__run_provider_server__mutmut_48': x__run_provider_server__mutmut_48, 
    'x__run_provider_server__mutmut_49': x__run_provider_server__mutmut_49, 
    'x__run_provider_server__mutmut_50': x__run_provider_server__mutmut_50, 
    'x__run_provider_server__mutmut_51': x__run_provider_server__mutmut_51, 
    'x__run_provider_server__mutmut_52': x__run_provider_server__mutmut_52, 
    'x__run_provider_server__mutmut_53': x__run_provider_server__mutmut_53, 
    'x__run_provider_server__mutmut_54': x__run_provider_server__mutmut_54, 
    'x__run_provider_server__mutmut_55': x__run_provider_server__mutmut_55, 
    'x__run_provider_server__mutmut_56': x__run_provider_server__mutmut_56, 
    'x__run_provider_server__mutmut_57': x__run_provider_server__mutmut_57, 
    'x__run_provider_server__mutmut_58': x__run_provider_server__mutmut_58, 
    'x__run_provider_server__mutmut_59': x__run_provider_server__mutmut_59, 
    'x__run_provider_server__mutmut_60': x__run_provider_server__mutmut_60, 
    'x__run_provider_server__mutmut_61': x__run_provider_server__mutmut_61, 
    'x__run_provider_server__mutmut_62': x__run_provider_server__mutmut_62, 
    'x__run_provider_server__mutmut_63': x__run_provider_server__mutmut_63, 
    'x__run_provider_server__mutmut_64': x__run_provider_server__mutmut_64, 
    'x__run_provider_server__mutmut_65': x__run_provider_server__mutmut_65, 
    'x__run_provider_server__mutmut_66': x__run_provider_server__mutmut_66, 
    'x__run_provider_server__mutmut_67': x__run_provider_server__mutmut_67, 
    'x__run_provider_server__mutmut_68': x__run_provider_server__mutmut_68, 
    'x__run_provider_server__mutmut_69': x__run_provider_server__mutmut_69, 
    'x__run_provider_server__mutmut_70': x__run_provider_server__mutmut_70, 
    'x__run_provider_server__mutmut_71': x__run_provider_server__mutmut_71, 
    'x__run_provider_server__mutmut_72': x__run_provider_server__mutmut_72, 
    'x__run_provider_server__mutmut_73': x__run_provider_server__mutmut_73, 
    'x__run_provider_server__mutmut_74': x__run_provider_server__mutmut_74, 
    'x__run_provider_server__mutmut_75': x__run_provider_server__mutmut_75, 
    'x__run_provider_server__mutmut_76': x__run_provider_server__mutmut_76, 
    'x__run_provider_server__mutmut_77': x__run_provider_server__mutmut_77, 
    'x__run_provider_server__mutmut_78': x__run_provider_server__mutmut_78, 
    'x__run_provider_server__mutmut_79': x__run_provider_server__mutmut_79, 
    'x__run_provider_server__mutmut_80': x__run_provider_server__mutmut_80, 
    'x__run_provider_server__mutmut_81': x__run_provider_server__mutmut_81, 
    'x__run_provider_server__mutmut_82': x__run_provider_server__mutmut_82, 
    'x__run_provider_server__mutmut_83': x__run_provider_server__mutmut_83, 
    'x__run_provider_server__mutmut_84': x__run_provider_server__mutmut_84, 
    'x__run_provider_server__mutmut_85': x__run_provider_server__mutmut_85, 
    'x__run_provider_server__mutmut_86': x__run_provider_server__mutmut_86, 
    'x__run_provider_server__mutmut_87': x__run_provider_server__mutmut_87, 
    'x__run_provider_server__mutmut_88': x__run_provider_server__mutmut_88, 
    'x__run_provider_server__mutmut_89': x__run_provider_server__mutmut_89, 
    'x__run_provider_server__mutmut_90': x__run_provider_server__mutmut_90, 
    'x__run_provider_server__mutmut_91': x__run_provider_server__mutmut_91, 
    'x__run_provider_server__mutmut_92': x__run_provider_server__mutmut_92, 
    'x__run_provider_server__mutmut_93': x__run_provider_server__mutmut_93, 
    'x__run_provider_server__mutmut_94': x__run_provider_server__mutmut_94, 
    'x__run_provider_server__mutmut_95': x__run_provider_server__mutmut_95, 
    'x__run_provider_server__mutmut_96': x__run_provider_server__mutmut_96, 
    'x__run_provider_server__mutmut_97': x__run_provider_server__mutmut_97, 
    'x__run_provider_server__mutmut_98': x__run_provider_server__mutmut_98, 
    'x__run_provider_server__mutmut_99': x__run_provider_server__mutmut_99, 
    'x__run_provider_server__mutmut_100': x__run_provider_server__mutmut_100, 
    'x__run_provider_server__mutmut_101': x__run_provider_server__mutmut_101, 
    'x__run_provider_server__mutmut_102': x__run_provider_server__mutmut_102, 
    'x__run_provider_server__mutmut_103': x__run_provider_server__mutmut_103, 
    'x__run_provider_server__mutmut_104': x__run_provider_server__mutmut_104, 
    'x__run_provider_server__mutmut_105': x__run_provider_server__mutmut_105, 
    'x__run_provider_server__mutmut_106': x__run_provider_server__mutmut_106, 
    'x__run_provider_server__mutmut_107': x__run_provider_server__mutmut_107, 
    'x__run_provider_server__mutmut_108': x__run_provider_server__mutmut_108, 
    'x__run_provider_server__mutmut_109': x__run_provider_server__mutmut_109, 
    'x__run_provider_server__mutmut_110': x__run_provider_server__mutmut_110
}

def _run_provider_server(*args, **kwargs):
    result = _mutmut_trampoline(x__run_provider_server__mutmut_orig, x__run_provider_server__mutmut_mutants, args, kwargs)
    return result 

_run_provider_server.__signature__ = _mutmut_signature(x__run_provider_server__mutmut_orig)
x__run_provider_server__mutmut_orig.__name__ = 'x__run_provider_server'


@cli.command("provide")
@click.option(
    "--force",
    is_flag=True,
    default=False,
    help="Force the provider to start in server mode, ignoring the magic cookie check.",
)
@click.pass_context
def provide_cmd(ctx: click.Context, force: bool, **kwargs: Any) -> None:
    """
    Starts the provider in gRPC server mode for Terraform. (This is the default
    action when run by Terraform or when the binary is run with no arguments).
    """
    # --- FIX: Import discovery and error handling utilities ---
    from pyvider.cli.components_commands import _handle_discovery_errors
    from pyvider.hub.components import registry
    from pyvider.hub.discovery import ComponentDiscovery

    magic_cookie = os.environ.get("TF_PLUGIN_MAGIC_COOKIE")
    script_name = Path(sys.argv[0]).name

    # Check if Terraform is trying to launch us but we can't detect it properly
    if magic_cookie and not force and "terraform-provider" not in script_name.lower() and "terraform-provider" not in sys.argv[0].lower():
        click.secho("\n" + "─" * 70, fg="red")
        click.secho(" ❌  Provider Detection Error", fg="red", bold=True)
        click.secho("─" * 70, fg="red")
        click.secho(
            "\nTerraform is trying to launch this provider (TF_PLUGIN_MAGIC_COOKIE is set),\n"
            f"but the binary name '{script_name}' doesn't contain 'terraform-provider'.",
            fg="yellow",
        )
        click.secho(
            "\nThis usually happens when:",
            fg="white",
        )
        click.secho(
            "  1. The provider binary was renamed or symlinked incorrectly",
            fg="white",
        )
        click.secho(
            "  2. The PSPF package was built with an incorrect command configuration",
            fg="white",
        )
        click.secho("\nTo fix this:", fg="cyan", bold=True)
        click.secho(
            f"  • Ensure the binary is named 'terraform-provider-pyvider' (not '{script_name}')",
            fg="cyan",
        )
        click.secho(
            "  • Check the [tool.flavor] configuration in pyproject.toml",
            fg="cyan",
        )
        click.secho(
            "  • Rebuild the package with the correct command path",
            fg="cyan",
        )
        click.secho("─" * 70, fg="red")
        click.secho("\nDebug Info:", fg="white", dim=True)
        click.secho(f"  sys.argv[0]: {sys.argv[0]}", fg="white", dim=True)
        click.secho(f"  script_name: {script_name}", fg="white", dim=True)
        click.secho(f"  TF_PLUGIN_MAGIC_COOKIE: {magic_cookie[:20]}...", fg="white", dim=True)
        sys.exit(1)

    if not magic_cookie and not force:
        # Show launch context in interactive mode
        from pyvider.common.launch_context import detect_launch_context

        launch_context = detect_launch_context()

        click.secho("\n" + "─" * 70, fg="cyan")
        click.secho(" i  Interactive Mode", fg="cyan", bold=True)
        click.secho("─" * 70, fg="cyan")
        click.secho(
            "\nThis executable is a Pyvider-based Terraform provider. It was not started by\n"
            "Terraform, so it has entered interactive CLI mode.",
            fg="white",
        )

        # Display launch context
        click.secho("\n🚀 Launch Context:", fg="green", bold=True)
        click.secho(f"   Method: {launch_context.method.value}", fg="white")
        click.secho(f"   Executable: {launch_context.executable_path}", fg="white")
        click.secho(f"   Python: {launch_context.python_executable}", fg="white")

        if launch_context.details:
            for key, value in list(launch_context.details.items())[:3]:  # Show first 3 details
                click.secho(f"   {key}: {value}", fg="white")

        click.secho(
            "\nYou can use the commands below to inspect the provider's components.",
            fg="white",
        )
        click.secho(
            f"\nTo run in server mode for testing, use: '{script_name} provide --force'",
            fg="yellow",
        )
        click.secho("─" * 70, fg="cyan")

        # Display the full help message for the main CLI group
        click.echo("\n" + ctx.parent.get_help())
        sys.exit(0)

    # --- FIX: Run discovery and handle errors before starting the server ---
    pyvider_ctx = ctx.obj
    asyncio.run(
        pyvider_ctx._ensure_components_discovered(registry, ComponentDiscovery, click.echo, click.secho)
    )
    _handle_discovery_errors(pyvider_ctx)

    # If --force is used, provide a dummy cookie value.
    cookie_to_use = magic_cookie or "forced-by-cli"

    try:
        asyncio.run(_run_provider_server(cookie_to_use))
    except KeyboardInterrupt:
        click.echo("\n🚦 Provider service interrupted by user.")
        sys.exit(0)
