# pyvider-schema/src/pyvider/schema/types/object.py
from __future__ import annotations

from typing import TYPE_CHECKING

from attrs import define, field

from pyvider.cty import CtyList, CtyMap, CtyObject, CtySet
from pyvider.schema.types.enums import NestingMode
from pyvider.schema.types.types_base import PvsType

if TYPE_CHECKING:
    from pyvider.schema.types.attribute import PvsAttribute
    from pyvider.schema.types.blocks import PvsNestedBlock
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


@define(frozen=True, kw_only=True)
class PvsObjectType(PvsType):
    """
    A schema object that holds full attribute definitions.
    It no longer inherits from CtyObject, but can produce one.
    """

    attributes: dict[str, PvsAttribute] = field(factory=dict)
    block_types: tuple[PvsNestedBlock, ...] = field(factory=tuple)
    description: str | None = field(default=None)
    deprecated: bool = field(default=False)

    def to_cty_type(self) -> CtyObject:
        """
        Converts this schema definition into its equivalent CtyObject type
        for validation and data manipulation. This now correctly includes
        attributes derived from nested blocks.
        """
        attribute_types = {name: attr.type for name, attr in self.attributes.items()}
        optional_attributes = {
            name for name, attr in self.attributes.items() if attr.optional or attr.computed
        }

        # FIX: Add types for nested blocks so the CtyObject is complete.
        for block in self.block_types:
            block_cty_type = block.block.to_cty_type()
            if block.nesting == NestingMode.LIST:
                attribute_types[block.type_name] = CtyList(element_type=block_cty_type)
            elif block.nesting == NestingMode.SET:
                attribute_types[block.type_name] = CtySet(element_type=block_cty_type)
            elif block.nesting == NestingMode.MAP:
                attribute_types[block.type_name] = CtyMap(element_type=block_cty_type)
            else:  # SINGLE or GROUP
                attribute_types[block.type_name] = block_cty_type

            optional_attributes.add(block.type_name)

        return CtyObject(
            attribute_types=attribute_types,
            optional_attributes=frozenset(optional_attributes),
        )
