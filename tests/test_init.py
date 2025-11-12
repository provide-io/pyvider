#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for pyvider/__init__.py module."""

from pathlib import Path


def test_version_is_available() -> None:
    """Test that __version__ is available in the package."""
    # Import from source, not installed package
    import importlib.util

    init_path = Path(__file__).parent.parent / "src" / "pyvider" / "__init__.py"
    spec = importlib.util.spec_from_file_location("pyvider_test", init_path)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        assert hasattr(module, "__version__")
        assert isinstance(module.__version__, str)




def test_init_module_structure() -> None:
    """Test the __init__.py module structure."""
    import importlib.util

    init_path = Path(__file__).parent.parent / "src" / "pyvider" / "__init__.py"
    spec = importlib.util.spec_from_file_location("pyvider_test", init_path)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        # Check __all__ is defined
        assert hasattr(module, "__all__")
        assert "__version__" in module.__all__


# 🐍🏗️🔚
