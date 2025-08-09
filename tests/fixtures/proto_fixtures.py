import pytest

from pyvider.proto.v6.tfplugin6_pb2 import Schema


@pytest.fixture
def sample_v6_proto():
    return Schema(description="Sample schema", version=6)

# 🐍🏗️📄🪄
