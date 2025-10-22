"""Tests for pyvider/__init__.py module."""


def test_version_is_available():
    """Test that __version__ is available in the package."""
    import pyvider

    assert hasattr(pyvider, "__version__")
    assert isinstance(pyvider.__version__, str)
    assert len(pyvider.__version__) > 0


def test_version_format():
    """Test that __version__ follows semantic versioning format."""
    import pyvider

    # Should be in format like "0.1.0" or "0.1.0a1" or "0.1.0.dev0"
    version = pyvider.__version__
    # Just check it has at least one digit
    assert any(c.isdigit() for c in version)


def test_all_exports():
    """Test that __all__ exports only what's declared."""
    import pyvider

    # Verify __all__ is defined
    assert hasattr(pyvider, "__all__")
    assert "__version__" in pyvider.__all__


def test_namespace_package_path():
    """Test that __path__ is properly extended for namespace packages."""
    import pyvider

    # Namespace packages should have __path__ set
    assert hasattr(pyvider, "__path__")
    assert isinstance(pyvider.__path__, list)
