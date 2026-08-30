#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for msgpack availability detection utilities."""

from collections.abc import Generator
import importlib
import sys
from typing import Never

from provide.testkit.logger import mock_logger_factory
import pytest


@pytest.fixture(autouse=True)
def _reset_availability_module() -> Generator[None, None, None]:
    """Ensure a clean import of the availability module for each test."""
    sys.modules.pop("pyvider.common.utils.availability", None)
    yield
    sys.modules.pop("pyvider.common.utils.availability", None)


def _import_with(monkeypatch: pytest.MonkeyPatch, *, spec_result: object | None, logger: any) -> any:
    """Import the availability module with patched dependencies."""
    original_find_spec = importlib.util.find_spec

    def _find_spec(name: str, *args: any, **kwargs: any) -> any:
        if name == "msgpack":
            return spec_result
        return original_find_spec(name, *args, **kwargs)

    monkeypatch.setattr(importlib.util, "find_spec", _find_spec)
    foundation_logger_core = importlib.import_module("provide.foundation.logger.core")
    monkeypatch.setattr(foundation_logger_core, "get_global_logger", lambda: logger)
    return importlib.import_module("pyvider.common.utils.availability")


def test_has_msgpack_when_library_present(monkeypatch: pytest.MonkeyPatch) -> None:
    """The module should flag availability and log success when msgpack exists."""
    logger = mock_logger_factory()

    module = _import_with(monkeypatch, spec_result=object(), logger=logger)

    assert module.HAS_MSGPACK is True
    logger.warning.assert_not_called()
    logger.error.assert_not_called()


def test_logs_warning_when_msgpack_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    """The module should warn and disable features when msgpack cannot be located."""
    logger = mock_logger_factory()

    module = _import_with(monkeypatch, spec_result=None, logger=logger)

    assert module.HAS_MSGPACK is False
    logger.warning.assert_called_once_with(
        "⚠️ msgpack library not found. msgpack features will be unavailable."
    )
    logger.info.assert_not_called()
    logger.error.assert_not_called()


def test_logs_error_when_detection_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    """Unexpected errors should be surfaced while falling back to HAS_MSGPACK=False."""
    logger = mock_logger_factory()

    def _boom(_: str) -> Never:
        raise RuntimeError("boom")

    original_find_spec = importlib.util.find_spec

    def _find_spec(name: str, *args: any, **kwargs: any) -> any:
        if name == "msgpack":
            return _boom(name)
        return original_find_spec(name, *args, **kwargs)

    monkeypatch.setattr(importlib.util, "find_spec", _find_spec)
    foundation_logger_core = importlib.import_module("provide.foundation.logger.core")
    monkeypatch.setattr(foundation_logger_core, "get_global_logger", lambda: logger)

    module = importlib.import_module("pyvider.common.utils.availability")

    assert module.HAS_MSGPACK is False
    logger.error.assert_called_once()
    message = logger.error.call_args.args[0]
    assert "Error checking msgpack availability" in message
    assert "boom" in logger.error.call_args.kwargs.get("error", "")


# 🐍🏗️🔚
