import asyncio
import sys
from typing import Any

import click
from provide.foundation.cli.decorators import flexible_options
from provide.foundation.console import perr, pout
from provide.foundation.formatting import format_table
from provide.foundation.utils import timed_block

from pyvider.cli.main import PyviderContext, cli, pass_ctx
from pyvider.hub.components import get_hub_diagnostics, registry
from pyvider.hub.discovery import ComponentDiscovery
from pyvider.schema import PvsAttribute, PvsNestedBlock, PvsObjectType, PvsSchema
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


def x__handle_discovery_errors__mutmut_orig(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_1(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr(None)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_2(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" - "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_3(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("XX\nXX" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_4(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" / 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_5(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "XX─XX" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_6(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 71)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_7(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(None, style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_8(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style=None)
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_9(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_10(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", )
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_11(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr("XX ❌ Critical Error: Component Discovery FailedXX", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_12(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ critical error: component discovery failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_13(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ CRITICAL ERROR: COMPONENT DISCOVERY FAILED", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_14(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="XXboldXX")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_15(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="BOLD")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_16(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr(None)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_17(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" / 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_18(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("XX─XX" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_19(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 71)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_20(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            None
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_21(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "XX\nOne or more component modules could not be imported. This usually indicates\nXX"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_22(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\none or more component modules could not be imported. this usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_23(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nONE OR MORE COMPONENT MODULES COULD NOT BE IMPORTED. THIS USUALLY INDICATES\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_24(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "XXa missing dependency or a packaging problem.XX"
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_25(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "A MISSING DEPENDENCY OR A PACKAGING PROBLEM."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_26(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr(None)
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_27(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("XX\nFailed Modules:XX")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_28(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nfailed modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_29(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFAILED MODULES:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_30(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(None, style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_31(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style=None)
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_32(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_33(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", )
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_34(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="XXyellowXX")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_35(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="YELLOW")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_36(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(None)

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_37(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr(None)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_38(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" - "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_39(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("XX\nXX" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_40(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" / 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_41(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "XX─XX" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_42(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 71)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_43(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr(None, style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_44(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style=None)
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_45(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr(style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_46(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", )
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_47(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("XXAction Required:XX", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_48(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("action required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_49(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("ACTION REQUIRED:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_50(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="XXyellow boldXX")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_51(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="YELLOW BOLD")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_52(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr(None)
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_53(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("XX  1. Ensure all dependencies listed in 'pyproject.toml' are installed.XX")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_54(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_55(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. ENSURE ALL DEPENDENCIES LISTED IN 'PYPROJECT.TOML' ARE INSTALLED.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_56(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            None
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_57(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "XX  2. If developing locally, run 'uv pip install -e .[dev]' to install\nXX"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_58(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. if developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_59(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. IF DEVELOPING LOCALLY, RUN 'UV PIP INSTALL -E .[DEV]' TO INSTALL\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_60(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "XX     the project in editable mode with all development dependencies.XX"
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_61(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     THE PROJECT IN EDITABLE MODE WITH ALL DEVELOPMENT DEPENDENCIES."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_62(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr(None)
        sys.exit(1)


def x__handle_discovery_errors__mutmut_63(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("XX  3. Verify that all local component packages are correctly structured.XX")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_64(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. verify that all local component packages are correctly structured.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_65(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. VERIFY THAT ALL LOCAL COMPONENT PACKAGES ARE CORRECTLY STRUCTURED.")
        sys.exit(1)


def x__handle_discovery_errors__mutmut_66(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(None)


def x__handle_discovery_errors__mutmut_67(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
        sys.exit(2)

x__handle_discovery_errors__mutmut_mutants : ClassVar[MutantDict] = {
'x__handle_discovery_errors__mutmut_1': x__handle_discovery_errors__mutmut_1, 
    'x__handle_discovery_errors__mutmut_2': x__handle_discovery_errors__mutmut_2, 
    'x__handle_discovery_errors__mutmut_3': x__handle_discovery_errors__mutmut_3, 
    'x__handle_discovery_errors__mutmut_4': x__handle_discovery_errors__mutmut_4, 
    'x__handle_discovery_errors__mutmut_5': x__handle_discovery_errors__mutmut_5, 
    'x__handle_discovery_errors__mutmut_6': x__handle_discovery_errors__mutmut_6, 
    'x__handle_discovery_errors__mutmut_7': x__handle_discovery_errors__mutmut_7, 
    'x__handle_discovery_errors__mutmut_8': x__handle_discovery_errors__mutmut_8, 
    'x__handle_discovery_errors__mutmut_9': x__handle_discovery_errors__mutmut_9, 
    'x__handle_discovery_errors__mutmut_10': x__handle_discovery_errors__mutmut_10, 
    'x__handle_discovery_errors__mutmut_11': x__handle_discovery_errors__mutmut_11, 
    'x__handle_discovery_errors__mutmut_12': x__handle_discovery_errors__mutmut_12, 
    'x__handle_discovery_errors__mutmut_13': x__handle_discovery_errors__mutmut_13, 
    'x__handle_discovery_errors__mutmut_14': x__handle_discovery_errors__mutmut_14, 
    'x__handle_discovery_errors__mutmut_15': x__handle_discovery_errors__mutmut_15, 
    'x__handle_discovery_errors__mutmut_16': x__handle_discovery_errors__mutmut_16, 
    'x__handle_discovery_errors__mutmut_17': x__handle_discovery_errors__mutmut_17, 
    'x__handle_discovery_errors__mutmut_18': x__handle_discovery_errors__mutmut_18, 
    'x__handle_discovery_errors__mutmut_19': x__handle_discovery_errors__mutmut_19, 
    'x__handle_discovery_errors__mutmut_20': x__handle_discovery_errors__mutmut_20, 
    'x__handle_discovery_errors__mutmut_21': x__handle_discovery_errors__mutmut_21, 
    'x__handle_discovery_errors__mutmut_22': x__handle_discovery_errors__mutmut_22, 
    'x__handle_discovery_errors__mutmut_23': x__handle_discovery_errors__mutmut_23, 
    'x__handle_discovery_errors__mutmut_24': x__handle_discovery_errors__mutmut_24, 
    'x__handle_discovery_errors__mutmut_25': x__handle_discovery_errors__mutmut_25, 
    'x__handle_discovery_errors__mutmut_26': x__handle_discovery_errors__mutmut_26, 
    'x__handle_discovery_errors__mutmut_27': x__handle_discovery_errors__mutmut_27, 
    'x__handle_discovery_errors__mutmut_28': x__handle_discovery_errors__mutmut_28, 
    'x__handle_discovery_errors__mutmut_29': x__handle_discovery_errors__mutmut_29, 
    'x__handle_discovery_errors__mutmut_30': x__handle_discovery_errors__mutmut_30, 
    'x__handle_discovery_errors__mutmut_31': x__handle_discovery_errors__mutmut_31, 
    'x__handle_discovery_errors__mutmut_32': x__handle_discovery_errors__mutmut_32, 
    'x__handle_discovery_errors__mutmut_33': x__handle_discovery_errors__mutmut_33, 
    'x__handle_discovery_errors__mutmut_34': x__handle_discovery_errors__mutmut_34, 
    'x__handle_discovery_errors__mutmut_35': x__handle_discovery_errors__mutmut_35, 
    'x__handle_discovery_errors__mutmut_36': x__handle_discovery_errors__mutmut_36, 
    'x__handle_discovery_errors__mutmut_37': x__handle_discovery_errors__mutmut_37, 
    'x__handle_discovery_errors__mutmut_38': x__handle_discovery_errors__mutmut_38, 
    'x__handle_discovery_errors__mutmut_39': x__handle_discovery_errors__mutmut_39, 
    'x__handle_discovery_errors__mutmut_40': x__handle_discovery_errors__mutmut_40, 
    'x__handle_discovery_errors__mutmut_41': x__handle_discovery_errors__mutmut_41, 
    'x__handle_discovery_errors__mutmut_42': x__handle_discovery_errors__mutmut_42, 
    'x__handle_discovery_errors__mutmut_43': x__handle_discovery_errors__mutmut_43, 
    'x__handle_discovery_errors__mutmut_44': x__handle_discovery_errors__mutmut_44, 
    'x__handle_discovery_errors__mutmut_45': x__handle_discovery_errors__mutmut_45, 
    'x__handle_discovery_errors__mutmut_46': x__handle_discovery_errors__mutmut_46, 
    'x__handle_discovery_errors__mutmut_47': x__handle_discovery_errors__mutmut_47, 
    'x__handle_discovery_errors__mutmut_48': x__handle_discovery_errors__mutmut_48, 
    'x__handle_discovery_errors__mutmut_49': x__handle_discovery_errors__mutmut_49, 
    'x__handle_discovery_errors__mutmut_50': x__handle_discovery_errors__mutmut_50, 
    'x__handle_discovery_errors__mutmut_51': x__handle_discovery_errors__mutmut_51, 
    'x__handle_discovery_errors__mutmut_52': x__handle_discovery_errors__mutmut_52, 
    'x__handle_discovery_errors__mutmut_53': x__handle_discovery_errors__mutmut_53, 
    'x__handle_discovery_errors__mutmut_54': x__handle_discovery_errors__mutmut_54, 
    'x__handle_discovery_errors__mutmut_55': x__handle_discovery_errors__mutmut_55, 
    'x__handle_discovery_errors__mutmut_56': x__handle_discovery_errors__mutmut_56, 
    'x__handle_discovery_errors__mutmut_57': x__handle_discovery_errors__mutmut_57, 
    'x__handle_discovery_errors__mutmut_58': x__handle_discovery_errors__mutmut_58, 
    'x__handle_discovery_errors__mutmut_59': x__handle_discovery_errors__mutmut_59, 
    'x__handle_discovery_errors__mutmut_60': x__handle_discovery_errors__mutmut_60, 
    'x__handle_discovery_errors__mutmut_61': x__handle_discovery_errors__mutmut_61, 
    'x__handle_discovery_errors__mutmut_62': x__handle_discovery_errors__mutmut_62, 
    'x__handle_discovery_errors__mutmut_63': x__handle_discovery_errors__mutmut_63, 
    'x__handle_discovery_errors__mutmut_64': x__handle_discovery_errors__mutmut_64, 
    'x__handle_discovery_errors__mutmut_65': x__handle_discovery_errors__mutmut_65, 
    'x__handle_discovery_errors__mutmut_66': x__handle_discovery_errors__mutmut_66, 
    'x__handle_discovery_errors__mutmut_67': x__handle_discovery_errors__mutmut_67
}

def _handle_discovery_errors(*args, **kwargs):
    result = _mutmut_trampoline(x__handle_discovery_errors__mutmut_orig, x__handle_discovery_errors__mutmut_mutants, args, kwargs)
    return result 

_handle_discovery_errors.__signature__ = _mutmut_signature(x__handle_discovery_errors__mutmut_orig)
x__handle_discovery_errors__mutmut_orig.__name__ = 'x__handle_discovery_errors'


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_orig(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_1(attr: PvsAttribute, indent_level: int) -> None:
    indent = None
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_2(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " / indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_3(attr: PvsAttribute, indent_level: int) -> None:
    indent = "XX  XX" * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_4(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = None
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_5(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(None)
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_6(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style(None, fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_7(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg=None))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_8(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style(fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_9(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", ))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_10(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("XXRequiredXX", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_11(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_12(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("REQUIRED", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_13(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="XXbright_redXX"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_14(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="BRIGHT_RED"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_15(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(None)
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_16(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style(None, fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_17(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg=None))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_18(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style(fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_19(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", ))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_20(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("XXOptionalXX", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_21(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_22(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("OPTIONAL", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_23(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="XXbright_blueXX"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_24(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="BRIGHT_BLUE"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_25(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(None)
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_26(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style(None, fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_27(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg=None))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_28(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style(fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_29(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", ))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_30(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("XXComputedXX", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_31(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_32(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("COMPUTED", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_33(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="XXbright_cyanXX"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_34(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="BRIGHT_CYAN"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_35(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(None)
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_36(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style(None, fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_37(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg=None))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_38(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style(fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_39(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", ))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_40(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("XXSensitiveXX", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_41(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_42(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("SENSITIVE", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_43(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="XXmagentaXX"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_44(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="MAGENTA"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_45(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = None
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_46(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(None)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_47(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({'XX, XX'.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_48(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else "XXXX"
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_49(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(None, style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_50(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style=None)
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_51(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_52(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", )
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_53(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="XXyellowXX")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_54(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="YELLOW")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_55(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = None
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_56(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(None)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_57(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(None, style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_58(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style=None)
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_59(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_60(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", )
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_61(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="XXgreenXX")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_62(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="GREEN")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_63(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(None)
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_64(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is None:
        pout(f"{indent}  - Default: {attr.default}")


# --- Helper Functions for Displaying Schemas ---
def x__display_attribute__mutmut_65(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(None)

x__display_attribute__mutmut_mutants : ClassVar[MutantDict] = {
'x__display_attribute__mutmut_1': x__display_attribute__mutmut_1, 
    'x__display_attribute__mutmut_2': x__display_attribute__mutmut_2, 
    'x__display_attribute__mutmut_3': x__display_attribute__mutmut_3, 
    'x__display_attribute__mutmut_4': x__display_attribute__mutmut_4, 
    'x__display_attribute__mutmut_5': x__display_attribute__mutmut_5, 
    'x__display_attribute__mutmut_6': x__display_attribute__mutmut_6, 
    'x__display_attribute__mutmut_7': x__display_attribute__mutmut_7, 
    'x__display_attribute__mutmut_8': x__display_attribute__mutmut_8, 
    'x__display_attribute__mutmut_9': x__display_attribute__mutmut_9, 
    'x__display_attribute__mutmut_10': x__display_attribute__mutmut_10, 
    'x__display_attribute__mutmut_11': x__display_attribute__mutmut_11, 
    'x__display_attribute__mutmut_12': x__display_attribute__mutmut_12, 
    'x__display_attribute__mutmut_13': x__display_attribute__mutmut_13, 
    'x__display_attribute__mutmut_14': x__display_attribute__mutmut_14, 
    'x__display_attribute__mutmut_15': x__display_attribute__mutmut_15, 
    'x__display_attribute__mutmut_16': x__display_attribute__mutmut_16, 
    'x__display_attribute__mutmut_17': x__display_attribute__mutmut_17, 
    'x__display_attribute__mutmut_18': x__display_attribute__mutmut_18, 
    'x__display_attribute__mutmut_19': x__display_attribute__mutmut_19, 
    'x__display_attribute__mutmut_20': x__display_attribute__mutmut_20, 
    'x__display_attribute__mutmut_21': x__display_attribute__mutmut_21, 
    'x__display_attribute__mutmut_22': x__display_attribute__mutmut_22, 
    'x__display_attribute__mutmut_23': x__display_attribute__mutmut_23, 
    'x__display_attribute__mutmut_24': x__display_attribute__mutmut_24, 
    'x__display_attribute__mutmut_25': x__display_attribute__mutmut_25, 
    'x__display_attribute__mutmut_26': x__display_attribute__mutmut_26, 
    'x__display_attribute__mutmut_27': x__display_attribute__mutmut_27, 
    'x__display_attribute__mutmut_28': x__display_attribute__mutmut_28, 
    'x__display_attribute__mutmut_29': x__display_attribute__mutmut_29, 
    'x__display_attribute__mutmut_30': x__display_attribute__mutmut_30, 
    'x__display_attribute__mutmut_31': x__display_attribute__mutmut_31, 
    'x__display_attribute__mutmut_32': x__display_attribute__mutmut_32, 
    'x__display_attribute__mutmut_33': x__display_attribute__mutmut_33, 
    'x__display_attribute__mutmut_34': x__display_attribute__mutmut_34, 
    'x__display_attribute__mutmut_35': x__display_attribute__mutmut_35, 
    'x__display_attribute__mutmut_36': x__display_attribute__mutmut_36, 
    'x__display_attribute__mutmut_37': x__display_attribute__mutmut_37, 
    'x__display_attribute__mutmut_38': x__display_attribute__mutmut_38, 
    'x__display_attribute__mutmut_39': x__display_attribute__mutmut_39, 
    'x__display_attribute__mutmut_40': x__display_attribute__mutmut_40, 
    'x__display_attribute__mutmut_41': x__display_attribute__mutmut_41, 
    'x__display_attribute__mutmut_42': x__display_attribute__mutmut_42, 
    'x__display_attribute__mutmut_43': x__display_attribute__mutmut_43, 
    'x__display_attribute__mutmut_44': x__display_attribute__mutmut_44, 
    'x__display_attribute__mutmut_45': x__display_attribute__mutmut_45, 
    'x__display_attribute__mutmut_46': x__display_attribute__mutmut_46, 
    'x__display_attribute__mutmut_47': x__display_attribute__mutmut_47, 
    'x__display_attribute__mutmut_48': x__display_attribute__mutmut_48, 
    'x__display_attribute__mutmut_49': x__display_attribute__mutmut_49, 
    'x__display_attribute__mutmut_50': x__display_attribute__mutmut_50, 
    'x__display_attribute__mutmut_51': x__display_attribute__mutmut_51, 
    'x__display_attribute__mutmut_52': x__display_attribute__mutmut_52, 
    'x__display_attribute__mutmut_53': x__display_attribute__mutmut_53, 
    'x__display_attribute__mutmut_54': x__display_attribute__mutmut_54, 
    'x__display_attribute__mutmut_55': x__display_attribute__mutmut_55, 
    'x__display_attribute__mutmut_56': x__display_attribute__mutmut_56, 
    'x__display_attribute__mutmut_57': x__display_attribute__mutmut_57, 
    'x__display_attribute__mutmut_58': x__display_attribute__mutmut_58, 
    'x__display_attribute__mutmut_59': x__display_attribute__mutmut_59, 
    'x__display_attribute__mutmut_60': x__display_attribute__mutmut_60, 
    'x__display_attribute__mutmut_61': x__display_attribute__mutmut_61, 
    'x__display_attribute__mutmut_62': x__display_attribute__mutmut_62, 
    'x__display_attribute__mutmut_63': x__display_attribute__mutmut_63, 
    'x__display_attribute__mutmut_64': x__display_attribute__mutmut_64, 
    'x__display_attribute__mutmut_65': x__display_attribute__mutmut_65
}

def _display_attribute(*args, **kwargs):
    result = _mutmut_trampoline(x__display_attribute__mutmut_orig, x__display_attribute__mutmut_mutants, args, kwargs)
    return result 

_display_attribute.__signature__ = _mutmut_signature(x__display_attribute__mutmut_orig)
x__display_attribute__mutmut_orig.__name__ = 'x__display_attribute'


def x__display_block_type__mutmut_orig(block_def: PvsNestedBlock, indent_level: int) -> None:
    indent = "  " * indent_level
    nesting_str = f"({block_def.nesting.name})"
    pout(f"{indent}Block: {block_def.type_name} {nesting_str}", style="bright_yellow")
    if block_def.description:
        pout(f"{indent}  - Description: {block_def.description}")
    _display_block_content(block_def.block, indent_level + 1)


def x__display_block_type__mutmut_1(block_def: PvsNestedBlock, indent_level: int) -> None:
    indent = None
    nesting_str = f"({block_def.nesting.name})"
    pout(f"{indent}Block: {block_def.type_name} {nesting_str}", style="bright_yellow")
    if block_def.description:
        pout(f"{indent}  - Description: {block_def.description}")
    _display_block_content(block_def.block, indent_level + 1)


def x__display_block_type__mutmut_2(block_def: PvsNestedBlock, indent_level: int) -> None:
    indent = "  " / indent_level
    nesting_str = f"({block_def.nesting.name})"
    pout(f"{indent}Block: {block_def.type_name} {nesting_str}", style="bright_yellow")
    if block_def.description:
        pout(f"{indent}  - Description: {block_def.description}")
    _display_block_content(block_def.block, indent_level + 1)


def x__display_block_type__mutmut_3(block_def: PvsNestedBlock, indent_level: int) -> None:
    indent = "XX  XX" * indent_level
    nesting_str = f"({block_def.nesting.name})"
    pout(f"{indent}Block: {block_def.type_name} {nesting_str}", style="bright_yellow")
    if block_def.description:
        pout(f"{indent}  - Description: {block_def.description}")
    _display_block_content(block_def.block, indent_level + 1)


def x__display_block_type__mutmut_4(block_def: PvsNestedBlock, indent_level: int) -> None:
    indent = "  " * indent_level
    nesting_str = None
    pout(f"{indent}Block: {block_def.type_name} {nesting_str}", style="bright_yellow")
    if block_def.description:
        pout(f"{indent}  - Description: {block_def.description}")
    _display_block_content(block_def.block, indent_level + 1)


def x__display_block_type__mutmut_5(block_def: PvsNestedBlock, indent_level: int) -> None:
    indent = "  " * indent_level
    nesting_str = f"({block_def.nesting.name})"
    pout(None, style="bright_yellow")
    if block_def.description:
        pout(f"{indent}  - Description: {block_def.description}")
    _display_block_content(block_def.block, indent_level + 1)


def x__display_block_type__mutmut_6(block_def: PvsNestedBlock, indent_level: int) -> None:
    indent = "  " * indent_level
    nesting_str = f"({block_def.nesting.name})"
    pout(f"{indent}Block: {block_def.type_name} {nesting_str}", style=None)
    if block_def.description:
        pout(f"{indent}  - Description: {block_def.description}")
    _display_block_content(block_def.block, indent_level + 1)


def x__display_block_type__mutmut_7(block_def: PvsNestedBlock, indent_level: int) -> None:
    indent = "  " * indent_level
    nesting_str = f"({block_def.nesting.name})"
    pout(style="bright_yellow")
    if block_def.description:
        pout(f"{indent}  - Description: {block_def.description}")
    _display_block_content(block_def.block, indent_level + 1)


def x__display_block_type__mutmut_8(block_def: PvsNestedBlock, indent_level: int) -> None:
    indent = "  " * indent_level
    nesting_str = f"({block_def.nesting.name})"
    pout(f"{indent}Block: {block_def.type_name} {nesting_str}", )
    if block_def.description:
        pout(f"{indent}  - Description: {block_def.description}")
    _display_block_content(block_def.block, indent_level + 1)


def x__display_block_type__mutmut_9(block_def: PvsNestedBlock, indent_level: int) -> None:
    indent = "  " * indent_level
    nesting_str = f"({block_def.nesting.name})"
    pout(f"{indent}Block: {block_def.type_name} {nesting_str}", style="XXbright_yellowXX")
    if block_def.description:
        pout(f"{indent}  - Description: {block_def.description}")
    _display_block_content(block_def.block, indent_level + 1)


def x__display_block_type__mutmut_10(block_def: PvsNestedBlock, indent_level: int) -> None:
    indent = "  " * indent_level
    nesting_str = f"({block_def.nesting.name})"
    pout(f"{indent}Block: {block_def.type_name} {nesting_str}", style="BRIGHT_YELLOW")
    if block_def.description:
        pout(f"{indent}  - Description: {block_def.description}")
    _display_block_content(block_def.block, indent_level + 1)


def x__display_block_type__mutmut_11(block_def: PvsNestedBlock, indent_level: int) -> None:
    indent = "  " * indent_level
    nesting_str = f"({block_def.nesting.name})"
    pout(f"{indent}Block: {block_def.type_name} {nesting_str}", style="bright_yellow")
    if block_def.description:
        pout(None)
    _display_block_content(block_def.block, indent_level + 1)


def x__display_block_type__mutmut_12(block_def: PvsNestedBlock, indent_level: int) -> None:
    indent = "  " * indent_level
    nesting_str = f"({block_def.nesting.name})"
    pout(f"{indent}Block: {block_def.type_name} {nesting_str}", style="bright_yellow")
    if block_def.description:
        pout(f"{indent}  - Description: {block_def.description}")
    _display_block_content(None, indent_level + 1)


def x__display_block_type__mutmut_13(block_def: PvsNestedBlock, indent_level: int) -> None:
    indent = "  " * indent_level
    nesting_str = f"({block_def.nesting.name})"
    pout(f"{indent}Block: {block_def.type_name} {nesting_str}", style="bright_yellow")
    if block_def.description:
        pout(f"{indent}  - Description: {block_def.description}")
    _display_block_content(block_def.block, None)


def x__display_block_type__mutmut_14(block_def: PvsNestedBlock, indent_level: int) -> None:
    indent = "  " * indent_level
    nesting_str = f"({block_def.nesting.name})"
    pout(f"{indent}Block: {block_def.type_name} {nesting_str}", style="bright_yellow")
    if block_def.description:
        pout(f"{indent}  - Description: {block_def.description}")
    _display_block_content(indent_level + 1)


def x__display_block_type__mutmut_15(block_def: PvsNestedBlock, indent_level: int) -> None:
    indent = "  " * indent_level
    nesting_str = f"({block_def.nesting.name})"
    pout(f"{indent}Block: {block_def.type_name} {nesting_str}", style="bright_yellow")
    if block_def.description:
        pout(f"{indent}  - Description: {block_def.description}")
    _display_block_content(block_def.block, )


def x__display_block_type__mutmut_16(block_def: PvsNestedBlock, indent_level: int) -> None:
    indent = "  " * indent_level
    nesting_str = f"({block_def.nesting.name})"
    pout(f"{indent}Block: {block_def.type_name} {nesting_str}", style="bright_yellow")
    if block_def.description:
        pout(f"{indent}  - Description: {block_def.description}")
    _display_block_content(block_def.block, indent_level - 1)


def x__display_block_type__mutmut_17(block_def: PvsNestedBlock, indent_level: int) -> None:
    indent = "  " * indent_level
    nesting_str = f"({block_def.nesting.name})"
    pout(f"{indent}Block: {block_def.type_name} {nesting_str}", style="bright_yellow")
    if block_def.description:
        pout(f"{indent}  - Description: {block_def.description}")
    _display_block_content(block_def.block, indent_level + 2)

x__display_block_type__mutmut_mutants : ClassVar[MutantDict] = {
'x__display_block_type__mutmut_1': x__display_block_type__mutmut_1, 
    'x__display_block_type__mutmut_2': x__display_block_type__mutmut_2, 
    'x__display_block_type__mutmut_3': x__display_block_type__mutmut_3, 
    'x__display_block_type__mutmut_4': x__display_block_type__mutmut_4, 
    'x__display_block_type__mutmut_5': x__display_block_type__mutmut_5, 
    'x__display_block_type__mutmut_6': x__display_block_type__mutmut_6, 
    'x__display_block_type__mutmut_7': x__display_block_type__mutmut_7, 
    'x__display_block_type__mutmut_8': x__display_block_type__mutmut_8, 
    'x__display_block_type__mutmut_9': x__display_block_type__mutmut_9, 
    'x__display_block_type__mutmut_10': x__display_block_type__mutmut_10, 
    'x__display_block_type__mutmut_11': x__display_block_type__mutmut_11, 
    'x__display_block_type__mutmut_12': x__display_block_type__mutmut_12, 
    'x__display_block_type__mutmut_13': x__display_block_type__mutmut_13, 
    'x__display_block_type__mutmut_14': x__display_block_type__mutmut_14, 
    'x__display_block_type__mutmut_15': x__display_block_type__mutmut_15, 
    'x__display_block_type__mutmut_16': x__display_block_type__mutmut_16, 
    'x__display_block_type__mutmut_17': x__display_block_type__mutmut_17
}

def _display_block_type(*args, **kwargs):
    result = _mutmut_trampoline(x__display_block_type__mutmut_orig, x__display_block_type__mutmut_mutants, args, kwargs)
    return result 

_display_block_type.__signature__ = _mutmut_signature(x__display_block_type__mutmut_orig)
x__display_block_type__mutmut_orig.__name__ = 'x__display_block_type'


def x__display_block_content__mutmut_orig(block: PvsObjectType, indent_level: int) -> None:
    if block.attributes:
        for attr in block.attributes.values():
            _display_attribute(attr, indent_level + 1)
    if block.block_types:
        for nested_block in block.block_types:
            _display_block_type(nested_block, indent_level + 1)


def x__display_block_content__mutmut_1(block: PvsObjectType, indent_level: int) -> None:
    if block.attributes:
        for attr in block.attributes.values():
            _display_attribute(None, indent_level + 1)
    if block.block_types:
        for nested_block in block.block_types:
            _display_block_type(nested_block, indent_level + 1)


def x__display_block_content__mutmut_2(block: PvsObjectType, indent_level: int) -> None:
    if block.attributes:
        for attr in block.attributes.values():
            _display_attribute(attr, None)
    if block.block_types:
        for nested_block in block.block_types:
            _display_block_type(nested_block, indent_level + 1)


def x__display_block_content__mutmut_3(block: PvsObjectType, indent_level: int) -> None:
    if block.attributes:
        for attr in block.attributes.values():
            _display_attribute(indent_level + 1)
    if block.block_types:
        for nested_block in block.block_types:
            _display_block_type(nested_block, indent_level + 1)


def x__display_block_content__mutmut_4(block: PvsObjectType, indent_level: int) -> None:
    if block.attributes:
        for attr in block.attributes.values():
            _display_attribute(attr, )
    if block.block_types:
        for nested_block in block.block_types:
            _display_block_type(nested_block, indent_level + 1)


def x__display_block_content__mutmut_5(block: PvsObjectType, indent_level: int) -> None:
    if block.attributes:
        for attr in block.attributes.values():
            _display_attribute(attr, indent_level - 1)
    if block.block_types:
        for nested_block in block.block_types:
            _display_block_type(nested_block, indent_level + 1)


def x__display_block_content__mutmut_6(block: PvsObjectType, indent_level: int) -> None:
    if block.attributes:
        for attr in block.attributes.values():
            _display_attribute(attr, indent_level + 2)
    if block.block_types:
        for nested_block in block.block_types:
            _display_block_type(nested_block, indent_level + 1)


def x__display_block_content__mutmut_7(block: PvsObjectType, indent_level: int) -> None:
    if block.attributes:
        for attr in block.attributes.values():
            _display_attribute(attr, indent_level + 1)
    if block.block_types:
        for nested_block in block.block_types:
            _display_block_type(None, indent_level + 1)


def x__display_block_content__mutmut_8(block: PvsObjectType, indent_level: int) -> None:
    if block.attributes:
        for attr in block.attributes.values():
            _display_attribute(attr, indent_level + 1)
    if block.block_types:
        for nested_block in block.block_types:
            _display_block_type(nested_block, None)


def x__display_block_content__mutmut_9(block: PvsObjectType, indent_level: int) -> None:
    if block.attributes:
        for attr in block.attributes.values():
            _display_attribute(attr, indent_level + 1)
    if block.block_types:
        for nested_block in block.block_types:
            _display_block_type(indent_level + 1)


def x__display_block_content__mutmut_10(block: PvsObjectType, indent_level: int) -> None:
    if block.attributes:
        for attr in block.attributes.values():
            _display_attribute(attr, indent_level + 1)
    if block.block_types:
        for nested_block in block.block_types:
            _display_block_type(nested_block, )


def x__display_block_content__mutmut_11(block: PvsObjectType, indent_level: int) -> None:
    if block.attributes:
        for attr in block.attributes.values():
            _display_attribute(attr, indent_level + 1)
    if block.block_types:
        for nested_block in block.block_types:
            _display_block_type(nested_block, indent_level - 1)


def x__display_block_content__mutmut_12(block: PvsObjectType, indent_level: int) -> None:
    if block.attributes:
        for attr in block.attributes.values():
            _display_attribute(attr, indent_level + 1)
    if block.block_types:
        for nested_block in block.block_types:
            _display_block_type(nested_block, indent_level + 2)

x__display_block_content__mutmut_mutants : ClassVar[MutantDict] = {
'x__display_block_content__mutmut_1': x__display_block_content__mutmut_1, 
    'x__display_block_content__mutmut_2': x__display_block_content__mutmut_2, 
    'x__display_block_content__mutmut_3': x__display_block_content__mutmut_3, 
    'x__display_block_content__mutmut_4': x__display_block_content__mutmut_4, 
    'x__display_block_content__mutmut_5': x__display_block_content__mutmut_5, 
    'x__display_block_content__mutmut_6': x__display_block_content__mutmut_6, 
    'x__display_block_content__mutmut_7': x__display_block_content__mutmut_7, 
    'x__display_block_content__mutmut_8': x__display_block_content__mutmut_8, 
    'x__display_block_content__mutmut_9': x__display_block_content__mutmut_9, 
    'x__display_block_content__mutmut_10': x__display_block_content__mutmut_10, 
    'x__display_block_content__mutmut_11': x__display_block_content__mutmut_11, 
    'x__display_block_content__mutmut_12': x__display_block_content__mutmut_12
}

def _display_block_content(*args, **kwargs):
    result = _mutmut_trampoline(x__display_block_content__mutmut_orig, x__display_block_content__mutmut_mutants, args, kwargs)
    return result 

_display_block_content.__signature__ = _mutmut_signature(x__display_block_content__mutmut_orig)
x__display_block_content__mutmut_orig.__name__ = 'x__display_block_content'


# --- Main 'components' Group ---
@cli.group()
@flexible_options  # Allow logging control at the component group level
@pass_ctx
def components(ctx: PyviderContext, **kwargs: Any) -> None:
    """Manage, inspect, and diagnose Pyvider components."""
    # THE FIX: Run discovery and error handling for the entire command group.
    asyncio.run(ctx._ensure_components_discovered(registry, ComponentDiscovery, click.echo, click.secho))
    _handle_discovery_errors(ctx)


# --- Core Component Commands ---
@components.command(name="list")
@pass_ctx
def list_components(ctx: PyviderContext) -> None:
    """Lists all available Pyvider components."""
    all_comps = registry.list_components()
    if not any(all_comps.values()):
        click.secho("No components found.", fg="yellow")
        return
    for comp_type, comps_dict in sorted(all_comps.items()):
        if comps_dict:
            click.secho(f"\n{comp_type.capitalize()}:", fg="bright_cyan", bold=True)
            for name in sorted(comps_dict.keys()):
                click.secho(f"  - {name}")


@components.command(name="show")
@click.argument("component_type")
@click.argument("component_name")
@pass_ctx
def show_component(ctx: PyviderContext, component_type: str, component_name: str) -> None:
    """
    Shows detailed information and schema for a specific component.
    """
    comp_type_lower = component_type.lower()
    component = registry.get_component(comp_type_lower, component_name)
    if not component:
        perr(f"Component '{component_name}' of type '{comp_type_lower}' not found.")
        return
    pout(f"\n📋 Schema for {comp_type_lower}: {component_name}", style="bold bright_white")
    pout("=" * (20 + len(comp_type_lower) + len(component_name)))
    if comp_type_lower == "singleton" and hasattr(component, "schema"):
        schema = component.schema
    elif hasattr(component, "get_schema"):
        schema = component.get_schema()
    else:
        pout("This component does not expose a schema.", style="yellow")
        return
    if not isinstance(schema, PvsSchema):
        perr("Component's schema method did not return a PvsSchema object.")
        return
    if schema.block.description:
        pout(f"\n{schema.block.description}\n", style="italic")
    _display_block_content(schema.block, 0)
    pout("")


@components.command(name="diagnostics")
@pass_ctx
def show_diagnostics(ctx: PyviderContext) -> None:
    """Shows detailed autodiscovery diagnostics from the component hub."""
    pout("📊 Hub Diagnostics", style="bold")
    pout("=" * 30)

    try:
        with timed_block() as timer:
            diagnostics = get_hub_diagnostics()

        # Summary stats
        pout(f"🔢 Total component types: {diagnostics['total_component_types']}")
        pout(f"🔢 Total components: {diagnostics['total_components']}")
        pout(f"⏱️  Discovery time: {timer.elapsed:.3f}s")

        # Component breakdown table
        pout("\n📋 Component Breakdown:")

        # Prepare table data
        table_data = []
        for comp_type, count in diagnostics["component_breakdown"].items():
            table_data.append([comp_type.title(), str(count)])

        if table_data:
            # Use foundation's table formatter
            table = format_table(table_data, headers=["Component Type", "Count"], title="Components by Type")
            pout(table)
        else:
            pout("  No components discovered")

    except Exception as e:
        perr(f"❌ Failed to get diagnostics: {e}")
