"""
Launch context detection for Pyvider.

This module detects how Pyvider was launched and provides context information
about the execution environment.
"""

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
import os
from pathlib import Path
import sys
from typing import Any
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


class LaunchMethod(Enum):
    """Different ways Pyvider can be launched."""

    PSPF_PACKAGE = "pspf_package"
    SCRIPT_MODULE = "script_module"
    SCRIPT_DIRECT = "script_direct"
    EDITABLE_INSTALL = "editable_install"
    UNKNOWN = "unknown"


@dataclass
class LaunchContext:
    """Context information about how Pyvider was launched."""

    method: LaunchMethod
    executable_path: str
    python_executable: str
    working_directory: str
    environment_info: dict[str, Any]
    is_terraform_invoked: bool
    details: dict[str, Any]

    def __str__(self) -> str:
        """Human-readable representation of launch context."""
        lines = [
            "🚀 Pyvider Launch Context:",
            f"   Method: {self.method.value}",
            f"   Executable: {self.executable_path}",
            f"   Python: {self.python_executable}",
            f"   Working Dir: {self.working_directory}",
            f"   Terraform Invoked: {self.is_terraform_invoked}",
        ]

        if self.details:
            lines.append("   Details:")
            for key, value in self.details.items():
                lines.append(f"     {key}: {value}")

        return "\n".join(lines)


def x_detect_launch_context__mutmut_orig() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_1() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = None
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_2() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[1] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_3() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else "XXXX"
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_4() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = None
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_5() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = None
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_6() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(None)
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_7() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = None

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_8() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(None)

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_9() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get(None))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_10() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("XXTF_PLUGIN_MAGIC_COOKIEXX"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_11() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("tf_plugin_magic_cookie"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_12() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = None

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_13() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "XXpython_versionXX": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_14() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "PYTHON_VERSION": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_15() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "XXplatformXX": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_16() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "PLATFORM": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_17() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "XXargvXX": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_18() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "ARGV": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_19() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "XXpath_entriesXX": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_20() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "PATH_ENTRIES": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_21() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "XXterraform_cookie_presentXX": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_22() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "TERRAFORM_COOKIE_PRESENT": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_23() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = None
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_24() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") and "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_25() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith(None) or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_26() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("XXPSPF_XX") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_27() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("pspf_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_28() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "XXpspfXX" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_29() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "PSPF" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_30() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" not in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_31() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.upper():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_32() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = None
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_33() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = None

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_34() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["XXpspf_env_varsXX"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_35() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["PSPF_ENV_VARS"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_36() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = None

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_37() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(None, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_38() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, None)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_39() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_40() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, )

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_41() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=None,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_42() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=None,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_43() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=None,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_44() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=None,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_45() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=None,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_46() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=None,
        details=details,
    )


def x_detect_launch_context__mutmut_47() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=None,
    )


def x_detect_launch_context__mutmut_48() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_49() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_50() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_51() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_52() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        is_terraform_invoked=is_terraform_invoked,
        details=details,
    )


def x_detect_launch_context__mutmut_53() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        details=details,
    )


def x_detect_launch_context__mutmut_54() -> LaunchContext:
    """
    Detect how Pyvider was launched and return context information.

    Returns:
        LaunchContext with details about the execution environment
    """
    executable_path = sys.argv[0] if sys.argv else ""
    python_executable = sys.executable
    working_directory = str(Path.cwd())
    is_terraform_invoked = bool(os.environ.get("TF_PLUGIN_MAGIC_COOKIE"))

    # Gather environment information
    environment_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "argv": sys.argv,
        "path_entries": len(sys.path),
        "terraform_cookie_present": is_terraform_invoked,
    }

    # Add PSPF-specific environment variables if present
    pspf_env_vars = {}
    for key in os.environ:
        if key.startswith("PSPF_") or "pspf" in key.lower():
            pspf_env_vars[key] = os.environ[key]
    if pspf_env_vars:
        environment_info["pspf_env_vars"] = pspf_env_vars

    # Detect launch method and gather details
    method, details = _detect_launch_method(executable_path, python_executable)

    return LaunchContext(
        method=method,
        executable_path=executable_path,
        python_executable=python_executable,
        working_directory=working_directory,
        environment_info=environment_info,
        is_terraform_invoked=is_terraform_invoked,
        )

x_detect_launch_context__mutmut_mutants : ClassVar[MutantDict] = {
'x_detect_launch_context__mutmut_1': x_detect_launch_context__mutmut_1, 
    'x_detect_launch_context__mutmut_2': x_detect_launch_context__mutmut_2, 
    'x_detect_launch_context__mutmut_3': x_detect_launch_context__mutmut_3, 
    'x_detect_launch_context__mutmut_4': x_detect_launch_context__mutmut_4, 
    'x_detect_launch_context__mutmut_5': x_detect_launch_context__mutmut_5, 
    'x_detect_launch_context__mutmut_6': x_detect_launch_context__mutmut_6, 
    'x_detect_launch_context__mutmut_7': x_detect_launch_context__mutmut_7, 
    'x_detect_launch_context__mutmut_8': x_detect_launch_context__mutmut_8, 
    'x_detect_launch_context__mutmut_9': x_detect_launch_context__mutmut_9, 
    'x_detect_launch_context__mutmut_10': x_detect_launch_context__mutmut_10, 
    'x_detect_launch_context__mutmut_11': x_detect_launch_context__mutmut_11, 
    'x_detect_launch_context__mutmut_12': x_detect_launch_context__mutmut_12, 
    'x_detect_launch_context__mutmut_13': x_detect_launch_context__mutmut_13, 
    'x_detect_launch_context__mutmut_14': x_detect_launch_context__mutmut_14, 
    'x_detect_launch_context__mutmut_15': x_detect_launch_context__mutmut_15, 
    'x_detect_launch_context__mutmut_16': x_detect_launch_context__mutmut_16, 
    'x_detect_launch_context__mutmut_17': x_detect_launch_context__mutmut_17, 
    'x_detect_launch_context__mutmut_18': x_detect_launch_context__mutmut_18, 
    'x_detect_launch_context__mutmut_19': x_detect_launch_context__mutmut_19, 
    'x_detect_launch_context__mutmut_20': x_detect_launch_context__mutmut_20, 
    'x_detect_launch_context__mutmut_21': x_detect_launch_context__mutmut_21, 
    'x_detect_launch_context__mutmut_22': x_detect_launch_context__mutmut_22, 
    'x_detect_launch_context__mutmut_23': x_detect_launch_context__mutmut_23, 
    'x_detect_launch_context__mutmut_24': x_detect_launch_context__mutmut_24, 
    'x_detect_launch_context__mutmut_25': x_detect_launch_context__mutmut_25, 
    'x_detect_launch_context__mutmut_26': x_detect_launch_context__mutmut_26, 
    'x_detect_launch_context__mutmut_27': x_detect_launch_context__mutmut_27, 
    'x_detect_launch_context__mutmut_28': x_detect_launch_context__mutmut_28, 
    'x_detect_launch_context__mutmut_29': x_detect_launch_context__mutmut_29, 
    'x_detect_launch_context__mutmut_30': x_detect_launch_context__mutmut_30, 
    'x_detect_launch_context__mutmut_31': x_detect_launch_context__mutmut_31, 
    'x_detect_launch_context__mutmut_32': x_detect_launch_context__mutmut_32, 
    'x_detect_launch_context__mutmut_33': x_detect_launch_context__mutmut_33, 
    'x_detect_launch_context__mutmut_34': x_detect_launch_context__mutmut_34, 
    'x_detect_launch_context__mutmut_35': x_detect_launch_context__mutmut_35, 
    'x_detect_launch_context__mutmut_36': x_detect_launch_context__mutmut_36, 
    'x_detect_launch_context__mutmut_37': x_detect_launch_context__mutmut_37, 
    'x_detect_launch_context__mutmut_38': x_detect_launch_context__mutmut_38, 
    'x_detect_launch_context__mutmut_39': x_detect_launch_context__mutmut_39, 
    'x_detect_launch_context__mutmut_40': x_detect_launch_context__mutmut_40, 
    'x_detect_launch_context__mutmut_41': x_detect_launch_context__mutmut_41, 
    'x_detect_launch_context__mutmut_42': x_detect_launch_context__mutmut_42, 
    'x_detect_launch_context__mutmut_43': x_detect_launch_context__mutmut_43, 
    'x_detect_launch_context__mutmut_44': x_detect_launch_context__mutmut_44, 
    'x_detect_launch_context__mutmut_45': x_detect_launch_context__mutmut_45, 
    'x_detect_launch_context__mutmut_46': x_detect_launch_context__mutmut_46, 
    'x_detect_launch_context__mutmut_47': x_detect_launch_context__mutmut_47, 
    'x_detect_launch_context__mutmut_48': x_detect_launch_context__mutmut_48, 
    'x_detect_launch_context__mutmut_49': x_detect_launch_context__mutmut_49, 
    'x_detect_launch_context__mutmut_50': x_detect_launch_context__mutmut_50, 
    'x_detect_launch_context__mutmut_51': x_detect_launch_context__mutmut_51, 
    'x_detect_launch_context__mutmut_52': x_detect_launch_context__mutmut_52, 
    'x_detect_launch_context__mutmut_53': x_detect_launch_context__mutmut_53, 
    'x_detect_launch_context__mutmut_54': x_detect_launch_context__mutmut_54
}

def detect_launch_context(*args, **kwargs):
    result = _mutmut_trampoline(x_detect_launch_context__mutmut_orig, x_detect_launch_context__mutmut_mutants, args, kwargs)
    return result 

detect_launch_context.__signature__ = _mutmut_signature(x_detect_launch_context__mutmut_orig)
x_detect_launch_context__mutmut_orig.__name__ = 'x_detect_launch_context'


def x__detect_launch_method__mutmut_orig(executable_path: str, python_executable: str) -> tuple[LaunchMethod, dict[str, Any]]:
    """
    Detect the specific launch method based on executable path and environment.

    Returns:
        Tuple of (LaunchMethod, details_dict)
    """
    details = {}

    # Check if we're running from a PSPF package
    if _is_pspf_launch(executable_path, python_executable):
        details.update(_get_pspf_details())
        return LaunchMethod.PSPF_PACKAGE, details

    # Check if we're running as a Python module
    if _is_module_launch():
        details["module_name"] = _get_module_name()
        details["launch_command"] = " ".join(sys.argv)
        return LaunchMethod.SCRIPT_MODULE, details

    # Check if we're running from an editable install
    if _is_editable_install(executable_path):
        details.update(_get_editable_install_details(executable_path))
        return LaunchMethod.EDITABLE_INSTALL, details

    # Check if we're running as a direct script
    if _is_direct_script_launch(executable_path):
        details["script_path"] = executable_path
        details["is_symlink"] = Path(executable_path).is_symlink()
        return LaunchMethod.SCRIPT_DIRECT, details

    # Unknown launch method
    details["reason"] = "Could not determine launch method"
    details["executable_analysis"] = _analyze_executable(executable_path)
    return LaunchMethod.UNKNOWN, details


def x__detect_launch_method__mutmut_1(executable_path: str, python_executable: str) -> tuple[LaunchMethod, dict[str, Any]]:
    """
    Detect the specific launch method based on executable path and environment.

    Returns:
        Tuple of (LaunchMethod, details_dict)
    """
    details = None

    # Check if we're running from a PSPF package
    if _is_pspf_launch(executable_path, python_executable):
        details.update(_get_pspf_details())
        return LaunchMethod.PSPF_PACKAGE, details

    # Check if we're running as a Python module
    if _is_module_launch():
        details["module_name"] = _get_module_name()
        details["launch_command"] = " ".join(sys.argv)
        return LaunchMethod.SCRIPT_MODULE, details

    # Check if we're running from an editable install
    if _is_editable_install(executable_path):
        details.update(_get_editable_install_details(executable_path))
        return LaunchMethod.EDITABLE_INSTALL, details

    # Check if we're running as a direct script
    if _is_direct_script_launch(executable_path):
        details["script_path"] = executable_path
        details["is_symlink"] = Path(executable_path).is_symlink()
        return LaunchMethod.SCRIPT_DIRECT, details

    # Unknown launch method
    details["reason"] = "Could not determine launch method"
    details["executable_analysis"] = _analyze_executable(executable_path)
    return LaunchMethod.UNKNOWN, details


def x__detect_launch_method__mutmut_2(executable_path: str, python_executable: str) -> tuple[LaunchMethod, dict[str, Any]]:
    """
    Detect the specific launch method based on executable path and environment.

    Returns:
        Tuple of (LaunchMethod, details_dict)
    """
    details = {}

    # Check if we're running from a PSPF package
    if _is_pspf_launch(None, python_executable):
        details.update(_get_pspf_details())
        return LaunchMethod.PSPF_PACKAGE, details

    # Check if we're running as a Python module
    if _is_module_launch():
        details["module_name"] = _get_module_name()
        details["launch_command"] = " ".join(sys.argv)
        return LaunchMethod.SCRIPT_MODULE, details

    # Check if we're running from an editable install
    if _is_editable_install(executable_path):
        details.update(_get_editable_install_details(executable_path))
        return LaunchMethod.EDITABLE_INSTALL, details

    # Check if we're running as a direct script
    if _is_direct_script_launch(executable_path):
        details["script_path"] = executable_path
        details["is_symlink"] = Path(executable_path).is_symlink()
        return LaunchMethod.SCRIPT_DIRECT, details

    # Unknown launch method
    details["reason"] = "Could not determine launch method"
    details["executable_analysis"] = _analyze_executable(executable_path)
    return LaunchMethod.UNKNOWN, details


def x__detect_launch_method__mutmut_3(executable_path: str, python_executable: str) -> tuple[LaunchMethod, dict[str, Any]]:
    """
    Detect the specific launch method based on executable path and environment.

    Returns:
        Tuple of (LaunchMethod, details_dict)
    """
    details = {}

    # Check if we're running from a PSPF package
    if _is_pspf_launch(executable_path, None):
        details.update(_get_pspf_details())
        return LaunchMethod.PSPF_PACKAGE, details

    # Check if we're running as a Python module
    if _is_module_launch():
        details["module_name"] = _get_module_name()
        details["launch_command"] = " ".join(sys.argv)
        return LaunchMethod.SCRIPT_MODULE, details

    # Check if we're running from an editable install
    if _is_editable_install(executable_path):
        details.update(_get_editable_install_details(executable_path))
        return LaunchMethod.EDITABLE_INSTALL, details

    # Check if we're running as a direct script
    if _is_direct_script_launch(executable_path):
        details["script_path"] = executable_path
        details["is_symlink"] = Path(executable_path).is_symlink()
        return LaunchMethod.SCRIPT_DIRECT, details

    # Unknown launch method
    details["reason"] = "Could not determine launch method"
    details["executable_analysis"] = _analyze_executable(executable_path)
    return LaunchMethod.UNKNOWN, details


def x__detect_launch_method__mutmut_4(executable_path: str, python_executable: str) -> tuple[LaunchMethod, dict[str, Any]]:
    """
    Detect the specific launch method based on executable path and environment.

    Returns:
        Tuple of (LaunchMethod, details_dict)
    """
    details = {}

    # Check if we're running from a PSPF package
    if _is_pspf_launch(python_executable):
        details.update(_get_pspf_details())
        return LaunchMethod.PSPF_PACKAGE, details

    # Check if we're running as a Python module
    if _is_module_launch():
        details["module_name"] = _get_module_name()
        details["launch_command"] = " ".join(sys.argv)
        return LaunchMethod.SCRIPT_MODULE, details

    # Check if we're running from an editable install
    if _is_editable_install(executable_path):
        details.update(_get_editable_install_details(executable_path))
        return LaunchMethod.EDITABLE_INSTALL, details

    # Check if we're running as a direct script
    if _is_direct_script_launch(executable_path):
        details["script_path"] = executable_path
        details["is_symlink"] = Path(executable_path).is_symlink()
        return LaunchMethod.SCRIPT_DIRECT, details

    # Unknown launch method
    details["reason"] = "Could not determine launch method"
    details["executable_analysis"] = _analyze_executable(executable_path)
    return LaunchMethod.UNKNOWN, details


def x__detect_launch_method__mutmut_5(executable_path: str, python_executable: str) -> tuple[LaunchMethod, dict[str, Any]]:
    """
    Detect the specific launch method based on executable path and environment.

    Returns:
        Tuple of (LaunchMethod, details_dict)
    """
    details = {}

    # Check if we're running from a PSPF package
    if _is_pspf_launch(executable_path, ):
        details.update(_get_pspf_details())
        return LaunchMethod.PSPF_PACKAGE, details

    # Check if we're running as a Python module
    if _is_module_launch():
        details["module_name"] = _get_module_name()
        details["launch_command"] = " ".join(sys.argv)
        return LaunchMethod.SCRIPT_MODULE, details

    # Check if we're running from an editable install
    if _is_editable_install(executable_path):
        details.update(_get_editable_install_details(executable_path))
        return LaunchMethod.EDITABLE_INSTALL, details

    # Check if we're running as a direct script
    if _is_direct_script_launch(executable_path):
        details["script_path"] = executable_path
        details["is_symlink"] = Path(executable_path).is_symlink()
        return LaunchMethod.SCRIPT_DIRECT, details

    # Unknown launch method
    details["reason"] = "Could not determine launch method"
    details["executable_analysis"] = _analyze_executable(executable_path)
    return LaunchMethod.UNKNOWN, details


def x__detect_launch_method__mutmut_6(executable_path: str, python_executable: str) -> tuple[LaunchMethod, dict[str, Any]]:
    """
    Detect the specific launch method based on executable path and environment.

    Returns:
        Tuple of (LaunchMethod, details_dict)
    """
    details = {}

    # Check if we're running from a PSPF package
    if _is_pspf_launch(executable_path, python_executable):
        details.update(None)
        return LaunchMethod.PSPF_PACKAGE, details

    # Check if we're running as a Python module
    if _is_module_launch():
        details["module_name"] = _get_module_name()
        details["launch_command"] = " ".join(sys.argv)
        return LaunchMethod.SCRIPT_MODULE, details

    # Check if we're running from an editable install
    if _is_editable_install(executable_path):
        details.update(_get_editable_install_details(executable_path))
        return LaunchMethod.EDITABLE_INSTALL, details

    # Check if we're running as a direct script
    if _is_direct_script_launch(executable_path):
        details["script_path"] = executable_path
        details["is_symlink"] = Path(executable_path).is_symlink()
        return LaunchMethod.SCRIPT_DIRECT, details

    # Unknown launch method
    details["reason"] = "Could not determine launch method"
    details["executable_analysis"] = _analyze_executable(executable_path)
    return LaunchMethod.UNKNOWN, details


def x__detect_launch_method__mutmut_7(executable_path: str, python_executable: str) -> tuple[LaunchMethod, dict[str, Any]]:
    """
    Detect the specific launch method based on executable path and environment.

    Returns:
        Tuple of (LaunchMethod, details_dict)
    """
    details = {}

    # Check if we're running from a PSPF package
    if _is_pspf_launch(executable_path, python_executable):
        details.update(_get_pspf_details())
        return LaunchMethod.PSPF_PACKAGE, details

    # Check if we're running as a Python module
    if _is_module_launch():
        details["module_name"] = None
        details["launch_command"] = " ".join(sys.argv)
        return LaunchMethod.SCRIPT_MODULE, details

    # Check if we're running from an editable install
    if _is_editable_install(executable_path):
        details.update(_get_editable_install_details(executable_path))
        return LaunchMethod.EDITABLE_INSTALL, details

    # Check if we're running as a direct script
    if _is_direct_script_launch(executable_path):
        details["script_path"] = executable_path
        details["is_symlink"] = Path(executable_path).is_symlink()
        return LaunchMethod.SCRIPT_DIRECT, details

    # Unknown launch method
    details["reason"] = "Could not determine launch method"
    details["executable_analysis"] = _analyze_executable(executable_path)
    return LaunchMethod.UNKNOWN, details


def x__detect_launch_method__mutmut_8(executable_path: str, python_executable: str) -> tuple[LaunchMethod, dict[str, Any]]:
    """
    Detect the specific launch method based on executable path and environment.

    Returns:
        Tuple of (LaunchMethod, details_dict)
    """
    details = {}

    # Check if we're running from a PSPF package
    if _is_pspf_launch(executable_path, python_executable):
        details.update(_get_pspf_details())
        return LaunchMethod.PSPF_PACKAGE, details

    # Check if we're running as a Python module
    if _is_module_launch():
        details["XXmodule_nameXX"] = _get_module_name()
        details["launch_command"] = " ".join(sys.argv)
        return LaunchMethod.SCRIPT_MODULE, details

    # Check if we're running from an editable install
    if _is_editable_install(executable_path):
        details.update(_get_editable_install_details(executable_path))
        return LaunchMethod.EDITABLE_INSTALL, details

    # Check if we're running as a direct script
    if _is_direct_script_launch(executable_path):
        details["script_path"] = executable_path
        details["is_symlink"] = Path(executable_path).is_symlink()
        return LaunchMethod.SCRIPT_DIRECT, details

    # Unknown launch method
    details["reason"] = "Could not determine launch method"
    details["executable_analysis"] = _analyze_executable(executable_path)
    return LaunchMethod.UNKNOWN, details


def x__detect_launch_method__mutmut_9(executable_path: str, python_executable: str) -> tuple[LaunchMethod, dict[str, Any]]:
    """
    Detect the specific launch method based on executable path and environment.

    Returns:
        Tuple of (LaunchMethod, details_dict)
    """
    details = {}

    # Check if we're running from a PSPF package
    if _is_pspf_launch(executable_path, python_executable):
        details.update(_get_pspf_details())
        return LaunchMethod.PSPF_PACKAGE, details

    # Check if we're running as a Python module
    if _is_module_launch():
        details["MODULE_NAME"] = _get_module_name()
        details["launch_command"] = " ".join(sys.argv)
        return LaunchMethod.SCRIPT_MODULE, details

    # Check if we're running from an editable install
    if _is_editable_install(executable_path):
        details.update(_get_editable_install_details(executable_path))
        return LaunchMethod.EDITABLE_INSTALL, details

    # Check if we're running as a direct script
    if _is_direct_script_launch(executable_path):
        details["script_path"] = executable_path
        details["is_symlink"] = Path(executable_path).is_symlink()
        return LaunchMethod.SCRIPT_DIRECT, details

    # Unknown launch method
    details["reason"] = "Could not determine launch method"
    details["executable_analysis"] = _analyze_executable(executable_path)
    return LaunchMethod.UNKNOWN, details


def x__detect_launch_method__mutmut_10(executable_path: str, python_executable: str) -> tuple[LaunchMethod, dict[str, Any]]:
    """
    Detect the specific launch method based on executable path and environment.

    Returns:
        Tuple of (LaunchMethod, details_dict)
    """
    details = {}

    # Check if we're running from a PSPF package
    if _is_pspf_launch(executable_path, python_executable):
        details.update(_get_pspf_details())
        return LaunchMethod.PSPF_PACKAGE, details

    # Check if we're running as a Python module
    if _is_module_launch():
        details["module_name"] = _get_module_name()
        details["launch_command"] = None
        return LaunchMethod.SCRIPT_MODULE, details

    # Check if we're running from an editable install
    if _is_editable_install(executable_path):
        details.update(_get_editable_install_details(executable_path))
        return LaunchMethod.EDITABLE_INSTALL, details

    # Check if we're running as a direct script
    if _is_direct_script_launch(executable_path):
        details["script_path"] = executable_path
        details["is_symlink"] = Path(executable_path).is_symlink()
        return LaunchMethod.SCRIPT_DIRECT, details

    # Unknown launch method
    details["reason"] = "Could not determine launch method"
    details["executable_analysis"] = _analyze_executable(executable_path)
    return LaunchMethod.UNKNOWN, details


def x__detect_launch_method__mutmut_11(executable_path: str, python_executable: str) -> tuple[LaunchMethod, dict[str, Any]]:
    """
    Detect the specific launch method based on executable path and environment.

    Returns:
        Tuple of (LaunchMethod, details_dict)
    """
    details = {}

    # Check if we're running from a PSPF package
    if _is_pspf_launch(executable_path, python_executable):
        details.update(_get_pspf_details())
        return LaunchMethod.PSPF_PACKAGE, details

    # Check if we're running as a Python module
    if _is_module_launch():
        details["module_name"] = _get_module_name()
        details["XXlaunch_commandXX"] = " ".join(sys.argv)
        return LaunchMethod.SCRIPT_MODULE, details

    # Check if we're running from an editable install
    if _is_editable_install(executable_path):
        details.update(_get_editable_install_details(executable_path))
        return LaunchMethod.EDITABLE_INSTALL, details

    # Check if we're running as a direct script
    if _is_direct_script_launch(executable_path):
        details["script_path"] = executable_path
        details["is_symlink"] = Path(executable_path).is_symlink()
        return LaunchMethod.SCRIPT_DIRECT, details

    # Unknown launch method
    details["reason"] = "Could not determine launch method"
    details["executable_analysis"] = _analyze_executable(executable_path)
    return LaunchMethod.UNKNOWN, details


def x__detect_launch_method__mutmut_12(executable_path: str, python_executable: str) -> tuple[LaunchMethod, dict[str, Any]]:
    """
    Detect the specific launch method based on executable path and environment.

    Returns:
        Tuple of (LaunchMethod, details_dict)
    """
    details = {}

    # Check if we're running from a PSPF package
    if _is_pspf_launch(executable_path, python_executable):
        details.update(_get_pspf_details())
        return LaunchMethod.PSPF_PACKAGE, details

    # Check if we're running as a Python module
    if _is_module_launch():
        details["module_name"] = _get_module_name()
        details["LAUNCH_COMMAND"] = " ".join(sys.argv)
        return LaunchMethod.SCRIPT_MODULE, details

    # Check if we're running from an editable install
    if _is_editable_install(executable_path):
        details.update(_get_editable_install_details(executable_path))
        return LaunchMethod.EDITABLE_INSTALL, details

    # Check if we're running as a direct script
    if _is_direct_script_launch(executable_path):
        details["script_path"] = executable_path
        details["is_symlink"] = Path(executable_path).is_symlink()
        return LaunchMethod.SCRIPT_DIRECT, details

    # Unknown launch method
    details["reason"] = "Could not determine launch method"
    details["executable_analysis"] = _analyze_executable(executable_path)
    return LaunchMethod.UNKNOWN, details


