# pyvider/exceptions/function.py

from typing import Any

from provide.foundation.errors import (
    ConfigurationError as FoundationConfigurationError,
    RuntimeError as FoundationRuntimeError,
    ValidationError as FoundationValidationError,
)
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


class FunctionError(FoundationRuntimeError):
    """Base exception for function-related errors during execution."""

    def xǁFunctionErrorǁ__init____mutmut_orig(
        self, message: str, function_name: str | None = None, argument_index: int | None = None, **kwargs: Any
    ) -> None:
        self.function_name = function_name
        self.argument_index = argument_index

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionErrorǁ__init____mutmut_1(
        self, message: str, function_name: str | None = None, argument_index: int | None = None, **kwargs: Any
    ) -> None:
        self.function_name = None
        self.argument_index = argument_index

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionErrorǁ__init____mutmut_2(
        self, message: str, function_name: str | None = None, argument_index: int | None = None, **kwargs: Any
    ) -> None:
        self.function_name = function_name
        self.argument_index = None

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionErrorǁ__init____mutmut_3(
        self, message: str, function_name: str | None = None, argument_index: int | None = None, **kwargs: Any
    ) -> None:
        self.function_name = function_name
        self.argument_index = argument_index

        prefix = None
        full_message = f"{prefix} error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionErrorǁ__init____mutmut_4(
        self, message: str, function_name: str | None = None, argument_index: int | None = None, **kwargs: Any
    ) -> None:
        self.function_name = function_name
        self.argument_index = argument_index

        prefix = f"Function '{function_name}'" if function_name else "XXFunctionXX"
        full_message = f"{prefix} error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionErrorǁ__init____mutmut_5(
        self, message: str, function_name: str | None = None, argument_index: int | None = None, **kwargs: Any
    ) -> None:
        self.function_name = function_name
        self.argument_index = argument_index

        prefix = f"Function '{function_name}'" if function_name else "function"
        full_message = f"{prefix} error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionErrorǁ__init____mutmut_6(
        self, message: str, function_name: str | None = None, argument_index: int | None = None, **kwargs: Any
    ) -> None:
        self.function_name = function_name
        self.argument_index = argument_index

        prefix = f"Function '{function_name}'" if function_name else "FUNCTION"
        full_message = f"{prefix} error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionErrorǁ__init____mutmut_7(
        self, message: str, function_name: str | None = None, argument_index: int | None = None, **kwargs: Any
    ) -> None:
        self.function_name = function_name
        self.argument_index = argument_index

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = None

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionErrorǁ__init____mutmut_8(
        self, message: str, function_name: str | None = None, argument_index: int | None = None, **kwargs: Any
    ) -> None:
        self.function_name = function_name
        self.argument_index = argument_index

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = None
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionErrorǁ__init____mutmut_9(
        self, message: str, function_name: str | None = None, argument_index: int | None = None, **kwargs: Any
    ) -> None:
        self.function_name = function_name
        self.argument_index = argument_index

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} error: {message}"

        if function_name:
            kwargs.setdefault(None, {})["function.name"] = function_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionErrorǁ__init____mutmut_10(
        self, message: str, function_name: str | None = None, argument_index: int | None = None, **kwargs: Any
    ) -> None:
        self.function_name = function_name
        self.argument_index = argument_index

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} error: {message}"

        if function_name:
            kwargs.setdefault("context", None)["function.name"] = function_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionErrorǁ__init____mutmut_11(
        self, message: str, function_name: str | None = None, argument_index: int | None = None, **kwargs: Any
    ) -> None:
        self.function_name = function_name
        self.argument_index = argument_index

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} error: {message}"

        if function_name:
            kwargs.setdefault({})["function.name"] = function_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionErrorǁ__init____mutmut_12(
        self, message: str, function_name: str | None = None, argument_index: int | None = None, **kwargs: Any
    ) -> None:
        self.function_name = function_name
        self.argument_index = argument_index

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} error: {message}"

        if function_name:
            kwargs.setdefault("context", )["function.name"] = function_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionErrorǁ__init____mutmut_13(
        self, message: str, function_name: str | None = None, argument_index: int | None = None, **kwargs: Any
    ) -> None:
        self.function_name = function_name
        self.argument_index = argument_index

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} error: {message}"

        if function_name:
            kwargs.setdefault("XXcontextXX", {})["function.name"] = function_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionErrorǁ__init____mutmut_14(
        self, message: str, function_name: str | None = None, argument_index: int | None = None, **kwargs: Any
    ) -> None:
        self.function_name = function_name
        self.argument_index = argument_index

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} error: {message}"

        if function_name:
            kwargs.setdefault("CONTEXT", {})["function.name"] = function_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionErrorǁ__init____mutmut_15(
        self, message: str, function_name: str | None = None, argument_index: int | None = None, **kwargs: Any
    ) -> None:
        self.function_name = function_name
        self.argument_index = argument_index

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["XXfunction.nameXX"] = function_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionErrorǁ__init____mutmut_16(
        self, message: str, function_name: str | None = None, argument_index: int | None = None, **kwargs: Any
    ) -> None:
        self.function_name = function_name
        self.argument_index = argument_index

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["FUNCTION.NAME"] = function_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionErrorǁ__init____mutmut_17(
        self, message: str, function_name: str | None = None, argument_index: int | None = None, **kwargs: Any
    ) -> None:
        self.function_name = function_name
        self.argument_index = argument_index

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_index is None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionErrorǁ__init____mutmut_18(
        self, message: str, function_name: str | None = None, argument_index: int | None = None, **kwargs: Any
    ) -> None:
        self.function_name = function_name
        self.argument_index = argument_index

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = None

        super().__init__(full_message, **kwargs)

    def xǁFunctionErrorǁ__init____mutmut_19(
        self, message: str, function_name: str | None = None, argument_index: int | None = None, **kwargs: Any
    ) -> None:
        self.function_name = function_name
        self.argument_index = argument_index

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_index is not None:
            kwargs.setdefault(None, {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionErrorǁ__init____mutmut_20(
        self, message: str, function_name: str | None = None, argument_index: int | None = None, **kwargs: Any
    ) -> None:
        self.function_name = function_name
        self.argument_index = argument_index

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_index is not None:
            kwargs.setdefault("context", None)["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionErrorǁ__init____mutmut_21(
        self, message: str, function_name: str | None = None, argument_index: int | None = None, **kwargs: Any
    ) -> None:
        self.function_name = function_name
        self.argument_index = argument_index

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_index is not None:
            kwargs.setdefault({})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionErrorǁ__init____mutmut_22(
        self, message: str, function_name: str | None = None, argument_index: int | None = None, **kwargs: Any
    ) -> None:
        self.function_name = function_name
        self.argument_index = argument_index

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_index is not None:
            kwargs.setdefault("context", )["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionErrorǁ__init____mutmut_23(
        self, message: str, function_name: str | None = None, argument_index: int | None = None, **kwargs: Any
    ) -> None:
        self.function_name = function_name
        self.argument_index = argument_index

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_index is not None:
            kwargs.setdefault("XXcontextXX", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionErrorǁ__init____mutmut_24(
        self, message: str, function_name: str | None = None, argument_index: int | None = None, **kwargs: Any
    ) -> None:
        self.function_name = function_name
        self.argument_index = argument_index

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_index is not None:
            kwargs.setdefault("CONTEXT", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionErrorǁ__init____mutmut_25(
        self, message: str, function_name: str | None = None, argument_index: int | None = None, **kwargs: Any
    ) -> None:
        self.function_name = function_name
        self.argument_index = argument_index

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["XXfunction.argument_indexXX"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionErrorǁ__init____mutmut_26(
        self, message: str, function_name: str | None = None, argument_index: int | None = None, **kwargs: Any
    ) -> None:
        self.function_name = function_name
        self.argument_index = argument_index

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["FUNCTION.ARGUMENT_INDEX"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionErrorǁ__init____mutmut_27(
        self, message: str, function_name: str | None = None, argument_index: int | None = None, **kwargs: Any
    ) -> None:
        self.function_name = function_name
        self.argument_index = argument_index

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(None, **kwargs)

    def xǁFunctionErrorǁ__init____mutmut_28(
        self, message: str, function_name: str | None = None, argument_index: int | None = None, **kwargs: Any
    ) -> None:
        self.function_name = function_name
        self.argument_index = argument_index

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(**kwargs)

    def xǁFunctionErrorǁ__init____mutmut_29(
        self, message: str, function_name: str | None = None, argument_index: int | None = None, **kwargs: Any
    ) -> None:
        self.function_name = function_name
        self.argument_index = argument_index

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, )
    
    xǁFunctionErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁFunctionErrorǁ__init____mutmut_1': xǁFunctionErrorǁ__init____mutmut_1, 
        'xǁFunctionErrorǁ__init____mutmut_2': xǁFunctionErrorǁ__init____mutmut_2, 
        'xǁFunctionErrorǁ__init____mutmut_3': xǁFunctionErrorǁ__init____mutmut_3, 
        'xǁFunctionErrorǁ__init____mutmut_4': xǁFunctionErrorǁ__init____mutmut_4, 
        'xǁFunctionErrorǁ__init____mutmut_5': xǁFunctionErrorǁ__init____mutmut_5, 
        'xǁFunctionErrorǁ__init____mutmut_6': xǁFunctionErrorǁ__init____mutmut_6, 
        'xǁFunctionErrorǁ__init____mutmut_7': xǁFunctionErrorǁ__init____mutmut_7, 
        'xǁFunctionErrorǁ__init____mutmut_8': xǁFunctionErrorǁ__init____mutmut_8, 
        'xǁFunctionErrorǁ__init____mutmut_9': xǁFunctionErrorǁ__init____mutmut_9, 
        'xǁFunctionErrorǁ__init____mutmut_10': xǁFunctionErrorǁ__init____mutmut_10, 
        'xǁFunctionErrorǁ__init____mutmut_11': xǁFunctionErrorǁ__init____mutmut_11, 
        'xǁFunctionErrorǁ__init____mutmut_12': xǁFunctionErrorǁ__init____mutmut_12, 
        'xǁFunctionErrorǁ__init____mutmut_13': xǁFunctionErrorǁ__init____mutmut_13, 
        'xǁFunctionErrorǁ__init____mutmut_14': xǁFunctionErrorǁ__init____mutmut_14, 
        'xǁFunctionErrorǁ__init____mutmut_15': xǁFunctionErrorǁ__init____mutmut_15, 
        'xǁFunctionErrorǁ__init____mutmut_16': xǁFunctionErrorǁ__init____mutmut_16, 
        'xǁFunctionErrorǁ__init____mutmut_17': xǁFunctionErrorǁ__init____mutmut_17, 
        'xǁFunctionErrorǁ__init____mutmut_18': xǁFunctionErrorǁ__init____mutmut_18, 
        'xǁFunctionErrorǁ__init____mutmut_19': xǁFunctionErrorǁ__init____mutmut_19, 
        'xǁFunctionErrorǁ__init____mutmut_20': xǁFunctionErrorǁ__init____mutmut_20, 
        'xǁFunctionErrorǁ__init____mutmut_21': xǁFunctionErrorǁ__init____mutmut_21, 
        'xǁFunctionErrorǁ__init____mutmut_22': xǁFunctionErrorǁ__init____mutmut_22, 
        'xǁFunctionErrorǁ__init____mutmut_23': xǁFunctionErrorǁ__init____mutmut_23, 
        'xǁFunctionErrorǁ__init____mutmut_24': xǁFunctionErrorǁ__init____mutmut_24, 
        'xǁFunctionErrorǁ__init____mutmut_25': xǁFunctionErrorǁ__init____mutmut_25, 
        'xǁFunctionErrorǁ__init____mutmut_26': xǁFunctionErrorǁ__init____mutmut_26, 
        'xǁFunctionErrorǁ__init____mutmut_27': xǁFunctionErrorǁ__init____mutmut_27, 
        'xǁFunctionErrorǁ__init____mutmut_28': xǁFunctionErrorǁ__init____mutmut_28, 
        'xǁFunctionErrorǁ__init____mutmut_29': xǁFunctionErrorǁ__init____mutmut_29
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁFunctionErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁFunctionErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁFunctionErrorǁ__init____mutmut_orig)
    xǁFunctionErrorǁ__init____mutmut_orig.__name__ = 'xǁFunctionErrorǁ__init__'

    def xǁFunctionErrorǁ_default_code__mutmut_orig(self) -> str:
        return "FUNCTION_ERROR"

    def xǁFunctionErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXFUNCTION_ERRORXX"

    def xǁFunctionErrorǁ_default_code__mutmut_2(self) -> str:
        return "function_error"
    
    xǁFunctionErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁFunctionErrorǁ_default_code__mutmut_1': xǁFunctionErrorǁ_default_code__mutmut_1, 
        'xǁFunctionErrorǁ_default_code__mutmut_2': xǁFunctionErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁFunctionErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁFunctionErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁFunctionErrorǁ_default_code__mutmut_orig)
    xǁFunctionErrorǁ_default_code__mutmut_orig.__name__ = 'xǁFunctionErrorǁ_default_code'

    def xǁFunctionErrorǁto_proto__mutmut_orig(self) -> dict[str, Any]:
        """Convert to protobuf FunctionError message."""
        # Placeholder for actual protobuf conversion
        # from pyvider.protocols.tfprotov6.protobuf import FunctionError as ProtoFunctionError
        # proto_error = ProtoFunctionError(text=str(self))
        # if self.argument_index is not None:
        #     proto_error.function_argument = self.argument_index # Ensure field name matches proto
        # return proto_error
        return {"text": str(self), "argument_index": self.argument_index}

    def xǁFunctionErrorǁto_proto__mutmut_1(self) -> dict[str, Any]:
        """Convert to protobuf FunctionError message."""
        # Placeholder for actual protobuf conversion
        # from pyvider.protocols.tfprotov6.protobuf import FunctionError as ProtoFunctionError
        # proto_error = ProtoFunctionError(text=str(self))
        # if self.argument_index is not None:
        #     proto_error.function_argument = self.argument_index # Ensure field name matches proto
        # return proto_error
        return {"XXtextXX": str(self), "argument_index": self.argument_index}

    def xǁFunctionErrorǁto_proto__mutmut_2(self) -> dict[str, Any]:
        """Convert to protobuf FunctionError message."""
        # Placeholder for actual protobuf conversion
        # from pyvider.protocols.tfprotov6.protobuf import FunctionError as ProtoFunctionError
        # proto_error = ProtoFunctionError(text=str(self))
        # if self.argument_index is not None:
        #     proto_error.function_argument = self.argument_index # Ensure field name matches proto
        # return proto_error
        return {"TEXT": str(self), "argument_index": self.argument_index}

    def xǁFunctionErrorǁto_proto__mutmut_3(self) -> dict[str, Any]:
        """Convert to protobuf FunctionError message."""
        # Placeholder for actual protobuf conversion
        # from pyvider.protocols.tfprotov6.protobuf import FunctionError as ProtoFunctionError
        # proto_error = ProtoFunctionError(text=str(self))
        # if self.argument_index is not None:
        #     proto_error.function_argument = self.argument_index # Ensure field name matches proto
        # return proto_error
        return {"text": str(None), "argument_index": self.argument_index}

    def xǁFunctionErrorǁto_proto__mutmut_4(self) -> dict[str, Any]:
        """Convert to protobuf FunctionError message."""
        # Placeholder for actual protobuf conversion
        # from pyvider.protocols.tfprotov6.protobuf import FunctionError as ProtoFunctionError
        # proto_error = ProtoFunctionError(text=str(self))
        # if self.argument_index is not None:
        #     proto_error.function_argument = self.argument_index # Ensure field name matches proto
        # return proto_error
        return {"text": str(self), "XXargument_indexXX": self.argument_index}

    def xǁFunctionErrorǁto_proto__mutmut_5(self) -> dict[str, Any]:
        """Convert to protobuf FunctionError message."""
        # Placeholder for actual protobuf conversion
        # from pyvider.protocols.tfprotov6.protobuf import FunctionError as ProtoFunctionError
        # proto_error = ProtoFunctionError(text=str(self))
        # if self.argument_index is not None:
        #     proto_error.function_argument = self.argument_index # Ensure field name matches proto
        # return proto_error
        return {"text": str(self), "ARGUMENT_INDEX": self.argument_index}
    
    xǁFunctionErrorǁto_proto__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁFunctionErrorǁto_proto__mutmut_1': xǁFunctionErrorǁto_proto__mutmut_1, 
        'xǁFunctionErrorǁto_proto__mutmut_2': xǁFunctionErrorǁto_proto__mutmut_2, 
        'xǁFunctionErrorǁto_proto__mutmut_3': xǁFunctionErrorǁto_proto__mutmut_3, 
        'xǁFunctionErrorǁto_proto__mutmut_4': xǁFunctionErrorǁto_proto__mutmut_4, 
        'xǁFunctionErrorǁto_proto__mutmut_5': xǁFunctionErrorǁto_proto__mutmut_5
    }
    
    def to_proto(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁFunctionErrorǁto_proto__mutmut_orig"), object.__getattribute__(self, "xǁFunctionErrorǁto_proto__mutmut_mutants"), args, kwargs, self)
        return result 
    
    to_proto.__signature__ = _mutmut_signature(xǁFunctionErrorǁto_proto__mutmut_orig)
    xǁFunctionErrorǁto_proto__mutmut_orig.__name__ = 'xǁFunctionErrorǁto_proto'


class FunctionRegistrationError(FoundationConfigurationError):
    """Exception raised when a function cannot be registered properly."""

    def xǁFunctionRegistrationErrorǁ__init____mutmut_orig(self, message: str, function_name: str | None = None, **kwargs: Any) -> None:
        self.function_name = function_name

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} registration error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name

        super().__init__(full_message, **kwargs)

    def xǁFunctionRegistrationErrorǁ__init____mutmut_1(self, message: str, function_name: str | None = None, **kwargs: Any) -> None:
        self.function_name = None

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} registration error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name

        super().__init__(full_message, **kwargs)

    def xǁFunctionRegistrationErrorǁ__init____mutmut_2(self, message: str, function_name: str | None = None, **kwargs: Any) -> None:
        self.function_name = function_name

        prefix = None
        full_message = f"{prefix} registration error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name

        super().__init__(full_message, **kwargs)

    def xǁFunctionRegistrationErrorǁ__init____mutmut_3(self, message: str, function_name: str | None = None, **kwargs: Any) -> None:
        self.function_name = function_name

        prefix = f"Function '{function_name}'" if function_name else "XXFunctionXX"
        full_message = f"{prefix} registration error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name

        super().__init__(full_message, **kwargs)

    def xǁFunctionRegistrationErrorǁ__init____mutmut_4(self, message: str, function_name: str | None = None, **kwargs: Any) -> None:
        self.function_name = function_name

        prefix = f"Function '{function_name}'" if function_name else "function"
        full_message = f"{prefix} registration error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name

        super().__init__(full_message, **kwargs)

    def xǁFunctionRegistrationErrorǁ__init____mutmut_5(self, message: str, function_name: str | None = None, **kwargs: Any) -> None:
        self.function_name = function_name

        prefix = f"Function '{function_name}'" if function_name else "FUNCTION"
        full_message = f"{prefix} registration error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name

        super().__init__(full_message, **kwargs)

    def xǁFunctionRegistrationErrorǁ__init____mutmut_6(self, message: str, function_name: str | None = None, **kwargs: Any) -> None:
        self.function_name = function_name

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = None

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name

        super().__init__(full_message, **kwargs)

    def xǁFunctionRegistrationErrorǁ__init____mutmut_7(self, message: str, function_name: str | None = None, **kwargs: Any) -> None:
        self.function_name = function_name

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} registration error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = None

        super().__init__(full_message, **kwargs)

    def xǁFunctionRegistrationErrorǁ__init____mutmut_8(self, message: str, function_name: str | None = None, **kwargs: Any) -> None:
        self.function_name = function_name

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} registration error: {message}"

        if function_name:
            kwargs.setdefault(None, {})["function.name"] = function_name

        super().__init__(full_message, **kwargs)

    def xǁFunctionRegistrationErrorǁ__init____mutmut_9(self, message: str, function_name: str | None = None, **kwargs: Any) -> None:
        self.function_name = function_name

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} registration error: {message}"

        if function_name:
            kwargs.setdefault("context", None)["function.name"] = function_name

        super().__init__(full_message, **kwargs)

    def xǁFunctionRegistrationErrorǁ__init____mutmut_10(self, message: str, function_name: str | None = None, **kwargs: Any) -> None:
        self.function_name = function_name

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} registration error: {message}"

        if function_name:
            kwargs.setdefault({})["function.name"] = function_name

        super().__init__(full_message, **kwargs)

    def xǁFunctionRegistrationErrorǁ__init____mutmut_11(self, message: str, function_name: str | None = None, **kwargs: Any) -> None:
        self.function_name = function_name

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} registration error: {message}"

        if function_name:
            kwargs.setdefault("context", )["function.name"] = function_name

        super().__init__(full_message, **kwargs)

    def xǁFunctionRegistrationErrorǁ__init____mutmut_12(self, message: str, function_name: str | None = None, **kwargs: Any) -> None:
        self.function_name = function_name

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} registration error: {message}"

        if function_name:
            kwargs.setdefault("XXcontextXX", {})["function.name"] = function_name

        super().__init__(full_message, **kwargs)

    def xǁFunctionRegistrationErrorǁ__init____mutmut_13(self, message: str, function_name: str | None = None, **kwargs: Any) -> None:
        self.function_name = function_name

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} registration error: {message}"

        if function_name:
            kwargs.setdefault("CONTEXT", {})["function.name"] = function_name

        super().__init__(full_message, **kwargs)

    def xǁFunctionRegistrationErrorǁ__init____mutmut_14(self, message: str, function_name: str | None = None, **kwargs: Any) -> None:
        self.function_name = function_name

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} registration error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["XXfunction.nameXX"] = function_name

        super().__init__(full_message, **kwargs)

    def xǁFunctionRegistrationErrorǁ__init____mutmut_15(self, message: str, function_name: str | None = None, **kwargs: Any) -> None:
        self.function_name = function_name

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} registration error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["FUNCTION.NAME"] = function_name

        super().__init__(full_message, **kwargs)

    def xǁFunctionRegistrationErrorǁ__init____mutmut_16(self, message: str, function_name: str | None = None, **kwargs: Any) -> None:
        self.function_name = function_name

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} registration error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name

        super().__init__(None, **kwargs)

    def xǁFunctionRegistrationErrorǁ__init____mutmut_17(self, message: str, function_name: str | None = None, **kwargs: Any) -> None:
        self.function_name = function_name

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} registration error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name

        super().__init__(**kwargs)

    def xǁFunctionRegistrationErrorǁ__init____mutmut_18(self, message: str, function_name: str | None = None, **kwargs: Any) -> None:
        self.function_name = function_name

        prefix = f"Function '{function_name}'" if function_name else "Function"
        full_message = f"{prefix} registration error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name

        super().__init__(full_message, )
    
    xǁFunctionRegistrationErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁFunctionRegistrationErrorǁ__init____mutmut_1': xǁFunctionRegistrationErrorǁ__init____mutmut_1, 
        'xǁFunctionRegistrationErrorǁ__init____mutmut_2': xǁFunctionRegistrationErrorǁ__init____mutmut_2, 
        'xǁFunctionRegistrationErrorǁ__init____mutmut_3': xǁFunctionRegistrationErrorǁ__init____mutmut_3, 
        'xǁFunctionRegistrationErrorǁ__init____mutmut_4': xǁFunctionRegistrationErrorǁ__init____mutmut_4, 
        'xǁFunctionRegistrationErrorǁ__init____mutmut_5': xǁFunctionRegistrationErrorǁ__init____mutmut_5, 
        'xǁFunctionRegistrationErrorǁ__init____mutmut_6': xǁFunctionRegistrationErrorǁ__init____mutmut_6, 
        'xǁFunctionRegistrationErrorǁ__init____mutmut_7': xǁFunctionRegistrationErrorǁ__init____mutmut_7, 
        'xǁFunctionRegistrationErrorǁ__init____mutmut_8': xǁFunctionRegistrationErrorǁ__init____mutmut_8, 
        'xǁFunctionRegistrationErrorǁ__init____mutmut_9': xǁFunctionRegistrationErrorǁ__init____mutmut_9, 
        'xǁFunctionRegistrationErrorǁ__init____mutmut_10': xǁFunctionRegistrationErrorǁ__init____mutmut_10, 
        'xǁFunctionRegistrationErrorǁ__init____mutmut_11': xǁFunctionRegistrationErrorǁ__init____mutmut_11, 
        'xǁFunctionRegistrationErrorǁ__init____mutmut_12': xǁFunctionRegistrationErrorǁ__init____mutmut_12, 
        'xǁFunctionRegistrationErrorǁ__init____mutmut_13': xǁFunctionRegistrationErrorǁ__init____mutmut_13, 
        'xǁFunctionRegistrationErrorǁ__init____mutmut_14': xǁFunctionRegistrationErrorǁ__init____mutmut_14, 
        'xǁFunctionRegistrationErrorǁ__init____mutmut_15': xǁFunctionRegistrationErrorǁ__init____mutmut_15, 
        'xǁFunctionRegistrationErrorǁ__init____mutmut_16': xǁFunctionRegistrationErrorǁ__init____mutmut_16, 
        'xǁFunctionRegistrationErrorǁ__init____mutmut_17': xǁFunctionRegistrationErrorǁ__init____mutmut_17, 
        'xǁFunctionRegistrationErrorǁ__init____mutmut_18': xǁFunctionRegistrationErrorǁ__init____mutmut_18
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁFunctionRegistrationErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁFunctionRegistrationErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁFunctionRegistrationErrorǁ__init____mutmut_orig)
    xǁFunctionRegistrationErrorǁ__init____mutmut_orig.__name__ = 'xǁFunctionRegistrationErrorǁ__init__'

    def xǁFunctionRegistrationErrorǁ_default_code__mutmut_orig(self) -> str:
        return "FUNCTION_REGISTRATION_ERROR"

    def xǁFunctionRegistrationErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXFUNCTION_REGISTRATION_ERRORXX"

    def xǁFunctionRegistrationErrorǁ_default_code__mutmut_2(self) -> str:
        return "function_registration_error"
    
    xǁFunctionRegistrationErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁFunctionRegistrationErrorǁ_default_code__mutmut_1': xǁFunctionRegistrationErrorǁ_default_code__mutmut_1, 
        'xǁFunctionRegistrationErrorǁ_default_code__mutmut_2': xǁFunctionRegistrationErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁFunctionRegistrationErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁFunctionRegistrationErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁFunctionRegistrationErrorǁ_default_code__mutmut_orig)
    xǁFunctionRegistrationErrorǁ_default_code__mutmut_orig.__name__ = 'xǁFunctionRegistrationErrorǁ_default_code'


