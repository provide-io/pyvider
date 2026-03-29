#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


import asyncio
import contextlib
import os
from pathlib import Path
import sys
from typing import Any

import click
from provide.foundation.console import pout

from pyvider.cli.main import cli

# Terraform's magic cookie value - this must match what Terraform sends
# See: https://github.com/hashicorp/go-plugin
TERRAFORM_PLUGIN_MAGIC_COOKIE = "d602bf8f470bc67ca7faa0386276bbdd4330efaf76d1a219cb4d6991ca9872b2"


def _configure_telemetry(config: Any) -> None:
    # Deferred Imports for Provider Mode
    from provide.foundation import logger

    log_level = config.get("logging.level", "INFO")
    log_format = config.get("logging.format", "key_value")
    os.environ["PYVIDER_LOG_LEVEL"] = log_level
    os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = log_format
    # Note: Foundation automatically sets up logging on import, no explicit setup needed
    logger.info("Telemetry configured for provider server mode.", domain="system")


_discovery_done = False


async def _discover_components_once() -> None:
    global _discovery_done
    # Deferred Imports for Provider Mode
    from pyvider.hub import hub
    from pyvider.hub.discovery import ComponentDiscovery

    if _discovery_done:
        return

    discovery = ComponentDiscovery(hub)
    await discovery.discover_all()
    _discovery_done = True


async def _instantiate_providers(logger: Any, hub: Any) -> dict:
    provider_classes = hub.get_components("provider")

    if not provider_classes:
        logger.error(
            "No providers discovered",
            operation="provider_discovery",
            domain="system",
        )
        raise RuntimeError(
            "No providers found. Install a provider package (e.g., pyvider-components) "
            "that registers a provider using @register_provider('name')."
        )

    logger.info(
        "Discovered providers",
        operation="provider_discovery",
        providers=list(provider_classes.keys()),
    )

    provider_instances = {}
    for provider_name, provider_class in provider_classes.items():
        logger.debug(
            "Creating provider instance",
            operation="provider_create",
            provider=provider_name,
        )
        provider_instance = provider_class()
        await provider_instance.setup()
        provider_instances[provider_name] = provider_instance

        logger.debug(
            "Provider setup completed",
            operation="provider_setup",
            provider=provider_name,
        )
    return provider_instances


