#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from pyvider.hub import register_resource


@register_resource(category="test_category", name="mock_resource", description="A mock resource")
class MockResource:
    def __init__(self) -> None:
        pass


# 🐍🏗️🔚
