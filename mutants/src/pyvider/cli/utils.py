"""Internal utilities for the Pyvider CLI tool."""

import datetime
from pathlib import Path

from provide.foundation.console import pout
from provide.foundation.file import atomic_write_text, ensure_dir
from provide.foundation.process import run
from provide.foundation.utils import timed_block

from pyvider.cli.context import PyviderContext
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


def x__find_actual_venv__mutmut_orig(base_dir: Path) -> Path | None:
    """
    Find the actual virtual environment directory that exists.

    Searches for common venv locations in order of preference:
    1. .venv (standard)
    2. venv (alternative)
    3. .venv_* (platform-specific)
    4. workenv/*/ (wrkenv style)

    Args:
        base_dir: Directory to search in

    Returns:
        Path to venv directory if found, None otherwise
    """
    candidates = [
        base_dir / ".venv",
        base_dir / "venv",
    ]

    # Add platform-specific venvs
    candidates.extend(sorted(base_dir.glob(".venv_*")))

    # Add workenv style venvs
    candidates.extend(sorted(base_dir.glob("workenv/*/")))

    for venv_dir in candidates:
        activate_script = venv_dir / "bin" / "activate"
        if activate_script.exists():
            return venv_dir

    return None


def x__find_actual_venv__mutmut_1(base_dir: Path) -> Path | None:
    """
    Find the actual virtual environment directory that exists.

    Searches for common venv locations in order of preference:
    1. .venv (standard)
    2. venv (alternative)
    3. .venv_* (platform-specific)
    4. workenv/*/ (wrkenv style)

    Args:
        base_dir: Directory to search in

    Returns:
        Path to venv directory if found, None otherwise
    """
    candidates = None

    # Add platform-specific venvs
    candidates.extend(sorted(base_dir.glob(".venv_*")))

    # Add workenv style venvs
    candidates.extend(sorted(base_dir.glob("workenv/*/")))

    for venv_dir in candidates:
        activate_script = venv_dir / "bin" / "activate"
        if activate_script.exists():
            return venv_dir

    return None


def x__find_actual_venv__mutmut_2(base_dir: Path) -> Path | None:
    """
    Find the actual virtual environment directory that exists.

    Searches for common venv locations in order of preference:
    1. .venv (standard)
    2. venv (alternative)
    3. .venv_* (platform-specific)
    4. workenv/*/ (wrkenv style)

    Args:
        base_dir: Directory to search in

    Returns:
        Path to venv directory if found, None otherwise
    """
    candidates = [
        base_dir * ".venv",
        base_dir / "venv",
    ]

    # Add platform-specific venvs
    candidates.extend(sorted(base_dir.glob(".venv_*")))

    # Add workenv style venvs
    candidates.extend(sorted(base_dir.glob("workenv/*/")))

    for venv_dir in candidates:
        activate_script = venv_dir / "bin" / "activate"
        if activate_script.exists():
            return venv_dir

    return None


def x__find_actual_venv__mutmut_3(base_dir: Path) -> Path | None:
    """
    Find the actual virtual environment directory that exists.

    Searches for common venv locations in order of preference:
    1. .venv (standard)
    2. venv (alternative)
    3. .venv_* (platform-specific)
    4. workenv/*/ (wrkenv style)

    Args:
        base_dir: Directory to search in

    Returns:
        Path to venv directory if found, None otherwise
    """
    candidates = [
        base_dir / "XX.venvXX",
        base_dir / "venv",
    ]

    # Add platform-specific venvs
    candidates.extend(sorted(base_dir.glob(".venv_*")))

    # Add workenv style venvs
    candidates.extend(sorted(base_dir.glob("workenv/*/")))

    for venv_dir in candidates:
        activate_script = venv_dir / "bin" / "activate"
        if activate_script.exists():
            return venv_dir

    return None


def x__find_actual_venv__mutmut_4(base_dir: Path) -> Path | None:
    """
    Find the actual virtual environment directory that exists.

    Searches for common venv locations in order of preference:
    1. .venv (standard)
    2. venv (alternative)
    3. .venv_* (platform-specific)
    4. workenv/*/ (wrkenv style)

    Args:
        base_dir: Directory to search in

    Returns:
        Path to venv directory if found, None otherwise
    """
    candidates = [
        base_dir / ".VENV",
        base_dir / "venv",
    ]

    # Add platform-specific venvs
    candidates.extend(sorted(base_dir.glob(".venv_*")))

    # Add workenv style venvs
    candidates.extend(sorted(base_dir.glob("workenv/*/")))

    for venv_dir in candidates:
        activate_script = venv_dir / "bin" / "activate"
        if activate_script.exists():
            return venv_dir

    return None


def x__find_actual_venv__mutmut_5(base_dir: Path) -> Path | None:
    """
    Find the actual virtual environment directory that exists.

    Searches for common venv locations in order of preference:
    1. .venv (standard)
    2. venv (alternative)
    3. .venv_* (platform-specific)
    4. workenv/*/ (wrkenv style)

    Args:
        base_dir: Directory to search in

    Returns:
        Path to venv directory if found, None otherwise
    """
    candidates = [
        base_dir / ".venv",
        base_dir * "venv",
    ]

    # Add platform-specific venvs
    candidates.extend(sorted(base_dir.glob(".venv_*")))

    # Add workenv style venvs
    candidates.extend(sorted(base_dir.glob("workenv/*/")))

    for venv_dir in candidates:
        activate_script = venv_dir / "bin" / "activate"
        if activate_script.exists():
            return venv_dir

    return None