async def _run_provider_server(magic_cookie: str) -> None:
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
    from pyvider.rpcplugin import RPCPluginProtocol, RPCPluginServer

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
            return pb.DESCRIPTOR, "tfplugin6.Provider"  # type: ignore[attr-defined]

        async def add_to_server(self, server: Any, handler: Any) -> None:
            pb.add_ProviderServicer_to_server(handler, server)  # type: ignore[no-untyped-call]

    try:
        logger.info(
            "Provider server initialization started",
            operation="provider_init",
            python_version=sys.version.split()[0],
            platform=sys.platform,
        )

        config = PyviderConfig()
        _configure_telemetry(config)

        # Log launch context information
        from pyvider.common.launch_context import log_launch_context

        launch_context = log_launch_context(logger.info)
        logger.info(
            "Provider initialized with launch context",
            operation="provider_init",
            launch_method=launch_context.method.value,
            executable=launch_context.executable_path,
            domain="system",
        )

        # --- LAZY INITIALIZATION STRATEGY ---
        # Create an event that will be set when discovery is complete
        discovery_ready_event = asyncio.Event()
        hub.register("singleton", "_discovery_ready_event", discovery_ready_event)

        # Start component discovery immediately as a background task
        logger.debug(
            "Starting component discovery in background",
            operation="component_discovery",
        )

        async def discover_and_signal() -> None:
            """Run discovery and signal when it's complete."""
            await _discover_components_once()
            discovery_ready_event.set()
            logger.debug(
                "Discovery complete, signaling ready event",
                operation="component_discovery",
            )

        discovery_task = asyncio.create_task(discover_and_signal())

        # Create a coroutine for provider initialization (don't schedule yet)
        async def initialize_and_register_provider() -> None:
            """Initialize and register provider after discovery."""
            logger.debug(
                "Waiting for component discovery before provider instantiation",
                operation="provider_init",
            )
            await discovery_task
            logger.debug(
                "Component discovery completed, now instantiating providers",
                operation="provider_init",
            )
            provider_instances = await _instantiate_providers(logger, hub)
            primary_provider = next(iter(provider_instances.values()))
            logger.debug(
                "Primary provider instantiated",
                operation="provider_init",
                provider=next(iter(provider_instances.keys())),
            )
            hub.register("singleton", "provider", primary_provider)
            logger.debug(
                "Primary provider registered in hub",
                operation="hub_register",
                provider=next(iter(provider_instances.keys())),
            )

        # Create protocol immediately (doesn't need discovery or providers)
        protocol = PyviderProtocol()

        # Create handler without a provider - it will fetch from hub on first use
        logger.debug(
            "Creating RPC handler (will use lazy provider from hub)",
            operation="handler_creation",
        )
        handler = ProviderHandler()

        # Configure the RPC plugin server with Terraform's magic cookie
        server_config = {
            "PLUGIN_MAGIC_COOKIE_KEY": "TF_PLUGIN_MAGIC_COOKIE",
            "PLUGIN_MAGIC_COOKIE_VALUE": magic_cookie,  # Pass the actual magic cookie value
            "PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN": config.get("server.timeout_graceful_shutdown", 5),
        }

        logger.info(
            "Starting RPC plugin server",
            operation="server_start",
            magic_cookie_present=bool(magic_cookie),
            graceful_shutdown_timeout=server_config["PLUGIN_TIMEOUT_GRACEFUL_SHUTDOWN"],
            lazy_initialization="enabled (provider initializes in background)",
        )

        server: Any = RPCPluginServer(protocol=protocol, handler=handler, config=server_config)
        hub.register("singleton", "rpc_plugin_server", lambda: server)

        # Schedule provider initialization to run in background immediately
        # Server will start listening while provider initializes
        background_init = asyncio.create_task(initialize_and_register_provider())

        # Yield control to let background tasks start before blocking on server.serve()
        # This ensures provider initialization begins before the RPC server starts blocking
        await asyncio.sleep(0)

        try:
            logger.debug(
                "Starting RPC server to listen for Terraform connections",
                operation="server_startup",
            )
            # Start the server - it will respond to Terraform's handshake within seconds
            # while provider initialization happens in the background
            await server.serve()
        except asyncio.CancelledError:
            # Server was cancelled
            logger.info(
                "Provider server shutting down",
                operation="server_shutdown",
            )
            background_init.cancel()
            raise
        finally:
            # Clean up background initialization task if it's still running
            if not background_init.done():
                background_init.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await background_init

        logger.info(
            "Provider server has shut down gracefully",
            operation="server_shutdown",
            domain="system",
        )
    except Exception as e:
        import logging

        logging.basicConfig()
        local_logger = logging.getLogger("pyvider.critical")
        local_logger.error(
            "Provider server failed to start or crashed",
            exc_info=True,
            extra={
                "error_type": type(e).__name__,
                "error_message": str(e),
                "python_version": sys.version,
                "platform": sys.platform,
            },
        )

        # Enhanced error message for users
        pout("\n" + "═" * 70, fg="red", err=True)
        pout(" ❌  Provider Server Error", fg="red", bold=True, err=True)
        pout("═" * 70, fg="red", err=True)
        pout(
            "\nThe provider server failed to start or crashed unexpectedly.\n",
            fg="white",
            err=True,
        )
        pout(f"Error Type: {type(e).__name__}", fg="yellow", err=True)
        pout(f"Error Message: {e!s}\n", fg="yellow", err=True)

        pout("Troubleshooting Steps:", fg="cyan", bold=True, err=True)
        pout("  1. Check Python version compatibility (requires Python 3.11+)", fg="white", err=True)
        pout("  2. Verify all dependencies are installed: 'uv sync'", fg="white", err=True)
        pout("  3. Check provider configuration in pyproject.toml", fg="white", err=True)
        pout("  4. Review the full error trace above for specific details", fg="white", err=True)
        pout("  5. Enable debug logging: export PYVIDER_LOG_LEVEL=DEBUG", fg="white", err=True)

        pout("\nCommon Causes:", fg="cyan", bold=True, err=True)
        pout("  • Missing or incompatible dependencies", fg="white", err=True)
        pout("  • Invalid provider configuration", fg="white", err=True)
        pout("  • Port already in use (if binding to specific port)", fg="white", err=True)
        pout("  • Insufficient permissions", fg="white", err=True)
        pout("  • Corrupted provider binary or package", fg="white", err=True)

        pout("\nIf the issue persists:", fg="cyan", bold=True, err=True)
        pout("  • Report at: https://github.com/provide-io/pyvider/issues", fg="white", err=True)
        pout(
            f"  • Include: Error type, Python {sys.version.split()[0]}, Platform {sys.platform}",
            fg="white",
            err=True,
        )
        pout("═" * 70, fg="red", err=True)

        sys.exit(1)


