from pyvider.hub import register_function


@register_function(
    category="test_category", name="mock_function", description="A mock function for testing purposes"
)
def mock_function(data: dict) -> bool:
    """
    Mock function to validate data.

    Args:
        data (dict): Input data to validate.

    Returns:
        bool: True if the data contains the required key 'valid', False otherwise.
    """
    return "valid" in data
