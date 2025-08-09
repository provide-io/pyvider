from typing import Any

import attrs

from pyvider.cty import CtyList, CtyObject, CtyString
from pyvider.resources.base import BaseResource


@attrs.define(frozen=True)
class NestedConfig:
    setting: str

@attrs.define(frozen=True)
class TopLevelConfig:
    name: str
    nested: NestedConfig
    items: list[NestedConfig]

class DummyResource(BaseResource):
    config_class = TopLevelConfig
    state_class = None # Not needed for this test
    def get_schema(self): pass
    async def _validate_config(self, config: Any) -> list[str]: return []
    async def read(self, ctx): pass
    async def plan(self, ctx): pass
    async def apply(self, ctx): pass
    async def delete(self, ctx): pass

def test_from_cty_with_nested_objects():
    """
    TDD Test for BaseResource.from_cty to ensure it correctly
    deserializes nested CtyObjects into nested attrs classes.
    """
    nested_schema = CtyObject({"setting": CtyString()})
    top_level_schema = CtyObject({
        "name": CtyString(),
        "nested": nested_schema,
        "items": CtyList(element_type=nested_schema)
    })

    cty_value = top_level_schema.validate({
        "name": "test-resource",
        "nested": {"setting": "enabled"},
        "items": [{"setting": "item1"}, {"setting": "item2"}]
    })

    result = DummyResource.from_cty(cty_value, TopLevelConfig)

    assert isinstance(result, TopLevelConfig)
    assert result.name == "test-resource"
    assert isinstance(result.nested, NestedConfig)
    assert result.nested.setting == "enabled"
    assert isinstance(result.items, list)
    assert len(result.items) == 2
    assert isinstance(result.items[0], NestedConfig)
    assert result.items[0].setting == "item1"


# 🐍🏗️🧪🪄