def x__find_actual_venv__mutmut_6(base_dir: Path) -> Path | None:
    """
    Find the actual virtual environment directory that exists.

    Searches for common venv locations in order of preference:
    1. .venv (standard)
    2. venv (alternative)
    3. .venv_* (platform-specific)
    4. workenv/*/ (wrkenv style)

    Args:
        base_dir: Directory to search in

    Returns:
        Path to venv directory if found, None otherwise
    """
    candidates = [
        base_dir / ".venv",
        base_dir / "XXvenvXX",
    ]

    # Add platform-specific venvs
    candidates.extend(sorted(base_dir.glob(".venv_*")))

    # Add workenv style venvs
    candidates.extend(sorted(base_dir.glob("workenv/*/")))

    for venv_dir in candidates:
        activate_script = venv_dir / "bin" / "activate"
        if activate_script.exists():
            return venv_dir

    return None


def x__find_actual_venv__mutmut_7(base_dir: Path) -> Path | None:
    """
    Find the actual virtual environment directory that exists.

    Searches for common venv locations in order of preference:
    1. .venv (standard)
    2. venv (alternative)
    3. .venv_* (platform-specific)
    4. workenv/*/ (wrkenv style)

    Args:
        base_dir: Directory to search in

    Returns:
        Path to venv directory if found, None otherwise
    """
    candidates = [
        base_dir / ".venv",
        base_dir / "VENV",
    ]

    # Add platform-specific venvs
    candidates.extend(sorted(base_dir.glob(".venv_*")))

    # Add workenv style venvs
    candidates.extend(sorted(base_dir.glob("workenv/*/")))

    for venv_dir in candidates:
        activate_script = venv_dir / "bin" / "activate"
        if activate_script.exists():
            return venv_dir

    return None


def x__find_actual_venv__mutmut_8(base_dir: Path) -> Path | None:
    """
    Find the actual virtual environment directory that exists.

    Searches for common venv locations in order of preference:
    1. .venv (standard)
    2. venv (alternative)
    3. .venv_* (platform-specific)
    4. workenv/*/ (wrkenv style)

    Args:
        base_dir: Directory to search in

    Returns:
        Path to venv directory if found, None otherwise
    """
    candidates = [
        base_dir / ".venv",
        base_dir / "venv",
    ]

    # Add platform-specific venvs
    candidates.extend(None)

    # Add workenv style venvs
    candidates.extend(sorted(base_dir.glob("workenv/*/")))

    for venv_dir in candidates:
        activate_script = venv_dir / "bin" / "activate"
        if activate_script.exists():
            return venv_dir

    return None


def x__find_actual_venv__mutmut_9(base_dir: Path) -> Path | None:
    """
    Find the actual virtual environment directory that exists.

    Searches for common venv locations in order of preference:
    1. .venv (standard)
    2. venv (alternative)
    3. .venv_* (platform-specific)
    4. workenv/*/ (wrkenv style)

    Args:
        base_dir: Directory to search in

    Returns:
        Path to venv directory if found, None otherwise
    """
    candidates = [
        base_dir / ".venv",
        base_dir / "venv",
    ]

    # Add platform-specific venvs
    candidates.extend(sorted(None))

    # Add workenv style venvs
    candidates.extend(sorted(base_dir.glob("workenv/*/")))

    for venv_dir in candidates:
        activate_script = venv_dir / "bin" / "activate"
        if activate_script.exists():
            return venv_dir

    return None


def x__find_actual_venv__mutmut_10(base_dir: Path) -> Path | None:
    """
    Find the actual virtual environment directory that exists.

    Searches for common venv locations in order of preference:
    1. .venv (standard)
    2. venv (alternative)
    3. .venv_* (platform-specific)
    4. workenv/*/ (wrkenv style)

    Args:
        base_dir: Directory to search in

    Returns:
        Path to venv directory if found, None otherwise
    """
    candidates = [
        base_dir / ".venv",
        base_dir / "venv",
    ]

    # Add platform-specific venvs
    candidates.extend(sorted(base_dir.glob(None)))

    # Add workenv style venvs
    candidates.extend(sorted(base_dir.glob("workenv/*/")))

    for venv_dir in candidates:
        activate_script = venv_dir / "bin" / "activate"
        if activate_script.exists():
            return venv_dir

    return None


def x__find_actual_venv__mutmut_11(base_dir: Path) -> Path | None:
    """
    Find the actual virtual environment directory that exists.

    Searches for common venv locations in order of preference:
    1. .venv (standard)
    2. venv (alternative)
    3. .venv_* (platform-specific)
    4. workenv/*/ (wrkenv style)

    Args:
        base_dir: Directory to search in

    Returns:
        Path to venv directory if found, None otherwise
    """
    candidates = [
        base_dir / ".venv",
        base_dir / "venv",
    ]

    # Add platform-specific venvs
    candidates.extend(sorted(base_dir.glob("XX.venv_*XX")))

    # Add workenv style venvs
    candidates.extend(sorted(base_dir.glob("workenv/*/")))

    for venv_dir in candidates:
        activate_script = venv_dir / "bin" / "activate"
        if activate_script.exists():
            return venv_dir

    return None


def x__find_actual_venv__mutmut_12(base_dir: Path) -> Path | None:
    """
    Find the actual virtual environment directory that exists.

    Searches for common venv locations in order of preference:
    1. .venv (standard)
    2. venv (alternative)
    3. .venv_* (platform-specific)
    4. workenv/*/ (wrkenv style)

    Args:
        base_dir: Directory to search in

    Returns:
        Path to venv directory if found, None otherwise
    """
    candidates = [
        base_dir / ".venv",
        base_dir / "venv",
    ]

    # Add platform-specific venvs
    candidates.extend(sorted(base_dir.glob(".VENV_*")))

    # Add workenv style venvs
    candidates.extend(sorted(base_dir.glob("workenv/*/")))

    for venv_dir in candidates:
        activate_script = venv_dir / "bin" / "activate"
        if activate_script.exists():
            return venv_dir

    return None


