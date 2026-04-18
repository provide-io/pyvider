# SPDX-FileCopyrightText: Copyright (c) 2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Memory profiling test for schema processing."""

import pytest
from wrknv.memray.runner import run_memray_stress


@pytest.mark.memray
def test_schema_processing_memory(memray_output_dir, memray_baseline, memray_baselines_path):
    """Profile memory allocations in schema processing hot path."""
    run_memray_stress(
        script="scripts/memray/memray_schema_stress.py",
        baseline_key="schema_total_allocations",
        output_dir=memray_output_dir,
        baselines=memray_baseline,
        baselines_path=memray_baselines_path,
    )