@cli.command("provide")
@click.option(
    "--force",
    is_flag=True,
    default=False,
    help="Force the provider to start in server mode, ignoring the magic cookie check.",
)
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], case_sensitive=False),
    default="INFO",
    help="Set the logging level for the provider server.",
)
@click.pass_context
def provide_cmd(ctx: click.Context, /, force: bool, log_level: str, **kwargs: Any) -> None:
    """
    Starts the provider in gRPC server mode for Terraform. (This is the default
    action when run by Terraform or when the binary is run with no arguments).
    """
    magic_cookie = os.environ.get("TF_PLUGIN_MAGIC_COOKIE")
    script_name = Path(sys.argv[0]).name

    # Check if we're being called via the wrapper script
    # (wrapper sets PLUGIN_MAGIC_COOKIE_VALUE from TF_PLUGIN_MAGIC_COOKIE)
    via_wrapper = os.environ.get("PLUGIN_MAGIC_COOKIE_VALUE") is not None

    # Check if Terraform is trying to launch us but we can't detect it properly
    if (
        magic_cookie
        and not force
        and not via_wrapper
        and "terraform-provider" not in script_name.lower()
        and "terraform-provider" not in sys.argv[0].lower()
    ):
        pout("\n" + "─" * 70, fg="red")
        pout(" ❌  Provider Detection Error", fg="red", bold=True)
        pout("─" * 70, fg="red")
        pout(
            "\nTerraform is trying to launch this provider (TF_PLUGIN_MAGIC_COOKIE is set),\n"
            f"but the binary name '{script_name}' doesn't contain 'terraform-provider'.",
            fg="yellow",
        )
        pout(
            "\nThis usually happens when:",
            fg="white",
        )
        pout(
            "  1. The provider binary was renamed or symlinked incorrectly",
            fg="white",
        )
        pout(
            "  2. The PSPF package was built with an incorrect command configuration",
            fg="white",
        )
        pout("\nTo fix this:", fg="cyan", bold=True)
        pout(
            f"  • Ensure the binary is named 'terraform-provider-pyvider' (not '{script_name}')",
            fg="cyan",
        )
        pout(
            "  • Check the [tool.flavor] configuration in pyproject.toml",
            fg="cyan",
        )
        pout(
            "  • Rebuild the package with the correct command path",
            fg="cyan",
        )
        pout("─" * 70, fg="red")
        pout("\nDebug Info:", fg="white", dim=True)
        pout(f"  sys.argv[0]: {sys.argv[0]}", fg="white", dim=True)
        pout(f"  script_name: {script_name}", fg="white", dim=True)
        pout(f"  TF_PLUGIN_MAGIC_COOKIE: {magic_cookie[:20]}...", fg="white", dim=True)
        sys.exit(1)

    if not magic_cookie and not force:
        # Show launch context in interactive mode
        from pyvider.common.launch_context import detect_launch_context

        launch_context = detect_launch_context()

        try:
            pout("\n" + "─" * 70, fg="cyan")
            pout(" i  Interactive Mode", fg="cyan", bold=True)
            pout("─" * 70, fg="cyan")
            pout(
                "\nThis executable is a Pyvider-based Terraform provider. It was not started by\n"
                "Terraform, so it has entered interactive CLI mode.",
                fg="white",
            )

            # Display launch context
            pout("\n🚀 Launch Context:", fg="green", bold=True)
            pout(f"   Method: {launch_context.method.value}", fg="white")
            pout(f"   Executable: {launch_context.executable_path}", fg="white")
            pout(f"   Python: {launch_context.python_executable}", fg="white")

            if launch_context.details:
                for key, value in list(launch_context.details.items())[:3]:  # Show first 3 details
                    pout(f"   {key}: {value}", fg="white")

            pout(
                "\nYou can use the commands below to inspect the provider's components.",
                fg="white",
            )
            pout(
                f"\nTo run in server mode for testing, use: '{script_name} provide --force'",
                fg="yellow",
            )
            pout("─" * 70, fg="cyan")

            # Display the full help message for the main CLI group
            if ctx.parent:
                pout("\n" + ctx.parent.get_help())
            else:
                pout("\nNo parent context available for help")
        except (UnicodeEncodeError, UnicodeDecodeError):
            # If we can't print to console due to encoding issues, just proceed to server mode
            # This happens when running as a plugin with non-UTF-8 console encoding
            pass
        sys.exit(0)

    # If --force is used, provide a dummy cookie value.
    cookie_to_use = magic_cookie or "forced-by-cli"

    try:
        asyncio.run(_run_provider_server(cookie_to_use))
    except KeyboardInterrupt:
        pout("\n🚦 Provider service interrupted by user.")
        sys.exit(0)


# 🐍🏗️🔚
