#
# _version.py
#
"""
Version handling for pyvider.
Uses VERSION file with robust fallback mechanisms.
"""

from pathlib import Path
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


def x__find_project_root__mutmut_orig() -> Path | None:
    """Find the project root directory by looking for VERSION file."""
    current = Path(__file__).parent

    # Walk up the directory tree looking for VERSION file
    while current != current.parent:  # Stop at filesystem root
        version_file = current / "VERSION"
        if version_file.exists():
            return current
        current = current.parent

    return None


def x__find_project_root__mutmut_1() -> Path | None:
    """Find the project root directory by looking for VERSION file."""
    current = None

    # Walk up the directory tree looking for VERSION file
    while current != current.parent:  # Stop at filesystem root
        version_file = current / "VERSION"
        if version_file.exists():
            return current
        current = current.parent

    return None


def x__find_project_root__mutmut_2() -> Path | None:
    """Find the project root directory by looking for VERSION file."""
    current = Path(None).parent

    # Walk up the directory tree looking for VERSION file
    while current != current.parent:  # Stop at filesystem root
        version_file = current / "VERSION"
        if version_file.exists():
            return current
        current = current.parent

    return None


def x__find_project_root__mutmut_3() -> Path | None:
    """Find the project root directory by looking for VERSION file."""
    current = Path(__file__).parent

    # Walk up the directory tree looking for VERSION file
    while current == current.parent:  # Stop at filesystem root
        version_file = current / "VERSION"
        if version_file.exists():
            return current
        current = current.parent

    return None


def x__find_project_root__mutmut_4() -> Path | None:
    """Find the project root directory by looking for VERSION file."""
    current = Path(__file__).parent

    # Walk up the directory tree looking for VERSION file
    while current != current.parent:  # Stop at filesystem root
        version_file = None
        if version_file.exists():
            return current
        current = current.parent

    return None


def x__find_project_root__mutmut_5() -> Path | None:
    """Find the project root directory by looking for VERSION file."""
    current = Path(__file__).parent

    # Walk up the directory tree looking for VERSION file
    while current != current.parent:  # Stop at filesystem root
        version_file = current * "VERSION"
        if version_file.exists():
            return current
        current = current.parent

    return None


def x__find_project_root__mutmut_6() -> Path | None:
    """Find the project root directory by looking for VERSION file."""
    current = Path(__file__).parent

    # Walk up the directory tree looking for VERSION file
    while current != current.parent:  # Stop at filesystem root
        version_file = current / "XXVERSIONXX"
        if version_file.exists():
            return current
        current = current.parent

    return None


def x__find_project_root__mutmut_7() -> Path | None:
    """Find the project root directory by looking for VERSION file."""
    current = Path(__file__).parent

    # Walk up the directory tree looking for VERSION file
    while current != current.parent:  # Stop at filesystem root
        version_file = current / "version"
        if version_file.exists():
            return current
        current = current.parent

    return None


def x__find_project_root__mutmut_8() -> Path | None:
    """Find the project root directory by looking for VERSION file."""
    current = Path(__file__).parent

    # Walk up the directory tree looking for VERSION file
    while current != current.parent:  # Stop at filesystem root
        version_file = current / "VERSION"
        if version_file.exists():
            return current
        current = None

    return None

x__find_project_root__mutmut_mutants : ClassVar[MutantDict] = {
'x__find_project_root__mutmut_1': x__find_project_root__mutmut_1, 
    'x__find_project_root__mutmut_2': x__find_project_root__mutmut_2, 
    'x__find_project_root__mutmut_3': x__find_project_root__mutmut_3, 
    'x__find_project_root__mutmut_4': x__find_project_root__mutmut_4, 
    'x__find_project_root__mutmut_5': x__find_project_root__mutmut_5, 
    'x__find_project_root__mutmut_6': x__find_project_root__mutmut_6, 
    'x__find_project_root__mutmut_7': x__find_project_root__mutmut_7, 
    'x__find_project_root__mutmut_8': x__find_project_root__mutmut_8
}

