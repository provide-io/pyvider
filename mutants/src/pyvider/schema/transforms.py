# pyvider/schema/transforms.py
import attrs

from pyvider.schema.types.attribute import PvsAttribute
from pyvider.schema.types.object import PvsObjectType
from pyvider.schema.types.schema import PvsSchema
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


class PvsSchemaTransformer:
    """Utility for transforming and extending Terraform schemas."""

    def xǁPvsSchemaTransformerǁadd_attribute__mutmut_orig(self, schema: PvsSchema, attribute: PvsAttribute) -> PvsSchema:
        block = schema.block
        if attribute.name in block.attributes:
            raise ValueError(f"Attribute '{attribute.name}' already exists in schema")
        new_attrs = block.attributes.copy()
        new_attrs[attribute.name] = attribute
        new_block = attrs.evolve(block, attributes=new_attrs)
        return attrs.evolve(schema, block=new_block)

    def xǁPvsSchemaTransformerǁadd_attribute__mutmut_1(self, schema: PvsSchema, attribute: PvsAttribute) -> PvsSchema:
        block = None
        if attribute.name in block.attributes:
            raise ValueError(f"Attribute '{attribute.name}' already exists in schema")
        new_attrs = block.attributes.copy()
        new_attrs[attribute.name] = attribute
        new_block = attrs.evolve(block, attributes=new_attrs)
        return attrs.evolve(schema, block=new_block)

    def xǁPvsSchemaTransformerǁadd_attribute__mutmut_2(self, schema: PvsSchema, attribute: PvsAttribute) -> PvsSchema:
        block = schema.block
        if attribute.name not in block.attributes:
            raise ValueError(f"Attribute '{attribute.name}' already exists in schema")
        new_attrs = block.attributes.copy()
        new_attrs[attribute.name] = attribute
        new_block = attrs.evolve(block, attributes=new_attrs)
        return attrs.evolve(schema, block=new_block)

    def xǁPvsSchemaTransformerǁadd_attribute__mutmut_3(self, schema: PvsSchema, attribute: PvsAttribute) -> PvsSchema:
        block = schema.block
        if attribute.name in block.attributes:
            raise ValueError(None)
        new_attrs = block.attributes.copy()
        new_attrs[attribute.name] = attribute
        new_block = attrs.evolve(block, attributes=new_attrs)
        return attrs.evolve(schema, block=new_block)

    def xǁPvsSchemaTransformerǁadd_attribute__mutmut_4(self, schema: PvsSchema, attribute: PvsAttribute) -> PvsSchema:
        block = schema.block
        if attribute.name in block.attributes:
            raise ValueError(f"Attribute '{attribute.name}' already exists in schema")
        new_attrs = None
        new_attrs[attribute.name] = attribute
        new_block = attrs.evolve(block, attributes=new_attrs)
        return attrs.evolve(schema, block=new_block)

    def xǁPvsSchemaTransformerǁadd_attribute__mutmut_5(self, schema: PvsSchema, attribute: PvsAttribute) -> PvsSchema:
        block = schema.block
        if attribute.name in block.attributes:
            raise ValueError(f"Attribute '{attribute.name}' already exists in schema")
        new_attrs = block.attributes.copy()
        new_attrs[attribute.name] = None
        new_block = attrs.evolve(block, attributes=new_attrs)
        return attrs.evolve(schema, block=new_block)

    def xǁPvsSchemaTransformerǁadd_attribute__mutmut_6(self, schema: PvsSchema, attribute: PvsAttribute) -> PvsSchema:
        block = schema.block
        if attribute.name in block.attributes:
            raise ValueError(f"Attribute '{attribute.name}' already exists in schema")
        new_attrs = block.attributes.copy()
        new_attrs[attribute.name] = attribute
        new_block = None
        return attrs.evolve(schema, block=new_block)

    def xǁPvsSchemaTransformerǁadd_attribute__mutmut_7(self, schema: PvsSchema, attribute: PvsAttribute) -> PvsSchema:
        block = schema.block
        if attribute.name in block.attributes:
            raise ValueError(f"Attribute '{attribute.name}' already exists in schema")
        new_attrs = block.attributes.copy()
        new_attrs[attribute.name] = attribute
        new_block = attrs.evolve(None, attributes=new_attrs)
        return attrs.evolve(schema, block=new_block)

    def xǁPvsSchemaTransformerǁadd_attribute__mutmut_8(self, schema: PvsSchema, attribute: PvsAttribute) -> PvsSchema:
        block = schema.block
        if attribute.name in block.attributes:
            raise ValueError(f"Attribute '{attribute.name}' already exists in schema")
        new_attrs = block.attributes.copy()
        new_attrs[attribute.name] = attribute
        new_block = attrs.evolve(block, attributes=None)
        return attrs.evolve(schema, block=new_block)

    def xǁPvsSchemaTransformerǁadd_attribute__mutmut_9(self, schema: PvsSchema, attribute: PvsAttribute) -> PvsSchema:
        block = schema.block
        if attribute.name in block.attributes:
            raise ValueError(f"Attribute '{attribute.name}' already exists in schema")
        new_attrs = block.attributes.copy()
        new_attrs[attribute.name] = attribute
        new_block = attrs.evolve(attributes=new_attrs)
        return attrs.evolve(schema, block=new_block)

    def xǁPvsSchemaTransformerǁadd_attribute__mutmut_10(self, schema: PvsSchema, attribute: PvsAttribute) -> PvsSchema:
        block = schema.block
        if attribute.name in block.attributes:
            raise ValueError(f"Attribute '{attribute.name}' already exists in schema")
        new_attrs = block.attributes.copy()
        new_attrs[attribute.name] = attribute
        new_block = attrs.evolve(block, )
        return attrs.evolve(schema, block=new_block)

    def xǁPvsSchemaTransformerǁadd_attribute__mutmut_11(self, schema: PvsSchema, attribute: PvsAttribute) -> PvsSchema:
        block = schema.block
        if attribute.name in block.attributes:
            raise ValueError(f"Attribute '{attribute.name}' already exists in schema")
        new_attrs = block.attributes.copy()
        new_attrs[attribute.name] = attribute
        new_block = attrs.evolve(block, attributes=new_attrs)
        return attrs.evolve(None, block=new_block)

    def xǁPvsSchemaTransformerǁadd_attribute__mutmut_12(self, schema: PvsSchema, attribute: PvsAttribute) -> PvsSchema:
        block = schema.block
        if attribute.name in block.attributes:
            raise ValueError(f"Attribute '{attribute.name}' already exists in schema")
        new_attrs = block.attributes.copy()
        new_attrs[attribute.name] = attribute
        new_block = attrs.evolve(block, attributes=new_attrs)
        return attrs.evolve(schema, block=None)

    def xǁPvsSchemaTransformerǁadd_attribute__mutmut_13(self, schema: PvsSchema, attribute: PvsAttribute) -> PvsSchema:
        block = schema.block
        if attribute.name in block.attributes:
            raise ValueError(f"Attribute '{attribute.name}' already exists in schema")
        new_attrs = block.attributes.copy()
        new_attrs[attribute.name] = attribute
        new_block = attrs.evolve(block, attributes=new_attrs)
        return attrs.evolve(block=new_block)

    def xǁPvsSchemaTransformerǁadd_attribute__mutmut_14(self, schema: PvsSchema, attribute: PvsAttribute) -> PvsSchema:
        block = schema.block
        if attribute.name in block.attributes:
            raise ValueError(f"Attribute '{attribute.name}' already exists in schema")
        new_attrs = block.attributes.copy()
        new_attrs[attribute.name] = attribute
        new_block = attrs.evolve(block, attributes=new_attrs)
        return attrs.evolve(schema, )
    
    xǁPvsSchemaTransformerǁadd_attribute__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁPvsSchemaTransformerǁadd_attribute__mutmut_1': xǁPvsSchemaTransformerǁadd_attribute__mutmut_1, 
        'xǁPvsSchemaTransformerǁadd_attribute__mutmut_2': xǁPvsSchemaTransformerǁadd_attribute__mutmut_2, 
        'xǁPvsSchemaTransformerǁadd_attribute__mutmut_3': xǁPvsSchemaTransformerǁadd_attribute__mutmut_3, 
        'xǁPvsSchemaTransformerǁadd_attribute__mutmut_4': xǁPvsSchemaTransformerǁadd_attribute__mutmut_4, 
        'xǁPvsSchemaTransformerǁadd_attribute__mutmut_5': xǁPvsSchemaTransformerǁadd_attribute__mutmut_5, 
        'xǁPvsSchemaTransformerǁadd_attribute__mutmut_6': xǁPvsSchemaTransformerǁadd_attribute__mutmut_6, 
        'xǁPvsSchemaTransformerǁadd_attribute__mutmut_7': xǁPvsSchemaTransformerǁadd_attribute__mutmut_7, 
        'xǁPvsSchemaTransformerǁadd_attribute__mutmut_8': xǁPvsSchemaTransformerǁadd_attribute__mutmut_8, 
        'xǁPvsSchemaTransformerǁadd_attribute__mutmut_9': xǁPvsSchemaTransformerǁadd_attribute__mutmut_9, 
        'xǁPvsSchemaTransformerǁadd_attribute__mutmut_10': xǁPvsSchemaTransformerǁadd_attribute__mutmut_10, 
        'xǁPvsSchemaTransformerǁadd_attribute__mutmut_11': xǁPvsSchemaTransformerǁadd_attribute__mutmut_11, 
        'xǁPvsSchemaTransformerǁadd_attribute__mutmut_12': xǁPvsSchemaTransformerǁadd_attribute__mutmut_12, 
        'xǁPvsSchemaTransformerǁadd_attribute__mutmut_13': xǁPvsSchemaTransformerǁadd_attribute__mutmut_13, 
        'xǁPvsSchemaTransformerǁadd_attribute__mutmut_14': xǁPvsSchemaTransformerǁadd_attribute__mutmut_14
    }
    
    def add_attribute(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁPvsSchemaTransformerǁadd_attribute__mutmut_orig"), object.__getattribute__(self, "xǁPvsSchemaTransformerǁadd_attribute__mutmut_mutants"), args, kwargs, self)
        return result 
    
    add_attribute.__signature__ = _mutmut_signature(xǁPvsSchemaTransformerǁadd_attribute__mutmut_orig)
    xǁPvsSchemaTransformerǁadd_attribute__mutmut_orig.__name__ = 'xǁPvsSchemaTransformerǁadd_attribute'

    def xǁPvsSchemaTransformerǁremove_attribute__mutmut_orig(self, schema: PvsSchema, attribute_name: str) -> PvsSchema:
        block = schema.block
        if attribute_name not in block.attributes:
            raise ValueError(f"Attribute '{attribute_name}' not found in schema")
        new_attrs = {k: v for k, v in block.attributes.items() if k != attribute_name}
        new_block = attrs.evolve(block, attributes=new_attrs)
        return attrs.evolve(schema, block=new_block)

    def xǁPvsSchemaTransformerǁremove_attribute__mutmut_1(self, schema: PvsSchema, attribute_name: str) -> PvsSchema:
        block = None
        if attribute_name not in block.attributes:
            raise ValueError(f"Attribute '{attribute_name}' not found in schema")
        new_attrs = {k: v for k, v in block.attributes.items() if k != attribute_name}
        new_block = attrs.evolve(block, attributes=new_attrs)
        return attrs.evolve(schema, block=new_block)

    def xǁPvsSchemaTransformerǁremove_attribute__mutmut_2(self, schema: PvsSchema, attribute_name: str) -> PvsSchema:
        block = schema.block
        if attribute_name in block.attributes:
            raise ValueError(f"Attribute '{attribute_name}' not found in schema")
        new_attrs = {k: v for k, v in block.attributes.items() if k != attribute_name}
        new_block = attrs.evolve(block, attributes=new_attrs)
        return attrs.evolve(schema, block=new_block)

    def xǁPvsSchemaTransformerǁremove_attribute__mutmut_3(self, schema: PvsSchema, attribute_name: str) -> PvsSchema:
        block = schema.block
        if attribute_name not in block.attributes:
            raise ValueError(None)
        new_attrs = {k: v for k, v in block.attributes.items() if k != attribute_name}
        new_block = attrs.evolve(block, attributes=new_attrs)
        return attrs.evolve(schema, block=new_block)

    def xǁPvsSchemaTransformerǁremove_attribute__mutmut_4(self, schema: PvsSchema, attribute_name: str) -> PvsSchema:
        block = schema.block
        if attribute_name not in block.attributes:
            raise ValueError(f"Attribute '{attribute_name}' not found in schema")
        new_attrs = None
        new_block = attrs.evolve(block, attributes=new_attrs)
        return attrs.evolve(schema, block=new_block)

    def xǁPvsSchemaTransformerǁremove_attribute__mutmut_5(self, schema: PvsSchema, attribute_name: str) -> PvsSchema:
        block = schema.block
        if attribute_name not in block.attributes:
            raise ValueError(f"Attribute '{attribute_name}' not found in schema")
        new_attrs = {k: v for k, v in block.attributes.items() if k == attribute_name}
        new_block = attrs.evolve(block, attributes=new_attrs)
        return attrs.evolve(schema, block=new_block)

    def xǁPvsSchemaTransformerǁremove_attribute__mutmut_6(self, schema: PvsSchema, attribute_name: str) -> PvsSchema:
        block = schema.block
        if attribute_name not in block.attributes:
            raise ValueError(f"Attribute '{attribute_name}' not found in schema")
        new_attrs = {k: v for k, v in block.attributes.items() if k != attribute_name}
        new_block = None
        return attrs.evolve(schema, block=new_block)

    def xǁPvsSchemaTransformerǁremove_attribute__mutmut_7(self, schema: PvsSchema, attribute_name: str) -> PvsSchema:
        block = schema.block
        if attribute_name not in block.attributes:
            raise ValueError(f"Attribute '{attribute_name}' not found in schema")
        new_attrs = {k: v for k, v in block.attributes.items() if k != attribute_name}
        new_block = attrs.evolve(None, attributes=new_attrs)
        return attrs.evolve(schema, block=new_block)

    def xǁPvsSchemaTransformerǁremove_attribute__mutmut_8(self, schema: PvsSchema, attribute_name: str) -> PvsSchema:
        block = schema.block
        if attribute_name not in block.attributes:
            raise ValueError(f"Attribute '{attribute_name}' not found in schema")
        new_attrs = {k: v for k, v in block.attributes.items() if k != attribute_name}
        new_block = attrs.evolve(block, attributes=None)
        return attrs.evolve(schema, block=new_block)

    def xǁPvsSchemaTransformerǁremove_attribute__mutmut_9(self, schema: PvsSchema, attribute_name: str) -> PvsSchema:
        block = schema.block
        if attribute_name not in block.attributes:
            raise ValueError(f"Attribute '{attribute_name}' not found in schema")
        new_attrs = {k: v for k, v in block.attributes.items() if k != attribute_name}
        new_block = attrs.evolve(attributes=new_attrs)
        return attrs.evolve(schema, block=new_block)

    def xǁPvsSchemaTransformerǁremove_attribute__mutmut_10(self, schema: PvsSchema, attribute_name: str) -> PvsSchema:
        block = schema.block
        if attribute_name not in block.attributes:
            raise ValueError(f"Attribute '{attribute_name}' not found in schema")
        new_attrs = {k: v for k, v in block.attributes.items() if k != attribute_name}
        new_block = attrs.evolve(block, )
        return attrs.evolve(schema, block=new_block)

    def xǁPvsSchemaTransformerǁremove_attribute__mutmut_11(self, schema: PvsSchema, attribute_name: str) -> PvsSchema:
        block = schema.block
        if attribute_name not in block.attributes:
            raise ValueError(f"Attribute '{attribute_name}' not found in schema")
        new_attrs = {k: v for k, v in block.attributes.items() if k != attribute_name}
        new_block = attrs.evolve(block, attributes=new_attrs)
        return attrs.evolve(None, block=new_block)

    def xǁPvsSchemaTransformerǁremove_attribute__mutmut_12(self, schema: PvsSchema, attribute_name: str) -> PvsSchema:
        block = schema.block
        if attribute_name not in block.attributes:
            raise ValueError(f"Attribute '{attribute_name}' not found in schema")
        new_attrs = {k: v for k, v in block.attributes.items() if k != attribute_name}
        new_block = attrs.evolve(block, attributes=new_attrs)
        return attrs.evolve(schema, block=None)

    def xǁPvsSchemaTransformerǁremove_attribute__mutmut_13(self, schema: PvsSchema, attribute_name: str) -> PvsSchema:
        block = schema.block
        if attribute_name not in block.attributes:
            raise ValueError(f"Attribute '{attribute_name}' not found in schema")
        new_attrs = {k: v for k, v in block.attributes.items() if k != attribute_name}
        new_block = attrs.evolve(block, attributes=new_attrs)
        return attrs.evolve(block=new_block)

    def xǁPvsSchemaTransformerǁremove_attribute__mutmut_14(self, schema: PvsSchema, attribute_name: str) -> PvsSchema:
        block = schema.block
        if attribute_name not in block.attributes:
            raise ValueError(f"Attribute '{attribute_name}' not found in schema")
        new_attrs = {k: v for k, v in block.attributes.items() if k != attribute_name}
        new_block = attrs.evolve(block, attributes=new_attrs)
        return attrs.evolve(schema, )
    
    xǁPvsSchemaTransformerǁremove_attribute__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁPvsSchemaTransformerǁremove_attribute__mutmut_1': xǁPvsSchemaTransformerǁremove_attribute__mutmut_1, 
        'xǁPvsSchemaTransformerǁremove_attribute__mutmut_2': xǁPvsSchemaTransformerǁremove_attribute__mutmut_2, 
        'xǁPvsSchemaTransformerǁremove_attribute__mutmut_3': xǁPvsSchemaTransformerǁremove_attribute__mutmut_3, 
        'xǁPvsSchemaTransformerǁremove_attribute__mutmut_4': xǁPvsSchemaTransformerǁremove_attribute__mutmut_4, 
        'xǁPvsSchemaTransformerǁremove_attribute__mutmut_5': xǁPvsSchemaTransformerǁremove_attribute__mutmut_5, 
        'xǁPvsSchemaTransformerǁremove_attribute__mutmut_6': xǁPvsSchemaTransformerǁremove_attribute__mutmut_6, 
        'xǁPvsSchemaTransformerǁremove_attribute__mutmut_7': xǁPvsSchemaTransformerǁremove_attribute__mutmut_7, 
        'xǁPvsSchemaTransformerǁremove_attribute__mutmut_8': xǁPvsSchemaTransformerǁremove_attribute__mutmut_8, 
        'xǁPvsSchemaTransformerǁremove_attribute__mutmut_9': xǁPvsSchemaTransformerǁremove_attribute__mutmut_9, 
        'xǁPvsSchemaTransformerǁremove_attribute__mutmut_10': xǁPvsSchemaTransformerǁremove_attribute__mutmut_10, 
        'xǁPvsSchemaTransformerǁremove_attribute__mutmut_11': xǁPvsSchemaTransformerǁremove_attribute__mutmut_11, 
        'xǁPvsSchemaTransformerǁremove_attribute__mutmut_12': xǁPvsSchemaTransformerǁremove_attribute__mutmut_12, 
        'xǁPvsSchemaTransformerǁremove_attribute__mutmut_13': xǁPvsSchemaTransformerǁremove_attribute__mutmut_13, 
        'xǁPvsSchemaTransformerǁremove_attribute__mutmut_14': xǁPvsSchemaTransformerǁremove_attribute__mutmut_14
    }
    
    def remove_attribute(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁPvsSchemaTransformerǁremove_attribute__mutmut_orig"), object.__getattribute__(self, "xǁPvsSchemaTransformerǁremove_attribute__mutmut_mutants"), args, kwargs, self)
        return result 
    
    remove_attribute.__signature__ = _mutmut_signature(xǁPvsSchemaTransformerǁremove_attribute__mutmut_orig)
    xǁPvsSchemaTransformerǁremove_attribute__mutmut_orig.__name__ = 'xǁPvsSchemaTransformerǁremove_attribute'

    def xǁPvsSchemaTransformerǁmerge_schemas__mutmut_orig(self, schemas: list[PvsSchema], description: str = "") -> PvsSchema:
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

    def xǁPvsSchemaTransformerǁmerge_schemas__mutmut_1(self, schemas: list[PvsSchema], description: str = "XXXX") -> PvsSchema:
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

    def xǁPvsSchemaTransformerǁmerge_schemas__mutmut_2(self, schemas: list[PvsSchema], description: str = "") -> PvsSchema:
        all_attrs = None
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

    def xǁPvsSchemaTransformerǁmerge_schemas__mutmut_3(self, schemas: list[PvsSchema], description: str = "") -> PvsSchema:
        all_attrs = {}
        all_block_types = None
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

    def xǁPvsSchemaTransformerǁmerge_schemas__mutmut_4(self, schemas: list[PvsSchema], description: str = "") -> PvsSchema:
        all_attrs = {}
        all_block_types = []
        block_type_names = None
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

    def xǁPvsSchemaTransformerǁmerge_schemas__mutmut_5(self, schemas: list[PvsSchema], description: str = "") -> PvsSchema:
        all_attrs = {}
        all_block_types = []
        block_type_names = set()
        for s in schemas:
            block = None
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

    def xǁPvsSchemaTransformerǁmerge_schemas__mutmut_6(self, schemas: list[PvsSchema], description: str = "") -> PvsSchema:
        all_attrs = {}
        all_block_types = []
        block_type_names = set()
        for s in schemas:
            block = s.block
            for name, attr in block.attributes.items():
                if name not in all_attrs:
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

    def xǁPvsSchemaTransformerǁmerge_schemas__mutmut_7(self, schemas: list[PvsSchema], description: str = "") -> PvsSchema:
        all_attrs = {}
        all_block_types = []
        block_type_names = set()
        for s in schemas:
            block = s.block
            for name, attr in block.attributes.items():
                if name in all_attrs:
                    raise ValueError(None)
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

    def xǁPvsSchemaTransformerǁmerge_schemas__mutmut_8(self, schemas: list[PvsSchema], description: str = "") -> PvsSchema:
        all_attrs = {}
        all_block_types = []
        block_type_names = set()
        for s in schemas:
            block = s.block
            for name, attr in block.attributes.items():
                if name in all_attrs:
                    raise ValueError(f"Attribute name conflict: '{name}'")
                all_attrs[name] = None
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

    def xǁPvsSchemaTransformerǁmerge_schemas__mutmut_9(self, schemas: list[PvsSchema], description: str = "") -> PvsSchema:
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
                if bt.type_name not in block_type_names:
                    raise ValueError(f"Block type name conflict: '{bt.type_name}'")
                all_block_types.append(bt)
                block_type_names.add(bt.type_name)
        new_block = PvsObjectType(
            attributes=all_attrs,
            block_types=tuple(all_block_types),
            description=description,
        )
        return PvsSchema(version=1, block=new_block)

    def xǁPvsSchemaTransformerǁmerge_schemas__mutmut_10(self, schemas: list[PvsSchema], description: str = "") -> PvsSchema:
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
                    raise ValueError(None)
                all_block_types.append(bt)
                block_type_names.add(bt.type_name)
        new_block = PvsObjectType(
            attributes=all_attrs,
            block_types=tuple(all_block_types),
            description=description,
        )
        return PvsSchema(version=1, block=new_block)

    def xǁPvsSchemaTransformerǁmerge_schemas__mutmut_11(self, schemas: list[PvsSchema], description: str = "") -> PvsSchema:
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
                all_block_types.append(None)
                block_type_names.add(bt.type_name)
        new_block = PvsObjectType(
            attributes=all_attrs,
            block_types=tuple(all_block_types),
            description=description,
        )
        return PvsSchema(version=1, block=new_block)

    def xǁPvsSchemaTransformerǁmerge_schemas__mutmut_12(self, schemas: list[PvsSchema], description: str = "") -> PvsSchema:
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
                block_type_names.add(None)
        new_block = PvsObjectType(
            attributes=all_attrs,
            block_types=tuple(all_block_types),
            description=description,
        )
        return PvsSchema(version=1, block=new_block)

    def xǁPvsSchemaTransformerǁmerge_schemas__mutmut_13(self, schemas: list[PvsSchema], description: str = "") -> PvsSchema:
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
        new_block = None
        return PvsSchema(version=1, block=new_block)

    def xǁPvsSchemaTransformerǁmerge_schemas__mutmut_14(self, schemas: list[PvsSchema], description: str = "") -> PvsSchema:
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
            attributes=None,
            block_types=tuple(all_block_types),
            description=description,
        )
        return PvsSchema(version=1, block=new_block)

    def xǁPvsSchemaTransformerǁmerge_schemas__mutmut_15(self, schemas: list[PvsSchema], description: str = "") -> PvsSchema:
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
            block_types=None,
            description=description,
        )
        return PvsSchema(version=1, block=new_block)

    def xǁPvsSchemaTransformerǁmerge_schemas__mutmut_16(self, schemas: list[PvsSchema], description: str = "") -> PvsSchema:
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
            description=None,
        )
        return PvsSchema(version=1, block=new_block)

    def xǁPvsSchemaTransformerǁmerge_schemas__mutmut_17(self, schemas: list[PvsSchema], description: str = "") -> PvsSchema:
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
            block_types=tuple(all_block_types),
            description=description,
        )
        return PvsSchema(version=1, block=new_block)

    def xǁPvsSchemaTransformerǁmerge_schemas__mutmut_18(self, schemas: list[PvsSchema], description: str = "") -> PvsSchema:
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
            description=description,
        )
        return PvsSchema(version=1, block=new_block)

    def xǁPvsSchemaTransformerǁmerge_schemas__mutmut_19(self, schemas: list[PvsSchema], description: str = "") -> PvsSchema:
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
            )
        return PvsSchema(version=1, block=new_block)

    def xǁPvsSchemaTransformerǁmerge_schemas__mutmut_20(self, schemas: list[PvsSchema], description: str = "") -> PvsSchema:
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
            block_types=tuple(None),
            description=description,
        )
        return PvsSchema(version=1, block=new_block)

    def xǁPvsSchemaTransformerǁmerge_schemas__mutmut_21(self, schemas: list[PvsSchema], description: str = "") -> PvsSchema:
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
        return PvsSchema(version=None, block=new_block)

    def xǁPvsSchemaTransformerǁmerge_schemas__mutmut_22(self, schemas: list[PvsSchema], description: str = "") -> PvsSchema:
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
        return PvsSchema(version=1, block=None)

    def xǁPvsSchemaTransformerǁmerge_schemas__mutmut_23(self, schemas: list[PvsSchema], description: str = "") -> PvsSchema:
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
        return PvsSchema(block=new_block)

    def xǁPvsSchemaTransformerǁmerge_schemas__mutmut_24(self, schemas: list[PvsSchema], description: str = "") -> PvsSchema:
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
        return PvsSchema(version=1, )

    def xǁPvsSchemaTransformerǁmerge_schemas__mutmut_25(self, schemas: list[PvsSchema], description: str = "") -> PvsSchema:
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
        return PvsSchema(version=2, block=new_block)
    
    xǁPvsSchemaTransformerǁmerge_schemas__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁPvsSchemaTransformerǁmerge_schemas__mutmut_1': xǁPvsSchemaTransformerǁmerge_schemas__mutmut_1, 
        'xǁPvsSchemaTransformerǁmerge_schemas__mutmut_2': xǁPvsSchemaTransformerǁmerge_schemas__mutmut_2, 
        'xǁPvsSchemaTransformerǁmerge_schemas__mutmut_3': xǁPvsSchemaTransformerǁmerge_schemas__mutmut_3, 
        'xǁPvsSchemaTransformerǁmerge_schemas__mutmut_4': xǁPvsSchemaTransformerǁmerge_schemas__mutmut_4, 
        'xǁPvsSchemaTransformerǁmerge_schemas__mutmut_5': xǁPvsSchemaTransformerǁmerge_schemas__mutmut_5, 
        'xǁPvsSchemaTransformerǁmerge_schemas__mutmut_6': xǁPvsSchemaTransformerǁmerge_schemas__mutmut_6, 
        'xǁPvsSchemaTransformerǁmerge_schemas__mutmut_7': xǁPvsSchemaTransformerǁmerge_schemas__mutmut_7, 
        'xǁPvsSchemaTransformerǁmerge_schemas__mutmut_8': xǁPvsSchemaTransformerǁmerge_schemas__mutmut_8, 
        'xǁPvsSchemaTransformerǁmerge_schemas__mutmut_9': xǁPvsSchemaTransformerǁmerge_schemas__mutmut_9, 
        'xǁPvsSchemaTransformerǁmerge_schemas__mutmut_10': xǁPvsSchemaTransformerǁmerge_schemas__mutmut_10, 
        'xǁPvsSchemaTransformerǁmerge_schemas__mutmut_11': xǁPvsSchemaTransformerǁmerge_schemas__mutmut_11, 
        'xǁPvsSchemaTransformerǁmerge_schemas__mutmut_12': xǁPvsSchemaTransformerǁmerge_schemas__mutmut_12, 
        'xǁPvsSchemaTransformerǁmerge_schemas__mutmut_13': xǁPvsSchemaTransformerǁmerge_schemas__mutmut_13, 
        'xǁPvsSchemaTransformerǁmerge_schemas__mutmut_14': xǁPvsSchemaTransformerǁmerge_schemas__mutmut_14, 
        'xǁPvsSchemaTransformerǁmerge_schemas__mutmut_15': xǁPvsSchemaTransformerǁmerge_schemas__mutmut_15, 
        'xǁPvsSchemaTransformerǁmerge_schemas__mutmut_16': xǁPvsSchemaTransformerǁmerge_schemas__mutmut_16, 
        'xǁPvsSchemaTransformerǁmerge_schemas__mutmut_17': xǁPvsSchemaTransformerǁmerge_schemas__mutmut_17, 
        'xǁPvsSchemaTransformerǁmerge_schemas__mutmut_18': xǁPvsSchemaTransformerǁmerge_schemas__mutmut_18, 
        'xǁPvsSchemaTransformerǁmerge_schemas__mutmut_19': xǁPvsSchemaTransformerǁmerge_schemas__mutmut_19, 
        'xǁPvsSchemaTransformerǁmerge_schemas__mutmut_20': xǁPvsSchemaTransformerǁmerge_schemas__mutmut_20, 
        'xǁPvsSchemaTransformerǁmerge_schemas__mutmut_21': xǁPvsSchemaTransformerǁmerge_schemas__mutmut_21, 
        'xǁPvsSchemaTransformerǁmerge_schemas__mutmut_22': xǁPvsSchemaTransformerǁmerge_schemas__mutmut_22, 
        'xǁPvsSchemaTransformerǁmerge_schemas__mutmut_23': xǁPvsSchemaTransformerǁmerge_schemas__mutmut_23, 
        'xǁPvsSchemaTransformerǁmerge_schemas__mutmut_24': xǁPvsSchemaTransformerǁmerge_schemas__mutmut_24, 
        'xǁPvsSchemaTransformerǁmerge_schemas__mutmut_25': xǁPvsSchemaTransformerǁmerge_schemas__mutmut_25
    }
    
    def merge_schemas(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁPvsSchemaTransformerǁmerge_schemas__mutmut_orig"), object.__getattribute__(self, "xǁPvsSchemaTransformerǁmerge_schemas__mutmut_mutants"), args, kwargs, self)
        return result 
    
    merge_schemas.__signature__ = _mutmut_signature(xǁPvsSchemaTransformerǁmerge_schemas__mutmut_orig)
    xǁPvsSchemaTransformerǁmerge_schemas__mutmut_orig.__name__ = 'xǁPvsSchemaTransformerǁmerge_schemas'
