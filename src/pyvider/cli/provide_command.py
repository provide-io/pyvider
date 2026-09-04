#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


import asyncio
import contextlib
import os
from pathlib import Path
import sys
from typing import Any

import click
from provide.foundation.console import perr, pout

from pyvider.cli.main import cli

# Terraform's magic cookie value - this must match what Terraform sends
# See: https://github.com/hashicorp/go-plugin
TERRAFORM_PLUGIN_MAGIC_COOKIE = "d602bf8f470bc67ca7faa0386276bbdd4330efaf76d1a219cb4d6991ca9872b2"


def _configure_telemetry(config: Any) -> None:
    # Deferred Imports for Provider Mode
    from provide.foundation import logger

    # `PyviderConfig` documents "Environment Variable > Config File > Default",
    # and this wrote the config file's value over the environment, inverting it.
    # `setdefault` restores the documented order; an explicit `--log-level` has
    # already been applied to the environment in `main()`, before Foundation was
    # configured, so it wins over both.
    os.environ.setdefault("PYVIDER_LOG_LEVEL", config.get("logging.level", "INFO"))
    # Foundation reads PROVIDE_LOG_CONSOLE_FORMATTER; this used to write a
    # PYVIDER_-prefixed name that nothing reads, so `[logging] format` was inert.
    os.environ.setdefault("PROVIDE_LOG_CONSOLE_FORMATTER", config.get("logging.format", "key_value"))
    # Note: Foundation automatically sets up logging on import, no explicit setup needed
    logger.info("Telemetry configured for provider server mode.", domain="system")


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


def _report_detection_error(script_name: str, magic_cookie: str) -> None:
    """Explain a binary name Terraform will not accept, and exit non-zero.

    Terraform sets the magic cookie for any plugin it launches, but go-plugin
    resolves the provider by a binary named `terraform-provider-*`. A mismatch
    means the practitioner is one rename away from a working provider, so say
    exactly that rather than failing the handshake with nothing.
    """
    perr("\n" + "─" * 70, fg="red")
    perr(" ❌  Provider Detection Error", fg="red", bold=True)
    perr("─" * 70, fg="red")
    perr(
        "\nTerraform is trying to launch this provider (TF_PLUGIN_MAGIC_COOKIE is set),\n"
        f"but the binary name '{script_name}' doesn't contain 'terraform-provider'.",
        fg="yellow",
    )
    perr(
        "\nThis usually happens when:",
        fg="white",
    )
    perr(
        "  1. The provider binary was renamed or symlinked incorrectly",
        fg="white",
    )
    perr(
        "  2. The PSPF package was built with an incorrect command configuration",
        fg="white",
    )
    perr("\nTo fix this:", fg="cyan", bold=True)
    perr(
        f"  • Ensure the binary is named 'terraform-provider-pyvider' (not '{script_name}')",
        fg="cyan",
    )
    perr(
        "  • Check the [tool.flavor] configuration in pyproject.toml",
        fg="cyan",
    )
    perr(
        "  • Rebuild the package with the correct command path",
        fg="cyan",
    )
    perr("─" * 70, fg="red")
    perr("\nDebug Info:", fg="white", dim=True)
    perr(f"  sys.argv[0]: {sys.argv[0]}", fg="white", dim=True)
    perr(f"  script_name: {script_name}", fg="white", dim=True)
    perr(f"  TF_PLUGIN_MAGIC_COOKIE: {magic_cookie[:20]}...", fg="white", dim=True)
    sys.exit(1)


def _build_protocol() -> Any:
    """The RPC protocol object the plugin server speaks.

    Its imports are deferred with the rest of the server machinery: a plain CLI
    invocation must not pay for loading protobuf and grpc.
    """
    from attrs import define, field

    import pyvider.protocols.tfprotov6.protobuf as pb
    from pyvider.rpcplugin import RPCPluginProtocol

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

    return PyviderProtocol()


async def _discover_and_signal(logger: Any, hub: Any, ready_event: asyncio.Event) -> None:
    """Run component discovery and signal when it is done, however it ends.

    The event is set in `finally` deliberately: a failed discovery must still
    release everything waiting on it, or the server hangs instead of serving a
    provider with no components.
    """
    try:
        from pyvider.hub.discovery import ComponentDiscovery

        discovery = ComponentDiscovery(hub)
        await discovery.discover_all()
        logger.debug(
            "Discovery complete, signaling ready event",
            operation="component_discovery",
        )
    except Exception:
        logger.exception(
            "Component discovery failed",
            operation="component_discovery",
        )
    finally:
        ready_event.set()


