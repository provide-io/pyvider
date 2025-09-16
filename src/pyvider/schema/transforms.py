# pyvider/schema/transforms.py
import attrs

from pyvider.schema.types.attribute import PvsAttribute
from pyvider.schema.types.object import PvsObjectType
from pyvider.schema.types.schema import PvsSchema


class PvsSchemaTransformer:
    """Utility for transforming and extending Terraform schemas."""

    def add_attribute(self, schema: PvsSchema, attribute: PvsAttribute) -> PvsSchema:
        block = schema.block
        if attribute.name in block.attributes:
            raise ValueError(f"Attribute '{attribute.name}' already exists in schema")
        new_attrs = block.attributes.copy()
        new_attrs[attribute.name] = attribute
        new_block = attrs.evolve(block, attributes=new_attrs)
        return attrs.evolve(schema, block=new_block)

    def remove_attribute(self, schema: PvsSchema, attribute_name: str) -> PvsSchema:
        block = schema.block
        if attribute_name not in block.attributes:
            raise ValueError(f"Attribute '{attribute_name}' not found in schema")
        new_attrs = {k: v for k, v in block.attributes.items() if k != attribute_name}
        new_block = attrs.evolve(block, attributes=new_attrs)
        return attrs.evolve(schema, block=new_block)

    def merge_schemas(self, schemas: list[PvsSchema], description: str = "") -> PvsSchema:
        all_attrs = {}
        all_block_types = []
        block_type_names = set()
        for s in schemas:
            block = s.block
            for name, attr in block.attributes.items():
                if name in all_attrs:
                    raise ValueError(f"Attribute name conflict: '{name}'")
                all_attrs[name] = attr
            for bt in block.block_types:
                if bt.type_name in block_type_names:
                    raise ValueError(f"Block type name conflict: '{bt.type_name}'")
                all_block_types.append(bt)
                block_type_names.add(bt.type_name)
        new_block = PvsObjectType(
            attributes=all_attrs,
            block_types=tuple(all_block_types),
            description=description,
        )
        return PvsSchema(version=1, block=new_block)
