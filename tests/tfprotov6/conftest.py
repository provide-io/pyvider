import pytest

from pyvider.schema import PvsObjectType, a_num, a_str, s_resource


@pytest.fixture
def simple_resource_schema():
    return s_resource(
        PvsObjectType(
            attribute_types={
                "name": a_str(required=True).type,
                "count": a_num().type
            },
            optional_attributes=frozenset(["count"])
        )
    )


# 🐍🏗️🧪🪄
