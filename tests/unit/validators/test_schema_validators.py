from tests.validators.schema_validators import validate_schema_dict


def test_schema_validation():
    schema = {
        "description": "Valid schema",
        "attributes": [{"name": "attr1", "type": "string"}],
        "block_types": [{"name": "block1", "nested": True}]
    }
    validate_schema_dict(schema)
