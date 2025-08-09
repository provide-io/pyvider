from pyvider.hub import register_resource


@register_resource(category="test_category", name="mock_resource", description="A mock resource")
class MockResource:
    def __init__(self):
        pass


# 🐍🏗️📄🪄
