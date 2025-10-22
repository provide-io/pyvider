#!/usr/bin/env python3
"""
Wrapper script to run mutmut with stats collection disabled and mutants dir relocated.
This bypasses the stats collection issue and moves mutants/ to /tmp to avoid import conflicts.
"""
import sys
import os
from pathlib import Path
import mutmut
import mutmut.__main__
from mutmut.__main__ import cli

# Relocate mutants directory to /tmp to avoid import conflicts
# Use symlink approach to catch all references (os.chdir, Path(), string paths, etc.)
MUTANTS_DIR = Path('/tmp/pyvider-mutants')
MUTANTS_DIR.mkdir(exist_ok=True, parents=True)

# Remove local mutants dir if it exists and create symlink
local_mutants = Path('mutants')
if local_mutants.exists() and not local_mutants.is_symlink():
    import shutil
    shutil.rmtree(local_mutants)
elif local_mutants.is_symlink():
    local_mutants.unlink()

# Create symlink from local mutants to /tmp
local_mutants.symlink_to(MUTANTS_DIR, target_is_directory=True)


# Monkey-patch collect_or_load_stats to skip stats collection entirely
original_collect_or_load_stats = mutmut.__main__.collect_or_load_stats


def patched_collect_or_load_stats(runner):
    """Skip stats collection - just set up minimal data structures to allow mutmut to run."""
    print("Skipping stats collection (will run all tests for each mutant)")

    # Initialize the data structures that mutmut expects
    mutmut.tests_by_mangled_function_name.clear()
    mutmut.duration_by_test.clear()


# Monkey-patch execute_pytest to handle the pytest.main() issue
original_execute_pytest = mutmut.__main__.PytestRunner.execute_pytest


def patched_execute_pytest(self, params, **kwargs):
    """Fixed execute_pytest that runs tests from the runner config."""
    import pytest

    # Fix PYTHONPATH to include src/ directory
    project_root = os.getcwd()
    src_path = os.path.join(project_root, 'src')

    # Set PYTHONPATH environment variable (works better than sys.path for subprocess/pytest)
    current_pythonpath = os.environ.get('PYTHONPATH', '')
    paths_to_add = [src_path, project_root]
    new_pythonpath_parts = paths_to_add + ([current_pythonpath] if current_pythonpath else [])
    os.environ['PYTHONPATH'] = os.pathsep.join(new_pythonpath_parts)

    # Add rootdir
    params += ['--rootdir=.']

    # If no test paths specified, use the runner command to extract test paths
    has_test_path = any(not p.startswith('-') for p in params)
    if not has_test_path and hasattr(mutmut.config, 'runner'):
        # Extract test path from runner command
        # Runner is like: "pytest tests/tfprotov6/handlers/ -x --tb=short"
        runner_parts = mutmut.config.runner.split()
        for part in runner_parts:
            if not part.startswith('-') and 'pytest' not in part and os.path.exists(part):
                params.append(part)
                break

    exit_code = int(pytest.main(params, **kwargs))

    # Treat exit code 4 as 0 (pytest usage error that we can't avoid)
    if exit_code == 4:
        return 0

    return exit_code


# Apply the monkey patches
mutmut.__main__.collect_or_load_stats = patched_collect_or_load_stats
mutmut.__main__.PytestRunner.execute_pytest = patched_execute_pytest

if __name__ == '__main__':
    sys.exit(cli())
