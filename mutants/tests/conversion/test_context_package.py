"""Tests for the pyvider.conversion.context package placeholder."""

import importlib
import sys


def test_conversion_context_import_emits_debug(capsys) -> None:
    """Import should succeed and emit the debug notice once."""
    sys.modules.pop("pyvider.conversion.context", None)

    module = importlib.import_module("pyvider.conversion.context")
    captured = capsys.readouterr()
    assert module is not None
    assert "DEBUG: pyvider.conversion.context.__init__.py loaded" in captured.out
