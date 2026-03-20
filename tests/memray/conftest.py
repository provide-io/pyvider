"""Fixtures for memray memory profiling tests."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

_baseline_updates: dict[str, int] = {}


@pytest.fixture
def memray_output_dir() -> Path:
    """Return path to memray output directory, creating it if needed."""
    output_dir = Path(__file__).parent.parent.parent / "memray-output"
    output_dir.mkdir(exist_ok=True)
    return output_dir


@pytest.fixture
def memray_baseline() -> dict[str, int]:
    """Load baseline allocation counts from baselines.json, or return empty dict if not found."""
    baseline_path = Path(__file__).parent / "baselines.json"
    if baseline_path.exists():
        with baseline_path.open() as f:
            return json.load(f)
    return {}


@pytest.fixture(autouse=True)
def _save_memray_baseline_updates(request: Any) -> None:
    """Save baseline updates to baselines.json if MEMRAY_UPDATE_BASELINE is set."""
    yield
    if os.getenv("MEMRAY_UPDATE_BASELINE") and _baseline_updates:
        baseline_path = Path(__file__).parent / "baselines.json"
        # Merge with existing baselines
        existing: dict[str, int] = {}
        if baseline_path.exists():
            with baseline_path.open() as f:
                existing = json.load(f)
        existing.update(_baseline_updates)
        with baseline_path.open("w") as f:
            json.dump(existing, f, indent=2, sort_keys=True)
            f.write("\n")


def assert_allocation_within_threshold(
    baseline: int | None, current: int, name: str, tolerance: float = 0.15
) -> None:
    """Assert that current allocation count is within tolerance of baseline.

    Args:
        baseline: Baseline allocation count (or None if first run)
        current: Current allocation count
        name: Test name for error message
        tolerance: Allowed deviation as fraction (default 15%)
    """
    if baseline is None:
        # First run: record this value and skip assertion
        key = f"{name}_total_allocations"
        _baseline_updates[key] = current
        return
    max_allowed = int(baseline * (1 + tolerance))
    if current > max_allowed:
        percent_over = ((current - baseline) / baseline) * 100
        raise AssertionError(
            f"{name} allocation {current} exceeds baseline {baseline} by {percent_over:.1f}% "
            f"(tolerance: {tolerance * 100:.0f}%)"
        )
    # Always update if MEMRAY_UPDATE_BASELINE is set
    if os.getenv("MEMRAY_UPDATE_BASELINE"):
        key = f"{name}_total_allocations"
        _baseline_updates[key] = current


def run_memray_stress(
    script_name: str,
    output_dir: Path,
) -> tuple[Path, int]:
    """Run a stress test script under memray and return (bin_path, total_allocations).

    Args:
        script_name: Name of the script in scripts/memray/ (without .py)
        output_dir: Directory for memray .bin output

    Returns:
        Tuple of (path to .bin file, total allocation count)
    """
    scripts_dir = Path(__file__).parent.parent.parent / "scripts" / "memray"
    script_path = scripts_dir / f"{script_name}.py"
    bin_path = output_dir / f"{script_name}.bin"

    # Run script under memray using the current Python interpreter
    # (avoids uv run which may re-sync and revert editable installs)
    python = sys.executable
    result = subprocess.run(
        [python, "-m", "memray", "run", "--force", "-o", str(bin_path), str(script_path)],
        capture_output=True,
        text=True,
        timeout=120,
    )
    if result.returncode != 0:
        raise RuntimeError(f"memray run failed for {script_name}:\n{result.stderr}")

    # Extract total allocations from memray stats
    stats_result = subprocess.run(
        [python, "-m", "memray", "stats", str(bin_path)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    if stats_result.returncode != 0:
        raise RuntimeError(f"memray stats failed for {script_name}:\n{stats_result.stderr}")

    total_allocs = _parse_total_allocations(stats_result.stdout)
    return bin_path, total_allocs


def _parse_total_allocations(stats_output: str) -> int:
    """Parse total allocation count from memray stats output.

    Memray stats output format has the number on the line after the label:
        Total allocations:
        \t10559
    """
    lines = stats_output.split("\n")
    for i, line in enumerate(lines):
        if "total allocations" in line.lower():
            # The count is on the next line, tab-indented
            if i + 1 < len(lines):
                count_line = lines[i + 1].strip()
                match = re.match(r"(\d[\d,]*)", count_line)
                if match:
                    return int(match.group(1).replace(",", ""))
    # Fallback: try any line with just a number after a total allocations header
    match = re.search(r"Total allocations:\s*\n\s*(\d[\d,]*)", stats_output, re.IGNORECASE)
    if match:
        return int(match.group(1).replace(",", ""))
    raise RuntimeError(f"Could not parse total allocations from memray stats output:\n{stats_output}")
