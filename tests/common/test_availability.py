"""Tests for msgpack availability detection utilities."""

import importlib
import sys

import pytest

from provide.testkit.logger import mock_logger_factory


@pytest.fixture(autouse=True)
def _reset_availability_module():
    """Ensure a clean import of the availability module for each test."""
    yield
    sys.modules.pop("pyvider.common.utils.availability", None)


def _import_with(monkeypatch: pytest.MonkeyPatch, *, spec_result, logger):
    """Import the availability module with patched dependencies."""
    monkeypatch.setattr("importlib.util.find_spec", lambda _: spec_result)
    monkeypatch.setattr("provide.foundation.logger", logger, raising=False)
    module = importlib.import_module("pyvider.common.utils.availability")
    return module


def test_has_msgpack_when_library_present(monkeypatch: pytest.MonkeyPatch) -> None:
    """The module should flag availability and log success when msgpack exists."""
    logger = mock_logger_factory()

    module = _import_with(monkeypatch, spec_result=object(), logger=logger)

    assert module.HAS_MSGPACK is True
    logger.info.assert_called_once_with("📦 msgpack library loaded successfully.")
    logger.warning.assert_not_called()
    logger.error.assert_not_called()


def test_logs_warning_when_msgpack_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    """The module should warn and disable features when msgpack cannot be located."""
    logger = mock_logger_factory()

    module = _import_with(monkeypatch, spec_result=None, logger=logger)

    assert module.HAS_MSGPACK is False
    logger.warning.assert_called_once_with("⚠️ msgpack library not found. msgpack features will be unavailable.")
    logger.info.assert_not_called()
    logger.error.assert_not_called()


def test_logs_error_when_detection_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    """Unexpected errors should be surfaced while falling back to HAS_MSGPACK=False."""
    logger = mock_logger_factory()

    def _boom(_: str):
        raise RuntimeError("boom")

    monkeypatch.setattr("importlib.util.find_spec", _boom)
    monkeypatch.setattr("provide.foundation.logger", logger, raising=False)

    module = importlib.import_module("pyvider.common.utils.availability")

    assert module.HAS_MSGPACK is False
    logger.error.assert_called_once()
    message = logger.error.call_args.args[0]
    assert "❌ Error checking msgpack availability" in message
    assert "boom" in message