def _find_project_root(*args, **kwargs):
    result = _mutmut_trampoline(x__find_project_root__mutmut_orig, x__find_project_root__mutmut_mutants, args, kwargs)
    return result 

_find_project_root.__signature__ = _mutmut_signature(x__find_project_root__mutmut_orig)
x__find_project_root__mutmut_orig.__name__ = 'x__find_project_root'


def x_get_version__mutmut_orig() -> str:
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


def x_get_version__mutmut_1() -> str:
    """Get the current pyvider version.

    Reads from VERSION file if it exists, otherwise falls back to package metadata,
    then to default development version.

    Returns:
        str: The current version string
    """
    # Try VERSION file first (single source of truth)
    project_root = None
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


def x_get_version__mutmut_2() -> str:
    """Get the current pyvider version.

    Reads from VERSION file if it exists, otherwise falls back to package metadata,
    then to default development version.

    Returns:
        str: The current version string
    """
    # Try VERSION file first (single source of truth)
    project_root = _find_project_root()
    if project_root:
        version_file = None
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


def x_get_version__mutmut_3() -> str:
    """Get the current pyvider version.

    Reads from VERSION file if it exists, otherwise falls back to package metadata,
    then to default development version.

    Returns:
        str: The current version string
    """
    # Try VERSION file first (single source of truth)
    project_root = _find_project_root()
    if project_root:
        version_file = project_root * "VERSION"
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


def x_get_version__mutmut_4() -> str:
    """Get the current pyvider version.

    Reads from VERSION file if it exists, otherwise falls back to package metadata,
    then to default development version.

    Returns:
        str: The current version string
    """
    # Try VERSION file first (single source of truth)
    project_root = _find_project_root()
    if project_root:
        version_file = project_root / "XXVERSIONXX"
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


def x_get_version__mutmut_5() -> str:
    """Get the current pyvider version.

    Reads from VERSION file if it exists, otherwise falls back to package metadata,
    then to default development version.

    Returns:
        str: The current version string
    """
    # Try VERSION file first (single source of truth)
    project_root = _find_project_root()
    if project_root:
        version_file = project_root / "version"
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


def x_get_version__mutmut_6() -> str:
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

        return version(None)
    except PackageNotFoundError:
        pass

    # Final fallback
    return "0.0.0-dev"


def x_get_version__mutmut_7() -> str:
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

        return version("XXpyviderXX")
    except PackageNotFoundError:
        pass

    # Final fallback
    return "0.0.0-dev"


def x_get_version__mutmut_8() -> str:
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

        return version("PYVIDER")
    except PackageNotFoundError:
        pass

    # Final fallback
    return "0.0.0-dev"


def x_get_version__mutmut_9() -> str:
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
    return "XX0.0.0-devXX"


def x_get_version__mutmut_10() -> str:
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
    return "0.0.0-DEV"

x_get_version__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_version__mutmut_1': x_get_version__mutmut_1, 
    'x_get_version__mutmut_2': x_get_version__mutmut_2, 
    'x_get_version__mutmut_3': x_get_version__mutmut_3, 
    'x_get_version__mutmut_4': x_get_version__mutmut_4, 
    'x_get_version__mutmut_5': x_get_version__mutmut_5, 
    'x_get_version__mutmut_6': x_get_version__mutmut_6, 
    'x_get_version__mutmut_7': x_get_version__mutmut_7, 
    'x_get_version__mutmut_8': x_get_version__mutmut_8, 
    'x_get_version__mutmut_9': x_get_version__mutmut_9, 
    'x_get_version__mutmut_10': x_get_version__mutmut_10
}

def get_version(*args, **kwargs):
    result = _mutmut_trampoline(x_get_version__mutmut_orig, x_get_version__mutmut_mutants, args, kwargs)
    return result 

get_version.__signature__ = _mutmut_signature(x_get_version__mutmut_orig)
x_get_version__mutmut_orig.__name__ = 'x_get_version'


__version__ = get_version()