def x__detect_launch_method__mutmut_13(executable_path: str, python_executable: str) -> tuple[LaunchMethod, dict[str, Any]]:
    """
    Detect the specific launch method based on executable path and environment.

    Returns:
        Tuple of (LaunchMethod, details_dict)
    """
    details = {}

    # Check if we're running from a PSPF package
    if _is_pspf_launch(executable_path, python_executable):
        details.update(_get_pspf_details())
        return LaunchMethod.PSPF_PACKAGE, details

    # Check if we're running as a Python module
    if _is_module_launch():
        details["module_name"] = _get_module_name()
        details["launch_command"] = " ".join(None)
        return LaunchMethod.SCRIPT_MODULE, details

    # Check if we're running from an editable install
    if _is_editable_install(executable_path):
        details.update(_get_editable_install_details(executable_path))
        return LaunchMethod.EDITABLE_INSTALL, details

    # Check if we're running as a direct script
    if _is_direct_script_launch(executable_path):
        details["script_path"] = executable_path
        details["is_symlink"] = Path(executable_path).is_symlink()
        return LaunchMethod.SCRIPT_DIRECT, details

    # Unknown launch method
    details["reason"] = "Could not determine launch method"
    details["executable_analysis"] = _analyze_executable(executable_path)
    return LaunchMethod.UNKNOWN, details


def x__detect_launch_method__mutmut_14(executable_path: str, python_executable: str) -> tuple[LaunchMethod, dict[str, Any]]:
    """
    Detect the specific launch method based on executable path and environment.

    Returns:
        Tuple of (LaunchMethod, details_dict)
    """
    details = {}

    # Check if we're running from a PSPF package
    if _is_pspf_launch(executable_path, python_executable):
        details.update(_get_pspf_details())
        return LaunchMethod.PSPF_PACKAGE, details

    # Check if we're running as a Python module
    if _is_module_launch():
        details["module_name"] = _get_module_name()
        details["launch_command"] = "XX XX".join(sys.argv)
        return LaunchMethod.SCRIPT_MODULE, details

    # Check if we're running from an editable install
    if _is_editable_install(executable_path):
        details.update(_get_editable_install_details(executable_path))
        return LaunchMethod.EDITABLE_INSTALL, details

    # Check if we're running as a direct script
    if _is_direct_script_launch(executable_path):
        details["script_path"] = executable_path
        details["is_symlink"] = Path(executable_path).is_symlink()
        return LaunchMethod.SCRIPT_DIRECT, details

    # Unknown launch method
    details["reason"] = "Could not determine launch method"
    details["executable_analysis"] = _analyze_executable(executable_path)
    return LaunchMethod.UNKNOWN, details


def x__detect_launch_method__mutmut_15(executable_path: str, python_executable: str) -> tuple[LaunchMethod, dict[str, Any]]:
    """
    Detect the specific launch method based on executable path and environment.

    Returns:
        Tuple of (LaunchMethod, details_dict)
    """
    details = {}

    # Check if we're running from a PSPF package
    if _is_pspf_launch(executable_path, python_executable):
        details.update(_get_pspf_details())
        return LaunchMethod.PSPF_PACKAGE, details

    # Check if we're running as a Python module
    if _is_module_launch():
        details["module_name"] = _get_module_name()
        details["launch_command"] = " ".join(sys.argv)
        return LaunchMethod.SCRIPT_MODULE, details

    # Check if we're running from an editable install
    if _is_editable_install(None):
        details.update(_get_editable_install_details(executable_path))
        return LaunchMethod.EDITABLE_INSTALL, details

    # Check if we're running as a direct script
    if _is_direct_script_launch(executable_path):
        details["script_path"] = executable_path
        details["is_symlink"] = Path(executable_path).is_symlink()
        return LaunchMethod.SCRIPT_DIRECT, details

    # Unknown launch method
    details["reason"] = "Could not determine launch method"
    details["executable_analysis"] = _analyze_executable(executable_path)
    return LaunchMethod.UNKNOWN, details


def x__detect_launch_method__mutmut_16(executable_path: str, python_executable: str) -> tuple[LaunchMethod, dict[str, Any]]:
    """
    Detect the specific launch method based on executable path and environment.

    Returns:
        Tuple of (LaunchMethod, details_dict)
    """
    details = {}

    # Check if we're running from a PSPF package
    if _is_pspf_launch(executable_path, python_executable):
        details.update(_get_pspf_details())
        return LaunchMethod.PSPF_PACKAGE, details

    # Check if we're running as a Python module
    if _is_module_launch():
        details["module_name"] = _get_module_name()
        details["launch_command"] = " ".join(sys.argv)
        return LaunchMethod.SCRIPT_MODULE, details

    # Check if we're running from an editable install
    if _is_editable_install(executable_path):
        details.update(None)
        return LaunchMethod.EDITABLE_INSTALL, details

    # Check if we're running as a direct script
    if _is_direct_script_launch(executable_path):
        details["script_path"] = executable_path
        details["is_symlink"] = Path(executable_path).is_symlink()
        return LaunchMethod.SCRIPT_DIRECT, details

    # Unknown launch method
    details["reason"] = "Could not determine launch method"
    details["executable_analysis"] = _analyze_executable(executable_path)
    return LaunchMethod.UNKNOWN, details


def x__detect_launch_method__mutmut_17(executable_path: str, python_executable: str) -> tuple[LaunchMethod, dict[str, Any]]:
    """
    Detect the specific launch method based on executable path and environment.

    Returns:
        Tuple of (LaunchMethod, details_dict)
    """
    details = {}

    # Check if we're running from a PSPF package
    if _is_pspf_launch(executable_path, python_executable):
        details.update(_get_pspf_details())
        return LaunchMethod.PSPF_PACKAGE, details

    # Check if we're running as a Python module
    if _is_module_launch():
        details["module_name"] = _get_module_name()
        details["launch_command"] = " ".join(sys.argv)
        return LaunchMethod.SCRIPT_MODULE, details

    # Check if we're running from an editable install
    if _is_editable_install(executable_path):
        details.update(_get_editable_install_details(None))
        return LaunchMethod.EDITABLE_INSTALL, details

    # Check if we're running as a direct script
    if _is_direct_script_launch(executable_path):
        details["script_path"] = executable_path
        details["is_symlink"] = Path(executable_path).is_symlink()
        return LaunchMethod.SCRIPT_DIRECT, details

    # Unknown launch method
    details["reason"] = "Could not determine launch method"
    details["executable_analysis"] = _analyze_executable(executable_path)
    return LaunchMethod.UNKNOWN, details


def x__detect_launch_method__mutmut_18(executable_path: str, python_executable: str) -> tuple[LaunchMethod, dict[str, Any]]:
    """
    Detect the specific launch method based on executable path and environment.

    Returns:
        Tuple of (LaunchMethod, details_dict)
    """
    details = {}

    # Check if we're running from a PSPF package
    if _is_pspf_launch(executable_path, python_executable):
        details.update(_get_pspf_details())
        return LaunchMethod.PSPF_PACKAGE, details

    # Check if we're running as a Python module
    if _is_module_launch():
        details["module_name"] = _get_module_name()
        details["launch_command"] = " ".join(sys.argv)
        return LaunchMethod.SCRIPT_MODULE, details

    # Check if we're running from an editable install
    if _is_editable_install(executable_path):
        details.update(_get_editable_install_details(executable_path))
        return LaunchMethod.EDITABLE_INSTALL, details

    # Check if we're running as a direct script
    if _is_direct_script_launch(None):
        details["script_path"] = executable_path
        details["is_symlink"] = Path(executable_path).is_symlink()
        return LaunchMethod.SCRIPT_DIRECT, details

    # Unknown launch method
    details["reason"] = "Could not determine launch method"
    details["executable_analysis"] = _analyze_executable(executable_path)
    return LaunchMethod.UNKNOWN, details


def x__detect_launch_method__mutmut_19(executable_path: str, python_executable: str) -> tuple[LaunchMethod, dict[str, Any]]:
    """
    Detect the specific launch method based on executable path and environment.

    Returns:
        Tuple of (LaunchMethod, details_dict)
    """
    details = {}

    # Check if we're running from a PSPF package
    if _is_pspf_launch(executable_path, python_executable):
        details.update(_get_pspf_details())
        return LaunchMethod.PSPF_PACKAGE, details

    # Check if we're running as a Python module
    if _is_module_launch():
        details["module_name"] = _get_module_name()
        details["launch_command"] = " ".join(sys.argv)
        return LaunchMethod.SCRIPT_MODULE, details

    # Check if we're running from an editable install
    if _is_editable_install(executable_path):
        details.update(_get_editable_install_details(executable_path))
        return LaunchMethod.EDITABLE_INSTALL, details

    # Check if we're running as a direct script
    if _is_direct_script_launch(executable_path):
        details["script_path"] = None
        details["is_symlink"] = Path(executable_path).is_symlink()
        return LaunchMethod.SCRIPT_DIRECT, details

    # Unknown launch method
    details["reason"] = "Could not determine launch method"
    details["executable_analysis"] = _analyze_executable(executable_path)
    return LaunchMethod.UNKNOWN, details


def x__detect_launch_method__mutmut_20(executable_path: str, python_executable: str) -> tuple[LaunchMethod, dict[str, Any]]:
    """
    Detect the specific launch method based on executable path and environment.

    Returns:
        Tuple of (LaunchMethod, details_dict)
    """
    details = {}

    # Check if we're running from a PSPF package
    if _is_pspf_launch(executable_path, python_executable):
        details.update(_get_pspf_details())
        return LaunchMethod.PSPF_PACKAGE, details

    # Check if we're running as a Python module
    if _is_module_launch():
        details["module_name"] = _get_module_name()
        details["launch_command"] = " ".join(sys.argv)
        return LaunchMethod.SCRIPT_MODULE, details

    # Check if we're running from an editable install
    if _is_editable_install(executable_path):
        details.update(_get_editable_install_details(executable_path))
        return LaunchMethod.EDITABLE_INSTALL, details

    # Check if we're running as a direct script
    if _is_direct_script_launch(executable_path):
        details["XXscript_pathXX"] = executable_path
        details["is_symlink"] = Path(executable_path).is_symlink()
        return LaunchMethod.SCRIPT_DIRECT, details

    # Unknown launch method
    details["reason"] = "Could not determine launch method"
    details["executable_analysis"] = _analyze_executable(executable_path)
    return LaunchMethod.UNKNOWN, details


def x__detect_launch_method__mutmut_21(executable_path: str, python_executable: str) -> tuple[LaunchMethod, dict[str, Any]]:
    """
    Detect the specific launch method based on executable path and environment.

    Returns:
        Tuple of (LaunchMethod, details_dict)
    """
    details = {}

    # Check if we're running from a PSPF package
    if _is_pspf_launch(executable_path, python_executable):
        details.update(_get_pspf_details())
        return LaunchMethod.PSPF_PACKAGE, details

    # Check if we're running as a Python module
    if _is_module_launch():
        details["module_name"] = _get_module_name()
        details["launch_command"] = " ".join(sys.argv)
        return LaunchMethod.SCRIPT_MODULE, details

    # Check if we're running from an editable install
    if _is_editable_install(executable_path):
        details.update(_get_editable_install_details(executable_path))
        return LaunchMethod.EDITABLE_INSTALL, details

    # Check if we're running as a direct script
    if _is_direct_script_launch(executable_path):
        details["SCRIPT_PATH"] = executable_path
        details["is_symlink"] = Path(executable_path).is_symlink()
        return LaunchMethod.SCRIPT_DIRECT, details

    # Unknown launch method
    details["reason"] = "Could not determine launch method"
    details["executable_analysis"] = _analyze_executable(executable_path)
    return LaunchMethod.UNKNOWN, details


def x__detect_launch_method__mutmut_22(executable_path: str, python_executable: str) -> tuple[LaunchMethod, dict[str, Any]]:
    """
    Detect the specific launch method based on executable path and environment.

    Returns:
        Tuple of (LaunchMethod, details_dict)
    """
    details = {}

    # Check if we're running from a PSPF package
    if _is_pspf_launch(executable_path, python_executable):
        details.update(_get_pspf_details())
        return LaunchMethod.PSPF_PACKAGE, details

    # Check if we're running as a Python module
    if _is_module_launch():
        details["module_name"] = _get_module_name()
        details["launch_command"] = " ".join(sys.argv)
        return LaunchMethod.SCRIPT_MODULE, details

    # Check if we're running from an editable install
    if _is_editable_install(executable_path):
        details.update(_get_editable_install_details(executable_path))
        return LaunchMethod.EDITABLE_INSTALL, details

    # Check if we're running as a direct script
    if _is_direct_script_launch(executable_path):
        details["script_path"] = executable_path
        details["is_symlink"] = None
        return LaunchMethod.SCRIPT_DIRECT, details

    # Unknown launch method
    details["reason"] = "Could not determine launch method"
    details["executable_analysis"] = _analyze_executable(executable_path)
    return LaunchMethod.UNKNOWN, details


def x__detect_launch_method__mutmut_23(executable_path: str, python_executable: str) -> tuple[LaunchMethod, dict[str, Any]]:
    """
    Detect the specific launch method based on executable path and environment.

    Returns:
        Tuple of (LaunchMethod, details_dict)
    """
    details = {}

    # Check if we're running from a PSPF package
    if _is_pspf_launch(executable_path, python_executable):
        details.update(_get_pspf_details())
        return LaunchMethod.PSPF_PACKAGE, details

    # Check if we're running as a Python module
    if _is_module_launch():
        details["module_name"] = _get_module_name()
        details["launch_command"] = " ".join(sys.argv)
        return LaunchMethod.SCRIPT_MODULE, details

    # Check if we're running from an editable install
    if _is_editable_install(executable_path):
        details.update(_get_editable_install_details(executable_path))
        return LaunchMethod.EDITABLE_INSTALL, details

    # Check if we're running as a direct script
    if _is_direct_script_launch(executable_path):
        details["script_path"] = executable_path
        details["XXis_symlinkXX"] = Path(executable_path).is_symlink()
        return LaunchMethod.SCRIPT_DIRECT, details

    # Unknown launch method
    details["reason"] = "Could not determine launch method"
    details["executable_analysis"] = _analyze_executable(executable_path)
    return LaunchMethod.UNKNOWN, details


def x__detect_launch_method__mutmut_24(executable_path: str, python_executable: str) -> tuple[LaunchMethod, dict[str, Any]]:
    """
    Detect the specific launch method based on executable path and environment.

    Returns:
        Tuple of (LaunchMethod, details_dict)
    """
    details = {}

    # Check if we're running from a PSPF package
    if _is_pspf_launch(executable_path, python_executable):
        details.update(_get_pspf_details())
        return LaunchMethod.PSPF_PACKAGE, details

    # Check if we're running as a Python module
    if _is_module_launch():
        details["module_name"] = _get_module_name()
        details["launch_command"] = " ".join(sys.argv)
        return LaunchMethod.SCRIPT_MODULE, details

    # Check if we're running from an editable install
    if _is_editable_install(executable_path):
        details.update(_get_editable_install_details(executable_path))
        return LaunchMethod.EDITABLE_INSTALL, details

    # Check if we're running as a direct script
    if _is_direct_script_launch(executable_path):
        details["script_path"] = executable_path
        details["IS_SYMLINK"] = Path(executable_path).is_symlink()
        return LaunchMethod.SCRIPT_DIRECT, details

    # Unknown launch method
    details["reason"] = "Could not determine launch method"
    details["executable_analysis"] = _analyze_executable(executable_path)
    return LaunchMethod.UNKNOWN, details


def x__detect_launch_method__mutmut_25(executable_path: str, python_executable: str) -> tuple[LaunchMethod, dict[str, Any]]:
    """
    Detect the specific launch method based on executable path and environment.

    Returns:
        Tuple of (LaunchMethod, details_dict)
    """
    details = {}

    # Check if we're running from a PSPF package
    if _is_pspf_launch(executable_path, python_executable):
        details.update(_get_pspf_details())
        return LaunchMethod.PSPF_PACKAGE, details

    # Check if we're running as a Python module
    if _is_module_launch():
        details["module_name"] = _get_module_name()
        details["launch_command"] = " ".join(sys.argv)
        return LaunchMethod.SCRIPT_MODULE, details

    # Check if we're running from an editable install
    if _is_editable_install(executable_path):
        details.update(_get_editable_install_details(executable_path))
        return LaunchMethod.EDITABLE_INSTALL, details

    # Check if we're running as a direct script
    if _is_direct_script_launch(executable_path):
        details["script_path"] = executable_path
        details["is_symlink"] = Path(None).is_symlink()
        return LaunchMethod.SCRIPT_DIRECT, details

    # Unknown launch method
    details["reason"] = "Could not determine launch method"
    details["executable_analysis"] = _analyze_executable(executable_path)
    return LaunchMethod.UNKNOWN, details


def x__detect_launch_method__mutmut_26(executable_path: str, python_executable: str) -> tuple[LaunchMethod, dict[str, Any]]:
    """
    Detect the specific launch method based on executable path and environment.

    Returns:
        Tuple of (LaunchMethod, details_dict)
    """
    details = {}

    # Check if we're running from a PSPF package
    if _is_pspf_launch(executable_path, python_executable):
        details.update(_get_pspf_details())
        return LaunchMethod.PSPF_PACKAGE, details

    # Check if we're running as a Python module
    if _is_module_launch():
        details["module_name"] = _get_module_name()
        details["launch_command"] = " ".join(sys.argv)
        return LaunchMethod.SCRIPT_MODULE, details

    # Check if we're running from an editable install
    if _is_editable_install(executable_path):
        details.update(_get_editable_install_details(executable_path))
        return LaunchMethod.EDITABLE_INSTALL, details

    # Check if we're running as a direct script
    if _is_direct_script_launch(executable_path):
        details["script_path"] = executable_path
        details["is_symlink"] = Path(executable_path).is_symlink()
        return LaunchMethod.SCRIPT_DIRECT, details

    # Unknown launch method
    details["reason"] = None
    details["executable_analysis"] = _analyze_executable(executable_path)
    return LaunchMethod.UNKNOWN, details


def x__detect_launch_method__mutmut_27(executable_path: str, python_executable: str) -> tuple[LaunchMethod, dict[str, Any]]:
    """
    Detect the specific launch method based on executable path and environment.

    Returns:
        Tuple of (LaunchMethod, details_dict)
    """
    details = {}

    # Check if we're running from a PSPF package
    if _is_pspf_launch(executable_path, python_executable):
        details.update(_get_pspf_details())
        return LaunchMethod.PSPF_PACKAGE, details

    # Check if we're running as a Python module
    if _is_module_launch():
        details["module_name"] = _get_module_name()
        details["launch_command"] = " ".join(sys.argv)
        return LaunchMethod.SCRIPT_MODULE, details

    # Check if we're running from an editable install
    if _is_editable_install(executable_path):
        details.update(_get_editable_install_details(executable_path))
        return LaunchMethod.EDITABLE_INSTALL, details

    # Check if we're running as a direct script
    if _is_direct_script_launch(executable_path):
        details["script_path"] = executable_path
        details["is_symlink"] = Path(executable_path).is_symlink()
        return LaunchMethod.SCRIPT_DIRECT, details

    # Unknown launch method
    details["XXreasonXX"] = "Could not determine launch method"
    details["executable_analysis"] = _analyze_executable(executable_path)
    return LaunchMethod.UNKNOWN, details


def x__detect_launch_method__mutmut_28(executable_path: str, python_executable: str) -> tuple[LaunchMethod, dict[str, Any]]:
    """
    Detect the specific launch method based on executable path and environment.

    Returns:
        Tuple of (LaunchMethod, details_dict)
    """
    details = {}

    # Check if we're running from a PSPF package
    if _is_pspf_launch(executable_path, python_executable):
        details.update(_get_pspf_details())
        return LaunchMethod.PSPF_PACKAGE, details

    # Check if we're running as a Python module
    if _is_module_launch():
        details["module_name"] = _get_module_name()
        details["launch_command"] = " ".join(sys.argv)
        return LaunchMethod.SCRIPT_MODULE, details

    # Check if we're running from an editable install
    if _is_editable_install(executable_path):
        details.update(_get_editable_install_details(executable_path))
        return LaunchMethod.EDITABLE_INSTALL, details

    # Check if we're running as a direct script
    if _is_direct_script_launch(executable_path):
        details["script_path"] = executable_path
        details["is_symlink"] = Path(executable_path).is_symlink()
        return LaunchMethod.SCRIPT_DIRECT, details

    # Unknown launch method
    details["REASON"] = "Could not determine launch method"
    details["executable_analysis"] = _analyze_executable(executable_path)
    return LaunchMethod.UNKNOWN, details


def x__detect_launch_method__mutmut_29(executable_path: str, python_executable: str) -> tuple[LaunchMethod, dict[str, Any]]:
    """
    Detect the specific launch method based on executable path and environment.

    Returns:
        Tuple of (LaunchMethod, details_dict)
    """
    details = {}

    # Check if we're running from a PSPF package
    if _is_pspf_launch(executable_path, python_executable):
        details.update(_get_pspf_details())
        return LaunchMethod.PSPF_PACKAGE, details

    # Check if we're running as a Python module
    if _is_module_launch():
        details["module_name"] = _get_module_name()
        details["launch_command"] = " ".join(sys.argv)
        return LaunchMethod.SCRIPT_MODULE, details

    # Check if we're running from an editable install
    if _is_editable_install(executable_path):
        details.update(_get_editable_install_details(executable_path))
        return LaunchMethod.EDITABLE_INSTALL, details

    # Check if we're running as a direct script
    if _is_direct_script_launch(executable_path):
        details["script_path"] = executable_path
        details["is_symlink"] = Path(executable_path).is_symlink()
        return LaunchMethod.SCRIPT_DIRECT, details

    # Unknown launch method
    details["reason"] = "XXCould not determine launch methodXX"
    details["executable_analysis"] = _analyze_executable(executable_path)
    return LaunchMethod.UNKNOWN, details


def x__detect_launch_method__mutmut_30(executable_path: str, python_executable: str) -> tuple[LaunchMethod, dict[str, Any]]:
    """
    Detect the specific launch method based on executable path and environment.

    Returns:
        Tuple of (LaunchMethod, details_dict)
    """
    details = {}

    # Check if we're running from a PSPF package
    if _is_pspf_launch(executable_path, python_executable):
        details.update(_get_pspf_details())
        return LaunchMethod.PSPF_PACKAGE, details

    # Check if we're running as a Python module
    if _is_module_launch():
        details["module_name"] = _get_module_name()
        details["launch_command"] = " ".join(sys.argv)
        return LaunchMethod.SCRIPT_MODULE, details

    # Check if we're running from an editable install
    if _is_editable_install(executable_path):
        details.update(_get_editable_install_details(executable_path))
        return LaunchMethod.EDITABLE_INSTALL, details

    # Check if we're running as a direct script
    if _is_direct_script_launch(executable_path):
        details["script_path"] = executable_path
        details["is_symlink"] = Path(executable_path).is_symlink()
        return LaunchMethod.SCRIPT_DIRECT, details

    # Unknown launch method
    details["reason"] = "could not determine launch method"
    details["executable_analysis"] = _analyze_executable(executable_path)
    return LaunchMethod.UNKNOWN, details


def x__detect_launch_method__mutmut_31(executable_path: str, python_executable: str) -> tuple[LaunchMethod, dict[str, Any]]:
    """
    Detect the specific launch method based on executable path and environment.

    Returns:
        Tuple of (LaunchMethod, details_dict)
    """
    details = {}

    # Check if we're running from a PSPF package
    if _is_pspf_launch(executable_path, python_executable):
        details.update(_get_pspf_details())
        return LaunchMethod.PSPF_PACKAGE, details

    # Check if we're running as a Python module
    if _is_module_launch():
        details["module_name"] = _get_module_name()
        details["launch_command"] = " ".join(sys.argv)
        return LaunchMethod.SCRIPT_MODULE, details

    # Check if we're running from an editable install
    if _is_editable_install(executable_path):
        details.update(_get_editable_install_details(executable_path))
        return LaunchMethod.EDITABLE_INSTALL, details

    # Check if we're running as a direct script
    if _is_direct_script_launch(executable_path):
        details["script_path"] = executable_path
        details["is_symlink"] = Path(executable_path).is_symlink()
        return LaunchMethod.SCRIPT_DIRECT, details

    # Unknown launch method
    details["reason"] = "COULD NOT DETERMINE LAUNCH METHOD"
    details["executable_analysis"] = _analyze_executable(executable_path)
    return LaunchMethod.UNKNOWN, details


def x__detect_launch_method__mutmut_32(executable_path: str, python_executable: str) -> tuple[LaunchMethod, dict[str, Any]]:
    """
    Detect the specific launch method based on executable path and environment.

    Returns:
        Tuple of (LaunchMethod, details_dict)
    """
    details = {}

    # Check if we're running from a PSPF package
    if _is_pspf_launch(executable_path, python_executable):
        details.update(_get_pspf_details())
        return LaunchMethod.PSPF_PACKAGE, details

    # Check if we're running as a Python module
    if _is_module_launch():
        details["module_name"] = _get_module_name()
        details["launch_command"] = " ".join(sys.argv)
        return LaunchMethod.SCRIPT_MODULE, details

    # Check if we're running from an editable install
    if _is_editable_install(executable_path):
        details.update(_get_editable_install_details(executable_path))
        return LaunchMethod.EDITABLE_INSTALL, details

    # Check if we're running as a direct script
    if _is_direct_script_launch(executable_path):
        details["script_path"] = executable_path
        details["is_symlink"] = Path(executable_path).is_symlink()
        return LaunchMethod.SCRIPT_DIRECT, details

    # Unknown launch method
    details["reason"] = "Could not determine launch method"
    details["executable_analysis"] = None
    return LaunchMethod.UNKNOWN, details


