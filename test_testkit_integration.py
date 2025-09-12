"""Test that testkit fixtures work correctly in pyvider."""

import os
import pytest
from pathlib import Path

# Import testkit fixtures
try:
    from provide.testkit import clean_event_loop, temp_file, temp_directory
    TESTKIT_AVAILABLE = True
except ImportError:
    TESTKIT_AVAILABLE = False
    pytest.skip("testkit not available", allow_module_level=True)


def test_temp_file_fixture(temp_file):
    """Test that temp_file fixture works."""
    # temp_file should be a path to a file that exists
    assert os.path.exists(temp_file)
    
    # We should be able to write to it
    with open(temp_file, 'w') as f:
        f.write("test content")
    
    # And read from it
    with open(temp_file, 'r') as f:
        content = f.read()
    
    assert content == "test content"


def test_temp_directory_fixture(temp_directory):
    """Test that temp_directory fixture works."""
    # temp_directory should be a path to a directory that exists
    assert os.path.isdir(temp_directory)
    
    # We should be able to create files in it
    test_file = Path(temp_directory) / "test.txt"
    test_file.write_text("hello world")
    
    assert test_file.read_text() == "hello world"


@pytest.mark.asyncio
async def test_clean_event_loop_fixture(clean_event_loop):
    """Test that clean_event_loop fixture works."""
    import asyncio
    
    # Should be able to use async/await
    async def dummy_task():
        return "success"
    
    result = await dummy_task()
    assert result == "success"
    
    # Should have a clean event loop
    assert asyncio.get_event_loop() is not None


if __name__ == "__main__":
    print("Running testkit integration tests...")
    pytest.main([__file__, "-v"])