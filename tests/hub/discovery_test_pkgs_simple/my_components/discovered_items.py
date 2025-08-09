# This file will be "imported" by the test

# Minimal stubs, registration is the focus
class DiscoveredRes:
    _is_registered_resource = True
    _registered_name = "discovered_res_simple"
    def get_schema(self): return None # Placeholder

def discovered_func_simple(): pass
discovered_func_simple._is_registered_function = True # type: ignore
discovered_func_simple._registered_name = "discovered_func_simple" # type: ignore


# 🐍🏗️📄🪄
