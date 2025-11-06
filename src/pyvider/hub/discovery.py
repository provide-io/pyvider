#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

import importlib
import importlib.metadata
import inspect
import pkgutil
from typing import Any

from provide.foundation import logger, resilient, retry

from pyvider.hub.components import ComponentRegistry


class ComponentDiscovery:
    """
    Discovers and registers components by scanning for installed packages that
    declare the 'pyvider' entry point.
    """

    ENTRY_POINT_GROUP = "pyvider"

    def __init__(self, hub: ComponentRegistry) -> None:
        self.hub = hub
        self._discovered_modules: set[str] = set()
        self.import_errors: list[tuple[str, Exception]] = []

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

        for entry_point in entry_points:
            logger.debug(
                "🛰️🔍 Discovered entry point",
                name=entry_point.name,
                module=entry_point.value,
            )
            await self._discover_package(entry_point.value, strict=strict)

        {k: len(v) for k, v in self.hub.list_components().items()}

    async def _discover_package(self, package_name: str, strict: bool) -> None:
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

    async def _process_module(self, module: Any) -> None:
        """Process a module to find and register decorated components."""
        for _, obj in inspect.getmembers(module):
            if not (inspect.isclass(obj) or inspect.isfunction(obj)):
                continue

            if inspect.isclass(obj) and inspect.isabstract(obj):
                logger.debug(f"Skipping abstract class: {obj.__name__}")
                continue

            reg_checks = [
                ("_is_registered_provider", "provider"),
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
                            "🛰️🔍✅ Registered component",
                            component_type=comp_type,
                            component_name=name,
                            module=module.__name__,
                        )
                    break


# 🐍🏗️🔚
