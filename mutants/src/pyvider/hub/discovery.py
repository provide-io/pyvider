import importlib
import importlib.metadata
import inspect
import pkgutil
from typing import Any

from provide.foundation import logger, resilient, retry

from pyvider.hub.components import ComponentRegistry
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


class ComponentDiscovery:
    """
    Discovers and registers components by scanning for installed packages that
    declare the 'pyvider.components' entry point.
    """

    ENTRY_POINT_GROUP = "pyvider.components"

    def xǁComponentDiscoveryǁ__init____mutmut_orig(self, hub: ComponentRegistry) -> None:
        self.hub = hub
        self._discovered_modules: set[str] = set()
        self.import_errors: list[tuple[str, Exception]] = []

    def xǁComponentDiscoveryǁ__init____mutmut_1(self, hub: ComponentRegistry) -> None:
        self.hub = None
        self._discovered_modules: set[str] = set()
        self.import_errors: list[tuple[str, Exception]] = []

    def xǁComponentDiscoveryǁ__init____mutmut_2(self, hub: ComponentRegistry) -> None:
        self.hub = hub
        self._discovered_modules: set[str] = None
        self.import_errors: list[tuple[str, Exception]] = []

    def xǁComponentDiscoveryǁ__init____mutmut_3(self, hub: ComponentRegistry) -> None:
        self.hub = hub
        self._discovered_modules: set[str] = set()
        self.import_errors: list[tuple[str, Exception]] = None
    
    xǁComponentDiscoveryǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁComponentDiscoveryǁ__init____mutmut_1': xǁComponentDiscoveryǁ__init____mutmut_1, 
        'xǁComponentDiscoveryǁ__init____mutmut_2': xǁComponentDiscoveryǁ__init____mutmut_2, 
        'xǁComponentDiscoveryǁ__init____mutmut_3': xǁComponentDiscoveryǁ__init____mutmut_3
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁComponentDiscoveryǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁComponentDiscoveryǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁComponentDiscoveryǁ__init____mutmut_orig)
    xǁComponentDiscoveryǁ__init____mutmut_orig.__name__ = 'xǁComponentDiscoveryǁ__init__'

    @resilient()
    @retry(max_attempts=2, base_delay=1.0)
    async def discover_all(self, strict: bool = False) -> None:
        """
        Discovers all components. In strict mode, it re-raises import errors.
        Enhanced with error handling and retry logic.
        """
        self.import_errors = []
        logger.debug("🛰️🔍🔄 Starting component discovery", group=self.ENTRY_POINT_GROUP)

        try:
            entry_points = importlib.metadata.entry_points(group=self.ENTRY_POINT_GROUP)
        except Exception as e:
            logger.error("🛰️🔍❌ Failed to query for entry points", error=e, exc_info=True)
            return

        if not entry_points:
            logger.info(" i No packages found declaring the 'pyvider.components' entry point.")
            logger.info(" i Manually discovering built-in component packages.")
            await self._discover_package("pyvider.components", strict=strict)
            await self._discover_package("pyvider.providers.capabilities", strict=strict)
        else:
            for entry_point in entry_points:
                logger.debug(
                    "🛰️🔍📦 Found component package entry point",
                    name=entry_point.name,
                    module=entry_point.value,
                )
                await self._discover_package(entry_point.value, strict=strict)

        component_counts = {k: len(v) for k, v in self.hub.list_components().items()}
        logger.info("🛰️🔍✅ Component discovery complete", components=component_counts)

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_orig(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_1(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name not in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_2(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = None
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_3(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(None)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_4(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(None)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_5(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(None)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_6(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(None, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_7(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, None):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_8(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr("__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_9(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, ):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_10(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "XX__path__XX"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_11(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__PATH__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_12(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(None, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_13(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, None):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_14(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_15(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, ):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_16(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ - "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_17(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "XX.XX"):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_18(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_19(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(None, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_20(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=None)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_21(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_22(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, )

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_23(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append(None)
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_24(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                None,
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_25(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=None,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_26(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=None,
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_27(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_28(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_29(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_30(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "XX🛰️🔍⚠️ Could not import component module, skippingXX",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_31(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_32(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ COULD NOT IMPORT COMPONENT MODULE, SKIPPING",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_33(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(None),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_34(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append(None)
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_35(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                None,
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_36(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=None,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_37(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=None,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_38(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=None,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_39(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_40(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_41(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_42(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_43(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "XX🛰️🔍❌ Unexpected error discovering packageXX",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_44(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_45(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ UNEXPECTED ERROR DISCOVERING PACKAGE",
                package=package_name,
                error=e,
                exc_info=True,
            )

    async def xǁComponentDiscoveryǁ_discover_package__mutmut_46(self, package_name: str, strict: bool) -> None:
        """Recursively discover all modules within a given package name."""
        if package_name in self._discovered_modules:
            return

        try:
            package = importlib.import_module(package_name)
            self._discovered_modules.add(package_name)
            await self._process_module(package)

            if hasattr(package, "__path__"):
                for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                    if module_info.name not in self._discovered_modules:
                        await self._discover_package(module_info.name, strict=strict)

        except (ImportError, ModuleNotFoundError) as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.warning(
                "🛰️🔍⚠️ Could not import component module, skipping",
                module=package_name,
                error=str(e),
            )
        except Exception as e:
            if strict:
                raise
            self.import_errors.append((package_name, e))
            logger.error(
                "🛰️🔍❌ Unexpected error discovering package",
                package=package_name,
                error=e,
                exc_info=False,
            )
    
    xǁComponentDiscoveryǁ_discover_package__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁComponentDiscoveryǁ_discover_package__mutmut_1': xǁComponentDiscoveryǁ_discover_package__mutmut_1, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_2': xǁComponentDiscoveryǁ_discover_package__mutmut_2, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_3': xǁComponentDiscoveryǁ_discover_package__mutmut_3, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_4': xǁComponentDiscoveryǁ_discover_package__mutmut_4, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_5': xǁComponentDiscoveryǁ_discover_package__mutmut_5, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_6': xǁComponentDiscoveryǁ_discover_package__mutmut_6, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_7': xǁComponentDiscoveryǁ_discover_package__mutmut_7, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_8': xǁComponentDiscoveryǁ_discover_package__mutmut_8, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_9': xǁComponentDiscoveryǁ_discover_package__mutmut_9, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_10': xǁComponentDiscoveryǁ_discover_package__mutmut_10, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_11': xǁComponentDiscoveryǁ_discover_package__mutmut_11, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_12': xǁComponentDiscoveryǁ_discover_package__mutmut_12, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_13': xǁComponentDiscoveryǁ_discover_package__mutmut_13, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_14': xǁComponentDiscoveryǁ_discover_package__mutmut_14, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_15': xǁComponentDiscoveryǁ_discover_package__mutmut_15, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_16': xǁComponentDiscoveryǁ_discover_package__mutmut_16, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_17': xǁComponentDiscoveryǁ_discover_package__mutmut_17, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_18': xǁComponentDiscoveryǁ_discover_package__mutmut_18, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_19': xǁComponentDiscoveryǁ_discover_package__mutmut_19, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_20': xǁComponentDiscoveryǁ_discover_package__mutmut_20, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_21': xǁComponentDiscoveryǁ_discover_package__mutmut_21, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_22': xǁComponentDiscoveryǁ_discover_package__mutmut_22, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_23': xǁComponentDiscoveryǁ_discover_package__mutmut_23, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_24': xǁComponentDiscoveryǁ_discover_package__mutmut_24, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_25': xǁComponentDiscoveryǁ_discover_package__mutmut_25, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_26': xǁComponentDiscoveryǁ_discover_package__mutmut_26, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_27': xǁComponentDiscoveryǁ_discover_package__mutmut_27, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_28': xǁComponentDiscoveryǁ_discover_package__mutmut_28, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_29': xǁComponentDiscoveryǁ_discover_package__mutmut_29, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_30': xǁComponentDiscoveryǁ_discover_package__mutmut_30, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_31': xǁComponentDiscoveryǁ_discover_package__mutmut_31, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_32': xǁComponentDiscoveryǁ_discover_package__mutmut_32, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_33': xǁComponentDiscoveryǁ_discover_package__mutmut_33, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_34': xǁComponentDiscoveryǁ_discover_package__mutmut_34, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_35': xǁComponentDiscoveryǁ_discover_package__mutmut_35, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_36': xǁComponentDiscoveryǁ_discover_package__mutmut_36, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_37': xǁComponentDiscoveryǁ_discover_package__mutmut_37, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_38': xǁComponentDiscoveryǁ_discover_package__mutmut_38, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_39': xǁComponentDiscoveryǁ_discover_package__mutmut_39, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_40': xǁComponentDiscoveryǁ_discover_package__mutmut_40, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_41': xǁComponentDiscoveryǁ_discover_package__mutmut_41, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_42': xǁComponentDiscoveryǁ_discover_package__mutmut_42, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_43': xǁComponentDiscoveryǁ_discover_package__mutmut_43, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_44': xǁComponentDiscoveryǁ_discover_package__mutmut_44, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_45': xǁComponentDiscoveryǁ_discover_package__mutmut_45, 
        'xǁComponentDiscoveryǁ_discover_package__mutmut_46': xǁComponentDiscoveryǁ_discover_package__mutmut_46
    }
    
    def _discover_package(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁComponentDiscoveryǁ_discover_package__mutmut_orig"), object.__getattribute__(self, "xǁComponentDiscoveryǁ_discover_package__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _discover_package.__signature__ = _mutmut_signature(xǁComponentDiscoveryǁ_discover_package__mutmut_orig)
    xǁComponentDiscoveryǁ_discover_package__mutmut_orig.__name__ = 'xǁComponentDiscoveryǁ_discover_package'

    async def xǁComponentDiscoveryǁ_process_module__mutmut_orig(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_1(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(None):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_2(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_3(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) and inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_4(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(None) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_5(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(None)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_6(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                break

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_7(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) or inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_8(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(None) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_9(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(None):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_10(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(None)
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_11(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                break

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_12(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = None
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_13(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("XX_is_registered_resourceXX", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_14(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_IS_REGISTERED_RESOURCE", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_15(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "XXresourceXX"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_16(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "RESOURCE"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_17(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("XX_is_registered_data_sourceXX", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_18(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_IS_REGISTERED_DATA_SOURCE", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_19(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "XXdata_sourceXX"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_20(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "DATA_SOURCE"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_21(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("XX_is_registered_functionXX", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_22(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_IS_REGISTERED_FUNCTION", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_23(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "XXfunctionXX"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_24(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "FUNCTION"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_25(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("XX_is_registered_capabilityXX", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_26(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_IS_REGISTERED_CAPABILITY", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_27(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "XXcapabilityXX"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_28(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "CAPABILITY"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_29(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(None, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_30(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, None, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_31(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, None):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_32(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_33(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_34(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, ):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_35(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, True):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_36(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = None
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_37(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(None, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_38(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, None, None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_39(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr("_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_40(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_41(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", )
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_42(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "XX_registered_nameXX", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_43(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_REGISTERED_NAME", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_44(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(None, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_45(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, None, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_46(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, None)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_47(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_48(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_49(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, )
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_50(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            None,
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_51(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=None,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_52(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            module=module.__name__,
                        )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_53(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            )
                    break

    async def xǁComponentDiscoveryǁ_process_module__mutmut_54(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_resource", "resource"),
                ("_is_registered_data_source", "data_source"),
                ("_is_registered_function", "function"),
                ("_is_registered_capability", "capability"),
            ]
            for marker, comp_type in reg_checks:
                if getattr(obj, marker, False):
                    name = getattr(obj, "_registered_name", None)
                    if name:
                        self.hub.register(comp_type, name, obj)
                        logger.debug(
                            f"🛰️🔍✅ Registered {comp_type}: {name}",
                            module=module.__name__,
                        )
                    return
    
    xǁComponentDiscoveryǁ_process_module__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁComponentDiscoveryǁ_process_module__mutmut_1': xǁComponentDiscoveryǁ_process_module__mutmut_1, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_2': xǁComponentDiscoveryǁ_process_module__mutmut_2, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_3': xǁComponentDiscoveryǁ_process_module__mutmut_3, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_4': xǁComponentDiscoveryǁ_process_module__mutmut_4, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_5': xǁComponentDiscoveryǁ_process_module__mutmut_5, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_6': xǁComponentDiscoveryǁ_process_module__mutmut_6, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_7': xǁComponentDiscoveryǁ_process_module__mutmut_7, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_8': xǁComponentDiscoveryǁ_process_module__mutmut_8, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_9': xǁComponentDiscoveryǁ_process_module__mutmut_9, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_10': xǁComponentDiscoveryǁ_process_module__mutmut_10, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_11': xǁComponentDiscoveryǁ_process_module__mutmut_11, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_12': xǁComponentDiscoveryǁ_process_module__mutmut_12, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_13': xǁComponentDiscoveryǁ_process_module__mutmut_13, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_14': xǁComponentDiscoveryǁ_process_module__mutmut_14, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_15': xǁComponentDiscoveryǁ_process_module__mutmut_15, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_16': xǁComponentDiscoveryǁ_process_module__mutmut_16, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_17': xǁComponentDiscoveryǁ_process_module__mutmut_17, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_18': xǁComponentDiscoveryǁ_process_module__mutmut_18, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_19': xǁComponentDiscoveryǁ_process_module__mutmut_19, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_20': xǁComponentDiscoveryǁ_process_module__mutmut_20, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_21': xǁComponentDiscoveryǁ_process_module__mutmut_21, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_22': xǁComponentDiscoveryǁ_process_module__mutmut_22, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_23': xǁComponentDiscoveryǁ_process_module__mutmut_23, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_24': xǁComponentDiscoveryǁ_process_module__mutmut_24, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_25': xǁComponentDiscoveryǁ_process_module__mutmut_25, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_26': xǁComponentDiscoveryǁ_process_module__mutmut_26, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_27': xǁComponentDiscoveryǁ_process_module__mutmut_27, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_28': xǁComponentDiscoveryǁ_process_module__mutmut_28, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_29': xǁComponentDiscoveryǁ_process_module__mutmut_29, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_30': xǁComponentDiscoveryǁ_process_module__mutmut_30, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_31': xǁComponentDiscoveryǁ_process_module__mutmut_31, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_32': xǁComponentDiscoveryǁ_process_module__mutmut_32, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_33': xǁComponentDiscoveryǁ_process_module__mutmut_33, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_34': xǁComponentDiscoveryǁ_process_module__mutmut_34, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_35': xǁComponentDiscoveryǁ_process_module__mutmut_35, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_36': xǁComponentDiscoveryǁ_process_module__mutmut_36, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_37': xǁComponentDiscoveryǁ_process_module__mutmut_37, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_38': xǁComponentDiscoveryǁ_process_module__mutmut_38, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_39': xǁComponentDiscoveryǁ_process_module__mutmut_39, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_40': xǁComponentDiscoveryǁ_process_module__mutmut_40, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_41': xǁComponentDiscoveryǁ_process_module__mutmut_41, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_42': xǁComponentDiscoveryǁ_process_module__mutmut_42, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_43': xǁComponentDiscoveryǁ_process_module__mutmut_43, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_44': xǁComponentDiscoveryǁ_process_module__mutmut_44, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_45': xǁComponentDiscoveryǁ_process_module__mutmut_45, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_46': xǁComponentDiscoveryǁ_process_module__mutmut_46, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_47': xǁComponentDiscoveryǁ_process_module__mutmut_47, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_48': xǁComponentDiscoveryǁ_process_module__mutmut_48, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_49': xǁComponentDiscoveryǁ_process_module__mutmut_49, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_50': xǁComponentDiscoveryǁ_process_module__mutmut_50, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_51': xǁComponentDiscoveryǁ_process_module__mutmut_51, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_52': xǁComponentDiscoveryǁ_process_module__mutmut_52, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_53': xǁComponentDiscoveryǁ_process_module__mutmut_53, 
        'xǁComponentDiscoveryǁ_process_module__mutmut_54': xǁComponentDiscoveryǁ_process_module__mutmut_54
    }
    
    def _process_module(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁComponentDiscoveryǁ_process_module__mutmut_orig"), object.__getattribute__(self, "xǁComponentDiscoveryǁ_process_module__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _process_module.__signature__ = _mutmut_signature(xǁComponentDiscoveryǁ_process_module__mutmut_orig)
    xǁComponentDiscoveryǁ_process_module__mutmut_orig.__name__ = 'xǁComponentDiscoveryǁ_process_module'
