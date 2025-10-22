import asyncio
from typing import Any

from attrs import define, field
from provide.foundation import logger

from pyvider.cty import CtyType
from pyvider.exceptions import FrameworkConfigurationError, ProviderError
from pyvider.schema import PvsSchema
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


@define
class ProviderCapabilities:
    """Provider capability configuration."""

    plan_destroy: bool = True
    get_provider_schema_optional: bool = False
    move_resource_state: bool = True


@define
class ProviderMetadata:
    """Provider metadata configuration."""

    name: str
    version: str
    protocol_version: str = "6"
    capabilities: ProviderCapabilities = field(factory=ProviderCapabilities)


@define
class BaseProvider:
    """
    Base provider implementation that handles gRPC service initialization
    and provider lifecycle management.
    """

    metadata: ProviderMetadata
    config_class: Any | None = None  # Add config_class attribute
    _configured: bool = field(default=False, init=False)
    _final_schema: PvsSchema | None = field(default=None, init=False)

    async def setup(self) -> None:
        """
        An initialization hook called by the framework after component
        discovery but before serving requests. This is the ideal place
        to assemble the final schema by integrating capabilities.
        """
        pass  # pragma: no cover

    async def configure(self, config: dict[str, CtyType]) -> None:
        """Configure the provider with the given configuration."""
        async with asyncio.Lock():
            if self._configured:
                raise ProviderError("Provider already configured")

            logger.info("Provider configured with data (logic to be implemented).")
            self._configured = True

    @property
    def schema(self) -> PvsSchema:
        """Get the provider schema."""
        if self._final_schema is None:
            raise FrameworkConfigurationError("Provider schema was requested before the setup() hook was run.")
        return self._final_schema
