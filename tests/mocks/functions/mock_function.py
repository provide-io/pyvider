#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


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


# 🐍🏗️🔚