def x__detect_launch_method__mutmut_33(executable_path: str, python_executable: str) -> tuple[LaunchMethod, dict[str, Any]]:
    """
    Detect the specific launch method based on executable path and environment.

    Returns:
        Tuple of (LaunchMethod, details_dict)
    """
    details = {}

    # Check if we're running from a PSPF package
    if _is_pspf_launch(executable_path, python_executable):
        details.update(_get_pspf_details())
        return LaunchMethod.PSPF_PACKAGE, details

    # Check if we're running as a Python module
    if _is_module_launch():
        details["module_name"] = _get_module_name()
        details["launch_command"] = " ".join(sys.argv)
        return LaunchMethod.SCRIPT_MODULE, details

    # Check if we're running from an editable install
    if _is_editable_install(executable_path):
        details.update(_get_editable_install_details(executable_path))
        return LaunchMethod.EDITABLE_INSTALL, details

    # Check if we're running as a direct script
    if _is_direct_script_launch(executable_path):
        details["script_path"] = executable_path
        details["is_symlink"] = Path(executable_path).is_symlink()
        return LaunchMethod.SCRIPT_DIRECT, details

    # Unknown launch method
    details["reason"] = "Could not determine launch method"
    details["XXexecutable_analysisXX"] = _analyze_executable(executable_path)
    return LaunchMethod.UNKNOWN, details


def x__detect_launch_method__mutmut_34(executable_path: str, python_executable: str) -> tuple[LaunchMethod, dict[str, Any]]:
    """
    Detect the specific launch method based on executable path and environment.

    Returns:
        Tuple of (LaunchMethod, details_dict)
    """
    details = {}

    # Check if we're running from a PSPF package
    if _is_pspf_launch(executable_path, python_executable):
        details.update(_get_pspf_details())
        return LaunchMethod.PSPF_PACKAGE, details

    # Check if we're running as a Python module
    if _is_module_launch():
        details["module_name"] = _get_module_name()
        details["launch_command"] = " ".join(sys.argv)
        return LaunchMethod.SCRIPT_MODULE, details

    # Check if we're running from an editable install
    if _is_editable_install(executable_path):
        details.update(_get_editable_install_details(executable_path))
        return LaunchMethod.EDITABLE_INSTALL, details

    # Check if we're running as a direct script
    if _is_direct_script_launch(executable_path):
        details["script_path"] = executable_path
        details["is_symlink"] = Path(executable_path).is_symlink()
        return LaunchMethod.SCRIPT_DIRECT, details

    # Unknown launch method
    details["reason"] = "Could not determine launch method"
    details["EXECUTABLE_ANALYSIS"] = _analyze_executable(executable_path)
    return LaunchMethod.UNKNOWN, details


def x__detect_launch_method__mutmut_35(executable_path: str, python_executable: str) -> tuple[LaunchMethod, dict[str, Any]]:
    """
    Detect the specific launch method based on executable path and environment.

    Returns:
        Tuple of (LaunchMethod, details_dict)
    """
    details = {}

    # Check if we're running from a PSPF package
    if _is_pspf_launch(executable_path, python_executable):
        details.update(_get_pspf_details())
        return LaunchMethod.PSPF_PACKAGE, details

    # Check if we're running as a Python module
    if _is_module_launch():
        details["module_name"] = _get_module_name()
        details["launch_command"] = " ".join(sys.argv)
        return LaunchMethod.SCRIPT_MODULE, details

    # Check if we're running from an editable install
    if _is_editable_install(executable_path):
        details.update(_get_editable_install_details(executable_path))
        return LaunchMethod.EDITABLE_INSTALL, details

    # Check if we're running as a direct script
    if _is_direct_script_launch(executable_path):
        details["script_path"] = executable_path
        details["is_symlink"] = Path(executable_path).is_symlink()
        return LaunchMethod.SCRIPT_DIRECT, details

    # Unknown launch method
    details["reason"] = "Could not determine launch method"
    details["executable_analysis"] = _analyze_executable(None)
    return LaunchMethod.UNKNOWN, details

x__detect_launch_method__mutmut_mutants : ClassVar[MutantDict] = {
'x__detect_launch_method__mutmut_1': x__detect_launch_method__mutmut_1, 
    'x__detect_launch_method__mutmut_2': x__detect_launch_method__mutmut_2, 
    'x__detect_launch_method__mutmut_3': x__detect_launch_method__mutmut_3, 
    'x__detect_launch_method__mutmut_4': x__detect_launch_method__mutmut_4, 
    'x__detect_launch_method__mutmut_5': x__detect_launch_method__mutmut_5, 
    'x__detect_launch_method__mutmut_6': x__detect_launch_method__mutmut_6, 
    'x__detect_launch_method__mutmut_7': x__detect_launch_method__mutmut_7, 
    'x__detect_launch_method__mutmut_8': x__detect_launch_method__mutmut_8, 
    'x__detect_launch_method__mutmut_9': x__detect_launch_method__mutmut_9, 
    'x__detect_launch_method__mutmut_10': x__detect_launch_method__mutmut_10, 
    'x__detect_launch_method__mutmut_11': x__detect_launch_method__mutmut_11, 
    'x__detect_launch_method__mutmut_12': x__detect_launch_method__mutmut_12, 
    'x__detect_launch_method__mutmut_13': x__detect_launch_method__mutmut_13, 
    'x__detect_launch_method__mutmut_14': x__detect_launch_method__mutmut_14, 
    'x__detect_launch_method__mutmut_15': x__detect_launch_method__mutmut_15, 
    'x__detect_launch_method__mutmut_16': x__detect_launch_method__mutmut_16, 
    'x__detect_launch_method__mutmut_17': x__detect_launch_method__mutmut_17, 
    'x__detect_launch_method__mutmut_18': x__detect_launch_method__mutmut_18, 
    'x__detect_launch_method__mutmut_19': x__detect_launch_method__mutmut_19, 
    'x__detect_launch_method__mutmut_20': x__detect_launch_method__mutmut_20, 
    'x__detect_launch_method__mutmut_21': x__detect_launch_method__mutmut_21, 
    'x__detect_launch_method__mutmut_22': x__detect_launch_method__mutmut_22, 
    'x__detect_launch_method__mutmut_23': x__detect_launch_method__mutmut_23, 
    'x__detect_launch_method__mutmut_24': x__detect_launch_method__mutmut_24, 
    'x__detect_launch_method__mutmut_25': x__detect_launch_method__mutmut_25, 
    'x__detect_launch_method__mutmut_26': x__detect_launch_method__mutmut_26, 
    'x__detect_launch_method__mutmut_27': x__detect_launch_method__mutmut_27, 
    'x__detect_launch_method__mutmut_28': x__detect_launch_method__mutmut_28, 
    'x__detect_launch_method__mutmut_29': x__detect_launch_method__mutmut_29, 
    'x__detect_launch_method__mutmut_30': x__detect_launch_method__mutmut_30, 
    'x__detect_launch_method__mutmut_31': x__detect_launch_method__mutmut_31, 
    'x__detect_launch_method__mutmut_32': x__detect_launch_method__mutmut_32, 
    'x__detect_launch_method__mutmut_33': x__detect_launch_method__mutmut_33, 
    'x__detect_launch_method__mutmut_34': x__detect_launch_method__mutmut_34, 
    'x__detect_launch_method__mutmut_35': x__detect_launch_method__mutmut_35
}

def _detect_launch_method(*args, **kwargs):
    result = _mutmut_trampoline(x__detect_launch_method__mutmut_orig, x__detect_launch_method__mutmut_mutants, args, kwargs)
    return result 

_detect_launch_method.__signature__ = _mutmut_signature(x__detect_launch_method__mutmut_orig)
x__detect_launch_method__mutmut_orig.__name__ = 'x__detect_launch_method'


def x__is_pspf_launch__mutmut_orig(executable_path: str, python_executable: str) -> bool:
    """Check if we're running from a PSPF package."""
    # PSPF packages typically have a cache directory structure
    cache_indicators = ["/.cache/pspf/", "/cache/bin/python", "/pspf_", "terraform-provider-"]

    # Check if Python is running from a cache-like directory
    for indicator in cache_indicators:
        if indicator in python_executable.lower():
            return True

    # Check if executable path suggests PSPF
    if any(indicator in executable_path.lower() for indicator in ["terraform-provider-", "pspf"]):
        # Additional check: see if we're in a temporary/cache directory structure
        python_path = Path(python_executable)
        if any(part in str(python_path) for part in [".cache", "cache", "temp"]):
            return True

    return False


def x__is_pspf_launch__mutmut_1(executable_path: str, python_executable: str) -> bool:
    """Check if we're running from a PSPF package."""
    # PSPF packages typically have a cache directory structure
    cache_indicators = None

    # Check if Python is running from a cache-like directory
    for indicator in cache_indicators:
        if indicator in python_executable.lower():
            return True

    # Check if executable path suggests PSPF
    if any(indicator in executable_path.lower() for indicator in ["terraform-provider-", "pspf"]):
        # Additional check: see if we're in a temporary/cache directory structure
        python_path = Path(python_executable)
        if any(part in str(python_path) for part in [".cache", "cache", "temp"]):
            return True

    return False


def x__is_pspf_launch__mutmut_2(executable_path: str, python_executable: str) -> bool:
    """Check if we're running from a PSPF package."""
    # PSPF packages typically have a cache directory structure
    cache_indicators = ["XX/.cache/pspf/XX", "/cache/bin/python", "/pspf_", "terraform-provider-"]

    # Check if Python is running from a cache-like directory
    for indicator in cache_indicators:
        if indicator in python_executable.lower():
            return True

    # Check if executable path suggests PSPF
    if any(indicator in executable_path.lower() for indicator in ["terraform-provider-", "pspf"]):
        # Additional check: see if we're in a temporary/cache directory structure
        python_path = Path(python_executable)
        if any(part in str(python_path) for part in [".cache", "cache", "temp"]):
            return True

    return False


def x__is_pspf_launch__mutmut_3(executable_path: str, python_executable: str) -> bool:
    """Check if we're running from a PSPF package."""
    # PSPF packages typically have a cache directory structure
    cache_indicators = ["/.CACHE/PSPF/", "/cache/bin/python", "/pspf_", "terraform-provider-"]

    # Check if Python is running from a cache-like directory
    for indicator in cache_indicators:
        if indicator in python_executable.lower():
            return True

    # Check if executable path suggests PSPF
    if any(indicator in executable_path.lower() for indicator in ["terraform-provider-", "pspf"]):
        # Additional check: see if we're in a temporary/cache directory structure
        python_path = Path(python_executable)
        if any(part in str(python_path) for part in [".cache", "cache", "temp"]):
            return True

    return False


def x__is_pspf_launch__mutmut_4(executable_path: str, python_executable: str) -> bool:
    """Check if we're running from a PSPF package."""
    # PSPF packages typically have a cache directory structure
    cache_indicators = ["/.cache/pspf/", "XX/cache/bin/pythonXX", "/pspf_", "terraform-provider-"]

    # Check if Python is running from a cache-like directory
    for indicator in cache_indicators:
        if indicator in python_executable.lower():
            return True

    # Check if executable path suggests PSPF
    if any(indicator in executable_path.lower() for indicator in ["terraform-provider-", "pspf"]):
        # Additional check: see if we're in a temporary/cache directory structure
        python_path = Path(python_executable)
        if any(part in str(python_path) for part in [".cache", "cache", "temp"]):
            return True

    return False


def x__is_pspf_launch__mutmut_5(executable_path: str, python_executable: str) -> bool:
    """Check if we're running from a PSPF package."""
    # PSPF packages typically have a cache directory structure
    cache_indicators = ["/.cache/pspf/", "/CACHE/BIN/PYTHON", "/pspf_", "terraform-provider-"]

    # Check if Python is running from a cache-like directory
    for indicator in cache_indicators:
        if indicator in python_executable.lower():
            return True

    # Check if executable path suggests PSPF
    if any(indicator in executable_path.lower() for indicator in ["terraform-provider-", "pspf"]):
        # Additional check: see if we're in a temporary/cache directory structure
        python_path = Path(python_executable)
        if any(part in str(python_path) for part in [".cache", "cache", "temp"]):
            return True

    return False


def x__is_pspf_launch__mutmut_6(executable_path: str, python_executable: str) -> bool:
    """Check if we're running from a PSPF package."""
    # PSPF packages typically have a cache directory structure
    cache_indicators = ["/.cache/pspf/", "/cache/bin/python", "XX/pspf_XX", "terraform-provider-"]

    # Check if Python is running from a cache-like directory
    for indicator in cache_indicators:
        if indicator in python_executable.lower():
            return True

    # Check if executable path suggests PSPF
    if any(indicator in executable_path.lower() for indicator in ["terraform-provider-", "pspf"]):
        # Additional check: see if we're in a temporary/cache directory structure
        python_path = Path(python_executable)
        if any(part in str(python_path) for part in [".cache", "cache", "temp"]):
            return True

    return False


def x__is_pspf_launch__mutmut_7(executable_path: str, python_executable: str) -> bool:
    """Check if we're running from a PSPF package."""
    # PSPF packages typically have a cache directory structure
    cache_indicators = ["/.cache/pspf/", "/cache/bin/python", "/PSPF_", "terraform-provider-"]

    # Check if Python is running from a cache-like directory
    for indicator in cache_indicators:
        if indicator in python_executable.lower():
            return True

    # Check if executable path suggests PSPF
    if any(indicator in executable_path.lower() for indicator in ["terraform-provider-", "pspf"]):
        # Additional check: see if we're in a temporary/cache directory structure
        python_path = Path(python_executable)
        if any(part in str(python_path) for part in [".cache", "cache", "temp"]):
            return True

    return False


def x__is_pspf_launch__mutmut_8(executable_path: str, python_executable: str) -> bool:
    """Check if we're running from a PSPF package."""
    # PSPF packages typically have a cache directory structure
    cache_indicators = ["/.cache/pspf/", "/cache/bin/python", "/pspf_", "XXterraform-provider-XX"]

    # Check if Python is running from a cache-like directory
    for indicator in cache_indicators:
        if indicator in python_executable.lower():
            return True

    # Check if executable path suggests PSPF
    if any(indicator in executable_path.lower() for indicator in ["terraform-provider-", "pspf"]):
        # Additional check: see if we're in a temporary/cache directory structure
        python_path = Path(python_executable)
        if any(part in str(python_path) for part in [".cache", "cache", "temp"]):
            return True

    return False


def x__is_pspf_launch__mutmut_9(executable_path: str, python_executable: str) -> bool:
    """Check if we're running from a PSPF package."""
    # PSPF packages typically have a cache directory structure
    cache_indicators = ["/.cache/pspf/", "/cache/bin/python", "/pspf_", "TERRAFORM-PROVIDER-"]

    # Check if Python is running from a cache-like directory
    for indicator in cache_indicators:
        if indicator in python_executable.lower():
            return True

    # Check if executable path suggests PSPF
    if any(indicator in executable_path.lower() for indicator in ["terraform-provider-", "pspf"]):
        # Additional check: see if we're in a temporary/cache directory structure
        python_path = Path(python_executable)
        if any(part in str(python_path) for part in [".cache", "cache", "temp"]):
            return True

    return False


def x__is_pspf_launch__mutmut_10(executable_path: str, python_executable: str) -> bool:
    """Check if we're running from a PSPF package."""
    # PSPF packages typically have a cache directory structure
    cache_indicators = ["/.cache/pspf/", "/cache/bin/python", "/pspf_", "terraform-provider-"]

    # Check if Python is running from a cache-like directory
    for indicator in cache_indicators:
        if indicator not in python_executable.lower():
            return True

    # Check if executable path suggests PSPF
    if any(indicator in executable_path.lower() for indicator in ["terraform-provider-", "pspf"]):
        # Additional check: see if we're in a temporary/cache directory structure
        python_path = Path(python_executable)
        if any(part in str(python_path) for part in [".cache", "cache", "temp"]):
            return True

    return False


def x__is_pspf_launch__mutmut_11(executable_path: str, python_executable: str) -> bool:
    """Check if we're running from a PSPF package."""
    # PSPF packages typically have a cache directory structure
    cache_indicators = ["/.cache/pspf/", "/cache/bin/python", "/pspf_", "terraform-provider-"]

    # Check if Python is running from a cache-like directory
    for indicator in cache_indicators:
        if indicator in python_executable.upper():
            return True

    # Check if executable path suggests PSPF
    if any(indicator in executable_path.lower() for indicator in ["terraform-provider-", "pspf"]):
        # Additional check: see if we're in a temporary/cache directory structure
        python_path = Path(python_executable)
        if any(part in str(python_path) for part in [".cache", "cache", "temp"]):
            return True

    return False


def x__is_pspf_launch__mutmut_12(executable_path: str, python_executable: str) -> bool:
    """Check if we're running from a PSPF package."""
    # PSPF packages typically have a cache directory structure
    cache_indicators = ["/.cache/pspf/", "/cache/bin/python", "/pspf_", "terraform-provider-"]

    # Check if Python is running from a cache-like directory
    for indicator in cache_indicators:
        if indicator in python_executable.lower():
            return False

    # Check if executable path suggests PSPF
    if any(indicator in executable_path.lower() for indicator in ["terraform-provider-", "pspf"]):
        # Additional check: see if we're in a temporary/cache directory structure
        python_path = Path(python_executable)
        if any(part in str(python_path) for part in [".cache", "cache", "temp"]):
            return True

    return False


def x__is_pspf_launch__mutmut_13(executable_path: str, python_executable: str) -> bool:
    """Check if we're running from a PSPF package."""
    # PSPF packages typically have a cache directory structure
    cache_indicators = ["/.cache/pspf/", "/cache/bin/python", "/pspf_", "terraform-provider-"]

    # Check if Python is running from a cache-like directory
    for indicator in cache_indicators:
        if indicator in python_executable.lower():
            return True

    # Check if executable path suggests PSPF
    if any(None):
        # Additional check: see if we're in a temporary/cache directory structure
        python_path = Path(python_executable)
        if any(part in str(python_path) for part in [".cache", "cache", "temp"]):
            return True

    return False


def x__is_pspf_launch__mutmut_14(executable_path: str, python_executable: str) -> bool:
    """Check if we're running from a PSPF package."""
    # PSPF packages typically have a cache directory structure
    cache_indicators = ["/.cache/pspf/", "/cache/bin/python", "/pspf_", "terraform-provider-"]

    # Check if Python is running from a cache-like directory
    for indicator in cache_indicators:
        if indicator in python_executable.lower():
            return True

    # Check if executable path suggests PSPF
    if any(indicator not in executable_path.lower() for indicator in ["terraform-provider-", "pspf"]):
        # Additional check: see if we're in a temporary/cache directory structure
        python_path = Path(python_executable)
        if any(part in str(python_path) for part in [".cache", "cache", "temp"]):
            return True

    return False


def x__is_pspf_launch__mutmut_15(executable_path: str, python_executable: str) -> bool:
    """Check if we're running from a PSPF package."""
    # PSPF packages typically have a cache directory structure
    cache_indicators = ["/.cache/pspf/", "/cache/bin/python", "/pspf_", "terraform-provider-"]

    # Check if Python is running from a cache-like directory
    for indicator in cache_indicators:
        if indicator in python_executable.lower():
            return True

    # Check if executable path suggests PSPF
    if any(indicator in executable_path.upper() for indicator in ["terraform-provider-", "pspf"]):
        # Additional check: see if we're in a temporary/cache directory structure
        python_path = Path(python_executable)
        if any(part in str(python_path) for part in [".cache", "cache", "temp"]):
            return True

    return False


def x__is_pspf_launch__mutmut_16(executable_path: str, python_executable: str) -> bool:
    """Check if we're running from a PSPF package."""
    # PSPF packages typically have a cache directory structure
    cache_indicators = ["/.cache/pspf/", "/cache/bin/python", "/pspf_", "terraform-provider-"]

    # Check if Python is running from a cache-like directory
    for indicator in cache_indicators:
        if indicator in python_executable.lower():
            return True

    # Check if executable path suggests PSPF
    if any(indicator in executable_path.lower() for indicator in ["XXterraform-provider-XX", "pspf"]):
        # Additional check: see if we're in a temporary/cache directory structure
        python_path = Path(python_executable)
        if any(part in str(python_path) for part in [".cache", "cache", "temp"]):
            return True

    return False


def x__is_pspf_launch__mutmut_17(executable_path: str, python_executable: str) -> bool:
    """Check if we're running from a PSPF package."""
    # PSPF packages typically have a cache directory structure
    cache_indicators = ["/.cache/pspf/", "/cache/bin/python", "/pspf_", "terraform-provider-"]

    # Check if Python is running from a cache-like directory
    for indicator in cache_indicators:
        if indicator in python_executable.lower():
            return True

    # Check if executable path suggests PSPF
    if any(indicator in executable_path.lower() for indicator in ["TERRAFORM-PROVIDER-", "pspf"]):
        # Additional check: see if we're in a temporary/cache directory structure
        python_path = Path(python_executable)
        if any(part in str(python_path) for part in [".cache", "cache", "temp"]):
            return True

    return False


def x__is_pspf_launch__mutmut_18(executable_path: str, python_executable: str) -> bool:
    """Check if we're running from a PSPF package."""
    # PSPF packages typically have a cache directory structure
    cache_indicators = ["/.cache/pspf/", "/cache/bin/python", "/pspf_", "terraform-provider-"]

    # Check if Python is running from a cache-like directory
    for indicator in cache_indicators:
        if indicator in python_executable.lower():
            return True

    # Check if executable path suggests PSPF
    if any(indicator in executable_path.lower() for indicator in ["terraform-provider-", "XXpspfXX"]):
        # Additional check: see if we're in a temporary/cache directory structure
        python_path = Path(python_executable)
        if any(part in str(python_path) for part in [".cache", "cache", "temp"]):
            return True

    return False


def x__is_pspf_launch__mutmut_19(executable_path: str, python_executable: str) -> bool:
    """Check if we're running from a PSPF package."""
    # PSPF packages typically have a cache directory structure
    cache_indicators = ["/.cache/pspf/", "/cache/bin/python", "/pspf_", "terraform-provider-"]

    # Check if Python is running from a cache-like directory
    for indicator in cache_indicators:
        if indicator in python_executable.lower():
            return True

    # Check if executable path suggests PSPF
    if any(indicator in executable_path.lower() for indicator in ["terraform-provider-", "PSPF"]):
        # Additional check: see if we're in a temporary/cache directory structure
        python_path = Path(python_executable)
        if any(part in str(python_path) for part in [".cache", "cache", "temp"]):
            return True

    return False


def x__is_pspf_launch__mutmut_20(executable_path: str, python_executable: str) -> bool:
    """Check if we're running from a PSPF package."""
    # PSPF packages typically have a cache directory structure
    cache_indicators = ["/.cache/pspf/", "/cache/bin/python", "/pspf_", "terraform-provider-"]

    # Check if Python is running from a cache-like directory
    for indicator in cache_indicators:
        if indicator in python_executable.lower():
            return True

    # Check if executable path suggests PSPF
    if any(indicator in executable_path.lower() for indicator in ["terraform-provider-", "pspf"]):
        # Additional check: see if we're in a temporary/cache directory structure
        python_path = None
        if any(part in str(python_path) for part in [".cache", "cache", "temp"]):
            return True

    return False


def x__is_pspf_launch__mutmut_21(executable_path: str, python_executable: str) -> bool:
    """Check if we're running from a PSPF package."""
    # PSPF packages typically have a cache directory structure
    cache_indicators = ["/.cache/pspf/", "/cache/bin/python", "/pspf_", "terraform-provider-"]

    # Check if Python is running from a cache-like directory
    for indicator in cache_indicators:
        if indicator in python_executable.lower():
            return True

    # Check if executable path suggests PSPF
    if any(indicator in executable_path.lower() for indicator in ["terraform-provider-", "pspf"]):
        # Additional check: see if we're in a temporary/cache directory structure
        python_path = Path(None)
        if any(part in str(python_path) for part in [".cache", "cache", "temp"]):
            return True

    return False


def x__is_pspf_launch__mutmut_22(executable_path: str, python_executable: str) -> bool:
    """Check if we're running from a PSPF package."""
    # PSPF packages typically have a cache directory structure
    cache_indicators = ["/.cache/pspf/", "/cache/bin/python", "/pspf_", "terraform-provider-"]

    # Check if Python is running from a cache-like directory
    for indicator in cache_indicators:
        if indicator in python_executable.lower():
            return True

    # Check if executable path suggests PSPF
    if any(indicator in executable_path.lower() for indicator in ["terraform-provider-", "pspf"]):
        # Additional check: see if we're in a temporary/cache directory structure
        python_path = Path(python_executable)
        if any(None):
            return True

    return False


def x__is_pspf_launch__mutmut_23(executable_path: str, python_executable: str) -> bool:
    """Check if we're running from a PSPF package."""
    # PSPF packages typically have a cache directory structure
    cache_indicators = ["/.cache/pspf/", "/cache/bin/python", "/pspf_", "terraform-provider-"]

    # Check if Python is running from a cache-like directory
    for indicator in cache_indicators:
        if indicator in python_executable.lower():
            return True

    # Check if executable path suggests PSPF
    if any(indicator in executable_path.lower() for indicator in ["terraform-provider-", "pspf"]):
        # Additional check: see if we're in a temporary/cache directory structure
        python_path = Path(python_executable)
        if any(part not in str(python_path) for part in [".cache", "cache", "temp"]):
            return True

    return False


def x__is_pspf_launch__mutmut_24(executable_path: str, python_executable: str) -> bool:
    """Check if we're running from a PSPF package."""
    # PSPF packages typically have a cache directory structure
    cache_indicators = ["/.cache/pspf/", "/cache/bin/python", "/pspf_", "terraform-provider-"]

    # Check if Python is running from a cache-like directory
    for indicator in cache_indicators:
        if indicator in python_executable.lower():
            return True

    # Check if executable path suggests PSPF
    if any(indicator in executable_path.lower() for indicator in ["terraform-provider-", "pspf"]):
        # Additional check: see if we're in a temporary/cache directory structure
        python_path = Path(python_executable)
        if any(part in str(None) for part in [".cache", "cache", "temp"]):
            return True

    return False


def x__is_pspf_launch__mutmut_25(executable_path: str, python_executable: str) -> bool:
    """Check if we're running from a PSPF package."""
    # PSPF packages typically have a cache directory structure
    cache_indicators = ["/.cache/pspf/", "/cache/bin/python", "/pspf_", "terraform-provider-"]

    # Check if Python is running from a cache-like directory
    for indicator in cache_indicators:
        if indicator in python_executable.lower():
            return True

    # Check if executable path suggests PSPF
    if any(indicator in executable_path.lower() for indicator in ["terraform-provider-", "pspf"]):
        # Additional check: see if we're in a temporary/cache directory structure
        python_path = Path(python_executable)
        if any(part in str(python_path) for part in ["XX.cacheXX", "cache", "temp"]):
            return True

    return False


