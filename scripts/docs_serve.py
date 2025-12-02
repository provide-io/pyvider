#!/usr/bin/env python
"""Serve documentation with automatic port detection."""

from __future__ import annotations

import re
import socket
import subprocess
import sys
from pathlib import Path


def find_available_port(start_port: int = 11000) -> int:
    """Find an available port starting from start_port."""
    for port in range(start_port, start_port + 100):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("127.0.0.1", port))
                return port
        except OSError:
            continue

    raise RuntimeError(
        f"No available ports in range {start_port}-{start_port + 100}"
    )


def main() -> int:
    """Serve documentation with smart port detection."""
    # Run preflight check
    result = subprocess.run([sys.executable, "scripts/docs_preflight.py"])
    if result.returncode != 0:
        return 1

    # Find project's default port from mkdocs.yml
    default_port = 11000
    mkdocs_yml = Path("mkdocs.yml")
    if mkdocs_yml.exists():
        content = mkdocs_yml.read_text()
        match = re.search(r'dev_addr:\s*["\']?127\.0\.0\.1:(\d+)', content)
        if match:
            default_port = int(match.group(1))

    # Try default port first
    port = find_available_port(default_port)

    if port != default_port:
        print(f"⚠️  Port {default_port} busy, using {port} instead")

    print(f"🚀 Serving documentation on http://127.0.0.1:{port}")
    print("   Press Ctrl+C to stop")
    print()

    cmd = ["mkdocs", "serve", "--dev-addr", f"127.0.0.1:{port}"]
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n✅ Documentation server stopped")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