class FunctionValidationError(FoundationValidationError):
    """Exception raised when function arguments fail validation."""

    def xǁFunctionValidationErrorǁ__init____mutmut_orig(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_name:
            kwargs.setdefault("context", {})["function.argument_name"] = argument_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_1(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = None
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_name:
            kwargs.setdefault("context", {})["function.argument_name"] = argument_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_2(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = None
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_name:
            kwargs.setdefault("context", {})["function.argument_name"] = argument_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_3(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = None

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_name:
            kwargs.setdefault("context", {})["function.argument_name"] = argument_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_4(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name or function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_name:
            kwargs.setdefault("context", {})["function.argument_name"] = argument_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_5(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = None
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_name:
            kwargs.setdefault("context", {})["function.argument_name"] = argument_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_6(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = None
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_name:
            kwargs.setdefault("context", {})["function.argument_name"] = argument_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_7(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = None
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_name:
            kwargs.setdefault("context", {})["function.argument_name"] = argument_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_8(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = None

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_name:
            kwargs.setdefault("context", {})["function.argument_name"] = argument_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_9(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = None
        if argument_name:
            kwargs.setdefault("context", {})["function.argument_name"] = argument_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_10(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault(None, {})["function.name"] = function_name
        if argument_name:
            kwargs.setdefault("context", {})["function.argument_name"] = argument_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_11(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("context", None)["function.name"] = function_name
        if argument_name:
            kwargs.setdefault("context", {})["function.argument_name"] = argument_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_12(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault({})["function.name"] = function_name
        if argument_name:
            kwargs.setdefault("context", {})["function.argument_name"] = argument_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_13(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("context", )["function.name"] = function_name
        if argument_name:
            kwargs.setdefault("context", {})["function.argument_name"] = argument_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_14(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("XXcontextXX", {})["function.name"] = function_name
        if argument_name:
            kwargs.setdefault("context", {})["function.argument_name"] = argument_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_15(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("CONTEXT", {})["function.name"] = function_name
        if argument_name:
            kwargs.setdefault("context", {})["function.argument_name"] = argument_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_16(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["XXfunction.nameXX"] = function_name
        if argument_name:
            kwargs.setdefault("context", {})["function.argument_name"] = argument_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_17(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["FUNCTION.NAME"] = function_name
        if argument_name:
            kwargs.setdefault("context", {})["function.argument_name"] = argument_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_18(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_name:
            kwargs.setdefault("context", {})["function.argument_name"] = None
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_19(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_name:
            kwargs.setdefault(None, {})["function.argument_name"] = argument_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_20(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_name:
            kwargs.setdefault("context", None)["function.argument_name"] = argument_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_21(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_name:
            kwargs.setdefault({})["function.argument_name"] = argument_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_22(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_name:
            kwargs.setdefault("context", )["function.argument_name"] = argument_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_23(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_name:
            kwargs.setdefault("XXcontextXX", {})["function.argument_name"] = argument_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_24(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_name:
            kwargs.setdefault("CONTEXT", {})["function.argument_name"] = argument_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_25(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_name:
            kwargs.setdefault("context", {})["XXfunction.argument_nameXX"] = argument_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_26(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_name:
            kwargs.setdefault("context", {})["FUNCTION.ARGUMENT_NAME"] = argument_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_27(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_name:
            kwargs.setdefault("context", {})["function.argument_name"] = argument_name
        if argument_index is None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_28(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_name:
            kwargs.setdefault("context", {})["function.argument_name"] = argument_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = None

        super().__init__(full_message, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_29(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_name:
            kwargs.setdefault("context", {})["function.argument_name"] = argument_name
        if argument_index is not None:
            kwargs.setdefault(None, {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_30(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_name:
            kwargs.setdefault("context", {})["function.argument_name"] = argument_name
        if argument_index is not None:
            kwargs.setdefault("context", None)["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_31(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_name:
            kwargs.setdefault("context", {})["function.argument_name"] = argument_name
        if argument_index is not None:
            kwargs.setdefault({})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_32(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_name:
            kwargs.setdefault("context", {})["function.argument_name"] = argument_name
        if argument_index is not None:
            kwargs.setdefault("context", )["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_33(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_name:
            kwargs.setdefault("context", {})["function.argument_name"] = argument_name
        if argument_index is not None:
            kwargs.setdefault("XXcontextXX", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_34(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_name:
            kwargs.setdefault("context", {})["function.argument_name"] = argument_name
        if argument_index is not None:
            kwargs.setdefault("CONTEXT", {})["function.argument_index"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_35(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_name:
            kwargs.setdefault("context", {})["function.argument_name"] = argument_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["XXfunction.argument_indexXX"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_36(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_name:
            kwargs.setdefault("context", {})["function.argument_name"] = argument_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["FUNCTION.ARGUMENT_INDEX"] = argument_index

        super().__init__(full_message, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_37(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_name:
            kwargs.setdefault("context", {})["function.argument_name"] = argument_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(None, **kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_38(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_name:
            kwargs.setdefault("context", {})["function.argument_name"] = argument_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(**kwargs)

    def xǁFunctionValidationErrorǁ__init____mutmut_39(
        self,
        message: str,
        function_name: str | None = None,
        argument_name: str | None = None,
        argument_index: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.function_name = function_name
        self.argument_name = argument_name
        self.argument_index = argument_index

        # Build enhanced message
        if argument_name and function_name:
            full_message = (
                f"Function '{function_name}' validation error for argument '{argument_name}': {message}"
            )
        elif argument_name:
            full_message = f"Argument '{argument_name}' validation error: {message}"
        elif function_name:
            full_message = f"Function '{function_name}' validation error: {message}"
        else:
            full_message = f"Function validation error: {message}"

        if function_name:
            kwargs.setdefault("context", {})["function.name"] = function_name
        if argument_name:
            kwargs.setdefault("context", {})["function.argument_name"] = argument_name
        if argument_index is not None:
            kwargs.setdefault("context", {})["function.argument_index"] = argument_index

        super().__init__(full_message, )
    
    xǁFunctionValidationErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁFunctionValidationErrorǁ__init____mutmut_1': xǁFunctionValidationErrorǁ__init____mutmut_1, 
        'xǁFunctionValidationErrorǁ__init____mutmut_2': xǁFunctionValidationErrorǁ__init____mutmut_2, 
        'xǁFunctionValidationErrorǁ__init____mutmut_3': xǁFunctionValidationErrorǁ__init____mutmut_3, 
        'xǁFunctionValidationErrorǁ__init____mutmut_4': xǁFunctionValidationErrorǁ__init____mutmut_4, 
        'xǁFunctionValidationErrorǁ__init____mutmut_5': xǁFunctionValidationErrorǁ__init____mutmut_5, 
        'xǁFunctionValidationErrorǁ__init____mutmut_6': xǁFunctionValidationErrorǁ__init____mutmut_6, 
        'xǁFunctionValidationErrorǁ__init____mutmut_7': xǁFunctionValidationErrorǁ__init____mutmut_7, 
        'xǁFunctionValidationErrorǁ__init____mutmut_8': xǁFunctionValidationErrorǁ__init____mutmut_8, 
        'xǁFunctionValidationErrorǁ__init____mutmut_9': xǁFunctionValidationErrorǁ__init____mutmut_9, 
        'xǁFunctionValidationErrorǁ__init____mutmut_10': xǁFunctionValidationErrorǁ__init____mutmut_10, 
        'xǁFunctionValidationErrorǁ__init____mutmut_11': xǁFunctionValidationErrorǁ__init____mutmut_11, 
        'xǁFunctionValidationErrorǁ__init____mutmut_12': xǁFunctionValidationErrorǁ__init____mutmut_12, 
        'xǁFunctionValidationErrorǁ__init____mutmut_13': xǁFunctionValidationErrorǁ__init____mutmut_13, 
        'xǁFunctionValidationErrorǁ__init____mutmut_14': xǁFunctionValidationErrorǁ__init____mutmut_14, 
        'xǁFunctionValidationErrorǁ__init____mutmut_15': xǁFunctionValidationErrorǁ__init____mutmut_15, 
        'xǁFunctionValidationErrorǁ__init____mutmut_16': xǁFunctionValidationErrorǁ__init____mutmut_16, 
        'xǁFunctionValidationErrorǁ__init____mutmut_17': xǁFunctionValidationErrorǁ__init____mutmut_17, 
        'xǁFunctionValidationErrorǁ__init____mutmut_18': xǁFunctionValidationErrorǁ__init____mutmut_18, 
        'xǁFunctionValidationErrorǁ__init____mutmut_19': xǁFunctionValidationErrorǁ__init____mutmut_19, 
        'xǁFunctionValidationErrorǁ__init____mutmut_20': xǁFunctionValidationErrorǁ__init____mutmut_20, 
        'xǁFunctionValidationErrorǁ__init____mutmut_21': xǁFunctionValidationErrorǁ__init____mutmut_21, 
        'xǁFunctionValidationErrorǁ__init____mutmut_22': xǁFunctionValidationErrorǁ__init____mutmut_22, 
        'xǁFunctionValidationErrorǁ__init____mutmut_23': xǁFunctionValidationErrorǁ__init____mutmut_23, 
        'xǁFunctionValidationErrorǁ__init____mutmut_24': xǁFunctionValidationErrorǁ__init____mutmut_24, 
        'xǁFunctionValidationErrorǁ__init____mutmut_25': xǁFunctionValidationErrorǁ__init____mutmut_25, 
        'xǁFunctionValidationErrorǁ__init____mutmut_26': xǁFunctionValidationErrorǁ__init____mutmut_26, 
        'xǁFunctionValidationErrorǁ__init____mutmut_27': xǁFunctionValidationErrorǁ__init____mutmut_27, 
        'xǁFunctionValidationErrorǁ__init____mutmut_28': xǁFunctionValidationErrorǁ__init____mutmut_28, 
        'xǁFunctionValidationErrorǁ__init____mutmut_29': xǁFunctionValidationErrorǁ__init____mutmut_29, 
        'xǁFunctionValidationErrorǁ__init____mutmut_30': xǁFunctionValidationErrorǁ__init____mutmut_30, 
        'xǁFunctionValidationErrorǁ__init____mutmut_31': xǁFunctionValidationErrorǁ__init____mutmut_31, 
        'xǁFunctionValidationErrorǁ__init____mutmut_32': xǁFunctionValidationErrorǁ__init____mutmut_32, 
        'xǁFunctionValidationErrorǁ__init____mutmut_33': xǁFunctionValidationErrorǁ__init____mutmut_33, 
        'xǁFunctionValidationErrorǁ__init____mutmut_34': xǁFunctionValidationErrorǁ__init____mutmut_34, 
        'xǁFunctionValidationErrorǁ__init____mutmut_35': xǁFunctionValidationErrorǁ__init____mutmut_35, 
        'xǁFunctionValidationErrorǁ__init____mutmut_36': xǁFunctionValidationErrorǁ__init____mutmut_36, 
        'xǁFunctionValidationErrorǁ__init____mutmut_37': xǁFunctionValidationErrorǁ__init____mutmut_37, 
        'xǁFunctionValidationErrorǁ__init____mutmut_38': xǁFunctionValidationErrorǁ__init____mutmut_38, 
        'xǁFunctionValidationErrorǁ__init____mutmut_39': xǁFunctionValidationErrorǁ__init____mutmut_39
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁFunctionValidationErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁFunctionValidationErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁFunctionValidationErrorǁ__init____mutmut_orig)
    xǁFunctionValidationErrorǁ__init____mutmut_orig.__name__ = 'xǁFunctionValidationErrorǁ__init__'

    def xǁFunctionValidationErrorǁ_default_code__mutmut_orig(self) -> str:
        return "FUNCTION_VALIDATION_ERROR"

    def xǁFunctionValidationErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXFUNCTION_VALIDATION_ERRORXX"

    def xǁFunctionValidationErrorǁ_default_code__mutmut_2(self) -> str:
        return "function_validation_error"
    
    xǁFunctionValidationErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁFunctionValidationErrorǁ_default_code__mutmut_1': xǁFunctionValidationErrorǁ_default_code__mutmut_1, 
        'xǁFunctionValidationErrorǁ_default_code__mutmut_2': xǁFunctionValidationErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁFunctionValidationErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁFunctionValidationErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁFunctionValidationErrorǁ_default_code__mutmut_orig)
    xǁFunctionValidationErrorǁ_default_code__mutmut_orig.__name__ = 'xǁFunctionValidationErrorǁ_default_code'
