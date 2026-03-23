#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Lazy import system for on-demand package extraction.

This module implements sys.meta_path hooks to load packages from a compressed
archive on-demand, deferring extraction until needed. This allows the provider
to start quickly without extracting all 300MB of packages upfront.
"""

import importlib.abc
import importlib.machinery
import importlib.util
import io
import os
import sys
import zipfile
from pathlib import Path
from typing import Optional


class LazyPackageLoader(importlib.abc.Loader):
    """Loader that extracts and loads packages from a compressed archive."""

    def __init__(self, archive_path: str, module_name: str, package_path: str):
        self.archive_path = archive_path
        self.module_name = module_name
        self.package_path = package_path

    def create_module(self, spec):
        """Return None to use the default module creation logic."""
        return None

    def exec_module(self, module):
        """Load and execute module code."""
        try:
            with zipfile.ZipFile(self.archive_path, 'r') as archive:
                # Try to load as a package first
                init_path = f"{self.package_path}/__init__.py"
                try:
                    code = archive.read(init_path).decode('utf-8')
                    exec(compile(code, init_path, 'exec'), module.__dict__)
                    return
                except KeyError:
                    pass

                # Try to load as a module
                module_file = f"{self.package_path}.py"
                try:
                    code = archive.read(module_file).decode('utf-8')
                    exec(compile(code, module_file, 'exec'), module.__dict__)
                    return
                except KeyError:
                    pass

                raise ImportError(f"Cannot find module {self.module_name} in archive")
        except Exception as e:
            raise ImportError(f"Failed to load {self.module_name} from archive: {e}") from e


class LazyPackageFinder(importlib.abc.MetaPathFinder):
    """Meta path finder that loads packages from a lazy archive."""

    # Packages that should be loaded from compressed archive on-demand
    LAZY_PACKAGES = {
        'mkdocs',  # Documentation generator (~7MB)
        'material',  # Material theme (~39MB)
        'babel',  # Internationalization (~32MB)
        'pygments',  # Syntax highlighting (~9.5MB)
        'pymarkdown',  # Markdown linter (~6MB)
        'pymdownx',  # Markdown extensions (~3.3MB)
        'backrefs',  # Markdown related (~2.8MB)
        'bs4',  # BeautifulSoup (~844KB)
        'beautifulsoup4',  # BeautifulSoup (~844KB)
        'markdown',  # Markdown (~864KB)
        'markdown_it',  # Markdown parser (~789KB)
        'jinja2',  # Template engine (~1.3MB) - optional
        'opentelemetry',  # Telemetry (~4.5MB) - optional
        'pip',  # Package manager (~13MB) - not needed at runtime
        'setuptools',  # Build tools (~11MB) - not needed at runtime
    }

    def __init__(self, archive_path: str):
        self.archive_path = archive_path
        if not os.path.exists(archive_path):
            raise RuntimeError(f"Lazy package archive not found: {archive_path}")

    def find_spec(self, fullname, path, target=None):
        """Find module spec, loading from archive if needed."""
        # Check if this module should be loaded from archive
        parts = fullname.split('.')
        root_package = parts[0]

        if root_package not in self.LAZY_PACKAGES:
            return None

        # Check if archive exists
        if not os.path.exists(self.archive_path):
            return None

        # Try to find in archive
        try:
            with zipfile.ZipFile(self.archive_path, 'r') as archive:
                # Try as package
                package_path = fullname.replace('.', '/')
                try:
                    archive.getinfo(f"{package_path}/__init__.py")
                    loader = LazyPackageLoader(self.archive_path, fullname, package_path)
                    return importlib.machinery.ModuleSpec(fullname, loader, is_package=True)
                except KeyError:
                    pass

                # Try as module
                try:
                    archive.getinfo(f"{package_path}.py")
                    loader = LazyPackageLoader(self.archive_path, fullname, package_path)
                    return importlib.machinery.ModuleSpec(fullname, loader)
                except KeyError:
                    pass
        except Exception:
            pass

        return None


def install_lazy_loader(archive_path: Optional[str] = None):
    """Install the lazy import system.

    Args:
        archive_path: Path to the lazy packages archive. If None, looks for
                     standard location in the workenv.
    """
    if archive_path is None:
        # Try to find in standard workenv locations
        workenv_paths = [
            os.path.join(os.path.dirname(__file__), '..', '..', 'lazy-packages.zip'),
            os.path.join(os.path.dirname(sys.executable), '..', 'lazy-packages.zip'),
        ]
        archive_path = next((p for p in workenv_paths if os.path.exists(p)), None)

    if archive_path and os.path.exists(archive_path):
        # Install at the beginning of sys.meta_path for priority
        finder = LazyPackageFinder(archive_path)
        sys.meta_path.insert(0, finder)
        return True

    return False


# 🐍📦🔚
