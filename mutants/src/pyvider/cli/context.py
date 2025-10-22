from pathlib import Path
from typing import Any

import click
from provide.foundation.context import CLIContext
from provide.foundation.platform import get_arch_name, get_os_name

from pyvider.common.config import PyviderConfig
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


# --- Pyvider Context Class ---
class PyviderContext(CLIContext):
    """
    Pyvider-specific context that extends foundation's CLIContext.

    Inherits debug, log_level, and other CLI settings from foundation CLIContext.
    """

    def xǁPyviderContextǁ__init____mutmut_orig(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / ".local" / "bin"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("version", "0.1.0")
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "plugins"
            / "local"
            / "providers"
            / "pyvider"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_1(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = None
        self.home = Path.home()
        self.local_bin_dir = self.home / ".local" / "bin"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("version", "0.1.0")
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "plugins"
            / "local"
            / "providers"
            / "pyvider"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_2(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = None
        self.local_bin_dir = self.home / ".local" / "bin"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("version", "0.1.0")
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "plugins"
            / "local"
            / "providers"
            / "pyvider"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_3(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = None
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("version", "0.1.0")
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "plugins"
            / "local"
            / "providers"
            / "pyvider"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_4(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / ".local" * "bin"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("version", "0.1.0")
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "plugins"
            / "local"
            / "providers"
            / "pyvider"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_5(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home * ".local" / "bin"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("version", "0.1.0")
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "plugins"
            / "local"
            / "providers"
            / "pyvider"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_6(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / "XX.localXX" / "bin"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("version", "0.1.0")
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "plugins"
            / "local"
            / "providers"
            / "pyvider"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_7(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / ".LOCAL" / "bin"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("version", "0.1.0")
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "plugins"
            / "local"
            / "providers"
            / "pyvider"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_8(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / ".local" / "XXbinXX"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("version", "0.1.0")
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "plugins"
            / "local"
            / "providers"
            / "pyvider"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_9(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / ".local" / "BIN"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("version", "0.1.0")
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "plugins"
            / "local"
            / "providers"
            / "pyvider"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_10(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / ".local" / "bin"
        self.tf_os = None
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("version", "0.1.0")
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "plugins"
            / "local"
            / "providers"
            / "pyvider"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_11(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / ".local" / "bin"
        self.tf_os = get_os_name()
        self.tf_arch = None
        self.pyvider_version = self.config.get("version", "0.1.0")
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "plugins"
            / "local"
            / "providers"
            / "pyvider"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_12(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / ".local" / "bin"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = None
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "plugins"
            / "local"
            / "providers"
            / "pyvider"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_13(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / ".local" / "bin"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get(None, "0.1.0")
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "plugins"
            / "local"
            / "providers"
            / "pyvider"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_14(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / ".local" / "bin"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("version", None)
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "plugins"
            / "local"
            / "providers"
            / "pyvider"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_15(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / ".local" / "bin"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("0.1.0")
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "plugins"
            / "local"
            / "providers"
            / "pyvider"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_16(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / ".local" / "bin"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("version", )
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "plugins"
            / "local"
            / "providers"
            / "pyvider"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_17(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / ".local" / "bin"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("XXversionXX", "0.1.0")
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "plugins"
            / "local"
            / "providers"
            / "pyvider"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_18(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / ".local" / "bin"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("VERSION", "0.1.0")
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "plugins"
            / "local"
            / "providers"
            / "pyvider"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_19(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / ".local" / "bin"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("version", "XX0.1.0XX")
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "plugins"
            / "local"
            / "providers"
            / "pyvider"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_20(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / ".local" / "bin"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("version", "0.1.0")
        self.tf_plugin_dir = None
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_21(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / ".local" / "bin"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("version", "0.1.0")
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "plugins"
            / "local"
            / "providers"
            / "pyvider"
            / self.pyvider_version * f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_22(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / ".local" / "bin"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("version", "0.1.0")
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "plugins"
            / "local"
            / "providers"
            / "pyvider" * self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_23(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / ".local" / "bin"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("version", "0.1.0")
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "plugins"
            / "local"
            / "providers" * "pyvider"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_24(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / ".local" / "bin"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("version", "0.1.0")
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "plugins"
            / "local" * "providers"
            / "pyvider"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_25(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / ".local" / "bin"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("version", "0.1.0")
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "plugins" * "local"
            / "providers"
            / "pyvider"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_26(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / ".local" / "bin"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("version", "0.1.0")
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d" * "plugins"
            / "local"
            / "providers"
            / "pyvider"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_27(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / ".local" / "bin"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("version", "0.1.0")
        self.tf_plugin_dir = (
            self.home * ".terraform.d"
            / "plugins"
            / "local"
            / "providers"
            / "pyvider"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_28(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / ".local" / "bin"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("version", "0.1.0")
        self.tf_plugin_dir = (
            self.home
            / "XX.terraform.dXX"
            / "plugins"
            / "local"
            / "providers"
            / "pyvider"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_29(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / ".local" / "bin"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("version", "0.1.0")
        self.tf_plugin_dir = (
            self.home
            / ".TERRAFORM.D"
            / "plugins"
            / "local"
            / "providers"
            / "pyvider"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_30(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / ".local" / "bin"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("version", "0.1.0")
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "XXpluginsXX"
            / "local"
            / "providers"
            / "pyvider"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_31(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / ".local" / "bin"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("version", "0.1.0")
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "PLUGINS"
            / "local"
            / "providers"
            / "pyvider"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_32(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / ".local" / "bin"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("version", "0.1.0")
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "plugins"
            / "XXlocalXX"
            / "providers"
            / "pyvider"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_33(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / ".local" / "bin"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("version", "0.1.0")
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "plugins"
            / "LOCAL"
            / "providers"
            / "pyvider"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_34(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / ".local" / "bin"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("version", "0.1.0")
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "plugins"
            / "local"
            / "XXprovidersXX"
            / "pyvider"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_35(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / ".local" / "bin"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("version", "0.1.0")
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "plugins"
            / "local"
            / "PROVIDERS"
            / "pyvider"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_36(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / ".local" / "bin"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("version", "0.1.0")
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "plugins"
            / "local"
            / "providers"
            / "XXpyviderXX"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_37(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / ".local" / "bin"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("version", "0.1.0")
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "plugins"
            / "local"
            / "providers"
            / "PYVIDER"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_38(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / ".local" / "bin"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("version", "0.1.0")
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "plugins"
            / "local"
            / "providers"
            / "pyvider"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = None
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_39(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / ".local" / "bin"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("version", "0.1.0")
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "plugins"
            / "local"
            / "providers"
            / "pyvider"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = True
        self.discovery_errors: list[tuple[str, Exception]] = []

    def xǁPyviderContextǁ__init____mutmut_40(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / ".local" / "bin"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = self.config.get("version", "0.1.0")
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "plugins"
            / "local"
            / "providers"
            / "pyvider"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = None
    
    xǁPyviderContextǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁPyviderContextǁ__init____mutmut_1': xǁPyviderContextǁ__init____mutmut_1, 
        'xǁPyviderContextǁ__init____mutmut_2': xǁPyviderContextǁ__init____mutmut_2, 
        'xǁPyviderContextǁ__init____mutmut_3': xǁPyviderContextǁ__init____mutmut_3, 
        'xǁPyviderContextǁ__init____mutmut_4': xǁPyviderContextǁ__init____mutmut_4, 
        'xǁPyviderContextǁ__init____mutmut_5': xǁPyviderContextǁ__init____mutmut_5, 
        'xǁPyviderContextǁ__init____mutmut_6': xǁPyviderContextǁ__init____mutmut_6, 
        'xǁPyviderContextǁ__init____mutmut_7': xǁPyviderContextǁ__init____mutmut_7, 
        'xǁPyviderContextǁ__init____mutmut_8': xǁPyviderContextǁ__init____mutmut_8, 
        'xǁPyviderContextǁ__init____mutmut_9': xǁPyviderContextǁ__init____mutmut_9, 
        'xǁPyviderContextǁ__init____mutmut_10': xǁPyviderContextǁ__init____mutmut_10, 
        'xǁPyviderContextǁ__init____mutmut_11': xǁPyviderContextǁ__init____mutmut_11, 
        'xǁPyviderContextǁ__init____mutmut_12': xǁPyviderContextǁ__init____mutmut_12, 
        'xǁPyviderContextǁ__init____mutmut_13': xǁPyviderContextǁ__init____mutmut_13, 
        'xǁPyviderContextǁ__init____mutmut_14': xǁPyviderContextǁ__init____mutmut_14, 
        'xǁPyviderContextǁ__init____mutmut_15': xǁPyviderContextǁ__init____mutmut_15, 
        'xǁPyviderContextǁ__init____mutmut_16': xǁPyviderContextǁ__init____mutmut_16, 
        'xǁPyviderContextǁ__init____mutmut_17': xǁPyviderContextǁ__init____mutmut_17, 
        'xǁPyviderContextǁ__init____mutmut_18': xǁPyviderContextǁ__init____mutmut_18, 
        'xǁPyviderContextǁ__init____mutmut_19': xǁPyviderContextǁ__init____mutmut_19, 
        'xǁPyviderContextǁ__init____mutmut_20': xǁPyviderContextǁ__init____mutmut_20, 
        'xǁPyviderContextǁ__init____mutmut_21': xǁPyviderContextǁ__init____mutmut_21, 
        'xǁPyviderContextǁ__init____mutmut_22': xǁPyviderContextǁ__init____mutmut_22, 
        'xǁPyviderContextǁ__init____mutmut_23': xǁPyviderContextǁ__init____mutmut_23, 
        'xǁPyviderContextǁ__init____mutmut_24': xǁPyviderContextǁ__init____mutmut_24, 
        'xǁPyviderContextǁ__init____mutmut_25': xǁPyviderContextǁ__init____mutmut_25, 
        'xǁPyviderContextǁ__init____mutmut_26': xǁPyviderContextǁ__init____mutmut_26, 
        'xǁPyviderContextǁ__init____mutmut_27': xǁPyviderContextǁ__init____mutmut_27, 
        'xǁPyviderContextǁ__init____mutmut_28': xǁPyviderContextǁ__init____mutmut_28, 
        'xǁPyviderContextǁ__init____mutmut_29': xǁPyviderContextǁ__init____mutmut_29, 
        'xǁPyviderContextǁ__init____mutmut_30': xǁPyviderContextǁ__init____mutmut_30, 
        'xǁPyviderContextǁ__init____mutmut_31': xǁPyviderContextǁ__init____mutmut_31, 
        'xǁPyviderContextǁ__init____mutmut_32': xǁPyviderContextǁ__init____mutmut_32, 
        'xǁPyviderContextǁ__init____mutmut_33': xǁPyviderContextǁ__init____mutmut_33, 
        'xǁPyviderContextǁ__init____mutmut_34': xǁPyviderContextǁ__init____mutmut_34, 
        'xǁPyviderContextǁ__init____mutmut_35': xǁPyviderContextǁ__init____mutmut_35, 
        'xǁPyviderContextǁ__init____mutmut_36': xǁPyviderContextǁ__init____mutmut_36, 
        'xǁPyviderContextǁ__init____mutmut_37': xǁPyviderContextǁ__init____mutmut_37, 
        'xǁPyviderContextǁ__init____mutmut_38': xǁPyviderContextǁ__init____mutmut_38, 
        'xǁPyviderContextǁ__init____mutmut_39': xǁPyviderContextǁ__init____mutmut_39, 
        'xǁPyviderContextǁ__init____mutmut_40': xǁPyviderContextǁ__init____mutmut_40
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁPyviderContextǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁPyviderContextǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁPyviderContextǁ__init____mutmut_orig)
    xǁPyviderContextǁ__init____mutmut_orig.__name__ = 'xǁPyviderContextǁ__init__'

    async def xǁPyviderContextǁ_ensure_components_discovered__mutmut_orig(
        self,
        registry_obj: Any,
        component_discovery_cls: Any,
        click_echo_func: Any,
        click_secho_func: Any,
    ) -> None:
        if not self.components_discovered:
            try:
                discovery = component_discovery_cls(registry_obj)
                # THE FIX: Run discovery in non-strict mode to capture all errors
                await discovery.discover_all(strict=False)
                self.discovery_errors = discovery.import_errors
                self.components_discovered = True
            except Exception as e:
                # Capture unexpected errors during the discovery process itself
                self.discovery_errors.append(("discovery_runner", e))
                self.components_discovered = False

    async def xǁPyviderContextǁ_ensure_components_discovered__mutmut_1(
        self,
        registry_obj: Any,
        component_discovery_cls: Any,
        click_echo_func: Any,
        click_secho_func: Any,
    ) -> None:
        if self.components_discovered:
            try:
                discovery = component_discovery_cls(registry_obj)
                # THE FIX: Run discovery in non-strict mode to capture all errors
                await discovery.discover_all(strict=False)
                self.discovery_errors = discovery.import_errors
                self.components_discovered = True
            except Exception as e:
                # Capture unexpected errors during the discovery process itself
                self.discovery_errors.append(("discovery_runner", e))
                self.components_discovered = False

    async def xǁPyviderContextǁ_ensure_components_discovered__mutmut_2(
        self,
        registry_obj: Any,
        component_discovery_cls: Any,
        click_echo_func: Any,
        click_secho_func: Any,
    ) -> None:
        if not self.components_discovered:
            try:
                discovery = None
                # THE FIX: Run discovery in non-strict mode to capture all errors
                await discovery.discover_all(strict=False)
                self.discovery_errors = discovery.import_errors
                self.components_discovered = True
            except Exception as e:
                # Capture unexpected errors during the discovery process itself
                self.discovery_errors.append(("discovery_runner", e))
                self.components_discovered = False

    async def xǁPyviderContextǁ_ensure_components_discovered__mutmut_3(
        self,
        registry_obj: Any,
        component_discovery_cls: Any,
        click_echo_func: Any,
        click_secho_func: Any,
    ) -> None:
        if not self.components_discovered:
            try:
                discovery = component_discovery_cls(None)
                # THE FIX: Run discovery in non-strict mode to capture all errors
                await discovery.discover_all(strict=False)
                self.discovery_errors = discovery.import_errors
                self.components_discovered = True
            except Exception as e:
                # Capture unexpected errors during the discovery process itself
                self.discovery_errors.append(("discovery_runner", e))
                self.components_discovered = False

    async def xǁPyviderContextǁ_ensure_components_discovered__mutmut_4(
        self,
        registry_obj: Any,
        component_discovery_cls: Any,
        click_echo_func: Any,
        click_secho_func: Any,
    ) -> None:
        if not self.components_discovered:
            try:
                discovery = component_discovery_cls(registry_obj)
                # THE FIX: Run discovery in non-strict mode to capture all errors
                await discovery.discover_all(strict=None)
                self.discovery_errors = discovery.import_errors
                self.components_discovered = True
            except Exception as e:
                # Capture unexpected errors during the discovery process itself
                self.discovery_errors.append(("discovery_runner", e))
                self.components_discovered = False

    async def xǁPyviderContextǁ_ensure_components_discovered__mutmut_5(
        self,
        registry_obj: Any,
        component_discovery_cls: Any,
        click_echo_func: Any,
        click_secho_func: Any,
    ) -> None:
        if not self.components_discovered:
            try:
                discovery = component_discovery_cls(registry_obj)
                # THE FIX: Run discovery in non-strict mode to capture all errors
                await discovery.discover_all(strict=True)
                self.discovery_errors = discovery.import_errors
                self.components_discovered = True
            except Exception as e:
                # Capture unexpected errors during the discovery process itself
                self.discovery_errors.append(("discovery_runner", e))
                self.components_discovered = False

    async def xǁPyviderContextǁ_ensure_components_discovered__mutmut_6(
        self,
        registry_obj: Any,
        component_discovery_cls: Any,
        click_echo_func: Any,
        click_secho_func: Any,
    ) -> None:
        if not self.components_discovered:
            try:
                discovery = component_discovery_cls(registry_obj)
                # THE FIX: Run discovery in non-strict mode to capture all errors
                await discovery.discover_all(strict=False)
                self.discovery_errors = None
                self.components_discovered = True
            except Exception as e:
                # Capture unexpected errors during the discovery process itself
                self.discovery_errors.append(("discovery_runner", e))
                self.components_discovered = False

    async def xǁPyviderContextǁ_ensure_components_discovered__mutmut_7(
        self,
        registry_obj: Any,
        component_discovery_cls: Any,
        click_echo_func: Any,
        click_secho_func: Any,
    ) -> None:
        if not self.components_discovered:
            try:
                discovery = component_discovery_cls(registry_obj)
                # THE FIX: Run discovery in non-strict mode to capture all errors
                await discovery.discover_all(strict=False)
                self.discovery_errors = discovery.import_errors
                self.components_discovered = None
            except Exception as e:
                # Capture unexpected errors during the discovery process itself
                self.discovery_errors.append(("discovery_runner", e))
                self.components_discovered = False

    async def xǁPyviderContextǁ_ensure_components_discovered__mutmut_8(
        self,
        registry_obj: Any,
        component_discovery_cls: Any,
        click_echo_func: Any,
        click_secho_func: Any,
    ) -> None:
        if not self.components_discovered:
            try:
                discovery = component_discovery_cls(registry_obj)
                # THE FIX: Run discovery in non-strict mode to capture all errors
                await discovery.discover_all(strict=False)
                self.discovery_errors = discovery.import_errors
                self.components_discovered = False
            except Exception as e:
                # Capture unexpected errors during the discovery process itself
                self.discovery_errors.append(("discovery_runner", e))
                self.components_discovered = False

    async def xǁPyviderContextǁ_ensure_components_discovered__mutmut_9(
        self,
        registry_obj: Any,
        component_discovery_cls: Any,
        click_echo_func: Any,
        click_secho_func: Any,
    ) -> None:
        if not self.components_discovered:
            try:
                discovery = component_discovery_cls(registry_obj)
                # THE FIX: Run discovery in non-strict mode to capture all errors
                await discovery.discover_all(strict=False)
                self.discovery_errors = discovery.import_errors
                self.components_discovered = True
            except Exception as e:
                # Capture unexpected errors during the discovery process itself
                self.discovery_errors.append(None)
                self.components_discovered = False

    async def xǁPyviderContextǁ_ensure_components_discovered__mutmut_10(
        self,
        registry_obj: Any,
        component_discovery_cls: Any,
        click_echo_func: Any,
        click_secho_func: Any,
    ) -> None:
        if not self.components_discovered:
            try:
                discovery = component_discovery_cls(registry_obj)
                # THE FIX: Run discovery in non-strict mode to capture all errors
                await discovery.discover_all(strict=False)
                self.discovery_errors = discovery.import_errors
                self.components_discovered = True
            except Exception as e:
                # Capture unexpected errors during the discovery process itself
                self.discovery_errors.append(("XXdiscovery_runnerXX", e))
                self.components_discovered = False

    async def xǁPyviderContextǁ_ensure_components_discovered__mutmut_11(
        self,
        registry_obj: Any,
        component_discovery_cls: Any,
        click_echo_func: Any,
        click_secho_func: Any,
    ) -> None:
        if not self.components_discovered:
            try:
                discovery = component_discovery_cls(registry_obj)
                # THE FIX: Run discovery in non-strict mode to capture all errors
                await discovery.discover_all(strict=False)
                self.discovery_errors = discovery.import_errors
                self.components_discovered = True
            except Exception as e:
                # Capture unexpected errors during the discovery process itself
                self.discovery_errors.append(("DISCOVERY_RUNNER", e))
                self.components_discovered = False

    async def xǁPyviderContextǁ_ensure_components_discovered__mutmut_12(
        self,
        registry_obj: Any,
        component_discovery_cls: Any,
        click_echo_func: Any,
        click_secho_func: Any,
    ) -> None:
        if not self.components_discovered:
            try:
                discovery = component_discovery_cls(registry_obj)
                # THE FIX: Run discovery in non-strict mode to capture all errors
                await discovery.discover_all(strict=False)
                self.discovery_errors = discovery.import_errors
                self.components_discovered = True
            except Exception as e:
                # Capture unexpected errors during the discovery process itself
                self.discovery_errors.append(("discovery_runner", e))
                self.components_discovered = None

    async def xǁPyviderContextǁ_ensure_components_discovered__mutmut_13(
        self,
        registry_obj: Any,
        component_discovery_cls: Any,
        click_echo_func: Any,
        click_secho_func: Any,
    ) -> None:
        if not self.components_discovered:
            try:
                discovery = component_discovery_cls(registry_obj)
                # THE FIX: Run discovery in non-strict mode to capture all errors
                await discovery.discover_all(strict=False)
                self.discovery_errors = discovery.import_errors
                self.components_discovered = True
            except Exception as e:
                # Capture unexpected errors during the discovery process itself
                self.discovery_errors.append(("discovery_runner", e))
                self.components_discovered = True
    
    xǁPyviderContextǁ_ensure_components_discovered__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁPyviderContextǁ_ensure_components_discovered__mutmut_1': xǁPyviderContextǁ_ensure_components_discovered__mutmut_1, 
        'xǁPyviderContextǁ_ensure_components_discovered__mutmut_2': xǁPyviderContextǁ_ensure_components_discovered__mutmut_2, 
        'xǁPyviderContextǁ_ensure_components_discovered__mutmut_3': xǁPyviderContextǁ_ensure_components_discovered__mutmut_3, 
        'xǁPyviderContextǁ_ensure_components_discovered__mutmut_4': xǁPyviderContextǁ_ensure_components_discovered__mutmut_4, 
        'xǁPyviderContextǁ_ensure_components_discovered__mutmut_5': xǁPyviderContextǁ_ensure_components_discovered__mutmut_5, 
        'xǁPyviderContextǁ_ensure_components_discovered__mutmut_6': xǁPyviderContextǁ_ensure_components_discovered__mutmut_6, 
        'xǁPyviderContextǁ_ensure_components_discovered__mutmut_7': xǁPyviderContextǁ_ensure_components_discovered__mutmut_7, 
        'xǁPyviderContextǁ_ensure_components_discovered__mutmut_8': xǁPyviderContextǁ_ensure_components_discovered__mutmut_8, 
        'xǁPyviderContextǁ_ensure_components_discovered__mutmut_9': xǁPyviderContextǁ_ensure_components_discovered__mutmut_9, 
        'xǁPyviderContextǁ_ensure_components_discovered__mutmut_10': xǁPyviderContextǁ_ensure_components_discovered__mutmut_10, 
        'xǁPyviderContextǁ_ensure_components_discovered__mutmut_11': xǁPyviderContextǁ_ensure_components_discovered__mutmut_11, 
        'xǁPyviderContextǁ_ensure_components_discovered__mutmut_12': xǁPyviderContextǁ_ensure_components_discovered__mutmut_12, 
        'xǁPyviderContextǁ_ensure_components_discovered__mutmut_13': xǁPyviderContextǁ_ensure_components_discovered__mutmut_13
    }
    
    def _ensure_components_discovered(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁPyviderContextǁ_ensure_components_discovered__mutmut_orig"), object.__getattribute__(self, "xǁPyviderContextǁ_ensure_components_discovered__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _ensure_components_discovered.__signature__ = _mutmut_signature(xǁPyviderContextǁ_ensure_components_discovered__mutmut_orig)
    xǁPyviderContextǁ_ensure_components_discovered__mutmut_orig.__name__ = 'xǁPyviderContextǁ_ensure_components_discovered'


pass_ctx = click.make_pass_decorator(PyviderContext, ensure=True)