def x__find_actual_venv__mutmut_13(base_dir: Path) -> Path | None:
    """
    Find the actual virtual environment directory that exists.

    Searches for common venv locations in order of preference:
    1. .venv (standard)
    2. venv (alternative)
    3. .venv_* (platform-specific)
    4. workenv/*/ (wrkenv style)

    Args:
        base_dir: Directory to search in

    Returns:
        Path to venv directory if found, None otherwise
    """
    candidates = [
        base_dir / ".venv",
        base_dir / "venv",
    ]

    # Add platform-specific venvs
    candidates.extend(sorted(base_dir.glob(".venv_*")))

    # Add workenv style venvs
    candidates.extend(None)

    for venv_dir in candidates:
        activate_script = venv_dir / "bin" / "activate"
        if activate_script.exists():
            return venv_dir

    return None


def x__find_actual_venv__mutmut_14(base_dir: Path) -> Path | None:
    """
    Find the actual virtual environment directory that exists.

    Searches for common venv locations in order of preference:
    1. .venv (standard)
    2. venv (alternative)
    3. .venv_* (platform-specific)
    4. workenv/*/ (wrkenv style)

    Args:
        base_dir: Directory to search in

    Returns:
        Path to venv directory if found, None otherwise
    """
    candidates = [
        base_dir / ".venv",
        base_dir / "venv",
    ]

    # Add platform-specific venvs
    candidates.extend(sorted(base_dir.glob(".venv_*")))

    # Add workenv style venvs
    candidates.extend(sorted(None))

    for venv_dir in candidates:
        activate_script = venv_dir / "bin" / "activate"
        if activate_script.exists():
            return venv_dir

    return None


def x__find_actual_venv__mutmut_15(base_dir: Path) -> Path | None:
    """
    Find the actual virtual environment directory that exists.

    Searches for common venv locations in order of preference:
    1. .venv (standard)
    2. venv (alternative)
    3. .venv_* (platform-specific)
    4. workenv/*/ (wrkenv style)

    Args:
        base_dir: Directory to search in

    Returns:
        Path to venv directory if found, None otherwise
    """
    candidates = [
        base_dir / ".venv",
        base_dir / "venv",
    ]

    # Add platform-specific venvs
    candidates.extend(sorted(base_dir.glob(".venv_*")))

    # Add workenv style venvs
    candidates.extend(sorted(base_dir.glob(None)))

    for venv_dir in candidates:
        activate_script = venv_dir / "bin" / "activate"
        if activate_script.exists():
            return venv_dir

    return None


def x__find_actual_venv__mutmut_16(base_dir: Path) -> Path | None:
    """
    Find the actual virtual environment directory that exists.

    Searches for common venv locations in order of preference:
    1. .venv (standard)
    2. venv (alternative)
    3. .venv_* (platform-specific)
    4. workenv/*/ (wrkenv style)

    Args:
        base_dir: Directory to search in

    Returns:
        Path to venv directory if found, None otherwise
    """
    candidates = [
        base_dir / ".venv",
        base_dir / "venv",
    ]

    # Add platform-specific venvs
    candidates.extend(sorted(base_dir.glob(".venv_*")))

    # Add workenv style venvs
    candidates.extend(sorted(base_dir.glob("XXworkenv/*/XX")))

    for venv_dir in candidates:
        activate_script = venv_dir / "bin" / "activate"
        if activate_script.exists():
            return venv_dir

    return None


def x__find_actual_venv__mutmut_17(base_dir: Path) -> Path | None:
    """
    Find the actual virtual environment directory that exists.

    Searches for common venv locations in order of preference:
    1. .venv (standard)
    2. venv (alternative)
    3. .venv_* (platform-specific)
    4. workenv/*/ (wrkenv style)

    Args:
        base_dir: Directory to search in

    Returns:
        Path to venv directory if found, None otherwise
    """
    candidates = [
        base_dir / ".venv",
        base_dir / "venv",
    ]

    # Add platform-specific venvs
    candidates.extend(sorted(base_dir.glob(".venv_*")))

    # Add workenv style venvs
    candidates.extend(sorted(base_dir.glob("WORKENV/*/")))

    for venv_dir in candidates:
        activate_script = venv_dir / "bin" / "activate"
        if activate_script.exists():
            return venv_dir

    return None


def x__find_actual_venv__mutmut_18(base_dir: Path) -> Path | None:
    """
    Find the actual virtual environment directory that exists.

    Searches for common venv locations in order of preference:
    1. .venv (standard)
    2. venv (alternative)
    3. .venv_* (platform-specific)
    4. workenv/*/ (wrkenv style)

    Args:
        base_dir: Directory to search in

    Returns:
        Path to venv directory if found, None otherwise
    """
    candidates = [
        base_dir / ".venv",
        base_dir / "venv",
    ]

    # Add platform-specific venvs
    candidates.extend(sorted(base_dir.glob(".venv_*")))

    # Add workenv style venvs
    candidates.extend(sorted(base_dir.glob("workenv/*/")))

    for venv_dir in candidates:
        activate_script = None
        if activate_script.exists():
            return venv_dir

    return None


def x__find_actual_venv__mutmut_19(base_dir: Path) -> Path | None:
    """
    Find the actual virtual environment directory that exists.

    Searches for common venv locations in order of preference:
    1. .venv (standard)
    2. venv (alternative)
    3. .venv_* (platform-specific)
    4. workenv/*/ (wrkenv style)

    Args:
        base_dir: Directory to search in

    Returns:
        Path to venv directory if found, None otherwise
    """
    candidates = [
        base_dir / ".venv",
        base_dir / "venv",
    ]

    # Add platform-specific venvs
    candidates.extend(sorted(base_dir.glob(".venv_*")))

    # Add workenv style venvs
    candidates.extend(sorted(base_dir.glob("workenv/*/")))

    for venv_dir in candidates:
        activate_script = venv_dir / "bin" * "activate"
        if activate_script.exists():
            return venv_dir

    return None


