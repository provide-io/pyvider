# pyvider/exceptions/base.py
from typing import Any

from provide.foundation.errors import (
    FoundationError,
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


class PyviderError(FoundationError):
    """Base class for all Pyvider framework errors.

    Inherits from FoundationError to gain:
    - Rich error context with namespace-based metadata
    - Automatic telemetry integration
    - Terraform diagnostic generation support
    """

    def xǁPyviderErrorǁ_default_code__mutmut_orig(self) -> str:
        """Default error code for pyvider errors."""
        return "PYVIDER_ERROR"

    def xǁPyviderErrorǁ_default_code__mutmut_1(self) -> str:
        """Default error code for pyvider errors."""
        return "XXPYVIDER_ERRORXX"

    def xǁPyviderErrorǁ_default_code__mutmut_2(self) -> str:
        """Default error code for pyvider errors."""
        return "pyvider_error"
    
    xǁPyviderErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁPyviderErrorǁ_default_code__mutmut_1': xǁPyviderErrorǁ_default_code__mutmut_1, 
        'xǁPyviderErrorǁ_default_code__mutmut_2': xǁPyviderErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁPyviderErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁPyviderErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁPyviderErrorǁ_default_code__mutmut_orig)
    xǁPyviderErrorǁ_default_code__mutmut_orig.__name__ = 'xǁPyviderErrorǁ_default_code'


