"""
The canonical entry point for the Pyvider CLI application.
"""

import asyncio

from provide.foundation import logger, shutdown_foundation

from pyvider.cli import cli
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


def x_main__mutmut_orig() -> None:
    """Main entry point for the Pyvider CLI application."""
    # Initialize Foundation logging for CLI mode
    # (Provider mode initializes logging separately in provide_command.py)
    # Note: logger module auto-initializes on first import, so just importing it is sufficient
    logger.debug("Pyvider CLI starting")

    try:
        # The `cli` object is the fully assembled click group.
        # This call hands over control to click to parse args and run the
        # appropriate subcommand.
        cli()
    finally:
        # Ensure proper cleanup of telemetry resources
        asyncio.run(shutdown_foundation())


def x_main__mutmut_1() -> None:
    """Main entry point for the Pyvider CLI application."""
    # Initialize Foundation logging for CLI mode
    # (Provider mode initializes logging separately in provide_command.py)
    # Note: logger module auto-initializes on first import, so just importing it is sufficient
    logger.debug(None)

    try:
        # The `cli` object is the fully assembled click group.
        # This call hands over control to click to parse args and run the
        # appropriate subcommand.
        cli()
    finally:
        # Ensure proper cleanup of telemetry resources
        asyncio.run(shutdown_foundation())


def x_main__mutmut_2() -> None:
    """Main entry point for the Pyvider CLI application."""
    # Initialize Foundation logging for CLI mode
    # (Provider mode initializes logging separately in provide_command.py)
    # Note: logger module auto-initializes on first import, so just importing it is sufficient
    logger.debug("XXPyvider CLI startingXX")

    try:
        # The `cli` object is the fully assembled click group.
        # This call hands over control to click to parse args and run the
        # appropriate subcommand.
        cli()
    finally:
        # Ensure proper cleanup of telemetry resources
        asyncio.run(shutdown_foundation())


def x_main__mutmut_3() -> None:
    """Main entry point for the Pyvider CLI application."""
    # Initialize Foundation logging for CLI mode
    # (Provider mode initializes logging separately in provide_command.py)
    # Note: logger module auto-initializes on first import, so just importing it is sufficient
    logger.debug("pyvider cli starting")

    try:
        # The `cli` object is the fully assembled click group.
        # This call hands over control to click to parse args and run the
        # appropriate subcommand.
        cli()
    finally:
        # Ensure proper cleanup of telemetry resources
        asyncio.run(shutdown_foundation())


def x_main__mutmut_4() -> None:
    """Main entry point for the Pyvider CLI application."""
    # Initialize Foundation logging for CLI mode
    # (Provider mode initializes logging separately in provide_command.py)
    # Note: logger module auto-initializes on first import, so just importing it is sufficient
    logger.debug("PYVIDER CLI STARTING")

    try:
        # The `cli` object is the fully assembled click group.
        # This call hands over control to click to parse args and run the
        # appropriate subcommand.
        cli()
    finally:
        # Ensure proper cleanup of telemetry resources
        asyncio.run(shutdown_foundation())


def x_main__mutmut_5() -> None:
    """Main entry point for the Pyvider CLI application."""
    # Initialize Foundation logging for CLI mode
    # (Provider mode initializes logging separately in provide_command.py)
    # Note: logger module auto-initializes on first import, so just importing it is sufficient
    logger.debug("Pyvider CLI starting")

    try:
        # The `cli` object is the fully assembled click group.
        # This call hands over control to click to parse args and run the
        # appropriate subcommand.
        cli()
    finally:
        # Ensure proper cleanup of telemetry resources
        asyncio.run(None)

x_main__mutmut_mutants : ClassVar[MutantDict] = {
'x_main__mutmut_1': x_main__mutmut_1, 
    'x_main__mutmut_2': x_main__mutmut_2, 
    'x_main__mutmut_3': x_main__mutmut_3, 
    'x_main__mutmut_4': x_main__mutmut_4, 
    'x_main__mutmut_5': x_main__mutmut_5
}

def main(*args, **kwargs):
    result = _mutmut_trampoline(x_main__mutmut_orig, x_main__mutmut_mutants, args, kwargs)
    return result 

main.__signature__ = _mutmut_signature(x_main__mutmut_orig)
x_main__mutmut_orig.__name__ = 'x_main'


if __name__ == "__main__":
    main()
