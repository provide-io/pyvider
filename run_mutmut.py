#!/usr/bin/env python3
"""
Wrapper script to run mutmut with a patched execute_pytest method.
This fixes the stats collection issue where pytest.main() returns exit code 4.
"""
import sys
import mutmut
from mutmut.__main__ import cli


# Monkey-patch the execute_pytest method to handle exit code 4 gracefully
original_execute_pytest = mutmut.__main__.PytestRunner.execute_pytest


def patched_execute_pytest(self, params, **kwargs):
    """Patched version that adds test paths and fixes PYTHONPATH."""
    import pytest
    import sys
    import os

    # Get absolute paths
    project_root = os.getcwd()
    src_path = os.path.join(project_root, 'src')

    # Ensure src/ is in PYTHONPATH for imports to work (at the front!)
    if src_path in sys.path:
        sys.path.remove(src_path)
    sys.path.insert(0, src_path)

    # Also ensure project root is in path
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    params += ['--rootdir=.']

    # If no test paths are specified (stats collection phase), add them from config
    # Make sure we use the ORIGINAL tests directory, not mutants/tests
    has_test_path = any(not p.startswith('-') for p in params)
    if not has_test_path:
        # Add absolute path to original tests to avoid mutants/ directory
        test_path = os.path.join(project_root, 'tests', 'tfprotov6', 'handlers')
        params.append(test_path)

    exit_code = int(pytest.main(params, **kwargs))

    return exit_code


# Apply the monkey patch
mutmut.__main__.PytestRunner.execute_pytest = patched_execute_pytest

if __name__ == '__main__':
    sys.exit(cli())