async def _initialize_and_register_provider(logger: Any, hub: Any, discovery_task: Any) -> None:
    """Instantiate the provider once discovery has finished, and publish it."""
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


def _reject_a_foreign_magic_cookie(magic_cookie: str | None, *, force: bool) -> None:
    """Refuse a cookie that is set but is not Terraform's.

    The value is fixed and public -- a "did a human run this by mistake" guard
    rather than a secret (go-plugin/server.go:49-52). It used to be compared
    against itself: the environment value was read and then handed back as the
    expected value, so any cookie at all was accepted and this guard never
    fired.
    """
    if not magic_cookie or force or magic_cookie == TERRAFORM_PLUGIN_MAGIC_COOKIE:
        return

    perr(
        "TF_PLUGIN_MAGIC_COOKIE is set but does not match the value Terraform uses, "
        "so this process was not launched by Terraform.\n\n"
        "This binary is a Terraform provider plugin. It is meant to be started by "
        "Terraform, not run directly."
    )
    sys.exit(1)


def _report_server_crash(e: Exception) -> None:
    """Explain a failed server start on stderr and exit non-zero.

    Terraform shows the practitioner very little of what a plugin prints, so
    this says everything it can while it still has a terminal to say it on.
    """
    import logging

    logging.basicConfig()
    local_logger = logging.getLogger("pyvider.critical")
    local_logger.error(
        "Provider server failed to start or crashed",
        exc_info=e,
        extra={
            "error_type": type(e).__name__,
            "error_message": str(e),
            "python_version": sys.version,
            "platform": sys.platform,
        },
    )

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


async def _run_provider_server(magic_cookie: str) -> None:
    """
    Initializes and runs the provider in server mode. This function contains
    all imports for the server machinery to prevent them from running during
    standard CLI mode, ensuring a clean and fast CLI experience.
    """
    # --- Deferred Imports for Provider Mode ---
    from provide.foundation import logger

    from pyvider.common.config import PyviderConfig
    from pyvider.handler import ProviderHandler
    from pyvider.hub import hub
    from pyvider.rpcplugin import RPCPluginServer

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
        from pyvider.hub import DISCOVERY_READY_EVENT

        discovery_ready_event = asyncio.Event()
        hub.register("singleton", DISCOVERY_READY_EVENT, discovery_ready_event)

        # Start component discovery immediately as a background task
        logger.debug(
            "Starting component discovery in background",
            operation="component_discovery",
        )

        discovery_task = asyncio.create_task(_discover_and_signal(logger, hub, discovery_ready_event))

        # Create protocol immediately (doesn't need discovery or providers)
        protocol = _build_protocol()

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
        background_init = asyncio.create_task(_initialize_and_register_provider(logger, hub, discovery_task))

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
            else:
                # A task that finished on its own still holds its exception until
                # someone asks for it. Nothing did, so a provider whose
                # initialization failed in the background logged nothing here and
                # surfaced only as asyncio's "Task exception was never retrieved"
                # at interpreter shutdown, long after the RPC that needed it.
                init_error = background_init.exception()
                if init_error is not None:
                    logger.error(
                        "Provider initialization failed in the background",
                        operation="provider_initialization",
                        error_type=type(init_error).__name__,
                        error_message=str(init_error),
                        exc_info=init_error,
                    )

        logger.info(
            "Provider server has shut down gracefully",
            operation="server_shutdown",
            domain="system",
        )
    except Exception as e:
        _report_server_crash(e)


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
        _report_detection_error(script_name, magic_cookie)

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

    _reject_a_foreign_magic_cookie(magic_cookie, force=force)

    cookie_to_use = magic_cookie or TERRAFORM_PLUGIN_MAGIC_COOKIE

    try:
        asyncio.run(_run_provider_server(cookie_to_use))
    except KeyboardInterrupt:
        pout("\n🚦 Provider service interrupted by user.")
        sys.exit(0)


# 🐍🏗️🔚