def x__find_actual_venv__mutmut_20(base_dir: Path) -> Path | None:
    """
    Find the actual virtual environment directory that exists.

    Searches for common venv locations in order of preference:
    1. .venv (standard)
    2. venv (alternative)
    3. .venv_* (platform-specific)
    4. workenv/*/ (wrkenv style)

    Args:
        base_dir: Directory to search in

    Returns:
        Path to venv directory if found, None otherwise
    """
    candidates = [
        base_dir / ".venv",
        base_dir / "venv",
    ]

    # Add platform-specific venvs
    candidates.extend(sorted(base_dir.glob(".venv_*")))

    # Add workenv style venvs
    candidates.extend(sorted(base_dir.glob("workenv/*/")))

    for venv_dir in candidates:
        activate_script = venv_dir * "bin" / "activate"
        if activate_script.exists():
            return venv_dir

    return None


def x__find_actual_venv__mutmut_21(base_dir: Path) -> Path | None:
    """
    Find the actual virtual environment directory that exists.

    Searches for common venv locations in order of preference:
    1. .venv (standard)
    2. venv (alternative)
    3. .venv_* (platform-specific)
    4. workenv/*/ (wrkenv style)

    Args:
        base_dir: Directory to search in

    Returns:
        Path to venv directory if found, None otherwise
    """
    candidates = [
        base_dir / ".venv",
        base_dir / "venv",
    ]

    # Add platform-specific venvs
    candidates.extend(sorted(base_dir.glob(".venv_*")))

    # Add workenv style venvs
    candidates.extend(sorted(base_dir.glob("workenv/*/")))

    for venv_dir in candidates:
        activate_script = venv_dir / "XXbinXX" / "activate"
        if activate_script.exists():
            return venv_dir

    return None


def x__find_actual_venv__mutmut_22(base_dir: Path) -> Path | None:
    """
    Find the actual virtual environment directory that exists.

    Searches for common venv locations in order of preference:
    1. .venv (standard)
    2. venv (alternative)
    3. .venv_* (platform-specific)
    4. workenv/*/ (wrkenv style)

    Args:
        base_dir: Directory to search in

    Returns:
        Path to venv directory if found, None otherwise
    """
    candidates = [
        base_dir / ".venv",
        base_dir / "venv",
    ]

    # Add platform-specific venvs
    candidates.extend(sorted(base_dir.glob(".venv_*")))

    # Add workenv style venvs
    candidates.extend(sorted(base_dir.glob("workenv/*/")))

    for venv_dir in candidates:
        activate_script = venv_dir / "BIN" / "activate"
        if activate_script.exists():
            return venv_dir

    return None


def x__find_actual_venv__mutmut_23(base_dir: Path) -> Path | None:
    """
    Find the actual virtual environment directory that exists.

    Searches for common venv locations in order of preference:
    1. .venv (standard)
    2. venv (alternative)
    3. .venv_* (platform-specific)
    4. workenv/*/ (wrkenv style)

    Args:
        base_dir: Directory to search in

    Returns:
        Path to venv directory if found, None otherwise
    """
    candidates = [
        base_dir / ".venv",
        base_dir / "venv",
    ]

    # Add platform-specific venvs
    candidates.extend(sorted(base_dir.glob(".venv_*")))

    # Add workenv style venvs
    candidates.extend(sorted(base_dir.glob("workenv/*/")))

    for venv_dir in candidates:
        activate_script = venv_dir / "bin" / "XXactivateXX"
        if activate_script.exists():
            return venv_dir

    return None


def x__find_actual_venv__mutmut_24(base_dir: Path) -> Path | None:
    """
    Find the actual virtual environment directory that exists.

    Searches for common venv locations in order of preference:
    1. .venv (standard)
    2. venv (alternative)
    3. .venv_* (platform-specific)
    4. workenv/*/ (wrkenv style)

    Args:
        base_dir: Directory to search in

    Returns:
        Path to venv directory if found, None otherwise
    """
    candidates = [
        base_dir / ".venv",
        base_dir / "venv",
    ]

    # Add platform-specific venvs
    candidates.extend(sorted(base_dir.glob(".venv_*")))

    # Add workenv style venvs
    candidates.extend(sorted(base_dir.glob("workenv/*/")))

    for venv_dir in candidates:
        activate_script = venv_dir / "bin" / "ACTIVATE"
        if activate_script.exists():
            return venv_dir

    return None

x__find_actual_venv__mutmut_mutants : ClassVar[MutantDict] = {
'x__find_actual_venv__mutmut_1': x__find_actual_venv__mutmut_1, 
    'x__find_actual_venv__mutmut_2': x__find_actual_venv__mutmut_2, 
    'x__find_actual_venv__mutmut_3': x__find_actual_venv__mutmut_3, 
    'x__find_actual_venv__mutmut_4': x__find_actual_venv__mutmut_4, 
    'x__find_actual_venv__mutmut_5': x__find_actual_venv__mutmut_5, 
    'x__find_actual_venv__mutmut_6': x__find_actual_venv__mutmut_6, 
    'x__find_actual_venv__mutmut_7': x__find_actual_venv__mutmut_7, 
    'x__find_actual_venv__mutmut_8': x__find_actual_venv__mutmut_8, 
    'x__find_actual_venv__mutmut_9': x__find_actual_venv__mutmut_9, 
    'x__find_actual_venv__mutmut_10': x__find_actual_venv__mutmut_10, 
    'x__find_actual_venv__mutmut_11': x__find_actual_venv__mutmut_11, 
    'x__find_actual_venv__mutmut_12': x__find_actual_venv__mutmut_12, 
    'x__find_actual_venv__mutmut_13': x__find_actual_venv__mutmut_13, 
    'x__find_actual_venv__mutmut_14': x__find_actual_venv__mutmut_14, 
    'x__find_actual_venv__mutmut_15': x__find_actual_venv__mutmut_15, 
    'x__find_actual_venv__mutmut_16': x__find_actual_venv__mutmut_16, 
    'x__find_actual_venv__mutmut_17': x__find_actual_venv__mutmut_17, 
    'x__find_actual_venv__mutmut_18': x__find_actual_venv__mutmut_18, 
    'x__find_actual_venv__mutmut_19': x__find_actual_venv__mutmut_19, 
    'x__find_actual_venv__mutmut_20': x__find_actual_venv__mutmut_20, 
    'x__find_actual_venv__mutmut_21': x__find_actual_venv__mutmut_21, 
    'x__find_actual_venv__mutmut_22': x__find_actual_venv__mutmut_22, 
    'x__find_actual_venv__mutmut_23': x__find_actual_venv__mutmut_23, 
    'x__find_actual_venv__mutmut_24': x__find_actual_venv__mutmut_24
}

