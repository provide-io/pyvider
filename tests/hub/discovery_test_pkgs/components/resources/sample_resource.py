from pyvider.resources.base import BaseResource
from pyvider.resources.decorators import register_resource
from pyvider.schema import a_str, s_resource


class DummySchemaProvider: # Minimal PvsSchema for testing
    def __init__(self):
        self.block = None # Simplified
        self.version = 1
    def validate_config(self, config, path_prefix=""): return []


@register_resource("discovered_sample_resource")
class DiscoveredSampleResource(BaseResource):
    def __init__(self):
        super().__init__(schema=s_resource({"name": a_str()}))
    async def read(self, ctx): pass
    async def plan(self, ctx): return None, b""
    async def apply(self, ctx): return None, b""
    async def delete(self, ctx): pass
    @staticmethod
    def get_schema(): return s_resource({"name": a_str()})


# 🐍🏗️📄🪄