def x__is_pspf_launch__mutmut_26(executable_path: str, python_executable: str) -> bool:
    """Check if we're running from a PSPF package."""
    # PSPF packages typically have a cache directory structure
    cache_indicators = ["/.cache/pspf/", "/cache/bin/python", "/pspf_", "terraform-provider-"]

    # Check if Python is running from a cache-like directory
    for indicator in cache_indicators:
        if indicator in python_executable.lower():
            return True

    # Check if executable path suggests PSPF
    if any(indicator in executable_path.lower() for indicator in ["terraform-provider-", "pspf"]):
        # Additional check: see if we're in a temporary/cache directory structure
        python_path = Path(python_executable)
        if any(part in str(python_path) for part in [".CACHE", "cache", "temp"]):
            return True

    return False


def x__is_pspf_launch__mutmut_27(executable_path: str, python_executable: str) -> bool:
    """Check if we're running from a PSPF package."""
    # PSPF packages typically have a cache directory structure
    cache_indicators = ["/.cache/pspf/", "/cache/bin/python", "/pspf_", "terraform-provider-"]

    # Check if Python is running from a cache-like directory
    for indicator in cache_indicators:
        if indicator in python_executable.lower():
            return True

    # Check if executable path suggests PSPF
    if any(indicator in executable_path.lower() for indicator in ["terraform-provider-", "pspf"]):
        # Additional check: see if we're in a temporary/cache directory structure
        python_path = Path(python_executable)
        if any(part in str(python_path) for part in [".cache", "XXcacheXX", "temp"]):
            return True

    return False


def x__is_pspf_launch__mutmut_28(executable_path: str, python_executable: str) -> bool:
    """Check if we're running from a PSPF package."""
    # PSPF packages typically have a cache directory structure
    cache_indicators = ["/.cache/pspf/", "/cache/bin/python", "/pspf_", "terraform-provider-"]

    # Check if Python is running from a cache-like directory
    for indicator in cache_indicators:
        if indicator in python_executable.lower():
            return True

    # Check if executable path suggests PSPF
    if any(indicator in executable_path.lower() for indicator in ["terraform-provider-", "pspf"]):
        # Additional check: see if we're in a temporary/cache directory structure
        python_path = Path(python_executable)
        if any(part in str(python_path) for part in [".cache", "CACHE", "temp"]):
            return True

    return False


def x__is_pspf_launch__mutmut_29(executable_path: str, python_executable: str) -> bool:
    """Check if we're running from a PSPF package."""
    # PSPF packages typically have a cache directory structure
    cache_indicators = ["/.cache/pspf/", "/cache/bin/python", "/pspf_", "terraform-provider-"]

    # Check if Python is running from a cache-like directory
    for indicator in cache_indicators:
        if indicator in python_executable.lower():
            return True

    # Check if executable path suggests PSPF
    if any(indicator in executable_path.lower() for indicator in ["terraform-provider-", "pspf"]):
        # Additional check: see if we're in a temporary/cache directory structure
        python_path = Path(python_executable)
        if any(part in str(python_path) for part in [".cache", "cache", "XXtempXX"]):
            return True

    return False


def x__is_pspf_launch__mutmut_30(executable_path: str, python_executable: str) -> bool:
    """Check if we're running from a PSPF package."""
    # PSPF packages typically have a cache directory structure
    cache_indicators = ["/.cache/pspf/", "/cache/bin/python", "/pspf_", "terraform-provider-"]

    # Check if Python is running from a cache-like directory
    for indicator in cache_indicators:
        if indicator in python_executable.lower():
            return True

    # Check if executable path suggests PSPF
    if any(indicator in executable_path.lower() for indicator in ["terraform-provider-", "pspf"]):
        # Additional check: see if we're in a temporary/cache directory structure
        python_path = Path(python_executable)
        if any(part in str(python_path) for part in [".cache", "cache", "TEMP"]):
            return True

    return False


def x__is_pspf_launch__mutmut_31(executable_path: str, python_executable: str) -> bool:
    """Check if we're running from a PSPF package."""
    # PSPF packages typically have a cache directory structure
    cache_indicators = ["/.cache/pspf/", "/cache/bin/python", "/pspf_", "terraform-provider-"]

    # Check if Python is running from a cache-like directory
    for indicator in cache_indicators:
        if indicator in python_executable.lower():
            return True

    # Check if executable path suggests PSPF
    if any(indicator in executable_path.lower() for indicator in ["terraform-provider-", "pspf"]):
        # Additional check: see if we're in a temporary/cache directory structure
        python_path = Path(python_executable)
        if any(part in str(python_path) for part in [".cache", "cache", "temp"]):
            return False

    return False


def x__is_pspf_launch__mutmut_32(executable_path: str, python_executable: str) -> bool:
    """Check if we're running from a PSPF package."""
    # PSPF packages typically have a cache directory structure
    cache_indicators = ["/.cache/pspf/", "/cache/bin/python", "/pspf_", "terraform-provider-"]

    # Check if Python is running from a cache-like directory
    for indicator in cache_indicators:
        if indicator in python_executable.lower():
            return True

    # Check if executable path suggests PSPF
    if any(indicator in executable_path.lower() for indicator in ["terraform-provider-", "pspf"]):
        # Additional check: see if we're in a temporary/cache directory structure
        python_path = Path(python_executable)
        if any(part in str(python_path) for part in [".cache", "cache", "temp"]):
            return True

    return True

x__is_pspf_launch__mutmut_mutants : ClassVar[MutantDict] = {
'x__is_pspf_launch__mutmut_1': x__is_pspf_launch__mutmut_1, 
    'x__is_pspf_launch__mutmut_2': x__is_pspf_launch__mutmut_2, 
    'x__is_pspf_launch__mutmut_3': x__is_pspf_launch__mutmut_3, 
    'x__is_pspf_launch__mutmut_4': x__is_pspf_launch__mutmut_4, 
    'x__is_pspf_launch__mutmut_5': x__is_pspf_launch__mutmut_5, 
    'x__is_pspf_launch__mutmut_6': x__is_pspf_launch__mutmut_6, 
    'x__is_pspf_launch__mutmut_7': x__is_pspf_launch__mutmut_7, 
    'x__is_pspf_launch__mutmut_8': x__is_pspf_launch__mutmut_8, 
    'x__is_pspf_launch__mutmut_9': x__is_pspf_launch__mutmut_9, 
    'x__is_pspf_launch__mutmut_10': x__is_pspf_launch__mutmut_10, 
    'x__is_pspf_launch__mutmut_11': x__is_pspf_launch__mutmut_11, 
    'x__is_pspf_launch__mutmut_12': x__is_pspf_launch__mutmut_12, 
    'x__is_pspf_launch__mutmut_13': x__is_pspf_launch__mutmut_13, 
    'x__is_pspf_launch__mutmut_14': x__is_pspf_launch__mutmut_14, 
    'x__is_pspf_launch__mutmut_15': x__is_pspf_launch__mutmut_15, 
    'x__is_pspf_launch__mutmut_16': x__is_pspf_launch__mutmut_16, 
    'x__is_pspf_launch__mutmut_17': x__is_pspf_launch__mutmut_17, 
    'x__is_pspf_launch__mutmut_18': x__is_pspf_launch__mutmut_18, 
    'x__is_pspf_launch__mutmut_19': x__is_pspf_launch__mutmut_19, 
    'x__is_pspf_launch__mutmut_20': x__is_pspf_launch__mutmut_20, 
    'x__is_pspf_launch__mutmut_21': x__is_pspf_launch__mutmut_21, 
    'x__is_pspf_launch__mutmut_22': x__is_pspf_launch__mutmut_22, 
    'x__is_pspf_launch__mutmut_23': x__is_pspf_launch__mutmut_23, 
    'x__is_pspf_launch__mutmut_24': x__is_pspf_launch__mutmut_24, 
    'x__is_pspf_launch__mutmut_25': x__is_pspf_launch__mutmut_25, 
    'x__is_pspf_launch__mutmut_26': x__is_pspf_launch__mutmut_26, 
    'x__is_pspf_launch__mutmut_27': x__is_pspf_launch__mutmut_27, 
    'x__is_pspf_launch__mutmut_28': x__is_pspf_launch__mutmut_28, 
    'x__is_pspf_launch__mutmut_29': x__is_pspf_launch__mutmut_29, 
    'x__is_pspf_launch__mutmut_30': x__is_pspf_launch__mutmut_30, 
    'x__is_pspf_launch__mutmut_31': x__is_pspf_launch__mutmut_31, 
    'x__is_pspf_launch__mutmut_32': x__is_pspf_launch__mutmut_32
}

def _is_pspf_launch(*args, **kwargs):
    result = _mutmut_trampoline(x__is_pspf_launch__mutmut_orig, x__is_pspf_launch__mutmut_mutants, args, kwargs)
    return result 

_is_pspf_launch.__signature__ = _mutmut_signature(x__is_pspf_launch__mutmut_orig)
x__is_pspf_launch__mutmut_orig.__name__ = 'x__is_pspf_launch'


def x__is_module_launch__mutmut_orig() -> bool:
    """Check if we're running as 'python -m pyvider'."""
    # Check if we're running via __main__.py (indicates module execution)
    if len(sys.argv) >= 1 and sys.argv[0].endswith("__main__.py"):
        return True

    # Check if -m is in the original command line
    # This is tricky because sys.argv doesn't contain the -m flag
    # But we can infer it from the executable path structure
    if len(sys.argv) >= 1:
        # If argv[0] ends with __main__.py, it's almost certainly python -m
        if "__main__.py" in sys.argv[0]:
            return True

        # If the first argument is just "pyvider" or similar module name
        # and we're running from a __main__.py, it's likely python -m
        first_arg = Path(sys.argv[0]).name
        if first_arg in ["pyvider", "__main__.py"] or first_arg.endswith("__main__.py"):
            return True

    return False


def x__is_module_launch__mutmut_1() -> bool:
    """Check if we're running as 'python -m pyvider'."""
    # Check if we're running via __main__.py (indicates module execution)
    if len(sys.argv) >= 1 or sys.argv[0].endswith("__main__.py"):
        return True

    # Check if -m is in the original command line
    # This is tricky because sys.argv doesn't contain the -m flag
    # But we can infer it from the executable path structure
    if len(sys.argv) >= 1:
        # If argv[0] ends with __main__.py, it's almost certainly python -m
        if "__main__.py" in sys.argv[0]:
            return True

        # If the first argument is just "pyvider" or similar module name
        # and we're running from a __main__.py, it's likely python -m
        first_arg = Path(sys.argv[0]).name
        if first_arg in ["pyvider", "__main__.py"] or first_arg.endswith("__main__.py"):
            return True

    return False


def x__is_module_launch__mutmut_2() -> bool:
    """Check if we're running as 'python -m pyvider'."""
    # Check if we're running via __main__.py (indicates module execution)
    if len(sys.argv) > 1 and sys.argv[0].endswith("__main__.py"):
        return True

    # Check if -m is in the original command line
    # This is tricky because sys.argv doesn't contain the -m flag
    # But we can infer it from the executable path structure
    if len(sys.argv) >= 1:
        # If argv[0] ends with __main__.py, it's almost certainly python -m
        if "__main__.py" in sys.argv[0]:
            return True

        # If the first argument is just "pyvider" or similar module name
        # and we're running from a __main__.py, it's likely python -m
        first_arg = Path(sys.argv[0]).name
        if first_arg in ["pyvider", "__main__.py"] or first_arg.endswith("__main__.py"):
            return True

    return False


def x__is_module_launch__mutmut_3() -> bool:
    """Check if we're running as 'python -m pyvider'."""
    # Check if we're running via __main__.py (indicates module execution)
    if len(sys.argv) >= 2 and sys.argv[0].endswith("__main__.py"):
        return True

    # Check if -m is in the original command line
    # This is tricky because sys.argv doesn't contain the -m flag
    # But we can infer it from the executable path structure
    if len(sys.argv) >= 1:
        # If argv[0] ends with __main__.py, it's almost certainly python -m
        if "__main__.py" in sys.argv[0]:
            return True

        # If the first argument is just "pyvider" or similar module name
        # and we're running from a __main__.py, it's likely python -m
        first_arg = Path(sys.argv[0]).name
        if first_arg in ["pyvider", "__main__.py"] or first_arg.endswith("__main__.py"):
            return True

    return False


def x__is_module_launch__mutmut_4() -> bool:
    """Check if we're running as 'python -m pyvider'."""
    # Check if we're running via __main__.py (indicates module execution)
    if len(sys.argv) >= 1 and sys.argv[0].endswith(None):
        return True

    # Check if -m is in the original command line
    # This is tricky because sys.argv doesn't contain the -m flag
    # But we can infer it from the executable path structure
    if len(sys.argv) >= 1:
        # If argv[0] ends with __main__.py, it's almost certainly python -m
        if "__main__.py" in sys.argv[0]:
            return True

        # If the first argument is just "pyvider" or similar module name
        # and we're running from a __main__.py, it's likely python -m
        first_arg = Path(sys.argv[0]).name
        if first_arg in ["pyvider", "__main__.py"] or first_arg.endswith("__main__.py"):
            return True

    return False


def x__is_module_launch__mutmut_5() -> bool:
    """Check if we're running as 'python -m pyvider'."""
    # Check if we're running via __main__.py (indicates module execution)
    if len(sys.argv) >= 1 and sys.argv[1].endswith("__main__.py"):
        return True

    # Check if -m is in the original command line
    # This is tricky because sys.argv doesn't contain the -m flag
    # But we can infer it from the executable path structure
    if len(sys.argv) >= 1:
        # If argv[0] ends with __main__.py, it's almost certainly python -m
        if "__main__.py" in sys.argv[0]:
            return True

        # If the first argument is just "pyvider" or similar module name
        # and we're running from a __main__.py, it's likely python -m
        first_arg = Path(sys.argv[0]).name
        if first_arg in ["pyvider", "__main__.py"] or first_arg.endswith("__main__.py"):
            return True

    return False


def x__is_module_launch__mutmut_6() -> bool:
    """Check if we're running as 'python -m pyvider'."""
    # Check if we're running via __main__.py (indicates module execution)
    if len(sys.argv) >= 1 and sys.argv[0].endswith("XX__main__.pyXX"):
        return True

    # Check if -m is in the original command line
    # This is tricky because sys.argv doesn't contain the -m flag
    # But we can infer it from the executable path structure
    if len(sys.argv) >= 1:
        # If argv[0] ends with __main__.py, it's almost certainly python -m
        if "__main__.py" in sys.argv[0]:
            return True

        # If the first argument is just "pyvider" or similar module name
        # and we're running from a __main__.py, it's likely python -m
        first_arg = Path(sys.argv[0]).name
        if first_arg in ["pyvider", "__main__.py"] or first_arg.endswith("__main__.py"):
            return True

    return False


def x__is_module_launch__mutmut_7() -> bool:
    """Check if we're running as 'python -m pyvider'."""
    # Check if we're running via __main__.py (indicates module execution)
    if len(sys.argv) >= 1 and sys.argv[0].endswith("__MAIN__.PY"):
        return True

    # Check if -m is in the original command line
    # This is tricky because sys.argv doesn't contain the -m flag
    # But we can infer it from the executable path structure
    if len(sys.argv) >= 1:
        # If argv[0] ends with __main__.py, it's almost certainly python -m
        if "__main__.py" in sys.argv[0]:
            return True

        # If the first argument is just "pyvider" or similar module name
        # and we're running from a __main__.py, it's likely python -m
        first_arg = Path(sys.argv[0]).name
        if first_arg in ["pyvider", "__main__.py"] or first_arg.endswith("__main__.py"):
            return True

    return False


def x__is_module_launch__mutmut_8() -> bool:
    """Check if we're running as 'python -m pyvider'."""
    # Check if we're running via __main__.py (indicates module execution)
    if len(sys.argv) >= 1 and sys.argv[0].endswith("__main__.py"):
        return False

    # Check if -m is in the original command line
    # This is tricky because sys.argv doesn't contain the -m flag
    # But we can infer it from the executable path structure
    if len(sys.argv) >= 1:
        # If argv[0] ends with __main__.py, it's almost certainly python -m
        if "__main__.py" in sys.argv[0]:
            return True

        # If the first argument is just "pyvider" or similar module name
        # and we're running from a __main__.py, it's likely python -m
        first_arg = Path(sys.argv[0]).name
        if first_arg in ["pyvider", "__main__.py"] or first_arg.endswith("__main__.py"):
            return True

    return False


def x__is_module_launch__mutmut_9() -> bool:
    """Check if we're running as 'python -m pyvider'."""
    # Check if we're running via __main__.py (indicates module execution)
    if len(sys.argv) >= 1 and sys.argv[0].endswith("__main__.py"):
        return True

    # Check if -m is in the original command line
    # This is tricky because sys.argv doesn't contain the -m flag
    # But we can infer it from the executable path structure
    if len(sys.argv) > 1:
        # If argv[0] ends with __main__.py, it's almost certainly python -m
        if "__main__.py" in sys.argv[0]:
            return True

        # If the first argument is just "pyvider" or similar module name
        # and we're running from a __main__.py, it's likely python -m
        first_arg = Path(sys.argv[0]).name
        if first_arg in ["pyvider", "__main__.py"] or first_arg.endswith("__main__.py"):
            return True

    return False


def x__is_module_launch__mutmut_10() -> bool:
    """Check if we're running as 'python -m pyvider'."""
    # Check if we're running via __main__.py (indicates module execution)
    if len(sys.argv) >= 1 and sys.argv[0].endswith("__main__.py"):
        return True

    # Check if -m is in the original command line
    # This is tricky because sys.argv doesn't contain the -m flag
    # But we can infer it from the executable path structure
    if len(sys.argv) >= 2:
        # If argv[0] ends with __main__.py, it's almost certainly python -m
        if "__main__.py" in sys.argv[0]:
            return True

        # If the first argument is just "pyvider" or similar module name
        # and we're running from a __main__.py, it's likely python -m
        first_arg = Path(sys.argv[0]).name
        if first_arg in ["pyvider", "__main__.py"] or first_arg.endswith("__main__.py"):
            return True

    return False


def x__is_module_launch__mutmut_11() -> bool:
    """Check if we're running as 'python -m pyvider'."""
    # Check if we're running via __main__.py (indicates module execution)
    if len(sys.argv) >= 1 and sys.argv[0].endswith("__main__.py"):
        return True

    # Check if -m is in the original command line
    # This is tricky because sys.argv doesn't contain the -m flag
    # But we can infer it from the executable path structure
    if len(sys.argv) >= 1:
        # If argv[0] ends with __main__.py, it's almost certainly python -m
        if "XX__main__.pyXX" in sys.argv[0]:
            return True

        # If the first argument is just "pyvider" or similar module name
        # and we're running from a __main__.py, it's likely python -m
        first_arg = Path(sys.argv[0]).name
        if first_arg in ["pyvider", "__main__.py"] or first_arg.endswith("__main__.py"):
            return True

    return False


def x__is_module_launch__mutmut_12() -> bool:
    """Check if we're running as 'python -m pyvider'."""
    # Check if we're running via __main__.py (indicates module execution)
    if len(sys.argv) >= 1 and sys.argv[0].endswith("__main__.py"):
        return True

    # Check if -m is in the original command line
    # This is tricky because sys.argv doesn't contain the -m flag
    # But we can infer it from the executable path structure
    if len(sys.argv) >= 1:
        # If argv[0] ends with __main__.py, it's almost certainly python -m
        if "__MAIN__.PY" in sys.argv[0]:
            return True

        # If the first argument is just "pyvider" or similar module name
        # and we're running from a __main__.py, it's likely python -m
        first_arg = Path(sys.argv[0]).name
        if first_arg in ["pyvider", "__main__.py"] or first_arg.endswith("__main__.py"):
            return True

    return False


def x__is_module_launch__mutmut_13() -> bool:
    """Check if we're running as 'python -m pyvider'."""
    # Check if we're running via __main__.py (indicates module execution)
    if len(sys.argv) >= 1 and sys.argv[0].endswith("__main__.py"):
        return True

    # Check if -m is in the original command line
    # This is tricky because sys.argv doesn't contain the -m flag
    # But we can infer it from the executable path structure
    if len(sys.argv) >= 1:
        # If argv[0] ends with __main__.py, it's almost certainly python -m
        if "__main__.py" not in sys.argv[0]:
            return True

        # If the first argument is just "pyvider" or similar module name
        # and we're running from a __main__.py, it's likely python -m
        first_arg = Path(sys.argv[0]).name
        if first_arg in ["pyvider", "__main__.py"] or first_arg.endswith("__main__.py"):
            return True

    return False


def x__is_module_launch__mutmut_14() -> bool:
    """Check if we're running as 'python -m pyvider'."""
    # Check if we're running via __main__.py (indicates module execution)
    if len(sys.argv) >= 1 and sys.argv[0].endswith("__main__.py"):
        return True

    # Check if -m is in the original command line
    # This is tricky because sys.argv doesn't contain the -m flag
    # But we can infer it from the executable path structure
    if len(sys.argv) >= 1:
        # If argv[0] ends with __main__.py, it's almost certainly python -m
        if "__main__.py" in sys.argv[1]:
            return True

        # If the first argument is just "pyvider" or similar module name
        # and we're running from a __main__.py, it's likely python -m
        first_arg = Path(sys.argv[0]).name
        if first_arg in ["pyvider", "__main__.py"] or first_arg.endswith("__main__.py"):
            return True

    return False


def x__is_module_launch__mutmut_15() -> bool:
    """Check if we're running as 'python -m pyvider'."""
    # Check if we're running via __main__.py (indicates module execution)
    if len(sys.argv) >= 1 and sys.argv[0].endswith("__main__.py"):
        return True

    # Check if -m is in the original command line
    # This is tricky because sys.argv doesn't contain the -m flag
    # But we can infer it from the executable path structure
    if len(sys.argv) >= 1:
        # If argv[0] ends with __main__.py, it's almost certainly python -m
        if "__main__.py" in sys.argv[0]:
            return False

        # If the first argument is just "pyvider" or similar module name
        # and we're running from a __main__.py, it's likely python -m
        first_arg = Path(sys.argv[0]).name
        if first_arg in ["pyvider", "__main__.py"] or first_arg.endswith("__main__.py"):
            return True

    return False


def x__is_module_launch__mutmut_16() -> bool:
    """Check if we're running as 'python -m pyvider'."""
    # Check if we're running via __main__.py (indicates module execution)
    if len(sys.argv) >= 1 and sys.argv[0].endswith("__main__.py"):
        return True

    # Check if -m is in the original command line
    # This is tricky because sys.argv doesn't contain the -m flag
    # But we can infer it from the executable path structure
    if len(sys.argv) >= 1:
        # If argv[0] ends with __main__.py, it's almost certainly python -m
        if "__main__.py" in sys.argv[0]:
            return True

        # If the first argument is just "pyvider" or similar module name
        # and we're running from a __main__.py, it's likely python -m
        first_arg = None
        if first_arg in ["pyvider", "__main__.py"] or first_arg.endswith("__main__.py"):
            return True

    return False


def x__is_module_launch__mutmut_17() -> bool:
    """Check if we're running as 'python -m pyvider'."""
    # Check if we're running via __main__.py (indicates module execution)
    if len(sys.argv) >= 1 and sys.argv[0].endswith("__main__.py"):
        return True

    # Check if -m is in the original command line
    # This is tricky because sys.argv doesn't contain the -m flag
    # But we can infer it from the executable path structure
    if len(sys.argv) >= 1:
        # If argv[0] ends with __main__.py, it's almost certainly python -m
        if "__main__.py" in sys.argv[0]:
            return True

        # If the first argument is just "pyvider" or similar module name
        # and we're running from a __main__.py, it's likely python -m
        first_arg = Path(None).name
        if first_arg in ["pyvider", "__main__.py"] or first_arg.endswith("__main__.py"):
            return True

    return False


def x__is_module_launch__mutmut_18() -> bool:
    """Check if we're running as 'python -m pyvider'."""
    # Check if we're running via __main__.py (indicates module execution)
    if len(sys.argv) >= 1 and sys.argv[0].endswith("__main__.py"):
        return True

    # Check if -m is in the original command line
    # This is tricky because sys.argv doesn't contain the -m flag
    # But we can infer it from the executable path structure
    if len(sys.argv) >= 1:
        # If argv[0] ends with __main__.py, it's almost certainly python -m
        if "__main__.py" in sys.argv[0]:
            return True

        # If the first argument is just "pyvider" or similar module name
        # and we're running from a __main__.py, it's likely python -m
        first_arg = Path(sys.argv[1]).name
        if first_arg in ["pyvider", "__main__.py"] or first_arg.endswith("__main__.py"):
            return True

    return False


def x__is_module_launch__mutmut_19() -> bool:
    """Check if we're running as 'python -m pyvider'."""
    # Check if we're running via __main__.py (indicates module execution)
    if len(sys.argv) >= 1 and sys.argv[0].endswith("__main__.py"):
        return True

    # Check if -m is in the original command line
    # This is tricky because sys.argv doesn't contain the -m flag
    # But we can infer it from the executable path structure
    if len(sys.argv) >= 1:
        # If argv[0] ends with __main__.py, it's almost certainly python -m
        if "__main__.py" in sys.argv[0]:
            return True

        # If the first argument is just "pyvider" or similar module name
        # and we're running from a __main__.py, it's likely python -m
        first_arg = Path(sys.argv[0]).name
        if first_arg in ["pyvider", "__main__.py"] and first_arg.endswith("__main__.py"):
            return True

    return False


def x__is_module_launch__mutmut_20() -> bool:
    """Check if we're running as 'python -m pyvider'."""
    # Check if we're running via __main__.py (indicates module execution)
    if len(sys.argv) >= 1 and sys.argv[0].endswith("__main__.py"):
        return True

    # Check if -m is in the original command line
    # This is tricky because sys.argv doesn't contain the -m flag
    # But we can infer it from the executable path structure
    if len(sys.argv) >= 1:
        # If argv[0] ends with __main__.py, it's almost certainly python -m
        if "__main__.py" in sys.argv[0]:
            return True

        # If the first argument is just "pyvider" or similar module name
        # and we're running from a __main__.py, it's likely python -m
        first_arg = Path(sys.argv[0]).name
        if first_arg not in ["pyvider", "__main__.py"] or first_arg.endswith("__main__.py"):
            return True

    return False