def _find_actual_venv(*args, **kwargs):
    result = _mutmut_trampoline(x__find_actual_venv__mutmut_orig, x__find_actual_venv__mutmut_mutants, args, kwargs)
    return result 

_find_actual_venv.__signature__ = _mutmut_signature(x__find_actual_venv__mutmut_orig)
x__find_actual_venv__mutmut_orig.__name__ = 'x__find_actual_venv'


def x__run_command__mutmut_orig(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_1(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = False,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_2(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "XXXX",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_3(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = None
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_4(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(None)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_5(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = "XX XX".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_6(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = None

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_7(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd and Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_8(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = None
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_9(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" * "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_10(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() * ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_11(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / "XX.pyviderXX" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_12(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".PYVIDER" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_13(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "XXlogsXX"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_14(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "LOGS"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_15(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(None)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_16(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = None

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_17(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir * "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_18(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "XXprep.logXX"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_19(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "PREP.LOG"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_20(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = None
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_21(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = None
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_22(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = None
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_23(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = None

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_24(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = None
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_25(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title and cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_26(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(None, style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_27(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style=None, end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_28(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end=None)

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_29(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_30(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_31(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", )

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_32(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="XXcyanXX", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_33(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="CYAN", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_34(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="XXXX")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_35(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = None
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_36(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                None,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_37(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=None,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_38(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=None,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_39(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=None,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_40(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_41(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_42(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_43(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_44(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=True,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_45(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = None
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_46(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = None

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_47(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = None

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_48(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = None
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_49(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = "XXXX"
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_50(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = None

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_51(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding=None)

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_52(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="XXutf-8XX")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_53(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="UTF-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_54(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(None, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_55(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, None)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_56(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_57(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, )

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_58(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content - log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_59(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check or return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_60(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code == 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_61(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 1:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_62(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(None, style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_63(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style=None)
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_64(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_65(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", )
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_66(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout("XX ❌ FAILEDXX", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_67(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ failed", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_68(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="XXredXX")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_69(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="RED")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_70(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = None
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_71(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(None, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_72(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style=None)
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_73(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_74(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, )
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_75(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="XXredXX")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_76(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="RED")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_77(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                None,
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_78(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=None,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_79(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=None,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_80(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=None,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_81(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=None,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_82(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_83(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_84(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_85(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_86(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_87(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(None, style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_88(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style=None)
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_89(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_90(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", )
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_91(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="XXgreenXX")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_92(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="GREEN")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_93(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(None, style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_94(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style=None)
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_95(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_96(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", )
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_97(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout("XX ❌ ERRORXX", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_98(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ error", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_99(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="XXredXX")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_100(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="RED")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_101(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = None
        pout(error_message, style="red")
        raise


def x__run_command__mutmut_102(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(None, style="red")
        raise


def x__run_command__mutmut_103(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style=None)
        raise


def x__run_command__mutmut_104(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(style="red")
        raise


def x__run_command__mutmut_105(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, )
        raise


def x__run_command__mutmut_106(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="XXredXX")
        raise


def x__run_command__mutmut_107(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="RED")
        raise

x__run_command__mutmut_mutants : ClassVar[MutantDict] = {
'x__run_command__mutmut_1': x__run_command__mutmut_1, 
    'x__run_command__mutmut_2': x__run_command__mutmut_2, 
    'x__run_command__mutmut_3': x__run_command__mutmut_3, 
    'x__run_command__mutmut_4': x__run_command__mutmut_4, 
    'x__run_command__mutmut_5': x__run_command__mutmut_5, 
    'x__run_command__mutmut_6': x__run_command__mutmut_6, 
    'x__run_command__mutmut_7': x__run_command__mutmut_7, 
    'x__run_command__mutmut_8': x__run_command__mutmut_8, 
    'x__run_command__mutmut_9': x__run_command__mutmut_9, 
    'x__run_command__mutmut_10': x__run_command__mutmut_10, 
    'x__run_command__mutmut_11': x__run_command__mutmut_11, 
    'x__run_command__mutmut_12': x__run_command__mutmut_12, 
    'x__run_command__mutmut_13': x__run_command__mutmut_13, 
    'x__run_command__mutmut_14': x__run_command__mutmut_14, 
    'x__run_command__mutmut_15': x__run_command__mutmut_15, 
    'x__run_command__mutmut_16': x__run_command__mutmut_16, 
    'x__run_command__mutmut_17': x__run_command__mutmut_17, 
    'x__run_command__mutmut_18': x__run_command__mutmut_18, 
    'x__run_command__mutmut_19': x__run_command__mutmut_19, 
    'x__run_command__mutmut_20': x__run_command__mutmut_20, 
    'x__run_command__mutmut_21': x__run_command__mutmut_21, 
    'x__run_command__mutmut_22': x__run_command__mutmut_22, 
    'x__run_command__mutmut_23': x__run_command__mutmut_23, 
    'x__run_command__mutmut_24': x__run_command__mutmut_24, 
    'x__run_command__mutmut_25': x__run_command__mutmut_25, 
    'x__run_command__mutmut_26': x__run_command__mutmut_26, 
    'x__run_command__mutmut_27': x__run_command__mutmut_27, 
    'x__run_command__mutmut_28': x__run_command__mutmut_28, 
    'x__run_command__mutmut_29': x__run_command__mutmut_29, 
    'x__run_command__mutmut_30': x__run_command__mutmut_30, 
    'x__run_command__mutmut_31': x__run_command__mutmut_31, 
    'x__run_command__mutmut_32': x__run_command__mutmut_32, 
    'x__run_command__mutmut_33': x__run_command__mutmut_33, 
    'x__run_command__mutmut_34': x__run_command__mutmut_34, 
    'x__run_command__mutmut_35': x__run_command__mutmut_35, 
    'x__run_command__mutmut_36': x__run_command__mutmut_36, 
    'x__run_command__mutmut_37': x__run_command__mutmut_37, 
    'x__run_command__mutmut_38': x__run_command__mutmut_38, 
    'x__run_command__mutmut_39': x__run_command__mutmut_39, 
    'x__run_command__mutmut_40': x__run_command__mutmut_40, 
    'x__run_command__mutmut_41': x__run_command__mutmut_41, 
    'x__run_command__mutmut_42': x__run_command__mutmut_42, 
    'x__run_command__mutmut_43': x__run_command__mutmut_43, 
    'x__run_command__mutmut_44': x__run_command__mutmut_44, 
    'x__run_command__mutmut_45': x__run_command__mutmut_45, 
    'x__run_command__mutmut_46': x__run_command__mutmut_46, 
    'x__run_command__mutmut_47': x__run_command__mutmut_47, 
    'x__run_command__mutmut_48': x__run_command__mutmut_48, 
    'x__run_command__mutmut_49': x__run_command__mutmut_49, 
    'x__run_command__mutmut_50': x__run_command__mutmut_50, 
    'x__run_command__mutmut_51': x__run_command__mutmut_51, 
    'x__run_command__mutmut_52': x__run_command__mutmut_52, 
    'x__run_command__mutmut_53': x__run_command__mutmut_53, 
    'x__run_command__mutmut_54': x__run_command__mutmut_54, 
    'x__run_command__mutmut_55': x__run_command__mutmut_55, 
    'x__run_command__mutmut_56': x__run_command__mutmut_56, 
    'x__run_command__mutmut_57': x__run_command__mutmut_57, 
    'x__run_command__mutmut_58': x__run_command__mutmut_58, 
    'x__run_command__mutmut_59': x__run_command__mutmut_59, 
    'x__run_command__mutmut_60': x__run_command__mutmut_60, 
    'x__run_command__mutmut_61': x__run_command__mutmut_61, 
    'x__run_command__mutmut_62': x__run_command__mutmut_62, 
    'x__run_command__mutmut_63': x__run_command__mutmut_63, 
    'x__run_command__mutmut_64': x__run_command__mutmut_64, 
    'x__run_command__mutmut_65': x__run_command__mutmut_65, 
    'x__run_command__mutmut_66': x__run_command__mutmut_66, 
    'x__run_command__mutmut_67': x__run_command__mutmut_67, 
    'x__run_command__mutmut_68': x__run_command__mutmut_68, 
    'x__run_command__mutmut_69': x__run_command__mutmut_69, 
    'x__run_command__mutmut_70': x__run_command__mutmut_70, 
    'x__run_command__mutmut_71': x__run_command__mutmut_71, 
    'x__run_command__mutmut_72': x__run_command__mutmut_72, 
    'x__run_command__mutmut_73': x__run_command__mutmut_73, 
    'x__run_command__mutmut_74': x__run_command__mutmut_74, 
    'x__run_command__mutmut_75': x__run_command__mutmut_75, 
    'x__run_command__mutmut_76': x__run_command__mutmut_76, 
    'x__run_command__mutmut_77': x__run_command__mutmut_77, 
    'x__run_command__mutmut_78': x__run_command__mutmut_78, 
    'x__run_command__mutmut_79': x__run_command__mutmut_79, 
    'x__run_command__mutmut_80': x__run_command__mutmut_80, 
    'x__run_command__mutmut_81': x__run_command__mutmut_81, 
    'x__run_command__mutmut_82': x__run_command__mutmut_82, 
    'x__run_command__mutmut_83': x__run_command__mutmut_83, 
    'x__run_command__mutmut_84': x__run_command__mutmut_84, 
    'x__run_command__mutmut_85': x__run_command__mutmut_85, 
    'x__run_command__mutmut_86': x__run_command__mutmut_86, 
    'x__run_command__mutmut_87': x__run_command__mutmut_87, 
    'x__run_command__mutmut_88': x__run_command__mutmut_88, 
    'x__run_command__mutmut_89': x__run_command__mutmut_89, 
    'x__run_command__mutmut_90': x__run_command__mutmut_90, 
    'x__run_command__mutmut_91': x__run_command__mutmut_91, 
    'x__run_command__mutmut_92': x__run_command__mutmut_92, 
    'x__run_command__mutmut_93': x__run_command__mutmut_93, 
    'x__run_command__mutmut_94': x__run_command__mutmut_94, 
    'x__run_command__mutmut_95': x__run_command__mutmut_95, 
    'x__run_command__mutmut_96': x__run_command__mutmut_96, 
    'x__run_command__mutmut_97': x__run_command__mutmut_97, 
    'x__run_command__mutmut_98': x__run_command__mutmut_98, 
    'x__run_command__mutmut_99': x__run_command__mutmut_99, 
    'x__run_command__mutmut_100': x__run_command__mutmut_100, 
    'x__run_command__mutmut_101': x__run_command__mutmut_101, 
    'x__run_command__mutmut_102': x__run_command__mutmut_102, 
    'x__run_command__mutmut_103': x__run_command__mutmut_103, 
    'x__run_command__mutmut_104': x__run_command__mutmut_104, 
    'x__run_command__mutmut_105': x__run_command__mutmut_105, 
    'x__run_command__mutmut_106': x__run_command__mutmut_106, 
    'x__run_command__mutmut_107': x__run_command__mutmut_107
}

def _run_command(*args, **kwargs):
    result = _mutmut_trampoline(x__run_command__mutmut_orig, x__run_command__mutmut_mutants, args, kwargs)
    return result 

_run_command.__signature__ = _mutmut_signature(x__run_command__mutmut_orig)
x__run_command__mutmut_orig.__name__ = 'x__run_command'


def x__place_terraform_provider_script__mutmut_orig(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_1(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_2(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=None, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_3(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=None)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_4(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_5(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, )

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_6(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=False, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_7(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=False)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_8(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = None
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_9(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir * "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_10(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "XXterraform-provider-pyviderXX"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_11(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "TERRAFORM-PROVIDER-PYVIDER"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_12(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = None

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_13(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = None
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_14(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(None)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_15(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_16(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                None
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_17(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = None
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_18(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" * "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_19(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir * "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_20(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "XXbinXX" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_21(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "BIN" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_22(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "XXpythonXX"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_23(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "PYTHON"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_24(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_25(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                None
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_26(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = None
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_27(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" * "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_28(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir * "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_29(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "XXbinXX" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_30(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "BIN" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_31(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "XXpyviderXX"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_32(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "PYVIDER"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_33(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = None

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_34(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = None
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_35(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'XXexec pyvider provide "$@"XX'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_36(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'EXEC PYVIDER PROVIDE "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_37(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = None
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_38(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "XXinstalled (pyvider command)XX"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_39(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "INSTALLED (PYVIDER COMMAND)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_40(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = None
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_41(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'XXexec python -m pyvider.cli provide "$@"XX'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_42(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'EXEC PYTHON -M PYVIDER.CLI PROVIDE "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_43(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = None

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_44(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "XXeditable (python -m)XX"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_45(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "EDITABLE (PYTHON -M)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_46(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = None

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_47(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(None, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_48(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, None)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_49(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_50(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, )
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_51(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(None)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_52(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode & 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_53(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 74)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_54(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(None, style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_55(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style=None)
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_56(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_57(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", )
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_58(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(None)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_59(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="XXcyanXX")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_60(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="CYAN")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_61(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(None, style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_62(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style=None)
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_63(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_64(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", )
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_65(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="XXcyanXX")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_66(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="CYAN")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_67(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(None, style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_68(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style=None)

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_69(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_70(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", )

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_71(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="XXcyanXX")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_72(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="CYAN")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_73(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            None,
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_74(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style=None,
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_75(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=None,
        )
        raise


def x__place_terraform_provider_script__mutmut_76(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            style="red",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_77(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_78(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            )
        raise


def x__place_terraform_provider_script__mutmut_79(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="XXredXX",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_80(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="RED",
            bold=True,
        )
        raise


def x__place_terraform_provider_script__mutmut_81(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=False,
        )
        raise

x__place_terraform_provider_script__mutmut_mutants : ClassVar[MutantDict] = {
'x__place_terraform_provider_script__mutmut_1': x__place_terraform_provider_script__mutmut_1, 
    'x__place_terraform_provider_script__mutmut_2': x__place_terraform_provider_script__mutmut_2, 
    'x__place_terraform_provider_script__mutmut_3': x__place_terraform_provider_script__mutmut_3, 
    'x__place_terraform_provider_script__mutmut_4': x__place_terraform_provider_script__mutmut_4, 
    'x__place_terraform_provider_script__mutmut_5': x__place_terraform_provider_script__mutmut_5, 
    'x__place_terraform_provider_script__mutmut_6': x__place_terraform_provider_script__mutmut_6, 
    'x__place_terraform_provider_script__mutmut_7': x__place_terraform_provider_script__mutmut_7, 
    'x__place_terraform_provider_script__mutmut_8': x__place_terraform_provider_script__mutmut_8, 
    'x__place_terraform_provider_script__mutmut_9': x__place_terraform_provider_script__mutmut_9, 
    'x__place_terraform_provider_script__mutmut_10': x__place_terraform_provider_script__mutmut_10, 
    'x__place_terraform_provider_script__mutmut_11': x__place_terraform_provider_script__mutmut_11, 
    'x__place_terraform_provider_script__mutmut_12': x__place_terraform_provider_script__mutmut_12, 
    'x__place_terraform_provider_script__mutmut_13': x__place_terraform_provider_script__mutmut_13, 
    'x__place_terraform_provider_script__mutmut_14': x__place_terraform_provider_script__mutmut_14, 
    'x__place_terraform_provider_script__mutmut_15': x__place_terraform_provider_script__mutmut_15, 
    'x__place_terraform_provider_script__mutmut_16': x__place_terraform_provider_script__mutmut_16, 
    'x__place_terraform_provider_script__mutmut_17': x__place_terraform_provider_script__mutmut_17, 
    'x__place_terraform_provider_script__mutmut_18': x__place_terraform_provider_script__mutmut_18, 
    'x__place_terraform_provider_script__mutmut_19': x__place_terraform_provider_script__mutmut_19, 
    'x__place_terraform_provider_script__mutmut_20': x__place_terraform_provider_script__mutmut_20, 
    'x__place_terraform_provider_script__mutmut_21': x__place_terraform_provider_script__mutmut_21, 
    'x__place_terraform_provider_script__mutmut_22': x__place_terraform_provider_script__mutmut_22, 
    'x__place_terraform_provider_script__mutmut_23': x__place_terraform_provider_script__mutmut_23, 
    'x__place_terraform_provider_script__mutmut_24': x__place_terraform_provider_script__mutmut_24, 
    'x__place_terraform_provider_script__mutmut_25': x__place_terraform_provider_script__mutmut_25, 
    'x__place_terraform_provider_script__mutmut_26': x__place_terraform_provider_script__mutmut_26, 
    'x__place_terraform_provider_script__mutmut_27': x__place_terraform_provider_script__mutmut_27, 
    'x__place_terraform_provider_script__mutmut_28': x__place_terraform_provider_script__mutmut_28, 
    'x__place_terraform_provider_script__mutmut_29': x__place_terraform_provider_script__mutmut_29, 
    'x__place_terraform_provider_script__mutmut_30': x__place_terraform_provider_script__mutmut_30, 
    'x__place_terraform_provider_script__mutmut_31': x__place_terraform_provider_script__mutmut_31, 
    'x__place_terraform_provider_script__mutmut_32': x__place_terraform_provider_script__mutmut_32, 
    'x__place_terraform_provider_script__mutmut_33': x__place_terraform_provider_script__mutmut_33, 
    'x__place_terraform_provider_script__mutmut_34': x__place_terraform_provider_script__mutmut_34, 
    'x__place_terraform_provider_script__mutmut_35': x__place_terraform_provider_script__mutmut_35, 
    'x__place_terraform_provider_script__mutmut_36': x__place_terraform_provider_script__mutmut_36, 
    'x__place_terraform_provider_script__mutmut_37': x__place_terraform_provider_script__mutmut_37, 
    'x__place_terraform_provider_script__mutmut_38': x__place_terraform_provider_script__mutmut_38, 
    'x__place_terraform_provider_script__mutmut_39': x__place_terraform_provider_script__mutmut_39, 
    'x__place_terraform_provider_script__mutmut_40': x__place_terraform_provider_script__mutmut_40, 
    'x__place_terraform_provider_script__mutmut_41': x__place_terraform_provider_script__mutmut_41, 
    'x__place_terraform_provider_script__mutmut_42': x__place_terraform_provider_script__mutmut_42, 
    'x__place_terraform_provider_script__mutmut_43': x__place_terraform_provider_script__mutmut_43, 
    'x__place_terraform_provider_script__mutmut_44': x__place_terraform_provider_script__mutmut_44, 
    'x__place_terraform_provider_script__mutmut_45': x__place_terraform_provider_script__mutmut_45, 
    'x__place_terraform_provider_script__mutmut_46': x__place_terraform_provider_script__mutmut_46, 
    'x__place_terraform_provider_script__mutmut_47': x__place_terraform_provider_script__mutmut_47, 
    'x__place_terraform_provider_script__mutmut_48': x__place_terraform_provider_script__mutmut_48, 
    'x__place_terraform_provider_script__mutmut_49': x__place_terraform_provider_script__mutmut_49, 
    'x__place_terraform_provider_script__mutmut_50': x__place_terraform_provider_script__mutmut_50, 
    'x__place_terraform_provider_script__mutmut_51': x__place_terraform_provider_script__mutmut_51, 
    'x__place_terraform_provider_script__mutmut_52': x__place_terraform_provider_script__mutmut_52, 
    'x__place_terraform_provider_script__mutmut_53': x__place_terraform_provider_script__mutmut_53, 
    'x__place_terraform_provider_script__mutmut_54': x__place_terraform_provider_script__mutmut_54, 
    'x__place_terraform_provider_script__mutmut_55': x__place_terraform_provider_script__mutmut_55, 
    'x__place_terraform_provider_script__mutmut_56': x__place_terraform_provider_script__mutmut_56, 
    'x__place_terraform_provider_script__mutmut_57': x__place_terraform_provider_script__mutmut_57, 
    'x__place_terraform_provider_script__mutmut_58': x__place_terraform_provider_script__mutmut_58, 
    'x__place_terraform_provider_script__mutmut_59': x__place_terraform_provider_script__mutmut_59, 
    'x__place_terraform_provider_script__mutmut_60': x__place_terraform_provider_script__mutmut_60, 
    'x__place_terraform_provider_script__mutmut_61': x__place_terraform_provider_script__mutmut_61, 
    'x__place_terraform_provider_script__mutmut_62': x__place_terraform_provider_script__mutmut_62, 
    'x__place_terraform_provider_script__mutmut_63': x__place_terraform_provider_script__mutmut_63, 
    'x__place_terraform_provider_script__mutmut_64': x__place_terraform_provider_script__mutmut_64, 
    'x__place_terraform_provider_script__mutmut_65': x__place_terraform_provider_script__mutmut_65, 
    'x__place_terraform_provider_script__mutmut_66': x__place_terraform_provider_script__mutmut_66, 
    'x__place_terraform_provider_script__mutmut_67': x__place_terraform_provider_script__mutmut_67, 
    'x__place_terraform_provider_script__mutmut_68': x__place_terraform_provider_script__mutmut_68, 
    'x__place_terraform_provider_script__mutmut_69': x__place_terraform_provider_script__mutmut_69, 
    'x__place_terraform_provider_script__mutmut_70': x__place_terraform_provider_script__mutmut_70, 
    'x__place_terraform_provider_script__mutmut_71': x__place_terraform_provider_script__mutmut_71, 
    'x__place_terraform_provider_script__mutmut_72': x__place_terraform_provider_script__mutmut_72, 
    'x__place_terraform_provider_script__mutmut_73': x__place_terraform_provider_script__mutmut_73, 
    'x__place_terraform_provider_script__mutmut_74': x__place_terraform_provider_script__mutmut_74, 
    'x__place_terraform_provider_script__mutmut_75': x__place_terraform_provider_script__mutmut_75, 
    'x__place_terraform_provider_script__mutmut_76': x__place_terraform_provider_script__mutmut_76, 
    'x__place_terraform_provider_script__mutmut_77': x__place_terraform_provider_script__mutmut_77, 
    'x__place_terraform_provider_script__mutmut_78': x__place_terraform_provider_script__mutmut_78, 
    'x__place_terraform_provider_script__mutmut_79': x__place_terraform_provider_script__mutmut_79, 
    'x__place_terraform_provider_script__mutmut_80': x__place_terraform_provider_script__mutmut_80, 
    'x__place_terraform_provider_script__mutmut_81': x__place_terraform_provider_script__mutmut_81
}

def _place_terraform_provider_script(*args, **kwargs):
    result = _mutmut_trampoline(x__place_terraform_provider_script__mutmut_orig, x__place_terraform_provider_script__mutmut_mutants, args, kwargs)
    return result 

_place_terraform_provider_script.__signature__ = _mutmut_signature(x__place_terraform_provider_script__mutmut_orig)
x__place_terraform_provider_script__mutmut_orig.__name__ = 'x__place_terraform_provider_script'
