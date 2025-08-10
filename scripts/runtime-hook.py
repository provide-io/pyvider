from pathlib import Path
import sys


def _append_path():
    """Append necessary paths."""
    # Get the base path of the frozen application
    base_path = Path(sys._MEIPASS if hasattr(sys, '_MEIPASS') else Path(sys.executable).parent)

    # Add Python's lib-dynload
    lib_dynload = base_path / 'lib-dynload'
    if lib_dynload.exists():
        sys.path.insert(0, str(lib_dynload))

    # Add site-packages
    site_packages = base_path / 'site-packages'
    if site_packages.exists():
        sys.path.insert(0, str(site_packages))

_append_path()

