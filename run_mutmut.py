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
    """Patched version that adds test paths for stats collection."""
    import pytest
    params += ['--rootdir=.']

    # If no test paths are specified (stats collection phase), add them from config
    has_test_path = any(not p.startswith('-') for p in params)
    if not has_test_path:
        # Add test path from mutmut runner config
        params.append('tests/tfprotov6/handlers/')

    exit_code = int(pytest.main(params, **kwargs))

    return exit_code


# Apply the monkey patch
mutmut.__main__.PytestRunner.execute_pytest = patched_execute_pytest

if __name__ == '__main__':
    sys.exit(cli())
