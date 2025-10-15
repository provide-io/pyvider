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
