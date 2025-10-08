"""Tests for CLI entrypoint modules."""

import importlib

import pytest


def test_cli_main_invokes_cli_and_shutdown(patch_fixture) -> None:
    """Ensure the CLI entrypoint delegates to click and cleans up Foundation."""
    import pyvider.cli.__main__ as cli_entrypoint

    mock_cli = patch_fixture("pyvider.cli.__main__.cli")
    mock_shutdown = patch_fixture("pyvider.cli.__main__.shutdown_foundation", return_value="sentinel")
    mock_run = patch_fixture("pyvider.cli.__main__.asyncio.run")

    cli_entrypoint.main()

    mock_cli.assert_called_once_with()
    mock_shutdown.assert_called_once_with()
    mock_run.assert_called_once_with("sentinel")


def test_cli_main_ensures_shutdown_on_error(patch_fixture) -> None:
    """Even when the click command fails, the shutdown routine must run."""
    import pyvider.cli.__main__ as cli_entrypoint

    mock_cli = patch_fixture("pyvider.cli.__main__.cli")
    mock_shutdown = patch_fixture("pyvider.cli.__main__.shutdown_foundation", return_value="sentinel")
    mock_run = patch_fixture("pyvider.cli.__main__.asyncio.run")

    mock_cli.side_effect = RuntimeError("boom")

    with pytest.raises(RuntimeError):
        cli_entrypoint.main()

    mock_shutdown.assert_called_once_with()
    mock_run.assert_called_once_with("sentinel")


def test_package_main_aliases_cli_main() -> None:
    """The package-level __main__ module should expose the CLI entrypoint."""
    cli_entrypoint = importlib.import_module("pyvider.cli.__main__")
    package_entrypoint = importlib.import_module("pyvider.__main__")

    assert package_entrypoint.main is cli_entrypoint.main