def x__is_module_launch__mutmut_21() -> bool:
    """Check if we're running as 'python -m pyvider'."""
    # Check if we're running via __main__.py (indicates module execution)
    if len(sys.argv) >= 1 and sys.argv[0].endswith("__main__.py"):
        return True

    # Check if -m is in the original command line
    # This is tricky because sys.argv doesn't contain the -m flag
    # But we can infer it from the executable path structure
    if len(sys.argv) >= 1:
        # If argv[0] ends with __main__.py, it's almost certainly python -m
        if "__main__.py" in sys.argv[0]:
            return True

        # If the first argument is just "pyvider" or similar module name
        # and we're running from a __main__.py, it's likely python -m
        first_arg = Path(sys.argv[0]).name
        if first_arg in ["XXpyviderXX", "__main__.py"] or first_arg.endswith("__main__.py"):
            return True

    return False


def x__is_module_launch__mutmut_22() -> bool:
    """Check if we're running as 'python -m pyvider'."""
    # Check if we're running via __main__.py (indicates module execution)
    if len(sys.argv) >= 1 and sys.argv[0].endswith("__main__.py"):
        return True

    # Check if -m is in the original command line
    # This is tricky because sys.argv doesn't contain the -m flag
    # But we can infer it from the executable path structure
    if len(sys.argv) >= 1:
        # If argv[0] ends with __main__.py, it's almost certainly python -m
        if "__main__.py" in sys.argv[0]:
            return True

        # If the first argument is just "pyvider" or similar module name
        # and we're running from a __main__.py, it's likely python -m
        first_arg = Path(sys.argv[0]).name
        if first_arg in ["PYVIDER", "__main__.py"] or first_arg.endswith("__main__.py"):
            return True

    return False


def x__is_module_launch__mutmut_23() -> bool:
    """Check if we're running as 'python -m pyvider'."""
    # Check if we're running via __main__.py (indicates module execution)
    if len(sys.argv) >= 1 and sys.argv[0].endswith("__main__.py"):
        return True

    # Check if -m is in the original command line
    # This is tricky because sys.argv doesn't contain the -m flag
    # But we can infer it from the executable path structure
    if len(sys.argv) >= 1:
        # If argv[0] ends with __main__.py, it's almost certainly python -m
        if "__main__.py" in sys.argv[0]:
            return True

        # If the first argument is just "pyvider" or similar module name
        # and we're running from a __main__.py, it's likely python -m
        first_arg = Path(sys.argv[0]).name
        if first_arg in ["pyvider", "XX__main__.pyXX"] or first_arg.endswith("__main__.py"):
            return True

    return False


def x__is_module_launch__mutmut_24() -> bool:
    """Check if we're running as 'python -m pyvider'."""
    # Check if we're running via __main__.py (indicates module execution)
    if len(sys.argv) >= 1 and sys.argv[0].endswith("__main__.py"):
        return True

    # Check if -m is in the original command line
    # This is tricky because sys.argv doesn't contain the -m flag
    # But we can infer it from the executable path structure
    if len(sys.argv) >= 1:
        # If argv[0] ends with __main__.py, it's almost certainly python -m
        if "__main__.py" in sys.argv[0]:
            return True

        # If the first argument is just "pyvider" or similar module name
        # and we're running from a __main__.py, it's likely python -m
        first_arg = Path(sys.argv[0]).name
        if first_arg in ["pyvider", "__MAIN__.PY"] or first_arg.endswith("__main__.py"):
            return True

    return False


def x__is_module_launch__mutmut_25() -> bool:
    """Check if we're running as 'python -m pyvider'."""
    # Check if we're running via __main__.py (indicates module execution)
    if len(sys.argv) >= 1 and sys.argv[0].endswith("__main__.py"):
        return True

    # Check if -m is in the original command line
    # This is tricky because sys.argv doesn't contain the -m flag
    # But we can infer it from the executable path structure
    if len(sys.argv) >= 1:
        # If argv[0] ends with __main__.py, it's almost certainly python -m
        if "__main__.py" in sys.argv[0]:
            return True

        # If the first argument is just "pyvider" or similar module name
        # and we're running from a __main__.py, it's likely python -m
        first_arg = Path(sys.argv[0]).name
        if first_arg in ["pyvider", "__main__.py"] or first_arg.endswith(None):
            return True

    return False


def x__is_module_launch__mutmut_26() -> bool:
    """Check if we're running as 'python -m pyvider'."""
    # Check if we're running via __main__.py (indicates module execution)
    if len(sys.argv) >= 1 and sys.argv[0].endswith("__main__.py"):
        return True

    # Check if -m is in the original command line
    # This is tricky because sys.argv doesn't contain the -m flag
    # But we can infer it from the executable path structure
    if len(sys.argv) >= 1:
        # If argv[0] ends with __main__.py, it's almost certainly python -m
        if "__main__.py" in sys.argv[0]:
            return True

        # If the first argument is just "pyvider" or similar module name
        # and we're running from a __main__.py, it's likely python -m
        first_arg = Path(sys.argv[0]).name
        if first_arg in ["pyvider", "__main__.py"] or first_arg.endswith("XX__main__.pyXX"):
            return True

    return False


def x__is_module_launch__mutmut_27() -> bool:
    """Check if we're running as 'python -m pyvider'."""
    # Check if we're running via __main__.py (indicates module execution)
    if len(sys.argv) >= 1 and sys.argv[0].endswith("__main__.py"):
        return True

    # Check if -m is in the original command line
    # This is tricky because sys.argv doesn't contain the -m flag
    # But we can infer it from the executable path structure
    if len(sys.argv) >= 1:
        # If argv[0] ends with __main__.py, it's almost certainly python -m
        if "__main__.py" in sys.argv[0]:
            return True

        # If the first argument is just "pyvider" or similar module name
        # and we're running from a __main__.py, it's likely python -m
        first_arg = Path(sys.argv[0]).name
        if first_arg in ["pyvider", "__main__.py"] or first_arg.endswith("__MAIN__.PY"):
            return True

    return False


def x__is_module_launch__mutmut_28() -> bool:
    """Check if we're running as 'python -m pyvider'."""
    # Check if we're running via __main__.py (indicates module execution)
    if len(sys.argv) >= 1 and sys.argv[0].endswith("__main__.py"):
        return True

    # Check if -m is in the original command line
    # This is tricky because sys.argv doesn't contain the -m flag
    # But we can infer it from the executable path structure
    if len(sys.argv) >= 1:
        # If argv[0] ends with __main__.py, it's almost certainly python -m
        if "__main__.py" in sys.argv[0]:
            return True

        # If the first argument is just "pyvider" or similar module name
        # and we're running from a __main__.py, it's likely python -m
        first_arg = Path(sys.argv[0]).name
        if first_arg in ["pyvider", "__main__.py"] or first_arg.endswith("__main__.py"):
            return False

    return False


def x__is_module_launch__mutmut_29() -> bool:
    """Check if we're running as 'python -m pyvider'."""
    # Check if we're running via __main__.py (indicates module execution)
    if len(sys.argv) >= 1 and sys.argv[0].endswith("__main__.py"):
        return True

    # Check if -m is in the original command line
    # This is tricky because sys.argv doesn't contain the -m flag
    # But we can infer it from the executable path structure
    if len(sys.argv) >= 1:
        # If argv[0] ends with __main__.py, it's almost certainly python -m
        if "__main__.py" in sys.argv[0]:
            return True

        # If the first argument is just "pyvider" or similar module name
        # and we're running from a __main__.py, it's likely python -m
        first_arg = Path(sys.argv[0]).name
        if first_arg in ["pyvider", "__main__.py"] or first_arg.endswith("__main__.py"):
            return True

    return True

x__is_module_launch__mutmut_mutants : ClassVar[MutantDict] = {
'x__is_module_launch__mutmut_1': x__is_module_launch__mutmut_1, 
    'x__is_module_launch__mutmut_2': x__is_module_launch__mutmut_2, 
    'x__is_module_launch__mutmut_3': x__is_module_launch__mutmut_3, 
    'x__is_module_launch__mutmut_4': x__is_module_launch__mutmut_4, 
    'x__is_module_launch__mutmut_5': x__is_module_launch__mutmut_5, 
    'x__is_module_launch__mutmut_6': x__is_module_launch__mutmut_6, 
    'x__is_module_launch__mutmut_7': x__is_module_launch__mutmut_7, 
    'x__is_module_launch__mutmut_8': x__is_module_launch__mutmut_8, 
    'x__is_module_launch__mutmut_9': x__is_module_launch__mutmut_9, 
    'x__is_module_launch__mutmut_10': x__is_module_launch__mutmut_10, 
    'x__is_module_launch__mutmut_11': x__is_module_launch__mutmut_11, 
    'x__is_module_launch__mutmut_12': x__is_module_launch__mutmut_12, 
    'x__is_module_launch__mutmut_13': x__is_module_launch__mutmut_13, 
    'x__is_module_launch__mutmut_14': x__is_module_launch__mutmut_14, 
    'x__is_module_launch__mutmut_15': x__is_module_launch__mutmut_15, 
    'x__is_module_launch__mutmut_16': x__is_module_launch__mutmut_16, 
    'x__is_module_launch__mutmut_17': x__is_module_launch__mutmut_17, 
    'x__is_module_launch__mutmut_18': x__is_module_launch__mutmut_18, 
    'x__is_module_launch__mutmut_19': x__is_module_launch__mutmut_19, 
    'x__is_module_launch__mutmut_20': x__is_module_launch__mutmut_20, 
    'x__is_module_launch__mutmut_21': x__is_module_launch__mutmut_21, 
    'x__is_module_launch__mutmut_22': x__is_module_launch__mutmut_22, 
    'x__is_module_launch__mutmut_23': x__is_module_launch__mutmut_23, 
    'x__is_module_launch__mutmut_24': x__is_module_launch__mutmut_24, 
    'x__is_module_launch__mutmut_25': x__is_module_launch__mutmut_25, 
    'x__is_module_launch__mutmut_26': x__is_module_launch__mutmut_26, 
    'x__is_module_launch__mutmut_27': x__is_module_launch__mutmut_27, 
    'x__is_module_launch__mutmut_28': x__is_module_launch__mutmut_28, 
    'x__is_module_launch__mutmut_29': x__is_module_launch__mutmut_29
}

def _is_module_launch(*args, **kwargs):
    result = _mutmut_trampoline(x__is_module_launch__mutmut_orig, x__is_module_launch__mutmut_mutants, args, kwargs)
    return result 

_is_module_launch.__signature__ = _mutmut_signature(x__is_module_launch__mutmut_orig)
x__is_module_launch__mutmut_orig.__name__ = 'x__is_module_launch'


def x__is_editable_install__mutmut_orig(executable_path: str) -> bool:
    """Check if we're running from an editable install."""
    exe_path = Path(executable_path)

    # Look for .egg-link files or site-packages with -e installs
    try:
        # Check if the executable is in a venv/conda env
        if any(env_dir in str(exe_path) for env_dir in [".venv", "venv", "conda", "anaconda"]):
            return True

        # Check if we can find pyvider in development mode
        import pyvider

        pyvider_path = Path(pyvider.__file__).parent.parent.parent
        if pyvider_path.name == "src":  # typical editable install structure
            return True

    except (ImportError, AttributeError):
        pass

    return False


def x__is_editable_install__mutmut_1(executable_path: str) -> bool:
    """Check if we're running from an editable install."""
    exe_path = None

    # Look for .egg-link files or site-packages with -e installs
    try:
        # Check if the executable is in a venv/conda env
        if any(env_dir in str(exe_path) for env_dir in [".venv", "venv", "conda", "anaconda"]):
            return True

        # Check if we can find pyvider in development mode
        import pyvider

        pyvider_path = Path(pyvider.__file__).parent.parent.parent
        if pyvider_path.name == "src":  # typical editable install structure
            return True

    except (ImportError, AttributeError):
        pass

    return False


def x__is_editable_install__mutmut_2(executable_path: str) -> bool:
    """Check if we're running from an editable install."""
    exe_path = Path(None)

    # Look for .egg-link files or site-packages with -e installs
    try:
        # Check if the executable is in a venv/conda env
        if any(env_dir in str(exe_path) for env_dir in [".venv", "venv", "conda", "anaconda"]):
            return True

        # Check if we can find pyvider in development mode
        import pyvider

        pyvider_path = Path(pyvider.__file__).parent.parent.parent
        if pyvider_path.name == "src":  # typical editable install structure
            return True

    except (ImportError, AttributeError):
        pass

    return False


def x__is_editable_install__mutmut_3(executable_path: str) -> bool:
    """Check if we're running from an editable install."""
    exe_path = Path(executable_path)

    # Look for .egg-link files or site-packages with -e installs
    try:
        # Check if the executable is in a venv/conda env
        if any(None):
            return True

        # Check if we can find pyvider in development mode
        import pyvider

        pyvider_path = Path(pyvider.__file__).parent.parent.parent
        if pyvider_path.name == "src":  # typical editable install structure
            return True

    except (ImportError, AttributeError):
        pass

    return False


def x__is_editable_install__mutmut_4(executable_path: str) -> bool:
    """Check if we're running from an editable install."""
    exe_path = Path(executable_path)

    # Look for .egg-link files or site-packages with -e installs
    try:
        # Check if the executable is in a venv/conda env
        if any(env_dir not in str(exe_path) for env_dir in [".venv", "venv", "conda", "anaconda"]):
            return True

        # Check if we can find pyvider in development mode
        import pyvider

        pyvider_path = Path(pyvider.__file__).parent.parent.parent
        if pyvider_path.name == "src":  # typical editable install structure
            return True

    except (ImportError, AttributeError):
        pass

    return False


def x__is_editable_install__mutmut_5(executable_path: str) -> bool:
    """Check if we're running from an editable install."""
    exe_path = Path(executable_path)

    # Look for .egg-link files or site-packages with -e installs
    try:
        # Check if the executable is in a venv/conda env
        if any(env_dir in str(None) for env_dir in [".venv", "venv", "conda", "anaconda"]):
            return True

        # Check if we can find pyvider in development mode
        import pyvider

        pyvider_path = Path(pyvider.__file__).parent.parent.parent
        if pyvider_path.name == "src":  # typical editable install structure
            return True

    except (ImportError, AttributeError):
        pass

    return False


def x__is_editable_install__mutmut_6(executable_path: str) -> bool:
    """Check if we're running from an editable install."""
    exe_path = Path(executable_path)

    # Look for .egg-link files or site-packages with -e installs
    try:
        # Check if the executable is in a venv/conda env
        if any(env_dir in str(exe_path) for env_dir in ["XX.venvXX", "venv", "conda", "anaconda"]):
            return True

        # Check if we can find pyvider in development mode
        import pyvider

        pyvider_path = Path(pyvider.__file__).parent.parent.parent
        if pyvider_path.name == "src":  # typical editable install structure
            return True

    except (ImportError, AttributeError):
        pass

    return False


def x__is_editable_install__mutmut_7(executable_path: str) -> bool:
    """Check if we're running from an editable install."""
    exe_path = Path(executable_path)

    # Look for .egg-link files or site-packages with -e installs
    try:
        # Check if the executable is in a venv/conda env
        if any(env_dir in str(exe_path) for env_dir in [".VENV", "venv", "conda", "anaconda"]):
            return True

        # Check if we can find pyvider in development mode
        import pyvider

        pyvider_path = Path(pyvider.__file__).parent.parent.parent
        if pyvider_path.name == "src":  # typical editable install structure
            return True

    except (ImportError, AttributeError):
        pass

    return False


def x__is_editable_install__mutmut_8(executable_path: str) -> bool:
    """Check if we're running from an editable install."""
    exe_path = Path(executable_path)

    # Look for .egg-link files or site-packages with -e installs
    try:
        # Check if the executable is in a venv/conda env
        if any(env_dir in str(exe_path) for env_dir in [".venv", "XXvenvXX", "conda", "anaconda"]):
            return True

        # Check if we can find pyvider in development mode
        import pyvider

        pyvider_path = Path(pyvider.__file__).parent.parent.parent
        if pyvider_path.name == "src":  # typical editable install structure
            return True

    except (ImportError, AttributeError):
        pass

    return False


def x__is_editable_install__mutmut_9(executable_path: str) -> bool:
    """Check if we're running from an editable install."""
    exe_path = Path(executable_path)

    # Look for .egg-link files or site-packages with -e installs
    try:
        # Check if the executable is in a venv/conda env
        if any(env_dir in str(exe_path) for env_dir in [".venv", "VENV", "conda", "anaconda"]):
            return True

        # Check if we can find pyvider in development mode
        import pyvider

        pyvider_path = Path(pyvider.__file__).parent.parent.parent
        if pyvider_path.name == "src":  # typical editable install structure
            return True

    except (ImportError, AttributeError):
        pass

    return False


def x__is_editable_install__mutmut_10(executable_path: str) -> bool:
    """Check if we're running from an editable install."""
    exe_path = Path(executable_path)

    # Look for .egg-link files or site-packages with -e installs
    try:
        # Check if the executable is in a venv/conda env
        if any(env_dir in str(exe_path) for env_dir in [".venv", "venv", "XXcondaXX", "anaconda"]):
            return True

        # Check if we can find pyvider in development mode
        import pyvider

        pyvider_path = Path(pyvider.__file__).parent.parent.parent
        if pyvider_path.name == "src":  # typical editable install structure
            return True

    except (ImportError, AttributeError):
        pass

    return False


def x__is_editable_install__mutmut_11(executable_path: str) -> bool:
    """Check if we're running from an editable install."""
    exe_path = Path(executable_path)

    # Look for .egg-link files or site-packages with -e installs
    try:
        # Check if the executable is in a venv/conda env
        if any(env_dir in str(exe_path) for env_dir in [".venv", "venv", "CONDA", "anaconda"]):
            return True

        # Check if we can find pyvider in development mode
        import pyvider

        pyvider_path = Path(pyvider.__file__).parent.parent.parent
        if pyvider_path.name == "src":  # typical editable install structure
            return True

    except (ImportError, AttributeError):
        pass

    return False


def x__is_editable_install__mutmut_12(executable_path: str) -> bool:
    """Check if we're running from an editable install."""
    exe_path = Path(executable_path)

    # Look for .egg-link files or site-packages with -e installs
    try:
        # Check if the executable is in a venv/conda env
        if any(env_dir in str(exe_path) for env_dir in [".venv", "venv", "conda", "XXanacondaXX"]):
            return True

        # Check if we can find pyvider in development mode
        import pyvider

        pyvider_path = Path(pyvider.__file__).parent.parent.parent
        if pyvider_path.name == "src":  # typical editable install structure
            return True

    except (ImportError, AttributeError):
        pass

    return False


def x__is_editable_install__mutmut_13(executable_path: str) -> bool:
    """Check if we're running from an editable install."""
    exe_path = Path(executable_path)

    # Look for .egg-link files or site-packages with -e installs
    try:
        # Check if the executable is in a venv/conda env
        if any(env_dir in str(exe_path) for env_dir in [".venv", "venv", "conda", "ANACONDA"]):
            return True

        # Check if we can find pyvider in development mode
        import pyvider

        pyvider_path = Path(pyvider.__file__).parent.parent.parent
        if pyvider_path.name == "src":  # typical editable install structure
            return True

    except (ImportError, AttributeError):
        pass

    return False


def x__is_editable_install__mutmut_14(executable_path: str) -> bool:
    """Check if we're running from an editable install."""
    exe_path = Path(executable_path)

    # Look for .egg-link files or site-packages with -e installs
    try:
        # Check if the executable is in a venv/conda env
        if any(env_dir in str(exe_path) for env_dir in [".venv", "venv", "conda", "anaconda"]):
            return False

        # Check if we can find pyvider in development mode
        import pyvider

        pyvider_path = Path(pyvider.__file__).parent.parent.parent
        if pyvider_path.name == "src":  # typical editable install structure
            return True

    except (ImportError, AttributeError):
        pass

    return False


def x__is_editable_install__mutmut_15(executable_path: str) -> bool:
    """Check if we're running from an editable install."""
    exe_path = Path(executable_path)

    # Look for .egg-link files or site-packages with -e installs
    try:
        # Check if the executable is in a venv/conda env
        if any(env_dir in str(exe_path) for env_dir in [".venv", "venv", "conda", "anaconda"]):
            return True

        # Check if we can find pyvider in development mode
        import pyvider

        pyvider_path = None
        if pyvider_path.name == "src":  # typical editable install structure
            return True

    except (ImportError, AttributeError):
        pass

    return False


def x__is_editable_install__mutmut_16(executable_path: str) -> bool:
    """Check if we're running from an editable install."""
    exe_path = Path(executable_path)

    # Look for .egg-link files or site-packages with -e installs
    try:
        # Check if the executable is in a venv/conda env
        if any(env_dir in str(exe_path) for env_dir in [".venv", "venv", "conda", "anaconda"]):
            return True

        # Check if we can find pyvider in development mode
        import pyvider

        pyvider_path = Path(None).parent.parent.parent
        if pyvider_path.name == "src":  # typical editable install structure
            return True

    except (ImportError, AttributeError):
        pass

    return False


def x__is_editable_install__mutmut_17(executable_path: str) -> bool:
    """Check if we're running from an editable install."""
    exe_path = Path(executable_path)

    # Look for .egg-link files or site-packages with -e installs
    try:
        # Check if the executable is in a venv/conda env
        if any(env_dir in str(exe_path) for env_dir in [".venv", "venv", "conda", "anaconda"]):
            return True

        # Check if we can find pyvider in development mode
        import pyvider

        pyvider_path = Path(pyvider.__file__).parent.parent.parent
        if pyvider_path.name != "src":  # typical editable install structure
            return True

    except (ImportError, AttributeError):
        pass

    return False


def x__is_editable_install__mutmut_18(executable_path: str) -> bool:
    """Check if we're running from an editable install."""
    exe_path = Path(executable_path)

    # Look for .egg-link files or site-packages with -e installs
    try:
        # Check if the executable is in a venv/conda env
        if any(env_dir in str(exe_path) for env_dir in [".venv", "venv", "conda", "anaconda"]):
            return True

        # Check if we can find pyvider in development mode
        import pyvider

        pyvider_path = Path(pyvider.__file__).parent.parent.parent
        if pyvider_path.name == "XXsrcXX":  # typical editable install structure
            return True

    except (ImportError, AttributeError):
        pass

    return False


def x__is_editable_install__mutmut_19(executable_path: str) -> bool:
    """Check if we're running from an editable install."""
    exe_path = Path(executable_path)

    # Look for .egg-link files or site-packages with -e installs
    try:
        # Check if the executable is in a venv/conda env
        if any(env_dir in str(exe_path) for env_dir in [".venv", "venv", "conda", "anaconda"]):
            return True

        # Check if we can find pyvider in development mode
        import pyvider

        pyvider_path = Path(pyvider.__file__).parent.parent.parent
        if pyvider_path.name == "SRC":  # typical editable install structure
            return True

    except (ImportError, AttributeError):
        pass

    return False


def x__is_editable_install__mutmut_20(executable_path: str) -> bool:
    """Check if we're running from an editable install."""
    exe_path = Path(executable_path)

    # Look for .egg-link files or site-packages with -e installs
    try:
        # Check if the executable is in a venv/conda env
        if any(env_dir in str(exe_path) for env_dir in [".venv", "venv", "conda", "anaconda"]):
            return True

        # Check if we can find pyvider in development mode
        import pyvider

        pyvider_path = Path(pyvider.__file__).parent.parent.parent
        if pyvider_path.name == "src":  # typical editable install structure
            return False

    except (ImportError, AttributeError):
        pass

    return False


def x__is_editable_install__mutmut_21(executable_path: str) -> bool:
    """Check if we're running from an editable install."""
    exe_path = Path(executable_path)

    # Look for .egg-link files or site-packages with -e installs
    try:
        # Check if the executable is in a venv/conda env
        if any(env_dir in str(exe_path) for env_dir in [".venv", "venv", "conda", "anaconda"]):
            return True

        # Check if we can find pyvider in development mode
        import pyvider

        pyvider_path = Path(pyvider.__file__).parent.parent.parent
        if pyvider_path.name == "src":  # typical editable install structure
            return True

    except (ImportError, AttributeError):
        pass

    return True

x__is_editable_install__mutmut_mutants : ClassVar[MutantDict] = {
'x__is_editable_install__mutmut_1': x__is_editable_install__mutmut_1, 
    'x__is_editable_install__mutmut_2': x__is_editable_install__mutmut_2, 
    'x__is_editable_install__mutmut_3': x__is_editable_install__mutmut_3, 
    'x__is_editable_install__mutmut_4': x__is_editable_install__mutmut_4, 
    'x__is_editable_install__mutmut_5': x__is_editable_install__mutmut_5, 
    'x__is_editable_install__mutmut_6': x__is_editable_install__mutmut_6, 
    'x__is_editable_install__mutmut_7': x__is_editable_install__mutmut_7, 
    'x__is_editable_install__mutmut_8': x__is_editable_install__mutmut_8, 
    'x__is_editable_install__mutmut_9': x__is_editable_install__mutmut_9, 
    'x__is_editable_install__mutmut_10': x__is_editable_install__mutmut_10, 
    'x__is_editable_install__mutmut_11': x__is_editable_install__mutmut_11, 
    'x__is_editable_install__mutmut_12': x__is_editable_install__mutmut_12, 
    'x__is_editable_install__mutmut_13': x__is_editable_install__mutmut_13, 
    'x__is_editable_install__mutmut_14': x__is_editable_install__mutmut_14, 
    'x__is_editable_install__mutmut_15': x__is_editable_install__mutmut_15, 
    'x__is_editable_install__mutmut_16': x__is_editable_install__mutmut_16, 
    'x__is_editable_install__mutmut_17': x__is_editable_install__mutmut_17, 
    'x__is_editable_install__mutmut_18': x__is_editable_install__mutmut_18, 
    'x__is_editable_install__mutmut_19': x__is_editable_install__mutmut_19, 
    'x__is_editable_install__mutmut_20': x__is_editable_install__mutmut_20, 
    'x__is_editable_install__mutmut_21': x__is_editable_install__mutmut_21
}

def _is_editable_install(*args, **kwargs):
    result = _mutmut_trampoline(x__is_editable_install__mutmut_orig, x__is_editable_install__mutmut_mutants, args, kwargs)
    return result 

_is_editable_install.__signature__ = _mutmut_signature(x__is_editable_install__mutmut_orig)
x__is_editable_install__mutmut_orig.__name__ = 'x__is_editable_install'


def x__is_direct_script_launch__mutmut_orig(executable_path: str) -> bool:
    """Check if we're running as a direct script."""
    return executable_path.endswith((".py", ".pyz")) or "python" in executable_path


