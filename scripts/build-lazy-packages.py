#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Build a compressed archive of lazy-loaded packages.

This script extracts packages that are not needed for RPC server startup
and creates a separate compressed archive that can be loaded on-demand
via the lazy import system.

Usage:
    python build-lazy-packages.py [--site-packages PATH] [--output PATH]

This significantly reduces initial extraction time by deferring non-critical
packages until they're actually imported.
"""

import argparse
import os
import shutil
import sys
import zipfile
from pathlib import Path


# Packages that should NOT be extracted initially
LAZY_PACKAGES = {
    "mkdocs",  # Documentation generator
    "material",  # Material theme
    "babel",  # Internationalization
    "pygments",  # Syntax highlighting
    "pymarkdown",  # Markdown linter
    "pymdownx",  # Markdown extensions
    "backrefs",  # Markdown related
    "bs4",  # BeautifulSoup
    "beautifulsoup4",  # BeautifulSoup
    "markdown",  # Markdown
    "markdown_it",  # Markdown parser
    "jinja2",  # Template engine
    "opentelemetry",  # Telemetry
    "pip",  # Package manager
    "setuptools",  # Build tools
    "wheel",  # Build tools
    "build",  # Build tools
    "packaging",  # Packaging utilities
}


def find_site_packages():
    """Find the site-packages directory."""
    for path in sys.path:
        if "site-packages" in path and os.path.isdir(path):
            return path
    raise RuntimeError("Could not find site-packages directory")


def get_package_path(site_packages: str, package_name: str) -> Path:
    """Get the path to a package in site-packages."""
    # Try as directory (package)
    path = Path(site_packages) / package_name
    if path.is_dir():
        return path

    # Try as .dist-info directory
    path = Path(site_packages) / f"{package_name}.dist-info"
    if path.is_dir():
        return path

    # Try with underscores instead of hyphens
    path = Path(site_packages) / package_name.replace("-", "_")
    if path.is_dir():
        return path

    raise FileNotFoundError(f"Package {package_name} not found in {site_packages}")


def build_lazy_archive(site_packages: str, output_path: str):
    """Build the lazy packages archive."""
    print(f"Building lazy packages archive...")
    print(f"Source: {site_packages}")
    print(f"Output: {output_path}")
    print()

    total_size = 0
    archive_size = 0

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for package_name in sorted(LAZY_PACKAGES):
            try:
                pkg_path = get_package_path(site_packages, package_name)

                # Add package to archive
                for root, dirs, files in os.walk(pkg_path):
                    for file in files:
                        file_path = Path(root) / file
                        rel_path = file_path.relative_to(Path(site_packages))

                        # Get file size
                        file_size = file_path.stat().st_size
                        total_size += file_size

                        # Add to archive
                        archive.write(file_path, arcname=rel_path)
                        archive_size += file_size

                pkg_size_mb = sum(
                    os.path.getsize(os.path.join(root, file))
                    for root, dirs, files in os.walk(pkg_path)
                    for file in files
                ) / (1024 * 1024)

                print(f"  OK {package_name:40} {pkg_size_mb:8.1f} MB")
            except FileNotFoundError:
                print(f"  -- {package_name:40} NOT FOUND")
            except Exception as e:
                print(f"  ER {package_name:40} ERROR: {e}")

    total_mb = total_size / (1024 * 1024)
    compressed_mb = os.path.getsize(output_path) / (1024 * 1024)
    compression_ratio = (1 - (os.path.getsize(output_path) / total_size)) * 100 if total_size > 0 else 0

    print()
    print(f"Total packages size:    {total_mb:8.1f} MB")
    print(f"Compressed size:        {compressed_mb:8.1f} MB")
    print(f"Compression ratio:      {compression_ratio:8.1f}%")
    print()
    print(f"SUCCESS: Archive created: {output_path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-packages", help="Path to site-packages directory")
    parser.add_argument("--output", default="lazy-packages.zip", help="Output archive path")
    args = parser.parse_args()

    # Find site-packages if not provided
    site_packages = args.site_packages or find_site_packages()

    if not os.path.isdir(site_packages):
        print(f"Error: site-packages not found: {site_packages}")
        sys.exit(1)

    build_lazy_archive(site_packages, args.output)


if __name__ == "__main__":
    main()
