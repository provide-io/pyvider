"""Memory profiling test for hub/discovery and schema-to-proto."""

import pytest

from tests.memray.conftest import assert_allocation_within_threshold, run_memray_stress


@pytest.mark.memray
def test_hub_discovery_memory(memray_output_dir, memray_baseline):
    """Profile memory allocations in hub registry and schema-to-proto hot path."""
    bin_path, total_allocs = run_memray_stress("memray_hub_stress", memray_output_dir)

    assert bin_path.exists(), f"memray binary not created: {bin_path}"
    assert total_allocs > 0, "No allocations recorded"

    baseline = memray_baseline.get("hub_total_allocations")
    assert_allocation_within_threshold(baseline, total_allocs, "hub")