class ConversionError(PyviderError):
    """Base class for data conversion errors within the Pyvider framework."""

    def xǁConversionErrorǁ__init____mutmut_orig(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_1(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = None
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_2(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = None

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_3(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = None
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_4(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_5(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(None)
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_6(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(None).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_7(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = None
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_8(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault(None, {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_9(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", None)["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_10(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault({})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_11(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", )["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_12(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("XXcontextXX", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_13(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("CONTEXT", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_14(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["XXconversion.source_typeXX"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_15(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["CONVERSION.SOURCE_TYPE"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_16(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(None).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_17(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = None
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_18(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault(None, {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_19(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", None)["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_20(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault({})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_21(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", )["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_22(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("XXcontextXX", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_23(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("CONTEXT", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_24(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["XXconversion.source_valueXX"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_25(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["CONVERSION.SOURCE_VALUE"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_26(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(None)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_27(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:101]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_28(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_29(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = None
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_30(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(None, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_31(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, None) else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_32(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr("__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_33(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, ) else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_34(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "XX__name__XX") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_35(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__NAME__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_36(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(None)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_37(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(None)
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_38(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = None

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_39(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault(None, {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_40(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", None)["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_41(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault({})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_42(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", )["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_43(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("XXcontextXX", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_44(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("CONTEXT", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_45(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["XXconversion.target_typeXX"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_46(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["CONVERSION.TARGET_TYPE"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_47(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = None

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_48(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(None)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_49(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({'XX, XX'.join(context_parts)})"

        super().__init__(message, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_50(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(None, **kwargs)

    def xǁConversionErrorǁ__init____mutmut_51(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(**kwargs)

    def xǁConversionErrorǁ__init____mutmut_52(
        self,
        message: str,
        *,
        source_value: Any = None,
        target_type: Any = None,
        **kwargs: Any,
    ) -> None:
        self.source_value = source_value
        self.target_type = target_type

        # Keep the old behavior of appending type info to message for compatibility
        context_parts: list[str] = []
        if source_value is not None:
            context_parts.append(f"source_type={type(source_value).__name__}")
            # Also add to foundation context
            kwargs.setdefault("context", {})["conversion.source_type"] = type(source_value).__name__
            kwargs.setdefault("context", {})["conversion.source_value"] = str(source_value)[:100]
        if target_type is not None:
            target_name = target_type.__name__ if hasattr(target_type, "__name__") else str(target_type)
            context_parts.append(f"target_type={target_name}")
            kwargs.setdefault("context", {})["conversion.target_type"] = target_name

        if context_parts:
            message = f"{message} ({', '.join(context_parts)})"

        super().__init__(message, )
    
    xǁConversionErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConversionErrorǁ__init____mutmut_1': xǁConversionErrorǁ__init____mutmut_1, 
        'xǁConversionErrorǁ__init____mutmut_2': xǁConversionErrorǁ__init____mutmut_2, 
        'xǁConversionErrorǁ__init____mutmut_3': xǁConversionErrorǁ__init____mutmut_3, 
        'xǁConversionErrorǁ__init____mutmut_4': xǁConversionErrorǁ__init____mutmut_4, 
        'xǁConversionErrorǁ__init____mutmut_5': xǁConversionErrorǁ__init____mutmut_5, 
        'xǁConversionErrorǁ__init____mutmut_6': xǁConversionErrorǁ__init____mutmut_6, 
        'xǁConversionErrorǁ__init____mutmut_7': xǁConversionErrorǁ__init____mutmut_7, 
        'xǁConversionErrorǁ__init____mutmut_8': xǁConversionErrorǁ__init____mutmut_8, 
        'xǁConversionErrorǁ__init____mutmut_9': xǁConversionErrorǁ__init____mutmut_9, 
        'xǁConversionErrorǁ__init____mutmut_10': xǁConversionErrorǁ__init____mutmut_10, 
        'xǁConversionErrorǁ__init____mutmut_11': xǁConversionErrorǁ__init____mutmut_11, 
        'xǁConversionErrorǁ__init____mutmut_12': xǁConversionErrorǁ__init____mutmut_12, 
        'xǁConversionErrorǁ__init____mutmut_13': xǁConversionErrorǁ__init____mutmut_13, 
        'xǁConversionErrorǁ__init____mutmut_14': xǁConversionErrorǁ__init____mutmut_14, 
        'xǁConversionErrorǁ__init____mutmut_15': xǁConversionErrorǁ__init____mutmut_15, 
        'xǁConversionErrorǁ__init____mutmut_16': xǁConversionErrorǁ__init____mutmut_16, 
        'xǁConversionErrorǁ__init____mutmut_17': xǁConversionErrorǁ__init____mutmut_17, 
        'xǁConversionErrorǁ__init____mutmut_18': xǁConversionErrorǁ__init____mutmut_18, 
        'xǁConversionErrorǁ__init____mutmut_19': xǁConversionErrorǁ__init____mutmut_19, 
        'xǁConversionErrorǁ__init____mutmut_20': xǁConversionErrorǁ__init____mutmut_20, 
        'xǁConversionErrorǁ__init____mutmut_21': xǁConversionErrorǁ__init____mutmut_21, 
        'xǁConversionErrorǁ__init____mutmut_22': xǁConversionErrorǁ__init____mutmut_22, 
        'xǁConversionErrorǁ__init____mutmut_23': xǁConversionErrorǁ__init____mutmut_23, 
        'xǁConversionErrorǁ__init____mutmut_24': xǁConversionErrorǁ__init____mutmut_24, 
        'xǁConversionErrorǁ__init____mutmut_25': xǁConversionErrorǁ__init____mutmut_25, 
        'xǁConversionErrorǁ__init____mutmut_26': xǁConversionErrorǁ__init____mutmut_26, 
        'xǁConversionErrorǁ__init____mutmut_27': xǁConversionErrorǁ__init____mutmut_27, 
        'xǁConversionErrorǁ__init____mutmut_28': xǁConversionErrorǁ__init____mutmut_28, 
        'xǁConversionErrorǁ__init____mutmut_29': xǁConversionErrorǁ__init____mutmut_29, 
        'xǁConversionErrorǁ__init____mutmut_30': xǁConversionErrorǁ__init____mutmut_30, 
        'xǁConversionErrorǁ__init____mutmut_31': xǁConversionErrorǁ__init____mutmut_31, 
        'xǁConversionErrorǁ__init____mutmut_32': xǁConversionErrorǁ__init____mutmut_32, 
        'xǁConversionErrorǁ__init____mutmut_33': xǁConversionErrorǁ__init____mutmut_33, 
        'xǁConversionErrorǁ__init____mutmut_34': xǁConversionErrorǁ__init____mutmut_34, 
        'xǁConversionErrorǁ__init____mutmut_35': xǁConversionErrorǁ__init____mutmut_35, 
        'xǁConversionErrorǁ__init____mutmut_36': xǁConversionErrorǁ__init____mutmut_36, 
        'xǁConversionErrorǁ__init____mutmut_37': xǁConversionErrorǁ__init____mutmut_37, 
        'xǁConversionErrorǁ__init____mutmut_38': xǁConversionErrorǁ__init____mutmut_38, 
        'xǁConversionErrorǁ__init____mutmut_39': xǁConversionErrorǁ__init____mutmut_39, 
        'xǁConversionErrorǁ__init____mutmut_40': xǁConversionErrorǁ__init____mutmut_40, 
        'xǁConversionErrorǁ__init____mutmut_41': xǁConversionErrorǁ__init____mutmut_41, 
        'xǁConversionErrorǁ__init____mutmut_42': xǁConversionErrorǁ__init____mutmut_42, 
        'xǁConversionErrorǁ__init____mutmut_43': xǁConversionErrorǁ__init____mutmut_43, 
        'xǁConversionErrorǁ__init____mutmut_44': xǁConversionErrorǁ__init____mutmut_44, 
        'xǁConversionErrorǁ__init____mutmut_45': xǁConversionErrorǁ__init____mutmut_45, 
        'xǁConversionErrorǁ__init____mutmut_46': xǁConversionErrorǁ__init____mutmut_46, 
        'xǁConversionErrorǁ__init____mutmut_47': xǁConversionErrorǁ__init____mutmut_47, 
        'xǁConversionErrorǁ__init____mutmut_48': xǁConversionErrorǁ__init____mutmut_48, 
        'xǁConversionErrorǁ__init____mutmut_49': xǁConversionErrorǁ__init____mutmut_49, 
        'xǁConversionErrorǁ__init____mutmut_50': xǁConversionErrorǁ__init____mutmut_50, 
        'xǁConversionErrorǁ__init____mutmut_51': xǁConversionErrorǁ__init____mutmut_51, 
        'xǁConversionErrorǁ__init____mutmut_52': xǁConversionErrorǁ__init____mutmut_52
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConversionErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁConversionErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁConversionErrorǁ__init____mutmut_orig)
    xǁConversionErrorǁ__init____mutmut_orig.__name__ = 'xǁConversionErrorǁ__init__'

    def xǁConversionErrorǁ_default_code__mutmut_orig(self) -> str:
        return "CONVERSION_ERROR"

    def xǁConversionErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXCONVERSION_ERRORXX"

    def xǁConversionErrorǁ_default_code__mutmut_2(self) -> str:
        return "conversion_error"
    
    xǁConversionErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConversionErrorǁ_default_code__mutmut_1': xǁConversionErrorǁ_default_code__mutmut_1, 
        'xǁConversionErrorǁ_default_code__mutmut_2': xǁConversionErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConversionErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁConversionErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁConversionErrorǁ_default_code__mutmut_orig)
    xǁConversionErrorǁ_default_code__mutmut_orig.__name__ = 'xǁConversionErrorǁ_default_code'


class WireFormatError(ConversionError):
    """For errors specific to wire format processing."""

    def xǁWireFormatErrorǁ__init____mutmut_orig(
        self,
        message: str,
        *,
        format_type: Any = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        self.format_type = format_type
        self.operation = operation

        # Add wire format context
        if format_type is not None:
            kwargs.setdefault("context", {})["wire.format_type"] = str(format_type)
        if operation is not None:
            kwargs.setdefault("context", {})["wire.operation"] = operation

        super().__init__(message, **kwargs)

    def xǁWireFormatErrorǁ__init____mutmut_1(
        self,
        message: str,
        *,
        format_type: Any = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        self.format_type = None
        self.operation = operation

        # Add wire format context
        if format_type is not None:
            kwargs.setdefault("context", {})["wire.format_type"] = str(format_type)
        if operation is not None:
            kwargs.setdefault("context", {})["wire.operation"] = operation

        super().__init__(message, **kwargs)

    def xǁWireFormatErrorǁ__init____mutmut_2(
        self,
        message: str,
        *,
        format_type: Any = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        self.format_type = format_type
        self.operation = None

        # Add wire format context
        if format_type is not None:
            kwargs.setdefault("context", {})["wire.format_type"] = str(format_type)
        if operation is not None:
            kwargs.setdefault("context", {})["wire.operation"] = operation

        super().__init__(message, **kwargs)

    def xǁWireFormatErrorǁ__init____mutmut_3(
        self,
        message: str,
        *,
        format_type: Any = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        self.format_type = format_type
        self.operation = operation

        # Add wire format context
        if format_type is None:
            kwargs.setdefault("context", {})["wire.format_type"] = str(format_type)
        if operation is not None:
            kwargs.setdefault("context", {})["wire.operation"] = operation

        super().__init__(message, **kwargs)

    def xǁWireFormatErrorǁ__init____mutmut_4(
        self,
        message: str,
        *,
        format_type: Any = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        self.format_type = format_type
        self.operation = operation

        # Add wire format context
        if format_type is not None:
            kwargs.setdefault("context", {})["wire.format_type"] = None
        if operation is not None:
            kwargs.setdefault("context", {})["wire.operation"] = operation

        super().__init__(message, **kwargs)

    def xǁWireFormatErrorǁ__init____mutmut_5(
        self,
        message: str,
        *,
        format_type: Any = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        self.format_type = format_type
        self.operation = operation

        # Add wire format context
        if format_type is not None:
            kwargs.setdefault(None, {})["wire.format_type"] = str(format_type)
        if operation is not None:
            kwargs.setdefault("context", {})["wire.operation"] = operation

        super().__init__(message, **kwargs)

    def xǁWireFormatErrorǁ__init____mutmut_6(
        self,
        message: str,
        *,
        format_type: Any = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        self.format_type = format_type
        self.operation = operation

        # Add wire format context
        if format_type is not None:
            kwargs.setdefault("context", None)["wire.format_type"] = str(format_type)
        if operation is not None:
            kwargs.setdefault("context", {})["wire.operation"] = operation

        super().__init__(message, **kwargs)

    def xǁWireFormatErrorǁ__init____mutmut_7(
        self,
        message: str,
        *,
        format_type: Any = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        self.format_type = format_type
        self.operation = operation

        # Add wire format context
        if format_type is not None:
            kwargs.setdefault({})["wire.format_type"] = str(format_type)
        if operation is not None:
            kwargs.setdefault("context", {})["wire.operation"] = operation

        super().__init__(message, **kwargs)

    def xǁWireFormatErrorǁ__init____mutmut_8(
        self,
        message: str,
        *,
        format_type: Any = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        self.format_type = format_type
        self.operation = operation

        # Add wire format context
        if format_type is not None:
            kwargs.setdefault("context", )["wire.format_type"] = str(format_type)
        if operation is not None:
            kwargs.setdefault("context", {})["wire.operation"] = operation

        super().__init__(message, **kwargs)

    def xǁWireFormatErrorǁ__init____mutmut_9(
        self,
        message: str,
        *,
        format_type: Any = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        self.format_type = format_type
        self.operation = operation

        # Add wire format context
        if format_type is not None:
            kwargs.setdefault("XXcontextXX", {})["wire.format_type"] = str(format_type)
        if operation is not None:
            kwargs.setdefault("context", {})["wire.operation"] = operation

        super().__init__(message, **kwargs)

    def xǁWireFormatErrorǁ__init____mutmut_10(
        self,
        message: str,
        *,
        format_type: Any = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        self.format_type = format_type
        self.operation = operation

        # Add wire format context
        if format_type is not None:
            kwargs.setdefault("CONTEXT", {})["wire.format_type"] = str(format_type)
        if operation is not None:
            kwargs.setdefault("context", {})["wire.operation"] = operation

        super().__init__(message, **kwargs)

    def xǁWireFormatErrorǁ__init____mutmut_11(
        self,
        message: str,
        *,
        format_type: Any = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        self.format_type = format_type
        self.operation = operation

        # Add wire format context
        if format_type is not None:
            kwargs.setdefault("context", {})["XXwire.format_typeXX"] = str(format_type)
        if operation is not None:
            kwargs.setdefault("context", {})["wire.operation"] = operation

        super().__init__(message, **kwargs)

    def xǁWireFormatErrorǁ__init____mutmut_12(
        self,
        message: str,
        *,
        format_type: Any = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        self.format_type = format_type
        self.operation = operation

        # Add wire format context
        if format_type is not None:
            kwargs.setdefault("context", {})["WIRE.FORMAT_TYPE"] = str(format_type)
        if operation is not None:
            kwargs.setdefault("context", {})["wire.operation"] = operation

        super().__init__(message, **kwargs)

    def xǁWireFormatErrorǁ__init____mutmut_13(
        self,
        message: str,
        *,
        format_type: Any = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        self.format_type = format_type
        self.operation = operation

        # Add wire format context
        if format_type is not None:
            kwargs.setdefault("context", {})["wire.format_type"] = str(None)
        if operation is not None:
            kwargs.setdefault("context", {})["wire.operation"] = operation

        super().__init__(message, **kwargs)

    def xǁWireFormatErrorǁ__init____mutmut_14(
        self,
        message: str,
        *,
        format_type: Any = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        self.format_type = format_type
        self.operation = operation

        # Add wire format context
        if format_type is not None:
            kwargs.setdefault("context", {})["wire.format_type"] = str(format_type)
        if operation is None:
            kwargs.setdefault("context", {})["wire.operation"] = operation

        super().__init__(message, **kwargs)

    def xǁWireFormatErrorǁ__init____mutmut_15(
        self,
        message: str,
        *,
        format_type: Any = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        self.format_type = format_type
        self.operation = operation

        # Add wire format context
        if format_type is not None:
            kwargs.setdefault("context", {})["wire.format_type"] = str(format_type)
        if operation is not None:
            kwargs.setdefault("context", {})["wire.operation"] = None

        super().__init__(message, **kwargs)

    def xǁWireFormatErrorǁ__init____mutmut_16(
        self,
        message: str,
        *,
        format_type: Any = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        self.format_type = format_type
        self.operation = operation

        # Add wire format context
        if format_type is not None:
            kwargs.setdefault("context", {})["wire.format_type"] = str(format_type)
        if operation is not None:
            kwargs.setdefault(None, {})["wire.operation"] = operation

        super().__init__(message, **kwargs)

    def xǁWireFormatErrorǁ__init____mutmut_17(
        self,
        message: str,
        *,
        format_type: Any = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        self.format_type = format_type
        self.operation = operation

        # Add wire format context
        if format_type is not None:
            kwargs.setdefault("context", {})["wire.format_type"] = str(format_type)
        if operation is not None:
            kwargs.setdefault("context", None)["wire.operation"] = operation

        super().__init__(message, **kwargs)

    def xǁWireFormatErrorǁ__init____mutmut_18(
        self,
        message: str,
        *,
        format_type: Any = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        self.format_type = format_type
        self.operation = operation

        # Add wire format context
        if format_type is not None:
            kwargs.setdefault("context", {})["wire.format_type"] = str(format_type)
        if operation is not None:
            kwargs.setdefault({})["wire.operation"] = operation

        super().__init__(message, **kwargs)

    def xǁWireFormatErrorǁ__init____mutmut_19(
        self,
        message: str,
        *,
        format_type: Any = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        self.format_type = format_type
        self.operation = operation

        # Add wire format context
        if format_type is not None:
            kwargs.setdefault("context", {})["wire.format_type"] = str(format_type)
        if operation is not None:
            kwargs.setdefault("context", )["wire.operation"] = operation

        super().__init__(message, **kwargs)

    def xǁWireFormatErrorǁ__init____mutmut_20(
        self,
        message: str,
        *,
        format_type: Any = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        self.format_type = format_type
        self.operation = operation

        # Add wire format context
        if format_type is not None:
            kwargs.setdefault("context", {})["wire.format_type"] = str(format_type)
        if operation is not None:
            kwargs.setdefault("XXcontextXX", {})["wire.operation"] = operation

        super().__init__(message, **kwargs)

    def xǁWireFormatErrorǁ__init____mutmut_21(
        self,
        message: str,
        *,
        format_type: Any = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        self.format_type = format_type
        self.operation = operation

        # Add wire format context
        if format_type is not None:
            kwargs.setdefault("context", {})["wire.format_type"] = str(format_type)
        if operation is not None:
            kwargs.setdefault("CONTEXT", {})["wire.operation"] = operation

        super().__init__(message, **kwargs)

    def xǁWireFormatErrorǁ__init____mutmut_22(
        self,
        message: str,
        *,
        format_type: Any = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        self.format_type = format_type
        self.operation = operation

        # Add wire format context
        if format_type is not None:
            kwargs.setdefault("context", {})["wire.format_type"] = str(format_type)
        if operation is not None:
            kwargs.setdefault("context", {})["XXwire.operationXX"] = operation

        super().__init__(message, **kwargs)

    def xǁWireFormatErrorǁ__init____mutmut_23(
        self,
        message: str,
        *,
        format_type: Any = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        self.format_type = format_type
        self.operation = operation

        # Add wire format context
        if format_type is not None:
            kwargs.setdefault("context", {})["wire.format_type"] = str(format_type)
        if operation is not None:
            kwargs.setdefault("context", {})["WIRE.OPERATION"] = operation

        super().__init__(message, **kwargs)

    def xǁWireFormatErrorǁ__init____mutmut_24(
        self,
        message: str,
        *,
        format_type: Any = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        self.format_type = format_type
        self.operation = operation

        # Add wire format context
        if format_type is not None:
            kwargs.setdefault("context", {})["wire.format_type"] = str(format_type)
        if operation is not None:
            kwargs.setdefault("context", {})["wire.operation"] = operation

        super().__init__(None, **kwargs)

    def xǁWireFormatErrorǁ__init____mutmut_25(
        self,
        message: str,
        *,
        format_type: Any = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        self.format_type = format_type
        self.operation = operation

        # Add wire format context
        if format_type is not None:
            kwargs.setdefault("context", {})["wire.format_type"] = str(format_type)
        if operation is not None:
            kwargs.setdefault("context", {})["wire.operation"] = operation

        super().__init__(**kwargs)

    def xǁWireFormatErrorǁ__init____mutmut_26(
        self,
        message: str,
        *,
        format_type: Any = None,
        operation: str | None = None,
        **kwargs: Any,
    ) -> None:
        self.format_type = format_type
        self.operation = operation

        # Add wire format context
        if format_type is not None:
            kwargs.setdefault("context", {})["wire.format_type"] = str(format_type)
        if operation is not None:
            kwargs.setdefault("context", {})["wire.operation"] = operation

        super().__init__(message, )
    
    xǁWireFormatErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁWireFormatErrorǁ__init____mutmut_1': xǁWireFormatErrorǁ__init____mutmut_1, 
        'xǁWireFormatErrorǁ__init____mutmut_2': xǁWireFormatErrorǁ__init____mutmut_2, 
        'xǁWireFormatErrorǁ__init____mutmut_3': xǁWireFormatErrorǁ__init____mutmut_3, 
        'xǁWireFormatErrorǁ__init____mutmut_4': xǁWireFormatErrorǁ__init____mutmut_4, 
        'xǁWireFormatErrorǁ__init____mutmut_5': xǁWireFormatErrorǁ__init____mutmut_5, 
        'xǁWireFormatErrorǁ__init____mutmut_6': xǁWireFormatErrorǁ__init____mutmut_6, 
        'xǁWireFormatErrorǁ__init____mutmut_7': xǁWireFormatErrorǁ__init____mutmut_7, 
        'xǁWireFormatErrorǁ__init____mutmut_8': xǁWireFormatErrorǁ__init____mutmut_8, 
        'xǁWireFormatErrorǁ__init____mutmut_9': xǁWireFormatErrorǁ__init____mutmut_9, 
        'xǁWireFormatErrorǁ__init____mutmut_10': xǁWireFormatErrorǁ__init____mutmut_10, 
        'xǁWireFormatErrorǁ__init____mutmut_11': xǁWireFormatErrorǁ__init____mutmut_11, 
        'xǁWireFormatErrorǁ__init____mutmut_12': xǁWireFormatErrorǁ__init____mutmut_12, 
        'xǁWireFormatErrorǁ__init____mutmut_13': xǁWireFormatErrorǁ__init____mutmut_13, 
        'xǁWireFormatErrorǁ__init____mutmut_14': xǁWireFormatErrorǁ__init____mutmut_14, 
        'xǁWireFormatErrorǁ__init____mutmut_15': xǁWireFormatErrorǁ__init____mutmut_15, 
        'xǁWireFormatErrorǁ__init____mutmut_16': xǁWireFormatErrorǁ__init____mutmut_16, 
        'xǁWireFormatErrorǁ__init____mutmut_17': xǁWireFormatErrorǁ__init____mutmut_17, 
        'xǁWireFormatErrorǁ__init____mutmut_18': xǁWireFormatErrorǁ__init____mutmut_18, 
        'xǁWireFormatErrorǁ__init____mutmut_19': xǁWireFormatErrorǁ__init____mutmut_19, 
        'xǁWireFormatErrorǁ__init____mutmut_20': xǁWireFormatErrorǁ__init____mutmut_20, 
        'xǁWireFormatErrorǁ__init____mutmut_21': xǁWireFormatErrorǁ__init____mutmut_21, 
        'xǁWireFormatErrorǁ__init____mutmut_22': xǁWireFormatErrorǁ__init____mutmut_22, 
        'xǁWireFormatErrorǁ__init____mutmut_23': xǁWireFormatErrorǁ__init____mutmut_23, 
        'xǁWireFormatErrorǁ__init____mutmut_24': xǁWireFormatErrorǁ__init____mutmut_24, 
        'xǁWireFormatErrorǁ__init____mutmut_25': xǁWireFormatErrorǁ__init____mutmut_25, 
        'xǁWireFormatErrorǁ__init____mutmut_26': xǁWireFormatErrorǁ__init____mutmut_26
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁWireFormatErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁWireFormatErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁWireFormatErrorǁ__init____mutmut_orig)
    xǁWireFormatErrorǁ__init____mutmut_orig.__name__ = 'xǁWireFormatErrorǁ__init__'

    def xǁWireFormatErrorǁ_default_code__mutmut_orig(self) -> str:
        return "WIRE_FORMAT_ERROR"

    def xǁWireFormatErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXWIRE_FORMAT_ERRORXX"

    def xǁWireFormatErrorǁ_default_code__mutmut_2(self) -> str:
        return "wire_format_error"
    
    xǁWireFormatErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁWireFormatErrorǁ_default_code__mutmut_1': xǁWireFormatErrorǁ_default_code__mutmut_1, 
        'xǁWireFormatErrorǁ_default_code__mutmut_2': xǁWireFormatErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁWireFormatErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁWireFormatErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁWireFormatErrorǁ_default_code__mutmut_orig)
    xǁWireFormatErrorǁ_default_code__mutmut_orig.__name__ = 'xǁWireFormatErrorǁ_default_code'


class FrameworkConfigurationError(PyviderError):
    """Errors related to the overall framework configuration."""

    def xǁFrameworkConfigurationErrorǁ_default_code__mutmut_orig(self) -> str:
        return "FRAMEWORK_CONFIG_ERROR"

    def xǁFrameworkConfigurationErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXFRAMEWORK_CONFIG_ERRORXX"

    def xǁFrameworkConfigurationErrorǁ_default_code__mutmut_2(self) -> str:
        return "framework_config_error"
    
    xǁFrameworkConfigurationErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁFrameworkConfigurationErrorǁ_default_code__mutmut_1': xǁFrameworkConfigurationErrorǁ_default_code__mutmut_1, 
        'xǁFrameworkConfigurationErrorǁ_default_code__mutmut_2': xǁFrameworkConfigurationErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁFrameworkConfigurationErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁFrameworkConfigurationErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁFrameworkConfigurationErrorǁ_default_code__mutmut_orig)
    xǁFrameworkConfigurationErrorǁ_default_code__mutmut_orig.__name__ = 'xǁFrameworkConfigurationErrorǁ_default_code'


class PluginError(PyviderError):
    """Base class for errors originating from plugin operations or lifecycle."""

    pass


class PyviderValueError(PyviderError):
    """Generic value-related errors within Pyvider."""

    def xǁPyviderValueErrorǁ_default_code__mutmut_orig(self) -> str:
        return "VALUE_ERROR"

    def xǁPyviderValueErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXVALUE_ERRORXX"

    def xǁPyviderValueErrorǁ_default_code__mutmut_2(self) -> str:
        return "value_error"
    
    xǁPyviderValueErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁPyviderValueErrorǁ_default_code__mutmut_1': xǁPyviderValueErrorǁ_default_code__mutmut_1, 
        'xǁPyviderValueErrorǁ_default_code__mutmut_2': xǁPyviderValueErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁPyviderValueErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁPyviderValueErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁPyviderValueErrorǁ_default_code__mutmut_orig)
    xǁPyviderValueErrorǁ_default_code__mutmut_orig.__name__ = 'xǁPyviderValueErrorǁ_default_code'


class InvalidTypeError(PyviderValueError):
    """Raised when a value does not match the expected type."""

    def xǁInvalidTypeErrorǁ__init____mutmut_orig(
        self,
        expected_type: str = "unknown",
        actual_type: str = "unknown",
        message_override: str | None = None,
    ) -> None:
        message = message_override or f"Invalid type: expected '{expected_type}', got '{actual_type}'."

        super().__init__(message, context={"type.expected": expected_type, "type.actual": actual_type})

    def xǁInvalidTypeErrorǁ__init____mutmut_1(
        self,
        expected_type: str = "XXunknownXX",
        actual_type: str = "unknown",
        message_override: str | None = None,
    ) -> None:
        message = message_override or f"Invalid type: expected '{expected_type}', got '{actual_type}'."

        super().__init__(message, context={"type.expected": expected_type, "type.actual": actual_type})

    def xǁInvalidTypeErrorǁ__init____mutmut_2(
        self,
        expected_type: str = "UNKNOWN",
        actual_type: str = "unknown",
        message_override: str | None = None,
    ) -> None:
        message = message_override or f"Invalid type: expected '{expected_type}', got '{actual_type}'."

        super().__init__(message, context={"type.expected": expected_type, "type.actual": actual_type})

    def xǁInvalidTypeErrorǁ__init____mutmut_3(
        self,
        expected_type: str = "unknown",
        actual_type: str = "XXunknownXX",
        message_override: str | None = None,
    ) -> None:
        message = message_override or f"Invalid type: expected '{expected_type}', got '{actual_type}'."

        super().__init__(message, context={"type.expected": expected_type, "type.actual": actual_type})

    def xǁInvalidTypeErrorǁ__init____mutmut_4(
        self,
        expected_type: str = "unknown",
        actual_type: str = "UNKNOWN",
        message_override: str | None = None,
    ) -> None:
        message = message_override or f"Invalid type: expected '{expected_type}', got '{actual_type}'."

        super().__init__(message, context={"type.expected": expected_type, "type.actual": actual_type})

    def xǁInvalidTypeErrorǁ__init____mutmut_5(
        self,
        expected_type: str = "unknown",
        actual_type: str = "unknown",
        message_override: str | None = None,
    ) -> None:
        message = None

        super().__init__(message, context={"type.expected": expected_type, "type.actual": actual_type})

    def xǁInvalidTypeErrorǁ__init____mutmut_6(
        self,
        expected_type: str = "unknown",
        actual_type: str = "unknown",
        message_override: str | None = None,
    ) -> None:
        message = message_override and f"Invalid type: expected '{expected_type}', got '{actual_type}'."

        super().__init__(message, context={"type.expected": expected_type, "type.actual": actual_type})

    def xǁInvalidTypeErrorǁ__init____mutmut_7(
        self,
        expected_type: str = "unknown",
        actual_type: str = "unknown",
        message_override: str | None = None,
    ) -> None:
        message = message_override or f"Invalid type: expected '{expected_type}', got '{actual_type}'."

        super().__init__(None, context={"type.expected": expected_type, "type.actual": actual_type})

    def xǁInvalidTypeErrorǁ__init____mutmut_8(
        self,
        expected_type: str = "unknown",
        actual_type: str = "unknown",
        message_override: str | None = None,
    ) -> None:
        message = message_override or f"Invalid type: expected '{expected_type}', got '{actual_type}'."

        super().__init__(message, context=None)

    def xǁInvalidTypeErrorǁ__init____mutmut_9(
        self,
        expected_type: str = "unknown",
        actual_type: str = "unknown",
        message_override: str | None = None,
    ) -> None:
        message = message_override or f"Invalid type: expected '{expected_type}', got '{actual_type}'."

        super().__init__(context={"type.expected": expected_type, "type.actual": actual_type})

    def xǁInvalidTypeErrorǁ__init____mutmut_10(
        self,
        expected_type: str = "unknown",
        actual_type: str = "unknown",
        message_override: str | None = None,
    ) -> None:
        message = message_override or f"Invalid type: expected '{expected_type}', got '{actual_type}'."

        super().__init__(message, )

    def xǁInvalidTypeErrorǁ__init____mutmut_11(
        self,
        expected_type: str = "unknown",
        actual_type: str = "unknown",
        message_override: str | None = None,
    ) -> None:
        message = message_override or f"Invalid type: expected '{expected_type}', got '{actual_type}'."

        super().__init__(message, context={"XXtype.expectedXX": expected_type, "type.actual": actual_type})

    def xǁInvalidTypeErrorǁ__init____mutmut_12(
        self,
        expected_type: str = "unknown",
        actual_type: str = "unknown",
        message_override: str | None = None,
    ) -> None:
        message = message_override or f"Invalid type: expected '{expected_type}', got '{actual_type}'."

        super().__init__(message, context={"TYPE.EXPECTED": expected_type, "type.actual": actual_type})

    def xǁInvalidTypeErrorǁ__init____mutmut_13(
        self,
        expected_type: str = "unknown",
        actual_type: str = "unknown",
        message_override: str | None = None,
    ) -> None:
        message = message_override or f"Invalid type: expected '{expected_type}', got '{actual_type}'."

        super().__init__(message, context={"type.expected": expected_type, "XXtype.actualXX": actual_type})

    def xǁInvalidTypeErrorǁ__init____mutmut_14(
        self,
        expected_type: str = "unknown",
        actual_type: str = "unknown",
        message_override: str | None = None,
    ) -> None:
        message = message_override or f"Invalid type: expected '{expected_type}', got '{actual_type}'."

        super().__init__(message, context={"type.expected": expected_type, "TYPE.ACTUAL": actual_type})
    
    xǁInvalidTypeErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁInvalidTypeErrorǁ__init____mutmut_1': xǁInvalidTypeErrorǁ__init____mutmut_1, 
        'xǁInvalidTypeErrorǁ__init____mutmut_2': xǁInvalidTypeErrorǁ__init____mutmut_2, 
        'xǁInvalidTypeErrorǁ__init____mutmut_3': xǁInvalidTypeErrorǁ__init____mutmut_3, 
        'xǁInvalidTypeErrorǁ__init____mutmut_4': xǁInvalidTypeErrorǁ__init____mutmut_4, 
        'xǁInvalidTypeErrorǁ__init____mutmut_5': xǁInvalidTypeErrorǁ__init____mutmut_5, 
        'xǁInvalidTypeErrorǁ__init____mutmut_6': xǁInvalidTypeErrorǁ__init____mutmut_6, 
        'xǁInvalidTypeErrorǁ__init____mutmut_7': xǁInvalidTypeErrorǁ__init____mutmut_7, 
        'xǁInvalidTypeErrorǁ__init____mutmut_8': xǁInvalidTypeErrorǁ__init____mutmut_8, 
        'xǁInvalidTypeErrorǁ__init____mutmut_9': xǁInvalidTypeErrorǁ__init____mutmut_9, 
        'xǁInvalidTypeErrorǁ__init____mutmut_10': xǁInvalidTypeErrorǁ__init____mutmut_10, 
        'xǁInvalidTypeErrorǁ__init____mutmut_11': xǁInvalidTypeErrorǁ__init____mutmut_11, 
        'xǁInvalidTypeErrorǁ__init____mutmut_12': xǁInvalidTypeErrorǁ__init____mutmut_12, 
        'xǁInvalidTypeErrorǁ__init____mutmut_13': xǁInvalidTypeErrorǁ__init____mutmut_13, 
        'xǁInvalidTypeErrorǁ__init____mutmut_14': xǁInvalidTypeErrorǁ__init____mutmut_14
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁInvalidTypeErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁInvalidTypeErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁInvalidTypeErrorǁ__init____mutmut_orig)
    xǁInvalidTypeErrorǁ__init____mutmut_orig.__name__ = 'xǁInvalidTypeErrorǁ__init__'

    def xǁInvalidTypeErrorǁ_default_code__mutmut_orig(self) -> str:
        return "INVALID_TYPE"

    def xǁInvalidTypeErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXINVALID_TYPEXX"

    def xǁInvalidTypeErrorǁ_default_code__mutmut_2(self) -> str:
        return "invalid_type"
    
    xǁInvalidTypeErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁInvalidTypeErrorǁ_default_code__mutmut_1': xǁInvalidTypeErrorǁ_default_code__mutmut_1, 
        'xǁInvalidTypeErrorǁ_default_code__mutmut_2': xǁInvalidTypeErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁInvalidTypeErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁInvalidTypeErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁInvalidTypeErrorǁ_default_code__mutmut_orig)
    xǁInvalidTypeErrorǁ_default_code__mutmut_orig.__name__ = 'xǁInvalidTypeErrorǁ_default_code'


class UnsupportedTypeError(PyviderValueError):
    """Raised when an unsupported type is encountered."""

    def xǁUnsupportedTypeErrorǁ__init____mutmut_orig(self, type_name: str = "unknown", message_override: str | None = None) -> None:
        message = message_override or f"Unsupported type encountered: '{type_name}'."

        super().__init__(message, context={"type.unsupported": type_name})

    def xǁUnsupportedTypeErrorǁ__init____mutmut_1(self, type_name: str = "XXunknownXX", message_override: str | None = None) -> None:
        message = message_override or f"Unsupported type encountered: '{type_name}'."

        super().__init__(message, context={"type.unsupported": type_name})

    def xǁUnsupportedTypeErrorǁ__init____mutmut_2(self, type_name: str = "UNKNOWN", message_override: str | None = None) -> None:
        message = message_override or f"Unsupported type encountered: '{type_name}'."

        super().__init__(message, context={"type.unsupported": type_name})

    def xǁUnsupportedTypeErrorǁ__init____mutmut_3(self, type_name: str = "unknown", message_override: str | None = None) -> None:
        message = None

        super().__init__(message, context={"type.unsupported": type_name})

    def xǁUnsupportedTypeErrorǁ__init____mutmut_4(self, type_name: str = "unknown", message_override: str | None = None) -> None:
        message = message_override and f"Unsupported type encountered: '{type_name}'."

        super().__init__(message, context={"type.unsupported": type_name})

    def xǁUnsupportedTypeErrorǁ__init____mutmut_5(self, type_name: str = "unknown", message_override: str | None = None) -> None:
        message = message_override or f"Unsupported type encountered: '{type_name}'."

        super().__init__(None, context={"type.unsupported": type_name})

    def xǁUnsupportedTypeErrorǁ__init____mutmut_6(self, type_name: str = "unknown", message_override: str | None = None) -> None:
        message = message_override or f"Unsupported type encountered: '{type_name}'."

        super().__init__(message, context=None)

    def xǁUnsupportedTypeErrorǁ__init____mutmut_7(self, type_name: str = "unknown", message_override: str | None = None) -> None:
        message = message_override or f"Unsupported type encountered: '{type_name}'."

        super().__init__(context={"type.unsupported": type_name})

    def xǁUnsupportedTypeErrorǁ__init____mutmut_8(self, type_name: str = "unknown", message_override: str | None = None) -> None:
        message = message_override or f"Unsupported type encountered: '{type_name}'."

        super().__init__(message, )

    def xǁUnsupportedTypeErrorǁ__init____mutmut_9(self, type_name: str = "unknown", message_override: str | None = None) -> None:
        message = message_override or f"Unsupported type encountered: '{type_name}'."

        super().__init__(message, context={"XXtype.unsupportedXX": type_name})

    def xǁUnsupportedTypeErrorǁ__init____mutmut_10(self, type_name: str = "unknown", message_override: str | None = None) -> None:
        message = message_override or f"Unsupported type encountered: '{type_name}'."

        super().__init__(message, context={"TYPE.UNSUPPORTED": type_name})
    
    xǁUnsupportedTypeErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁUnsupportedTypeErrorǁ__init____mutmut_1': xǁUnsupportedTypeErrorǁ__init____mutmut_1, 
        'xǁUnsupportedTypeErrorǁ__init____mutmut_2': xǁUnsupportedTypeErrorǁ__init____mutmut_2, 
        'xǁUnsupportedTypeErrorǁ__init____mutmut_3': xǁUnsupportedTypeErrorǁ__init____mutmut_3, 
        'xǁUnsupportedTypeErrorǁ__init____mutmut_4': xǁUnsupportedTypeErrorǁ__init____mutmut_4, 
        'xǁUnsupportedTypeErrorǁ__init____mutmut_5': xǁUnsupportedTypeErrorǁ__init____mutmut_5, 
        'xǁUnsupportedTypeErrorǁ__init____mutmut_6': xǁUnsupportedTypeErrorǁ__init____mutmut_6, 
        'xǁUnsupportedTypeErrorǁ__init____mutmut_7': xǁUnsupportedTypeErrorǁ__init____mutmut_7, 
        'xǁUnsupportedTypeErrorǁ__init____mutmut_8': xǁUnsupportedTypeErrorǁ__init____mutmut_8, 
        'xǁUnsupportedTypeErrorǁ__init____mutmut_9': xǁUnsupportedTypeErrorǁ__init____mutmut_9, 
        'xǁUnsupportedTypeErrorǁ__init____mutmut_10': xǁUnsupportedTypeErrorǁ__init____mutmut_10
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁUnsupportedTypeErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁUnsupportedTypeErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁUnsupportedTypeErrorǁ__init____mutmut_orig)
    xǁUnsupportedTypeErrorǁ__init____mutmut_orig.__name__ = 'xǁUnsupportedTypeErrorǁ__init__'

    def xǁUnsupportedTypeErrorǁ_default_code__mutmut_orig(self) -> str:
        return "UNSUPPORTED_TYPE"

    def xǁUnsupportedTypeErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXUNSUPPORTED_TYPEXX"

    def xǁUnsupportedTypeErrorǁ_default_code__mutmut_2(self) -> str:
        return "unsupported_type"
    
    xǁUnsupportedTypeErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁUnsupportedTypeErrorǁ_default_code__mutmut_1': xǁUnsupportedTypeErrorǁ_default_code__mutmut_1, 
        'xǁUnsupportedTypeErrorǁ_default_code__mutmut_2': xǁUnsupportedTypeErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁUnsupportedTypeErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁUnsupportedTypeErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁUnsupportedTypeErrorǁ_default_code__mutmut_orig)
    xǁUnsupportedTypeErrorǁ_default_code__mutmut_orig.__name__ = 'xǁUnsupportedTypeErrorǁ_default_code'


class ComponentConfigurationError(FrameworkConfigurationError):
    """Errors specific to component configuration (e.g., resource, provider)."""

    def xǁComponentConfigurationErrorǁ_default_code__mutmut_orig(self) -> str:
        return "COMPONENT_CONFIG_ERROR"

    def xǁComponentConfigurationErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXCOMPONENT_CONFIG_ERRORXX"

    def xǁComponentConfigurationErrorǁ_default_code__mutmut_2(self) -> str:
        return "component_config_error"
    
    xǁComponentConfigurationErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁComponentConfigurationErrorǁ_default_code__mutmut_1': xǁComponentConfigurationErrorǁ_default_code__mutmut_1, 
        'xǁComponentConfigurationErrorǁ_default_code__mutmut_2': xǁComponentConfigurationErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁComponentConfigurationErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁComponentConfigurationErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁComponentConfigurationErrorǁ_default_code__mutmut_orig)
    xǁComponentConfigurationErrorǁ_default_code__mutmut_orig.__name__ = 'xǁComponentConfigurationErrorǁ_default_code'


# 🐍🏗️