def x__is_direct_script_launch__mutmut_1(executable_path: str) -> bool:
    """Check if we're running as a direct script."""
    return executable_path.endswith((".py", ".pyz")) and "python" in executable_path


def x__is_direct_script_launch__mutmut_2(executable_path: str) -> bool:
    """Check if we're running as a direct script."""
    return executable_path.endswith(None) or "python" in executable_path


def x__is_direct_script_launch__mutmut_3(executable_path: str) -> bool:
    """Check if we're running as a direct script."""
    return executable_path.endswith(("XX.pyXX", ".pyz")) or "python" in executable_path


def x__is_direct_script_launch__mutmut_4(executable_path: str) -> bool:
    """Check if we're running as a direct script."""
    return executable_path.endswith((".PY", ".pyz")) or "python" in executable_path


def x__is_direct_script_launch__mutmut_5(executable_path: str) -> bool:
    """Check if we're running as a direct script."""
    return executable_path.endswith((".py", "XX.pyzXX")) or "python" in executable_path


def x__is_direct_script_launch__mutmut_6(executable_path: str) -> bool:
    """Check if we're running as a direct script."""
    return executable_path.endswith((".py", ".PYZ")) or "python" in executable_path


def x__is_direct_script_launch__mutmut_7(executable_path: str) -> bool:
    """Check if we're running as a direct script."""
    return executable_path.endswith((".py", ".pyz")) or "XXpythonXX" in executable_path


def x__is_direct_script_launch__mutmut_8(executable_path: str) -> bool:
    """Check if we're running as a direct script."""
    return executable_path.endswith((".py", ".pyz")) or "PYTHON" in executable_path


def x__is_direct_script_launch__mutmut_9(executable_path: str) -> bool:
    """Check if we're running as a direct script."""
    return executable_path.endswith((".py", ".pyz")) or "python" not in executable_path

x__is_direct_script_launch__mutmut_mutants : ClassVar[MutantDict] = {
'x__is_direct_script_launch__mutmut_1': x__is_direct_script_launch__mutmut_1, 
    'x__is_direct_script_launch__mutmut_2': x__is_direct_script_launch__mutmut_2, 
    'x__is_direct_script_launch__mutmut_3': x__is_direct_script_launch__mutmut_3, 
    'x__is_direct_script_launch__mutmut_4': x__is_direct_script_launch__mutmut_4, 
    'x__is_direct_script_launch__mutmut_5': x__is_direct_script_launch__mutmut_5, 
    'x__is_direct_script_launch__mutmut_6': x__is_direct_script_launch__mutmut_6, 
    'x__is_direct_script_launch__mutmut_7': x__is_direct_script_launch__mutmut_7, 
    'x__is_direct_script_launch__mutmut_8': x__is_direct_script_launch__mutmut_8, 
    'x__is_direct_script_launch__mutmut_9': x__is_direct_script_launch__mutmut_9
}

def _is_direct_script_launch(*args, **kwargs):
    result = _mutmut_trampoline(x__is_direct_script_launch__mutmut_orig, x__is_direct_script_launch__mutmut_mutants, args, kwargs)
    return result 

_is_direct_script_launch.__signature__ = _mutmut_signature(x__is_direct_script_launch__mutmut_orig)
x__is_direct_script_launch__mutmut_orig.__name__ = 'x__is_direct_script_launch'


def x__get_pspf_details__mutmut_orig() -> dict[str, Any]:
    """Get details specific to PSPF launches."""
    details: dict[str, Any] = {}

    # Try to find PSPF cache information
    python_path = Path(sys.executable)
    details["python_cache_path"] = str(python_path.parent.parent)
    details["cache_structure"] = _analyze_cache_structure(python_path)

    # Look for PSPF metadata
    cache_dir = python_path.parent.parent
    metadata_paths = [
        cache_dir / "metadata",
        cache_dir / "cache" / "metadata",
    ]

    for metadata_path in metadata_paths:
        if metadata_path.exists():
            details["metadata_path"] = str(metadata_path)
            break

    return details


def x__get_pspf_details__mutmut_1() -> dict[str, Any]:
    """Get details specific to PSPF launches."""
    details: dict[str, Any] = None

    # Try to find PSPF cache information
    python_path = Path(sys.executable)
    details["python_cache_path"] = str(python_path.parent.parent)
    details["cache_structure"] = _analyze_cache_structure(python_path)

    # Look for PSPF metadata
    cache_dir = python_path.parent.parent
    metadata_paths = [
        cache_dir / "metadata",
        cache_dir / "cache" / "metadata",
    ]

    for metadata_path in metadata_paths:
        if metadata_path.exists():
            details["metadata_path"] = str(metadata_path)
            break

    return details


def x__get_pspf_details__mutmut_2() -> dict[str, Any]:
    """Get details specific to PSPF launches."""
    details: dict[str, Any] = {}

    # Try to find PSPF cache information
    python_path = None
    details["python_cache_path"] = str(python_path.parent.parent)
    details["cache_structure"] = _analyze_cache_structure(python_path)

    # Look for PSPF metadata
    cache_dir = python_path.parent.parent
    metadata_paths = [
        cache_dir / "metadata",
        cache_dir / "cache" / "metadata",
    ]

    for metadata_path in metadata_paths:
        if metadata_path.exists():
            details["metadata_path"] = str(metadata_path)
            break

    return details


def x__get_pspf_details__mutmut_3() -> dict[str, Any]:
    """Get details specific to PSPF launches."""
    details: dict[str, Any] = {}

    # Try to find PSPF cache information
    python_path = Path(None)
    details["python_cache_path"] = str(python_path.parent.parent)
    details["cache_structure"] = _analyze_cache_structure(python_path)

    # Look for PSPF metadata
    cache_dir = python_path.parent.parent
    metadata_paths = [
        cache_dir / "metadata",
        cache_dir / "cache" / "metadata",
    ]

    for metadata_path in metadata_paths:
        if metadata_path.exists():
            details["metadata_path"] = str(metadata_path)
            break

    return details


def x__get_pspf_details__mutmut_4() -> dict[str, Any]:
    """Get details specific to PSPF launches."""
    details: dict[str, Any] = {}

    # Try to find PSPF cache information
    python_path = Path(sys.executable)
    details["python_cache_path"] = None
    details["cache_structure"] = _analyze_cache_structure(python_path)

    # Look for PSPF metadata
    cache_dir = python_path.parent.parent
    metadata_paths = [
        cache_dir / "metadata",
        cache_dir / "cache" / "metadata",
    ]

    for metadata_path in metadata_paths:
        if metadata_path.exists():
            details["metadata_path"] = str(metadata_path)
            break

    return details


def x__get_pspf_details__mutmut_5() -> dict[str, Any]:
    """Get details specific to PSPF launches."""
    details: dict[str, Any] = {}

    # Try to find PSPF cache information
    python_path = Path(sys.executable)
    details["XXpython_cache_pathXX"] = str(python_path.parent.parent)
    details["cache_structure"] = _analyze_cache_structure(python_path)

    # Look for PSPF metadata
    cache_dir = python_path.parent.parent
    metadata_paths = [
        cache_dir / "metadata",
        cache_dir / "cache" / "metadata",
    ]

    for metadata_path in metadata_paths:
        if metadata_path.exists():
            details["metadata_path"] = str(metadata_path)
            break

    return details


def x__get_pspf_details__mutmut_6() -> dict[str, Any]:
    """Get details specific to PSPF launches."""
    details: dict[str, Any] = {}

    # Try to find PSPF cache information
    python_path = Path(sys.executable)
    details["PYTHON_CACHE_PATH"] = str(python_path.parent.parent)
    details["cache_structure"] = _analyze_cache_structure(python_path)

    # Look for PSPF metadata
    cache_dir = python_path.parent.parent
    metadata_paths = [
        cache_dir / "metadata",
        cache_dir / "cache" / "metadata",
    ]

    for metadata_path in metadata_paths:
        if metadata_path.exists():
            details["metadata_path"] = str(metadata_path)
            break

    return details


def x__get_pspf_details__mutmut_7() -> dict[str, Any]:
    """Get details specific to PSPF launches."""
    details: dict[str, Any] = {}

    # Try to find PSPF cache information
    python_path = Path(sys.executable)
    details["python_cache_path"] = str(None)
    details["cache_structure"] = _analyze_cache_structure(python_path)

    # Look for PSPF metadata
    cache_dir = python_path.parent.parent
    metadata_paths = [
        cache_dir / "metadata",
        cache_dir / "cache" / "metadata",
    ]

    for metadata_path in metadata_paths:
        if metadata_path.exists():
            details["metadata_path"] = str(metadata_path)
            break

    return details


def x__get_pspf_details__mutmut_8() -> dict[str, Any]:
    """Get details specific to PSPF launches."""
    details: dict[str, Any] = {}

    # Try to find PSPF cache information
    python_path = Path(sys.executable)
    details["python_cache_path"] = str(python_path.parent.parent)
    details["cache_structure"] = None

    # Look for PSPF metadata
    cache_dir = python_path.parent.parent
    metadata_paths = [
        cache_dir / "metadata",
        cache_dir / "cache" / "metadata",
    ]

    for metadata_path in metadata_paths:
        if metadata_path.exists():
            details["metadata_path"] = str(metadata_path)
            break

    return details


def x__get_pspf_details__mutmut_9() -> dict[str, Any]:
    """Get details specific to PSPF launches."""
    details: dict[str, Any] = {}

    # Try to find PSPF cache information
    python_path = Path(sys.executable)
    details["python_cache_path"] = str(python_path.parent.parent)
    details["XXcache_structureXX"] = _analyze_cache_structure(python_path)

    # Look for PSPF metadata
    cache_dir = python_path.parent.parent
    metadata_paths = [
        cache_dir / "metadata",
        cache_dir / "cache" / "metadata",
    ]

    for metadata_path in metadata_paths:
        if metadata_path.exists():
            details["metadata_path"] = str(metadata_path)
            break

    return details


def x__get_pspf_details__mutmut_10() -> dict[str, Any]:
    """Get details specific to PSPF launches."""
    details: dict[str, Any] = {}

    # Try to find PSPF cache information
    python_path = Path(sys.executable)
    details["python_cache_path"] = str(python_path.parent.parent)
    details["CACHE_STRUCTURE"] = _analyze_cache_structure(python_path)

    # Look for PSPF metadata
    cache_dir = python_path.parent.parent
    metadata_paths = [
        cache_dir / "metadata",
        cache_dir / "cache" / "metadata",
    ]

    for metadata_path in metadata_paths:
        if metadata_path.exists():
            details["metadata_path"] = str(metadata_path)
            break

    return details


def x__get_pspf_details__mutmut_11() -> dict[str, Any]:
    """Get details specific to PSPF launches."""
    details: dict[str, Any] = {}

    # Try to find PSPF cache information
    python_path = Path(sys.executable)
    details["python_cache_path"] = str(python_path.parent.parent)
    details["cache_structure"] = _analyze_cache_structure(None)

    # Look for PSPF metadata
    cache_dir = python_path.parent.parent
    metadata_paths = [
        cache_dir / "metadata",
        cache_dir / "cache" / "metadata",
    ]

    for metadata_path in metadata_paths:
        if metadata_path.exists():
            details["metadata_path"] = str(metadata_path)
            break

    return details


def x__get_pspf_details__mutmut_12() -> dict[str, Any]:
    """Get details specific to PSPF launches."""
    details: dict[str, Any] = {}

    # Try to find PSPF cache information
    python_path = Path(sys.executable)
    details["python_cache_path"] = str(python_path.parent.parent)
    details["cache_structure"] = _analyze_cache_structure(python_path)

    # Look for PSPF metadata
    cache_dir = None
    metadata_paths = [
        cache_dir / "metadata",
        cache_dir / "cache" / "metadata",
    ]

    for metadata_path in metadata_paths:
        if metadata_path.exists():
            details["metadata_path"] = str(metadata_path)
            break

    return details


def x__get_pspf_details__mutmut_13() -> dict[str, Any]:
    """Get details specific to PSPF launches."""
    details: dict[str, Any] = {}

    # Try to find PSPF cache information
    python_path = Path(sys.executable)
    details["python_cache_path"] = str(python_path.parent.parent)
    details["cache_structure"] = _analyze_cache_structure(python_path)

    # Look for PSPF metadata
    cache_dir = python_path.parent.parent
    metadata_paths = None

    for metadata_path in metadata_paths:
        if metadata_path.exists():
            details["metadata_path"] = str(metadata_path)
            break

    return details


def x__get_pspf_details__mutmut_14() -> dict[str, Any]:
    """Get details specific to PSPF launches."""
    details: dict[str, Any] = {}

    # Try to find PSPF cache information
    python_path = Path(sys.executable)
    details["python_cache_path"] = str(python_path.parent.parent)
    details["cache_structure"] = _analyze_cache_structure(python_path)

    # Look for PSPF metadata
    cache_dir = python_path.parent.parent
    metadata_paths = [
        cache_dir * "metadata",
        cache_dir / "cache" / "metadata",
    ]

    for metadata_path in metadata_paths:
        if metadata_path.exists():
            details["metadata_path"] = str(metadata_path)
            break

    return details


def x__get_pspf_details__mutmut_15() -> dict[str, Any]:
    """Get details specific to PSPF launches."""
    details: dict[str, Any] = {}

    # Try to find PSPF cache information
    python_path = Path(sys.executable)
    details["python_cache_path"] = str(python_path.parent.parent)
    details["cache_structure"] = _analyze_cache_structure(python_path)

    # Look for PSPF metadata
    cache_dir = python_path.parent.parent
    metadata_paths = [
        cache_dir / "XXmetadataXX",
        cache_dir / "cache" / "metadata",
    ]

    for metadata_path in metadata_paths:
        if metadata_path.exists():
            details["metadata_path"] = str(metadata_path)
            break

    return details


def x__get_pspf_details__mutmut_16() -> dict[str, Any]:
    """Get details specific to PSPF launches."""
    details: dict[str, Any] = {}

    # Try to find PSPF cache information
    python_path = Path(sys.executable)
    details["python_cache_path"] = str(python_path.parent.parent)
    details["cache_structure"] = _analyze_cache_structure(python_path)

    # Look for PSPF metadata
    cache_dir = python_path.parent.parent
    metadata_paths = [
        cache_dir / "METADATA",
        cache_dir / "cache" / "metadata",
    ]

    for metadata_path in metadata_paths:
        if metadata_path.exists():
            details["metadata_path"] = str(metadata_path)
            break

    return details


def x__get_pspf_details__mutmut_17() -> dict[str, Any]:
    """Get details specific to PSPF launches."""
    details: dict[str, Any] = {}

    # Try to find PSPF cache information
    python_path = Path(sys.executable)
    details["python_cache_path"] = str(python_path.parent.parent)
    details["cache_structure"] = _analyze_cache_structure(python_path)

    # Look for PSPF metadata
    cache_dir = python_path.parent.parent
    metadata_paths = [
        cache_dir / "metadata",
        cache_dir / "cache" * "metadata",
    ]

    for metadata_path in metadata_paths:
        if metadata_path.exists():
            details["metadata_path"] = str(metadata_path)
            break

    return details


def x__get_pspf_details__mutmut_18() -> dict[str, Any]:
    """Get details specific to PSPF launches."""
    details: dict[str, Any] = {}

    # Try to find PSPF cache information
    python_path = Path(sys.executable)
    details["python_cache_path"] = str(python_path.parent.parent)
    details["cache_structure"] = _analyze_cache_structure(python_path)

    # Look for PSPF metadata
    cache_dir = python_path.parent.parent
    metadata_paths = [
        cache_dir / "metadata",
        cache_dir * "cache" / "metadata",
    ]

    for metadata_path in metadata_paths:
        if metadata_path.exists():
            details["metadata_path"] = str(metadata_path)
            break

    return details


def x__get_pspf_details__mutmut_19() -> dict[str, Any]:
    """Get details specific to PSPF launches."""
    details: dict[str, Any] = {}

    # Try to find PSPF cache information
    python_path = Path(sys.executable)
    details["python_cache_path"] = str(python_path.parent.parent)
    details["cache_structure"] = _analyze_cache_structure(python_path)

    # Look for PSPF metadata
    cache_dir = python_path.parent.parent
    metadata_paths = [
        cache_dir / "metadata",
        cache_dir / "XXcacheXX" / "metadata",
    ]

    for metadata_path in metadata_paths:
        if metadata_path.exists():
            details["metadata_path"] = str(metadata_path)
            break

    return details


def x__get_pspf_details__mutmut_20() -> dict[str, Any]:
    """Get details specific to PSPF launches."""
    details: dict[str, Any] = {}

    # Try to find PSPF cache information
    python_path = Path(sys.executable)
    details["python_cache_path"] = str(python_path.parent.parent)
    details["cache_structure"] = _analyze_cache_structure(python_path)

    # Look for PSPF metadata
    cache_dir = python_path.parent.parent
    metadata_paths = [
        cache_dir / "metadata",
        cache_dir / "CACHE" / "metadata",
    ]

    for metadata_path in metadata_paths:
        if metadata_path.exists():
            details["metadata_path"] = str(metadata_path)
            break

    return details


def x__get_pspf_details__mutmut_21() -> dict[str, Any]:
    """Get details specific to PSPF launches."""
    details: dict[str, Any] = {}

    # Try to find PSPF cache information
    python_path = Path(sys.executable)
    details["python_cache_path"] = str(python_path.parent.parent)
    details["cache_structure"] = _analyze_cache_structure(python_path)

    # Look for PSPF metadata
    cache_dir = python_path.parent.parent
    metadata_paths = [
        cache_dir / "metadata",
        cache_dir / "cache" / "XXmetadataXX",
    ]

    for metadata_path in metadata_paths:
        if metadata_path.exists():
            details["metadata_path"] = str(metadata_path)
            break

    return details


def x__get_pspf_details__mutmut_22() -> dict[str, Any]:
    """Get details specific to PSPF launches."""
    details: dict[str, Any] = {}

    # Try to find PSPF cache information
    python_path = Path(sys.executable)
    details["python_cache_path"] = str(python_path.parent.parent)
    details["cache_structure"] = _analyze_cache_structure(python_path)

    # Look for PSPF metadata
    cache_dir = python_path.parent.parent
    metadata_paths = [
        cache_dir / "metadata",
        cache_dir / "cache" / "METADATA",
    ]

    for metadata_path in metadata_paths:
        if metadata_path.exists():
            details["metadata_path"] = str(metadata_path)
            break

    return details


def x__get_pspf_details__mutmut_23() -> dict[str, Any]:
    """Get details specific to PSPF launches."""
    details: dict[str, Any] = {}

    # Try to find PSPF cache information
    python_path = Path(sys.executable)
    details["python_cache_path"] = str(python_path.parent.parent)
    details["cache_structure"] = _analyze_cache_structure(python_path)

    # Look for PSPF metadata
    cache_dir = python_path.parent.parent
    metadata_paths = [
        cache_dir / "metadata",
        cache_dir / "cache" / "metadata",
    ]

    for metadata_path in metadata_paths:
        if metadata_path.exists():
            details["metadata_path"] = None
            break

    return details


def x__get_pspf_details__mutmut_24() -> dict[str, Any]:
    """Get details specific to PSPF launches."""
    details: dict[str, Any] = {}

    # Try to find PSPF cache information
    python_path = Path(sys.executable)
    details["python_cache_path"] = str(python_path.parent.parent)
    details["cache_structure"] = _analyze_cache_structure(python_path)

    # Look for PSPF metadata
    cache_dir = python_path.parent.parent
    metadata_paths = [
        cache_dir / "metadata",
        cache_dir / "cache" / "metadata",
    ]

    for metadata_path in metadata_paths:
        if metadata_path.exists():
            details["XXmetadata_pathXX"] = str(metadata_path)
            break

    return details


def x__get_pspf_details__mutmut_25() -> dict[str, Any]:
    """Get details specific to PSPF launches."""
    details: dict[str, Any] = {}

    # Try to find PSPF cache information
    python_path = Path(sys.executable)
    details["python_cache_path"] = str(python_path.parent.parent)
    details["cache_structure"] = _analyze_cache_structure(python_path)

    # Look for PSPF metadata
    cache_dir = python_path.parent.parent
    metadata_paths = [
        cache_dir / "metadata",
        cache_dir / "cache" / "metadata",
    ]

    for metadata_path in metadata_paths:
        if metadata_path.exists():
            details["METADATA_PATH"] = str(metadata_path)
            break

    return details


def x__get_pspf_details__mutmut_26() -> dict[str, Any]:
    """Get details specific to PSPF launches."""
    details: dict[str, Any] = {}

    # Try to find PSPF cache information
    python_path = Path(sys.executable)
    details["python_cache_path"] = str(python_path.parent.parent)
    details["cache_structure"] = _analyze_cache_structure(python_path)

    # Look for PSPF metadata
    cache_dir = python_path.parent.parent
    metadata_paths = [
        cache_dir / "metadata",
        cache_dir / "cache" / "metadata",
    ]

    for metadata_path in metadata_paths:
        if metadata_path.exists():
            details["metadata_path"] = str(None)
            break

    return details


def x__get_pspf_details__mutmut_27() -> dict[str, Any]:
    """Get details specific to PSPF launches."""
    details: dict[str, Any] = {}

    # Try to find PSPF cache information
    python_path = Path(sys.executable)
    details["python_cache_path"] = str(python_path.parent.parent)
    details["cache_structure"] = _analyze_cache_structure(python_path)

    # Look for PSPF metadata
    cache_dir = python_path.parent.parent
    metadata_paths = [
        cache_dir / "metadata",
        cache_dir / "cache" / "metadata",
    ]

    for metadata_path in metadata_paths:
        if metadata_path.exists():
            details["metadata_path"] = str(metadata_path)
            return

    return details

x__get_pspf_details__mutmut_mutants : ClassVar[MutantDict] = {
'x__get_pspf_details__mutmut_1': x__get_pspf_details__mutmut_1, 
    'x__get_pspf_details__mutmut_2': x__get_pspf_details__mutmut_2, 
    'x__get_pspf_details__mutmut_3': x__get_pspf_details__mutmut_3, 
    'x__get_pspf_details__mutmut_4': x__get_pspf_details__mutmut_4, 
    'x__get_pspf_details__mutmut_5': x__get_pspf_details__mutmut_5, 
    'x__get_pspf_details__mutmut_6': x__get_pspf_details__mutmut_6, 
    'x__get_pspf_details__mutmut_7': x__get_pspf_details__mutmut_7, 
    'x__get_pspf_details__mutmut_8': x__get_pspf_details__mutmut_8, 
    'x__get_pspf_details__mutmut_9': x__get_pspf_details__mutmut_9, 
    'x__get_pspf_details__mutmut_10': x__get_pspf_details__mutmut_10, 
    'x__get_pspf_details__mutmut_11': x__get_pspf_details__mutmut_11, 
    'x__get_pspf_details__mutmut_12': x__get_pspf_details__mutmut_12, 
    'x__get_pspf_details__mutmut_13': x__get_pspf_details__mutmut_13, 
    'x__get_pspf_details__mutmut_14': x__get_pspf_details__mutmut_14, 
    'x__get_pspf_details__mutmut_15': x__get_pspf_details__mutmut_15, 
    'x__get_pspf_details__mutmut_16': x__get_pspf_details__mutmut_16, 
    'x__get_pspf_details__mutmut_17': x__get_pspf_details__mutmut_17, 
    'x__get_pspf_details__mutmut_18': x__get_pspf_details__mutmut_18, 
    'x__get_pspf_details__mutmut_19': x__get_pspf_details__mutmut_19, 
    'x__get_pspf_details__mutmut_20': x__get_pspf_details__mutmut_20, 
    'x__get_pspf_details__mutmut_21': x__get_pspf_details__mutmut_21, 
    'x__get_pspf_details__mutmut_22': x__get_pspf_details__mutmut_22, 
    'x__get_pspf_details__mutmut_23': x__get_pspf_details__mutmut_23, 
    'x__get_pspf_details__mutmut_24': x__get_pspf_details__mutmut_24, 
    'x__get_pspf_details__mutmut_25': x__get_pspf_details__mutmut_25, 
    'x__get_pspf_details__mutmut_26': x__get_pspf_details__mutmut_26, 
    'x__get_pspf_details__mutmut_27': x__get_pspf_details__mutmut_27
}

def _get_pspf_details(*args, **kwargs):
    result = _mutmut_trampoline(x__get_pspf_details__mutmut_orig, x__get_pspf_details__mutmut_mutants, args, kwargs)
    return result 

_get_pspf_details.__signature__ = _mutmut_signature(x__get_pspf_details__mutmut_orig)
x__get_pspf_details__mutmut_orig.__name__ = 'x__get_pspf_details'


