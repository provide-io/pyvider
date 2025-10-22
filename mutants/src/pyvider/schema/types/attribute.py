# pyvider/schema/types/attribute.py
from typing import Any

from attrs import define, field

from pyvider.cty import CtyType
from pyvider.schema.types.enums import StringKind  # Import StringKind
from pyvider.schema.types.object import PvsObjectType
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
class PvsAttribute:
    """Represents a fully resolved schema attribute, holding a CtyType."""

    name: str = field(default="")
    type: CtyType = field()
    description: str = field(default="")
    required: bool = field(default=False)
    optional: bool = field(default=False)
    computed: bool = field(default=False)
    sensitive: bool = field(default=False)
    deprecated: bool = field(default=False)
    default: Any = field(default=None)
    description_kind: StringKind = field(default=StringKind.PLAIN)  # Use Enum member
    object_type: "PvsObjectType" = field(default=None)

    def __attrs_post_init__(self) -> None:
        """
        Validates and sets default flags for the attribute.
        Terraform requires that an attribute is explicitly one of:
        - Required
        - Optional
        - Computed
        This hook enforces that logic.
        """
        # Use object.__setattr__ because the instance is frozen.
        is_req = self.required
        is_opt = self.optional
        is_comp = self.computed

        # Rule 1: If nothing is specified, it defaults to Optional.
        if not is_req and not is_opt and not is_comp:
            object.__setattr__(self, "optional", True)
            is_opt = True

        # Rule 2: An attribute can't be both Required and Optional. Required wins.
        if is_req and is_opt:
            object.__setattr__(self, "optional", False)

        # Rule 3: An attribute can't be both Required and Computed.
        if is_req and is_comp:
            raise ValueError(f"Attribute '{self.name}' cannot be both Required and Computed.")

        # Rule 4: Check that at least one flag is set after defaulting.
        # This check is now implicitly handled by the default-to-optional logic above.
        if not self.required and not self.optional and not self.computed:
            raise ValueError(f"Attribute '{self.name}' must be Optional, Required, or Computed.")
