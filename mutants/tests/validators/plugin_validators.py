import os


def validate_plugin_binary(plugin_path: str):
    """
    Validates the existence and executability of a plugin binary.

    Args:
        plugin_path (str): Path to the plugin binary.

    Raises:
        FileNotFoundError: If the binary does not exist.
        PermissionError: If the binary is not executable.
    """
    if not os.path.isfile(plugin_path):
        raise FileNotFoundError(f"Plugin binary not found: {plugin_path}")

    if not os.access(plugin_path, os.X_OK):
        raise PermissionError(f"Plugin binary is not executable: {plugin_path}")


def validate_plugin_output(plugin_path: str, expected_output: str):
    """
    Validates the output of a plugin binary against expected output.

    Args:
        plugin_path (str): Path to the plugin binary.
        expected_output (str): Expected output from the plugin.

    Raises:
        ValueError: If the plugin's output does not match the expected output.
    """
    import subprocess

    try:
        result = subprocess.run([plugin_path], capture_output=True, text=True, check=True)
        actual_output = result.stdout.strip()
        if actual_output != expected_output:
            raise ValueError(f"Plugin output mismatch. Expected: {expected_output}, Got: {actual_output}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Plugin execution failed with error: {e}") from e
