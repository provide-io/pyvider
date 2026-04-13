#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from pyvider.hub.components import register_data_source


@register_data_source(
    category="test_category", name="mock_data_source", description="A mock data source for testing"
)
class MockDataSource:
    """
    Mock data source for testing registry functionality.
    Simulates fetching data from an external source.
    """

    def fetch(self, identifier: str) -> dict:
        """
        Simulates fetching data for a given identifier.

        Args:
            identifier (str): Identifier for the data.

        Returns:
            dict: Mock data associated with the identifier.
        """
        return {"identifier": identifier, "value": f"Mock value for {identifier}"}


# 🐍🏗️🔚
