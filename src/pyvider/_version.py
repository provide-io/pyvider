#
# _version.py
#
"""
Version handling for pyvider.
Uses VERSION file with robust fallback mechanisms.
"""

from pathlib import Path


def _find_project_root() -> Path | None:
    """Find the project root directory by looking for VERSION file."""
    current = Path(__file__).parent

    # Walk up the directory tree looking for VERSION file
    while current != current.parent:  # Stop at filesystem root
        version_file = current / "VERSION"
        if version_file.exists():
            return current
        current = current.parent

    return None


def get_version() -> str:
    """Get the current pyvider version.

    Reads from VERSION file if it exists, otherwise falls back to package metadata,
    then to default development version.

    Returns:
        str: The current version string
    """
    # Try VERSION file first (single source of truth)
    project_root = _find_project_root()
    if project_root:
        version_file = project_root / "VERSION"
        if version_file.exists():
            return version_file.read_text().strip()

    # Fallback to package metadata
    try:
        from importlib.metadata import PackageNotFoundError, version

        return version("pyvider")
    except PackageNotFoundError:
        pass

    # Final fallback
    return "0.0.0-dev"


__version__ = get_version()
