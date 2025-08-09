# This simulates a component in a different top-level "components" package
from pyvider.resources.base import BaseResource
from pyvider.resources.decorators import register_resource
from pyvider.schema import a_str, s_resource


@register_resource("discovered_external_resource")
class DiscoveredExternalResource(BaseResource):
    def __init__(self):
        super().__init__(schema=s_resource({"id": a_str()}))
    async def read(self, ctx): pass
    async def plan(self, ctx): return None, b""
    async def apply(self, ctx): return None, b""
    async def delete(self, ctx): pass
    @staticmethod
    def get_schema(): return s_resource({"id": a_str()})


# 🐍🏗️📄🪄