def x__get_module_name__mutmut_orig() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[0]
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(path_parts)):
                if part == "__main__.py" and i + 1 < len(path_parts):
                    module_name = path_parts[-(i + 2)]  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = sys.argv.index("-m")
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_1() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) > 1:
        argv0 = sys.argv[0]
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(path_parts)):
                if part == "__main__.py" and i + 1 < len(path_parts):
                    module_name = path_parts[-(i + 2)]  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = sys.argv.index("-m")
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_2() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 2:
        argv0 = sys.argv[0]
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(path_parts)):
                if part == "__main__.py" and i + 1 < len(path_parts):
                    module_name = path_parts[-(i + 2)]  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = sys.argv.index("-m")
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_3() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = None
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(path_parts)):
                if part == "__main__.py" and i + 1 < len(path_parts):
                    module_name = path_parts[-(i + 2)]  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = sys.argv.index("-m")
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_4() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[1]
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(path_parts)):
                if part == "__main__.py" and i + 1 < len(path_parts):
                    module_name = path_parts[-(i + 2)]  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = sys.argv.index("-m")
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_5() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[0]
        if "XX__main__.pyXX" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(path_parts)):
                if part == "__main__.py" and i + 1 < len(path_parts):
                    module_name = path_parts[-(i + 2)]  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = sys.argv.index("-m")
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_6() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[0]
        if "__MAIN__.PY" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(path_parts)):
                if part == "__main__.py" and i + 1 < len(path_parts):
                    module_name = path_parts[-(i + 2)]  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = sys.argv.index("-m")
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_7() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[0]
        if "__main__.py" not in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(path_parts)):
                if part == "__main__.py" and i + 1 < len(path_parts):
                    module_name = path_parts[-(i + 2)]  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = sys.argv.index("-m")
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_8() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[0]
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = None
            for i, part in enumerate(reversed(path_parts)):
                if part == "__main__.py" and i + 1 < len(path_parts):
                    module_name = path_parts[-(i + 2)]  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = sys.argv.index("-m")
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_9() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[0]
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(None).parts
            for i, part in enumerate(reversed(path_parts)):
                if part == "__main__.py" and i + 1 < len(path_parts):
                    module_name = path_parts[-(i + 2)]  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = sys.argv.index("-m")
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_10() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[0]
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(None):
                if part == "__main__.py" and i + 1 < len(path_parts):
                    module_name = path_parts[-(i + 2)]  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = sys.argv.index("-m")
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_11() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[0]
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(None)):
                if part == "__main__.py" and i + 1 < len(path_parts):
                    module_name = path_parts[-(i + 2)]  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = sys.argv.index("-m")
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_12() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[0]
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(path_parts)):
                if part == "__main__.py" or i + 1 < len(path_parts):
                    module_name = path_parts[-(i + 2)]  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = sys.argv.index("-m")
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_13() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[0]
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(path_parts)):
                if part != "__main__.py" and i + 1 < len(path_parts):
                    module_name = path_parts[-(i + 2)]  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = sys.argv.index("-m")
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_14() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[0]
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(path_parts)):
                if part == "XX__main__.pyXX" and i + 1 < len(path_parts):
                    module_name = path_parts[-(i + 2)]  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = sys.argv.index("-m")
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_15() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[0]
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(path_parts)):
                if part == "__MAIN__.PY" and i + 1 < len(path_parts):
                    module_name = path_parts[-(i + 2)]  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = sys.argv.index("-m")
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_16() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[0]
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(path_parts)):
                if part == "__main__.py" and i - 1 < len(path_parts):
                    module_name = path_parts[-(i + 2)]  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = sys.argv.index("-m")
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_17() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[0]
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(path_parts)):
                if part == "__main__.py" and i + 2 < len(path_parts):
                    module_name = path_parts[-(i + 2)]  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = sys.argv.index("-m")
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_18() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[0]
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(path_parts)):
                if part == "__main__.py" and i + 1 <= len(path_parts):
                    module_name = path_parts[-(i + 2)]  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = sys.argv.index("-m")
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_19() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[0]
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(path_parts)):
                if part == "__main__.py" and i + 1 < len(path_parts):
                    module_name = None  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = sys.argv.index("-m")
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_20() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[0]
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(path_parts)):
                if part == "__main__.py" and i + 1 < len(path_parts):
                    module_name = path_parts[+(i + 2)]  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = sys.argv.index("-m")
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_21() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[0]
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(path_parts)):
                if part == "__main__.py" and i + 1 < len(path_parts):
                    module_name = path_parts[-(i - 2)]  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = sys.argv.index("-m")
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_22() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[0]
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(path_parts)):
                if part == "__main__.py" and i + 1 < len(path_parts):
                    module_name = path_parts[-(i + 3)]  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = sys.argv.index("-m")
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_23() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[0]
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(path_parts)):
                if part == "__main__.py" and i + 1 < len(path_parts):
                    module_name = path_parts[-(i + 2)]  # Get the parent directory
                    if module_name == "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = sys.argv.index("-m")
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_24() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[0]
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(path_parts)):
                if part == "__main__.py" and i + 1 < len(path_parts):
                    module_name = path_parts[-(i + 2)]  # Get the parent directory
                    if module_name != "XXsrcXX":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = sys.argv.index("-m")
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_25() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[0]
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(path_parts)):
                if part == "__main__.py" and i + 1 < len(path_parts):
                    module_name = path_parts[-(i + 2)]  # Get the parent directory
                    if module_name != "SRC":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = sys.argv.index("-m")
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_26() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[0]
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(path_parts)):
                if part == "__main__.py" and i + 1 < len(path_parts):
                    module_name = path_parts[-(i + 2)]  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "XX-mXX" in sys.argv:
        try:
            m_index = sys.argv.index("-m")
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_27() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[0]
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(path_parts)):
                if part == "__main__.py" and i + 1 < len(path_parts):
                    module_name = path_parts[-(i + 2)]  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-M" in sys.argv:
        try:
            m_index = sys.argv.index("-m")
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_28() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[0]
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(path_parts)):
                if part == "__main__.py" and i + 1 < len(path_parts):
                    module_name = path_parts[-(i + 2)]  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" not in sys.argv:
        try:
            m_index = sys.argv.index("-m")
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_29() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[0]
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(path_parts)):
                if part == "__main__.py" and i + 1 < len(path_parts):
                    module_name = path_parts[-(i + 2)]  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = None
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_30() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[0]
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(path_parts)):
                if part == "__main__.py" and i + 1 < len(path_parts):
                    module_name = path_parts[-(i + 2)]  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = sys.argv.index(None)
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_31() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[0]
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(path_parts)):
                if part == "__main__.py" and i + 1 < len(path_parts):
                    module_name = path_parts[-(i + 2)]  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = sys.argv.rindex("-m")
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_32() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[0]
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(path_parts)):
                if part == "__main__.py" and i + 1 < len(path_parts):
                    module_name = path_parts[-(i + 2)]  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = sys.argv.index("XX-mXX")
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_33() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[0]
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(path_parts)):
                if part == "__main__.py" and i + 1 < len(path_parts):
                    module_name = path_parts[-(i + 2)]  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = sys.argv.index("-M")
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_34() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[0]
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(path_parts)):
                if part == "__main__.py" and i + 1 < len(path_parts):
                    module_name = path_parts[-(i + 2)]  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = sys.argv.index("-m")
            if m_index - 1 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_35() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[0]
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(path_parts)):
                if part == "__main__.py" and i + 1 < len(path_parts):
                    module_name = path_parts[-(i + 2)]  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = sys.argv.index("-m")
            if m_index + 2 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_36() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[0]
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(path_parts)):
                if part == "__main__.py" and i + 1 < len(path_parts):
                    module_name = path_parts[-(i + 2)]  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = sys.argv.index("-m")
            if m_index + 1 <= len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_37() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[0]
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(path_parts)):
                if part == "__main__.py" and i + 1 < len(path_parts):
                    module_name = path_parts[-(i + 2)]  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = sys.argv.index("-m")
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index - 1]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_38() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[0]
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(path_parts)):
                if part == "__main__.py" and i + 1 < len(path_parts):
                    module_name = path_parts[-(i + 2)]  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = sys.argv.index("-m")
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index + 2]
        except (ValueError, IndexError):
            pass

    return "pyvider"  # Default assumption


def x__get_module_name__mutmut_39() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[0]
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(path_parts)):
                if part == "__main__.py" and i + 1 < len(path_parts):
                    module_name = path_parts[-(i + 2)]  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = sys.argv.index("-m")
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "XXpyviderXX"  # Default assumption


def x__get_module_name__mutmut_40() -> str:
    """Get the module name being executed."""
    # For python -m execution, the module name might not be in sys.argv
    # but we can infer it from the path structure
    if len(sys.argv) >= 1:
        argv0 = sys.argv[0]
        if "__main__.py" in argv0:
            # Try to extract module name from path
            # e.g., /path/to/pyvider/src/pyvider/__main__.py -> pyvider
            path_parts = Path(argv0).parts
            for i, part in enumerate(reversed(path_parts)):
                if part == "__main__.py" and i + 1 < len(path_parts):
                    module_name = path_parts[-(i + 2)]  # Get the parent directory
                    if module_name != "src":  # Skip src directory
                        return module_name

    # Fallback: check if -m is explicitly in sys.argv (rare but possible)
    if "-m" in sys.argv:
        try:
            m_index = sys.argv.index("-m")
            if m_index + 1 < len(sys.argv):
                return sys.argv[m_index + 1]
        except (ValueError, IndexError):
            pass

    return "PYVIDER"  # Default assumption

x__get_module_name__mutmut_mutants : ClassVar[MutantDict] = {
'x__get_module_name__mutmut_1': x__get_module_name__mutmut_1, 
    'x__get_module_name__mutmut_2': x__get_module_name__mutmut_2, 
    'x__get_module_name__mutmut_3': x__get_module_name__mutmut_3, 
    'x__get_module_name__mutmut_4': x__get_module_name__mutmut_4, 
    'x__get_module_name__mutmut_5': x__get_module_name__mutmut_5, 
    'x__get_module_name__mutmut_6': x__get_module_name__mutmut_6, 
    'x__get_module_name__mutmut_7': x__get_module_name__mutmut_7, 
    'x__get_module_name__mutmut_8': x__get_module_name__mutmut_8, 
    'x__get_module_name__mutmut_9': x__get_module_name__mutmut_9, 
    'x__get_module_name__mutmut_10': x__get_module_name__mutmut_10, 
    'x__get_module_name__mutmut_11': x__get_module_name__mutmut_11, 
    'x__get_module_name__mutmut_12': x__get_module_name__mutmut_12, 
    'x__get_module_name__mutmut_13': x__get_module_name__mutmut_13, 
    'x__get_module_name__mutmut_14': x__get_module_name__mutmut_14, 
    'x__get_module_name__mutmut_15': x__get_module_name__mutmut_15, 
    'x__get_module_name__mutmut_16': x__get_module_name__mutmut_16, 
    'x__get_module_name__mutmut_17': x__get_module_name__mutmut_17, 
    'x__get_module_name__mutmut_18': x__get_module_name__mutmut_18, 
    'x__get_module_name__mutmut_19': x__get_module_name__mutmut_19, 
    'x__get_module_name__mutmut_20': x__get_module_name__mutmut_20, 
    'x__get_module_name__mutmut_21': x__get_module_name__mutmut_21, 
    'x__get_module_name__mutmut_22': x__get_module_name__mutmut_22, 
    'x__get_module_name__mutmut_23': x__get_module_name__mutmut_23, 
    'x__get_module_name__mutmut_24': x__get_module_name__mutmut_24, 
    'x__get_module_name__mutmut_25': x__get_module_name__mutmut_25, 
    'x__get_module_name__mutmut_26': x__get_module_name__mutmut_26, 
    'x__get_module_name__mutmut_27': x__get_module_name__mutmut_27, 
    'x__get_module_name__mutmut_28': x__get_module_name__mutmut_28, 
    'x__get_module_name__mutmut_29': x__get_module_name__mutmut_29, 
    'x__get_module_name__mutmut_30': x__get_module_name__mutmut_30, 
    'x__get_module_name__mutmut_31': x__get_module_name__mutmut_31, 
    'x__get_module_name__mutmut_32': x__get_module_name__mutmut_32, 
    'x__get_module_name__mutmut_33': x__get_module_name__mutmut_33, 
    'x__get_module_name__mutmut_34': x__get_module_name__mutmut_34, 
    'x__get_module_name__mutmut_35': x__get_module_name__mutmut_35, 
    'x__get_module_name__mutmut_36': x__get_module_name__mutmut_36, 
    'x__get_module_name__mutmut_37': x__get_module_name__mutmut_37, 
    'x__get_module_name__mutmut_38': x__get_module_name__mutmut_38, 
    'x__get_module_name__mutmut_39': x__get_module_name__mutmut_39, 
    'x__get_module_name__mutmut_40': x__get_module_name__mutmut_40
}

def _get_module_name(*args, **kwargs):
    result = _mutmut_trampoline(x__get_module_name__mutmut_orig, x__get_module_name__mutmut_mutants, args, kwargs)
    return result 

_get_module_name.__signature__ = _mutmut_signature(x__get_module_name__mutmut_orig)
x__get_module_name__mutmut_orig.__name__ = 'x__get_module_name'


def x__get_editable_install_details__mutmut_orig(executable_path: str) -> dict[str, Any]:
    """Get details for editable installs."""
    details: dict[str, Any] = {"executable_path": executable_path}

    try:
        import pyvider

        details["pyvider_location"] = str(Path(pyvider.__file__).parent.parent)
        details["is_development_mode"] = "src" in str(pyvider.__path__[0])
    except (ImportError, AttributeError):
        details["pyvider_import_error"] = "Could not import pyvider"

    return details


def x__get_editable_install_details__mutmut_1(executable_path: str) -> dict[str, Any]:
    """Get details for editable installs."""
    details: dict[str, Any] = None

    try:
        import pyvider

        details["pyvider_location"] = str(Path(pyvider.__file__).parent.parent)
        details["is_development_mode"] = "src" in str(pyvider.__path__[0])
    except (ImportError, AttributeError):
        details["pyvider_import_error"] = "Could not import pyvider"

    return details


def x__get_editable_install_details__mutmut_2(executable_path: str) -> dict[str, Any]:
    """Get details for editable installs."""
    details: dict[str, Any] = {"XXexecutable_pathXX": executable_path}

    try:
        import pyvider

        details["pyvider_location"] = str(Path(pyvider.__file__).parent.parent)
        details["is_development_mode"] = "src" in str(pyvider.__path__[0])
    except (ImportError, AttributeError):
        details["pyvider_import_error"] = "Could not import pyvider"

    return details


def x__get_editable_install_details__mutmut_3(executable_path: str) -> dict[str, Any]:
    """Get details for editable installs."""
    details: dict[str, Any] = {"EXECUTABLE_PATH": executable_path}

    try:
        import pyvider

        details["pyvider_location"] = str(Path(pyvider.__file__).parent.parent)
        details["is_development_mode"] = "src" in str(pyvider.__path__[0])
    except (ImportError, AttributeError):
        details["pyvider_import_error"] = "Could not import pyvider"

    return details


def x__get_editable_install_details__mutmut_4(executable_path: str) -> dict[str, Any]:
    """Get details for editable installs."""
    details: dict[str, Any] = {"executable_path": executable_path}

    try:
        import pyvider

        details["pyvider_location"] = None
        details["is_development_mode"] = "src" in str(pyvider.__path__[0])
    except (ImportError, AttributeError):
        details["pyvider_import_error"] = "Could not import pyvider"

    return details


def x__get_editable_install_details__mutmut_5(executable_path: str) -> dict[str, Any]:
    """Get details for editable installs."""
    details: dict[str, Any] = {"executable_path": executable_path}

    try:
        import pyvider

        details["XXpyvider_locationXX"] = str(Path(pyvider.__file__).parent.parent)
        details["is_development_mode"] = "src" in str(pyvider.__path__[0])
    except (ImportError, AttributeError):
        details["pyvider_import_error"] = "Could not import pyvider"

    return details


def x__get_editable_install_details__mutmut_6(executable_path: str) -> dict[str, Any]:
    """Get details for editable installs."""
    details: dict[str, Any] = {"executable_path": executable_path}

    try:
        import pyvider

        details["PYVIDER_LOCATION"] = str(Path(pyvider.__file__).parent.parent)
        details["is_development_mode"] = "src" in str(pyvider.__path__[0])
    except (ImportError, AttributeError):
        details["pyvider_import_error"] = "Could not import pyvider"

    return details


def x__get_editable_install_details__mutmut_7(executable_path: str) -> dict[str, Any]:
    """Get details for editable installs."""
    details: dict[str, Any] = {"executable_path": executable_path}

    try:
        import pyvider

        details["pyvider_location"] = str(None)
        details["is_development_mode"] = "src" in str(pyvider.__path__[0])
    except (ImportError, AttributeError):
        details["pyvider_import_error"] = "Could not import pyvider"

    return details


def x__get_editable_install_details__mutmut_8(executable_path: str) -> dict[str, Any]:
    """Get details for editable installs."""
    details: dict[str, Any] = {"executable_path": executable_path}

    try:
        import pyvider

        details["pyvider_location"] = str(Path(None).parent.parent)
        details["is_development_mode"] = "src" in str(pyvider.__path__[0])
    except (ImportError, AttributeError):
        details["pyvider_import_error"] = "Could not import pyvider"

    return details


def x__get_editable_install_details__mutmut_9(executable_path: str) -> dict[str, Any]:
    """Get details for editable installs."""
    details: dict[str, Any] = {"executable_path": executable_path}

    try:
        import pyvider

        details["pyvider_location"] = str(Path(pyvider.__file__).parent.parent)
        details["is_development_mode"] = None
    except (ImportError, AttributeError):
        details["pyvider_import_error"] = "Could not import pyvider"

    return details


def x__get_editable_install_details__mutmut_10(executable_path: str) -> dict[str, Any]:
    """Get details for editable installs."""
    details: dict[str, Any] = {"executable_path": executable_path}

    try:
        import pyvider

        details["pyvider_location"] = str(Path(pyvider.__file__).parent.parent)
        details["XXis_development_modeXX"] = "src" in str(pyvider.__path__[0])
    except (ImportError, AttributeError):
        details["pyvider_import_error"] = "Could not import pyvider"

    return details


def x__get_editable_install_details__mutmut_11(executable_path: str) -> dict[str, Any]:
    """Get details for editable installs."""
    details: dict[str, Any] = {"executable_path": executable_path}

    try:
        import pyvider

        details["pyvider_location"] = str(Path(pyvider.__file__).parent.parent)
        details["IS_DEVELOPMENT_MODE"] = "src" in str(pyvider.__path__[0])
    except (ImportError, AttributeError):
        details["pyvider_import_error"] = "Could not import pyvider"

    return details


def x__get_editable_install_details__mutmut_12(executable_path: str) -> dict[str, Any]:
    """Get details for editable installs."""
    details: dict[str, Any] = {"executable_path": executable_path}

    try:
        import pyvider

        details["pyvider_location"] = str(Path(pyvider.__file__).parent.parent)
        details["is_development_mode"] = "XXsrcXX" in str(pyvider.__path__[0])
    except (ImportError, AttributeError):
        details["pyvider_import_error"] = "Could not import pyvider"

    return details


def x__get_editable_install_details__mutmut_13(executable_path: str) -> dict[str, Any]:
    """Get details for editable installs."""
    details: dict[str, Any] = {"executable_path": executable_path}

    try:
        import pyvider

        details["pyvider_location"] = str(Path(pyvider.__file__).parent.parent)
        details["is_development_mode"] = "SRC" in str(pyvider.__path__[0])
    except (ImportError, AttributeError):
        details["pyvider_import_error"] = "Could not import pyvider"

    return details


def x__get_editable_install_details__mutmut_14(executable_path: str) -> dict[str, Any]:
    """Get details for editable installs."""
    details: dict[str, Any] = {"executable_path": executable_path}

    try:
        import pyvider

        details["pyvider_location"] = str(Path(pyvider.__file__).parent.parent)
        details["is_development_mode"] = "src" not in str(pyvider.__path__[0])
    except (ImportError, AttributeError):
        details["pyvider_import_error"] = "Could not import pyvider"

    return details


def x__get_editable_install_details__mutmut_15(executable_path: str) -> dict[str, Any]:
    """Get details for editable installs."""
    details: dict[str, Any] = {"executable_path": executable_path}

    try:
        import pyvider

        details["pyvider_location"] = str(Path(pyvider.__file__).parent.parent)
        details["is_development_mode"] = "src" in str(None)
    except (ImportError, AttributeError):
        details["pyvider_import_error"] = "Could not import pyvider"

    return details


def x__get_editable_install_details__mutmut_16(executable_path: str) -> dict[str, Any]:
    """Get details for editable installs."""
    details: dict[str, Any] = {"executable_path": executable_path}

    try:
        import pyvider

        details["pyvider_location"] = str(Path(pyvider.__file__).parent.parent)
        details["is_development_mode"] = "src" in str(pyvider.__path__[1])
    except (ImportError, AttributeError):
        details["pyvider_import_error"] = "Could not import pyvider"

    return details


def x__get_editable_install_details__mutmut_17(executable_path: str) -> dict[str, Any]:
    """Get details for editable installs."""
    details: dict[str, Any] = {"executable_path": executable_path}

    try:
        import pyvider

        details["pyvider_location"] = str(Path(pyvider.__file__).parent.parent)
        details["is_development_mode"] = "src" in str(pyvider.__path__[0])
    except (ImportError, AttributeError):
        details["pyvider_import_error"] = None

    return details


def x__get_editable_install_details__mutmut_18(executable_path: str) -> dict[str, Any]:
    """Get details for editable installs."""
    details: dict[str, Any] = {"executable_path": executable_path}

    try:
        import pyvider

        details["pyvider_location"] = str(Path(pyvider.__file__).parent.parent)
        details["is_development_mode"] = "src" in str(pyvider.__path__[0])
    except (ImportError, AttributeError):
        details["XXpyvider_import_errorXX"] = "Could not import pyvider"

    return details


def x__get_editable_install_details__mutmut_19(executable_path: str) -> dict[str, Any]:
    """Get details for editable installs."""
    details: dict[str, Any] = {"executable_path": executable_path}

    try:
        import pyvider

        details["pyvider_location"] = str(Path(pyvider.__file__).parent.parent)
        details["is_development_mode"] = "src" in str(pyvider.__path__[0])
    except (ImportError, AttributeError):
        details["PYVIDER_IMPORT_ERROR"] = "Could not import pyvider"

    return details


def x__get_editable_install_details__mutmut_20(executable_path: str) -> dict[str, Any]:
    """Get details for editable installs."""
    details: dict[str, Any] = {"executable_path": executable_path}

    try:
        import pyvider

        details["pyvider_location"] = str(Path(pyvider.__file__).parent.parent)
        details["is_development_mode"] = "src" in str(pyvider.__path__[0])
    except (ImportError, AttributeError):
        details["pyvider_import_error"] = "XXCould not import pyviderXX"

    return details


def x__get_editable_install_details__mutmut_21(executable_path: str) -> dict[str, Any]:
    """Get details for editable installs."""
    details: dict[str, Any] = {"executable_path": executable_path}

    try:
        import pyvider

        details["pyvider_location"] = str(Path(pyvider.__file__).parent.parent)
        details["is_development_mode"] = "src" in str(pyvider.__path__[0])
    except (ImportError, AttributeError):
        details["pyvider_import_error"] = "could not import pyvider"

    return details


def x__get_editable_install_details__mutmut_22(executable_path: str) -> dict[str, Any]:
    """Get details for editable installs."""
    details: dict[str, Any] = {"executable_path": executable_path}

    try:
        import pyvider

        details["pyvider_location"] = str(Path(pyvider.__file__).parent.parent)
        details["is_development_mode"] = "src" in str(pyvider.__path__[0])
    except (ImportError, AttributeError):
        details["pyvider_import_error"] = "COULD NOT IMPORT PYVIDER"

    return details

x__get_editable_install_details__mutmut_mutants : ClassVar[MutantDict] = {
'x__get_editable_install_details__mutmut_1': x__get_editable_install_details__mutmut_1, 
    'x__get_editable_install_details__mutmut_2': x__get_editable_install_details__mutmut_2, 
    'x__get_editable_install_details__mutmut_3': x__get_editable_install_details__mutmut_3, 
    'x__get_editable_install_details__mutmut_4': x__get_editable_install_details__mutmut_4, 
    'x__get_editable_install_details__mutmut_5': x__get_editable_install_details__mutmut_5, 
    'x__get_editable_install_details__mutmut_6': x__get_editable_install_details__mutmut_6, 
    'x__get_editable_install_details__mutmut_7': x__get_editable_install_details__mutmut_7, 
    'x__get_editable_install_details__mutmut_8': x__get_editable_install_details__mutmut_8, 
    'x__get_editable_install_details__mutmut_9': x__get_editable_install_details__mutmut_9, 
    'x__get_editable_install_details__mutmut_10': x__get_editable_install_details__mutmut_10, 
    'x__get_editable_install_details__mutmut_11': x__get_editable_install_details__mutmut_11, 
    'x__get_editable_install_details__mutmut_12': x__get_editable_install_details__mutmut_12, 
    'x__get_editable_install_details__mutmut_13': x__get_editable_install_details__mutmut_13, 
    'x__get_editable_install_details__mutmut_14': x__get_editable_install_details__mutmut_14, 
    'x__get_editable_install_details__mutmut_15': x__get_editable_install_details__mutmut_15, 
    'x__get_editable_install_details__mutmut_16': x__get_editable_install_details__mutmut_16, 
    'x__get_editable_install_details__mutmut_17': x__get_editable_install_details__mutmut_17, 
    'x__get_editable_install_details__mutmut_18': x__get_editable_install_details__mutmut_18, 
    'x__get_editable_install_details__mutmut_19': x__get_editable_install_details__mutmut_19, 
    'x__get_editable_install_details__mutmut_20': x__get_editable_install_details__mutmut_20, 
    'x__get_editable_install_details__mutmut_21': x__get_editable_install_details__mutmut_21, 
    'x__get_editable_install_details__mutmut_22': x__get_editable_install_details__mutmut_22
}

def _get_editable_install_details(*args, **kwargs):
    result = _mutmut_trampoline(x__get_editable_install_details__mutmut_orig, x__get_editable_install_details__mutmut_mutants, args, kwargs)
    return result 

_get_editable_install_details.__signature__ = _mutmut_signature(x__get_editable_install_details__mutmut_orig)
x__get_editable_install_details__mutmut_orig.__name__ = 'x__get_editable_install_details'


def x__analyze_executable__mutmut_orig(executable_path: str) -> dict[str, Any]:
    """Analyze the executable for debugging unknown launch methods."""
    exe_path = Path(executable_path)

    return {
        "exists": exe_path.exists(),
        "is_file": exe_path.is_file() if exe_path.exists() else False,
        "is_symlink": exe_path.is_symlink() if exe_path.exists() else False,
        "suffix": exe_path.suffix,
        "parent": str(exe_path.parent),
        "name": exe_path.name,
    }


def x__analyze_executable__mutmut_1(executable_path: str) -> dict[str, Any]:
    """Analyze the executable for debugging unknown launch methods."""
    exe_path = None

    return {
        "exists": exe_path.exists(),
        "is_file": exe_path.is_file() if exe_path.exists() else False,
        "is_symlink": exe_path.is_symlink() if exe_path.exists() else False,
        "suffix": exe_path.suffix,
        "parent": str(exe_path.parent),
        "name": exe_path.name,
    }


def x__analyze_executable__mutmut_2(executable_path: str) -> dict[str, Any]:
    """Analyze the executable for debugging unknown launch methods."""
    exe_path = Path(None)

    return {
        "exists": exe_path.exists(),
        "is_file": exe_path.is_file() if exe_path.exists() else False,
        "is_symlink": exe_path.is_symlink() if exe_path.exists() else False,
        "suffix": exe_path.suffix,
        "parent": str(exe_path.parent),
        "name": exe_path.name,
    }


def x__analyze_executable__mutmut_3(executable_path: str) -> dict[str, Any]:
    """Analyze the executable for debugging unknown launch methods."""
    exe_path = Path(executable_path)

    return {
        "XXexistsXX": exe_path.exists(),
        "is_file": exe_path.is_file() if exe_path.exists() else False,
        "is_symlink": exe_path.is_symlink() if exe_path.exists() else False,
        "suffix": exe_path.suffix,
        "parent": str(exe_path.parent),
        "name": exe_path.name,
    }


def x__analyze_executable__mutmut_4(executable_path: str) -> dict[str, Any]:
    """Analyze the executable for debugging unknown launch methods."""
    exe_path = Path(executable_path)

    return {
        "EXISTS": exe_path.exists(),
        "is_file": exe_path.is_file() if exe_path.exists() else False,
        "is_symlink": exe_path.is_symlink() if exe_path.exists() else False,
        "suffix": exe_path.suffix,
        "parent": str(exe_path.parent),
        "name": exe_path.name,
    }


def x__analyze_executable__mutmut_5(executable_path: str) -> dict[str, Any]:
    """Analyze the executable for debugging unknown launch methods."""
    exe_path = Path(executable_path)

    return {
        "exists": exe_path.exists(),
        "XXis_fileXX": exe_path.is_file() if exe_path.exists() else False,
        "is_symlink": exe_path.is_symlink() if exe_path.exists() else False,
        "suffix": exe_path.suffix,
        "parent": str(exe_path.parent),
        "name": exe_path.name,
    }


def x__analyze_executable__mutmut_6(executable_path: str) -> dict[str, Any]:
    """Analyze the executable for debugging unknown launch methods."""
    exe_path = Path(executable_path)

    return {
        "exists": exe_path.exists(),
        "IS_FILE": exe_path.is_file() if exe_path.exists() else False,
        "is_symlink": exe_path.is_symlink() if exe_path.exists() else False,
        "suffix": exe_path.suffix,
        "parent": str(exe_path.parent),
        "name": exe_path.name,
    }


def x__analyze_executable__mutmut_7(executable_path: str) -> dict[str, Any]:
    """Analyze the executable for debugging unknown launch methods."""
    exe_path = Path(executable_path)

    return {
        "exists": exe_path.exists(),
        "is_file": exe_path.is_file() if exe_path.exists() else True,
        "is_symlink": exe_path.is_symlink() if exe_path.exists() else False,
        "suffix": exe_path.suffix,
        "parent": str(exe_path.parent),
        "name": exe_path.name,
    }


def x__analyze_executable__mutmut_8(executable_path: str) -> dict[str, Any]:
    """Analyze the executable for debugging unknown launch methods."""
    exe_path = Path(executable_path)

    return {
        "exists": exe_path.exists(),
        "is_file": exe_path.is_file() if exe_path.exists() else False,
        "XXis_symlinkXX": exe_path.is_symlink() if exe_path.exists() else False,
        "suffix": exe_path.suffix,
        "parent": str(exe_path.parent),
        "name": exe_path.name,
    }


def x__analyze_executable__mutmut_9(executable_path: str) -> dict[str, Any]:
    """Analyze the executable for debugging unknown launch methods."""
    exe_path = Path(executable_path)

    return {
        "exists": exe_path.exists(),
        "is_file": exe_path.is_file() if exe_path.exists() else False,
        "IS_SYMLINK": exe_path.is_symlink() if exe_path.exists() else False,
        "suffix": exe_path.suffix,
        "parent": str(exe_path.parent),
        "name": exe_path.name,
    }


def x__analyze_executable__mutmut_10(executable_path: str) -> dict[str, Any]:
    """Analyze the executable for debugging unknown launch methods."""
    exe_path = Path(executable_path)

    return {
        "exists": exe_path.exists(),
        "is_file": exe_path.is_file() if exe_path.exists() else False,
        "is_symlink": exe_path.is_symlink() if exe_path.exists() else True,
        "suffix": exe_path.suffix,
        "parent": str(exe_path.parent),
        "name": exe_path.name,
    }


def x__analyze_executable__mutmut_11(executable_path: str) -> dict[str, Any]:
    """Analyze the executable for debugging unknown launch methods."""
    exe_path = Path(executable_path)

    return {
        "exists": exe_path.exists(),
        "is_file": exe_path.is_file() if exe_path.exists() else False,
        "is_symlink": exe_path.is_symlink() if exe_path.exists() else False,
        "XXsuffixXX": exe_path.suffix,
        "parent": str(exe_path.parent),
        "name": exe_path.name,
    }


def x__analyze_executable__mutmut_12(executable_path: str) -> dict[str, Any]:
    """Analyze the executable for debugging unknown launch methods."""
    exe_path = Path(executable_path)

    return {
        "exists": exe_path.exists(),
        "is_file": exe_path.is_file() if exe_path.exists() else False,
        "is_symlink": exe_path.is_symlink() if exe_path.exists() else False,
        "SUFFIX": exe_path.suffix,
        "parent": str(exe_path.parent),
        "name": exe_path.name,
    }


def x__analyze_executable__mutmut_13(executable_path: str) -> dict[str, Any]:
    """Analyze the executable for debugging unknown launch methods."""
    exe_path = Path(executable_path)

    return {
        "exists": exe_path.exists(),
        "is_file": exe_path.is_file() if exe_path.exists() else False,
        "is_symlink": exe_path.is_symlink() if exe_path.exists() else False,
        "suffix": exe_path.suffix,
        "XXparentXX": str(exe_path.parent),
        "name": exe_path.name,
    }


def x__analyze_executable__mutmut_14(executable_path: str) -> dict[str, Any]:
    """Analyze the executable for debugging unknown launch methods."""
    exe_path = Path(executable_path)

    return {
        "exists": exe_path.exists(),
        "is_file": exe_path.is_file() if exe_path.exists() else False,
        "is_symlink": exe_path.is_symlink() if exe_path.exists() else False,
        "suffix": exe_path.suffix,
        "PARENT": str(exe_path.parent),
        "name": exe_path.name,
    }


def x__analyze_executable__mutmut_15(executable_path: str) -> dict[str, Any]:
    """Analyze the executable for debugging unknown launch methods."""
    exe_path = Path(executable_path)

    return {
        "exists": exe_path.exists(),
        "is_file": exe_path.is_file() if exe_path.exists() else False,
        "is_symlink": exe_path.is_symlink() if exe_path.exists() else False,
        "suffix": exe_path.suffix,
        "parent": str(None),
        "name": exe_path.name,
    }


def x__analyze_executable__mutmut_16(executable_path: str) -> dict[str, Any]:
    """Analyze the executable for debugging unknown launch methods."""
    exe_path = Path(executable_path)

    return {
        "exists": exe_path.exists(),
        "is_file": exe_path.is_file() if exe_path.exists() else False,
        "is_symlink": exe_path.is_symlink() if exe_path.exists() else False,
        "suffix": exe_path.suffix,
        "parent": str(exe_path.parent),
        "XXnameXX": exe_path.name,
    }


def x__analyze_executable__mutmut_17(executable_path: str) -> dict[str, Any]:
    """Analyze the executable for debugging unknown launch methods."""
    exe_path = Path(executable_path)

    return {
        "exists": exe_path.exists(),
        "is_file": exe_path.is_file() if exe_path.exists() else False,
        "is_symlink": exe_path.is_symlink() if exe_path.exists() else False,
        "suffix": exe_path.suffix,
        "parent": str(exe_path.parent),
        "NAME": exe_path.name,
    }

x__analyze_executable__mutmut_mutants : ClassVar[MutantDict] = {
'x__analyze_executable__mutmut_1': x__analyze_executable__mutmut_1, 
    'x__analyze_executable__mutmut_2': x__analyze_executable__mutmut_2, 
    'x__analyze_executable__mutmut_3': x__analyze_executable__mutmut_3, 
    'x__analyze_executable__mutmut_4': x__analyze_executable__mutmut_4, 
    'x__analyze_executable__mutmut_5': x__analyze_executable__mutmut_5, 
    'x__analyze_executable__mutmut_6': x__analyze_executable__mutmut_6, 
    'x__analyze_executable__mutmut_7': x__analyze_executable__mutmut_7, 
    'x__analyze_executable__mutmut_8': x__analyze_executable__mutmut_8, 
    'x__analyze_executable__mutmut_9': x__analyze_executable__mutmut_9, 
    'x__analyze_executable__mutmut_10': x__analyze_executable__mutmut_10, 
    'x__analyze_executable__mutmut_11': x__analyze_executable__mutmut_11, 
    'x__analyze_executable__mutmut_12': x__analyze_executable__mutmut_12, 
    'x__analyze_executable__mutmut_13': x__analyze_executable__mutmut_13, 
    'x__analyze_executable__mutmut_14': x__analyze_executable__mutmut_14, 
    'x__analyze_executable__mutmut_15': x__analyze_executable__mutmut_15, 
    'x__analyze_executable__mutmut_16': x__analyze_executable__mutmut_16, 
    'x__analyze_executable__mutmut_17': x__analyze_executable__mutmut_17
}

def _analyze_executable(*args, **kwargs):
    result = _mutmut_trampoline(x__analyze_executable__mutmut_orig, x__analyze_executable__mutmut_mutants, args, kwargs)
    return result 

_analyze_executable.__signature__ = _mutmut_signature(x__analyze_executable__mutmut_orig)
x__analyze_executable__mutmut_orig.__name__ = 'x__analyze_executable'


def x__analyze_cache_structure__mutmut_orig(python_path: Path) -> dict[str, Any]:
    """Analyze the cache directory structure for PSPF packages."""
    cache_dir = python_path.parent.parent

    structure = {
        "python_bin_dir": str(python_path.parent),
        "cache_root": str(cache_dir),
        "contents": [],
    }

    try:
        if cache_dir.exists():
            structure["contents"] = [item.name for item in cache_dir.iterdir() if item.is_dir()][
                :10
            ]  # Limit to 10 items
    except (OSError, PermissionError):
        structure["contents"] = ["<access_denied>"]

    return structure


def x__analyze_cache_structure__mutmut_1(python_path: Path) -> dict[str, Any]:
    """Analyze the cache directory structure for PSPF packages."""
    cache_dir = None

    structure = {
        "python_bin_dir": str(python_path.parent),
        "cache_root": str(cache_dir),
        "contents": [],
    }

    try:
        if cache_dir.exists():
            structure["contents"] = [item.name for item in cache_dir.iterdir() if item.is_dir()][
                :10
            ]  # Limit to 10 items
    except (OSError, PermissionError):
        structure["contents"] = ["<access_denied>"]

    return structure


def x__analyze_cache_structure__mutmut_2(python_path: Path) -> dict[str, Any]:
    """Analyze the cache directory structure for PSPF packages."""
    cache_dir = python_path.parent.parent

    structure = None

    try:
        if cache_dir.exists():
            structure["contents"] = [item.name for item in cache_dir.iterdir() if item.is_dir()][
                :10
            ]  # Limit to 10 items
    except (OSError, PermissionError):
        structure["contents"] = ["<access_denied>"]

    return structure


def x__analyze_cache_structure__mutmut_3(python_path: Path) -> dict[str, Any]:
    """Analyze the cache directory structure for PSPF packages."""
    cache_dir = python_path.parent.parent

    structure = {
        "XXpython_bin_dirXX": str(python_path.parent),
        "cache_root": str(cache_dir),
        "contents": [],
    }

    try:
        if cache_dir.exists():
            structure["contents"] = [item.name for item in cache_dir.iterdir() if item.is_dir()][
                :10
            ]  # Limit to 10 items
    except (OSError, PermissionError):
        structure["contents"] = ["<access_denied>"]

    return structure


def x__analyze_cache_structure__mutmut_4(python_path: Path) -> dict[str, Any]:
    """Analyze the cache directory structure for PSPF packages."""
    cache_dir = python_path.parent.parent

    structure = {
        "PYTHON_BIN_DIR": str(python_path.parent),
        "cache_root": str(cache_dir),
        "contents": [],
    }

    try:
        if cache_dir.exists():
            structure["contents"] = [item.name for item in cache_dir.iterdir() if item.is_dir()][
                :10
            ]  # Limit to 10 items
    except (OSError, PermissionError):
        structure["contents"] = ["<access_denied>"]

    return structure


def x__analyze_cache_structure__mutmut_5(python_path: Path) -> dict[str, Any]:
    """Analyze the cache directory structure for PSPF packages."""
    cache_dir = python_path.parent.parent

    structure = {
        "python_bin_dir": str(None),
        "cache_root": str(cache_dir),
        "contents": [],
    }

    try:
        if cache_dir.exists():
            structure["contents"] = [item.name for item in cache_dir.iterdir() if item.is_dir()][
                :10
            ]  # Limit to 10 items
    except (OSError, PermissionError):
        structure["contents"] = ["<access_denied>"]

    return structure


def x__analyze_cache_structure__mutmut_6(python_path: Path) -> dict[str, Any]:
    """Analyze the cache directory structure for PSPF packages."""
    cache_dir = python_path.parent.parent

    structure = {
        "python_bin_dir": str(python_path.parent),
        "XXcache_rootXX": str(cache_dir),
        "contents": [],
    }

    try:
        if cache_dir.exists():
            structure["contents"] = [item.name for item in cache_dir.iterdir() if item.is_dir()][
                :10
            ]  # Limit to 10 items
    except (OSError, PermissionError):
        structure["contents"] = ["<access_denied>"]

    return structure


def x__analyze_cache_structure__mutmut_7(python_path: Path) -> dict[str, Any]:
    """Analyze the cache directory structure for PSPF packages."""
    cache_dir = python_path.parent.parent

    structure = {
        "python_bin_dir": str(python_path.parent),
        "CACHE_ROOT": str(cache_dir),
        "contents": [],
    }

    try:
        if cache_dir.exists():
            structure["contents"] = [item.name for item in cache_dir.iterdir() if item.is_dir()][
                :10
            ]  # Limit to 10 items
    except (OSError, PermissionError):
        structure["contents"] = ["<access_denied>"]

    return structure


def x__analyze_cache_structure__mutmut_8(python_path: Path) -> dict[str, Any]:
    """Analyze the cache directory structure for PSPF packages."""
    cache_dir = python_path.parent.parent

    structure = {
        "python_bin_dir": str(python_path.parent),
        "cache_root": str(None),
        "contents": [],
    }

    try:
        if cache_dir.exists():
            structure["contents"] = [item.name for item in cache_dir.iterdir() if item.is_dir()][
                :10
            ]  # Limit to 10 items
    except (OSError, PermissionError):
        structure["contents"] = ["<access_denied>"]

    return structure


def x__analyze_cache_structure__mutmut_9(python_path: Path) -> dict[str, Any]:
    """Analyze the cache directory structure for PSPF packages."""
    cache_dir = python_path.parent.parent

    structure = {
        "python_bin_dir": str(python_path.parent),
        "cache_root": str(cache_dir),
        "XXcontentsXX": [],
    }

    try:
        if cache_dir.exists():
            structure["contents"] = [item.name for item in cache_dir.iterdir() if item.is_dir()][
                :10
            ]  # Limit to 10 items
    except (OSError, PermissionError):
        structure["contents"] = ["<access_denied>"]

    return structure


def x__analyze_cache_structure__mutmut_10(python_path: Path) -> dict[str, Any]:
    """Analyze the cache directory structure for PSPF packages."""
    cache_dir = python_path.parent.parent

    structure = {
        "python_bin_dir": str(python_path.parent),
        "cache_root": str(cache_dir),
        "CONTENTS": [],
    }

    try:
        if cache_dir.exists():
            structure["contents"] = [item.name for item in cache_dir.iterdir() if item.is_dir()][
                :10
            ]  # Limit to 10 items
    except (OSError, PermissionError):
        structure["contents"] = ["<access_denied>"]

    return structure


def x__analyze_cache_structure__mutmut_11(python_path: Path) -> dict[str, Any]:
    """Analyze the cache directory structure for PSPF packages."""
    cache_dir = python_path.parent.parent

    structure = {
        "python_bin_dir": str(python_path.parent),
        "cache_root": str(cache_dir),
        "contents": [],
    }

    try:
        if cache_dir.exists():
            structure["contents"] = None  # Limit to 10 items
    except (OSError, PermissionError):
        structure["contents"] = ["<access_denied>"]

    return structure


def x__analyze_cache_structure__mutmut_12(python_path: Path) -> dict[str, Any]:
    """Analyze the cache directory structure for PSPF packages."""
    cache_dir = python_path.parent.parent

    structure = {
        "python_bin_dir": str(python_path.parent),
        "cache_root": str(cache_dir),
        "contents": [],
    }

    try:
        if cache_dir.exists():
            structure["XXcontentsXX"] = [item.name for item in cache_dir.iterdir() if item.is_dir()][
                :10
            ]  # Limit to 10 items
    except (OSError, PermissionError):
        structure["contents"] = ["<access_denied>"]

    return structure


def x__analyze_cache_structure__mutmut_13(python_path: Path) -> dict[str, Any]:
    """Analyze the cache directory structure for PSPF packages."""
    cache_dir = python_path.parent.parent

    structure = {
        "python_bin_dir": str(python_path.parent),
        "cache_root": str(cache_dir),
        "contents": [],
    }

    try:
        if cache_dir.exists():
            structure["CONTENTS"] = [item.name for item in cache_dir.iterdir() if item.is_dir()][
                :10
            ]  # Limit to 10 items
    except (OSError, PermissionError):
        structure["contents"] = ["<access_denied>"]

    return structure


def x__analyze_cache_structure__mutmut_14(python_path: Path) -> dict[str, Any]:
    """Analyze the cache directory structure for PSPF packages."""
    cache_dir = python_path.parent.parent

    structure = {
        "python_bin_dir": str(python_path.parent),
        "cache_root": str(cache_dir),
        "contents": [],
    }

    try:
        if cache_dir.exists():
            structure["contents"] = [item.name for item in cache_dir.iterdir() if item.is_dir()][
                :11
            ]  # Limit to 10 items
    except (OSError, PermissionError):
        structure["contents"] = ["<access_denied>"]

    return structure


def x__analyze_cache_structure__mutmut_15(python_path: Path) -> dict[str, Any]:
    """Analyze the cache directory structure for PSPF packages."""
    cache_dir = python_path.parent.parent

    structure = {
        "python_bin_dir": str(python_path.parent),
        "cache_root": str(cache_dir),
        "contents": [],
    }

    try:
        if cache_dir.exists():
            structure["contents"] = [item.name for item in cache_dir.iterdir() if item.is_dir()][
                :10
            ]  # Limit to 10 items
    except (OSError, PermissionError):
        structure["contents"] = None

    return structure


def x__analyze_cache_structure__mutmut_16(python_path: Path) -> dict[str, Any]:
    """Analyze the cache directory structure for PSPF packages."""
    cache_dir = python_path.parent.parent

    structure = {
        "python_bin_dir": str(python_path.parent),
        "cache_root": str(cache_dir),
        "contents": [],
    }

    try:
        if cache_dir.exists():
            structure["contents"] = [item.name for item in cache_dir.iterdir() if item.is_dir()][
                :10
            ]  # Limit to 10 items
    except (OSError, PermissionError):
        structure["XXcontentsXX"] = ["<access_denied>"]

    return structure


def x__analyze_cache_structure__mutmut_17(python_path: Path) -> dict[str, Any]:
    """Analyze the cache directory structure for PSPF packages."""
    cache_dir = python_path.parent.parent

    structure = {
        "python_bin_dir": str(python_path.parent),
        "cache_root": str(cache_dir),
        "contents": [],
    }

    try:
        if cache_dir.exists():
            structure["contents"] = [item.name for item in cache_dir.iterdir() if item.is_dir()][
                :10
            ]  # Limit to 10 items
    except (OSError, PermissionError):
        structure["CONTENTS"] = ["<access_denied>"]

    return structure


def x__analyze_cache_structure__mutmut_18(python_path: Path) -> dict[str, Any]:
    """Analyze the cache directory structure for PSPF packages."""
    cache_dir = python_path.parent.parent

    structure = {
        "python_bin_dir": str(python_path.parent),
        "cache_root": str(cache_dir),
        "contents": [],
    }

    try:
        if cache_dir.exists():
            structure["contents"] = [item.name for item in cache_dir.iterdir() if item.is_dir()][
                :10
            ]  # Limit to 10 items
    except (OSError, PermissionError):
        structure["contents"] = ["XX<access_denied>XX"]

    return structure


def x__analyze_cache_structure__mutmut_19(python_path: Path) -> dict[str, Any]:
    """Analyze the cache directory structure for PSPF packages."""
    cache_dir = python_path.parent.parent

    structure = {
        "python_bin_dir": str(python_path.parent),
        "cache_root": str(cache_dir),
        "contents": [],
    }

    try:
        if cache_dir.exists():
            structure["contents"] = [item.name for item in cache_dir.iterdir() if item.is_dir()][
                :10
            ]  # Limit to 10 items
    except (OSError, PermissionError):
        structure["contents"] = ["<ACCESS_DENIED>"]

    return structure

x__analyze_cache_structure__mutmut_mutants : ClassVar[MutantDict] = {
'x__analyze_cache_structure__mutmut_1': x__analyze_cache_structure__mutmut_1, 
    'x__analyze_cache_structure__mutmut_2': x__analyze_cache_structure__mutmut_2, 
    'x__analyze_cache_structure__mutmut_3': x__analyze_cache_structure__mutmut_3, 
    'x__analyze_cache_structure__mutmut_4': x__analyze_cache_structure__mutmut_4, 
    'x__analyze_cache_structure__mutmut_5': x__analyze_cache_structure__mutmut_5, 
    'x__analyze_cache_structure__mutmut_6': x__analyze_cache_structure__mutmut_6, 
    'x__analyze_cache_structure__mutmut_7': x__analyze_cache_structure__mutmut_7, 
    'x__analyze_cache_structure__mutmut_8': x__analyze_cache_structure__mutmut_8, 
    'x__analyze_cache_structure__mutmut_9': x__analyze_cache_structure__mutmut_9, 
    'x__analyze_cache_structure__mutmut_10': x__analyze_cache_structure__mutmut_10, 
    'x__analyze_cache_structure__mutmut_11': x__analyze_cache_structure__mutmut_11, 
    'x__analyze_cache_structure__mutmut_12': x__analyze_cache_structure__mutmut_12, 
    'x__analyze_cache_structure__mutmut_13': x__analyze_cache_structure__mutmut_13, 
    'x__analyze_cache_structure__mutmut_14': x__analyze_cache_structure__mutmut_14, 
    'x__analyze_cache_structure__mutmut_15': x__analyze_cache_structure__mutmut_15, 
    'x__analyze_cache_structure__mutmut_16': x__analyze_cache_structure__mutmut_16, 
    'x__analyze_cache_structure__mutmut_17': x__analyze_cache_structure__mutmut_17, 
    'x__analyze_cache_structure__mutmut_18': x__analyze_cache_structure__mutmut_18, 
    'x__analyze_cache_structure__mutmut_19': x__analyze_cache_structure__mutmut_19
}

def _analyze_cache_structure(*args, **kwargs):
    result = _mutmut_trampoline(x__analyze_cache_structure__mutmut_orig, x__analyze_cache_structure__mutmut_mutants, args, kwargs)
    return result 

_analyze_cache_structure.__signature__ = _mutmut_signature(x__analyze_cache_structure__mutmut_orig)
x__analyze_cache_structure__mutmut_orig.__name__ = 'x__analyze_cache_structure'


def x_log_launch_context__mutmut_orig(logger_func: Callable[[str], None] | None = None) -> LaunchContext:
    """
    Detect and log the launch context.

    Args:
        logger_func: Optional logger function to use. If None, uses print.

    Returns:
        The detected LaunchContext
    """
    context = detect_launch_context()

    log_func = logger_func or print
    log_func(str(context))

    return context


def x_log_launch_context__mutmut_1(logger_func: Callable[[str], None] | None = None) -> LaunchContext:
    """
    Detect and log the launch context.

    Args:
        logger_func: Optional logger function to use. If None, uses print.

    Returns:
        The detected LaunchContext
    """
    context = None

    log_func = logger_func or print
    log_func(str(context))

    return context


def x_log_launch_context__mutmut_2(logger_func: Callable[[str], None] | None = None) -> LaunchContext:
    """
    Detect and log the launch context.

    Args:
        logger_func: Optional logger function to use. If None, uses print.

    Returns:
        The detected LaunchContext
    """
    context = detect_launch_context()

    log_func = None
    log_func(str(context))

    return context


def x_log_launch_context__mutmut_3(logger_func: Callable[[str], None] | None = None) -> LaunchContext:
    """
    Detect and log the launch context.

    Args:
        logger_func: Optional logger function to use. If None, uses print.

    Returns:
        The detected LaunchContext
    """
    context = detect_launch_context()

    log_func = logger_func and print
    log_func(str(context))

    return context


def x_log_launch_context__mutmut_4(logger_func: Callable[[str], None] | None = None) -> LaunchContext:
    """
    Detect and log the launch context.

    Args:
        logger_func: Optional logger function to use. If None, uses print.

    Returns:
        The detected LaunchContext
    """
    context = detect_launch_context()

    log_func = logger_func or print
    log_func(None)

    return context


def x_log_launch_context__mutmut_5(logger_func: Callable[[str], None] | None = None) -> LaunchContext:
    """
    Detect and log the launch context.

    Args:
        logger_func: Optional logger function to use. If None, uses print.

    Returns:
        The detected LaunchContext
    """
    context = detect_launch_context()

    log_func = logger_func or print
    log_func(str(None))

    return context

x_log_launch_context__mutmut_mutants : ClassVar[MutantDict] = {
'x_log_launch_context__mutmut_1': x_log_launch_context__mutmut_1, 
    'x_log_launch_context__mutmut_2': x_log_launch_context__mutmut_2, 
    'x_log_launch_context__mutmut_3': x_log_launch_context__mutmut_3, 
    'x_log_launch_context__mutmut_4': x_log_launch_context__mutmut_4, 
    'x_log_launch_context__mutmut_5': x_log_launch_context__mutmut_5
}

def log_launch_context(*args, **kwargs):
    result = _mutmut_trampoline(x_log_launch_context__mutmut_orig, x_log_launch_context__mutmut_mutants, args, kwargs)
    return result 

log_launch_context.__signature__ = _mutmut_signature(x_log_launch_context__mutmut_orig)
x_log_launch_context__mutmut_orig.__name__ = 'x_log_launch_context'
