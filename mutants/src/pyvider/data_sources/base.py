from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from pyvider.resources.base import BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.schema import PvsSchema

DataSourceType = TypeVar("DataSourceType")
StateType = TypeVar("StateType")
ConfigType = TypeVar("ConfigType")
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


class BaseDataSource(ABC, Generic[DataSourceType, StateType, ConfigType]):
    config_class: type[ConfigType] | None = None
    state_class: type[StateType]

    @classmethod
    @abstractmethod
    def get_schema(cls) -> PvsSchema: ...

    @classmethod
    def from_cty(cls, *args: Any, **kwargs: Any) -> Any:
        # Delegate to the common helper method on BaseResource
        return BaseResource.from_cty(*args, **kwargs)

    async def xǁBaseDataSourceǁvalidate__mutmut_orig(self, config: ConfigType | None) -> list[str]:
        """
        Runs custom validation logic for the data source's configuration.
        This is the template method that calls the developer-implemented hook.
        """
        if config is None:
            return []
        return await self._validate_config(config)

    async def xǁBaseDataSourceǁvalidate__mutmut_1(self, config: ConfigType | None) -> list[str]:
        """
        Runs custom validation logic for the data source's configuration.
        This is the template method that calls the developer-implemented hook.
        """
        if config is not None:
            return []
        return await self._validate_config(config)

    async def xǁBaseDataSourceǁvalidate__mutmut_2(self, config: ConfigType | None) -> list[str]:
        """
        Runs custom validation logic for the data source's configuration.
        This is the template method that calls the developer-implemented hook.
        """
        if config is None:
            return []
        return await self._validate_config(None)
    
    xǁBaseDataSourceǁvalidate__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBaseDataSourceǁvalidate__mutmut_1': xǁBaseDataSourceǁvalidate__mutmut_1, 
        'xǁBaseDataSourceǁvalidate__mutmut_2': xǁBaseDataSourceǁvalidate__mutmut_2
    }
    
    def validate(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBaseDataSourceǁvalidate__mutmut_orig"), object.__getattribute__(self, "xǁBaseDataSourceǁvalidate__mutmut_mutants"), args, kwargs, self)
        return result 
    
    validate.__signature__ = _mutmut_signature(xǁBaseDataSourceǁvalidate__mutmut_orig)
    xǁBaseDataSourceǁvalidate__mutmut_orig.__name__ = 'xǁBaseDataSourceǁvalidate'

    @abstractmethod
    async def _validate_config(self, config: ConfigType) -> list[str]:
        """
        [DEVELOPER] Implement this method to perform custom validation.

        This abstract method MUST be implemented by all concrete data source classes.
        Return a list of error strings if validation fails, or an empty list
        if it succeeds.
        """
        return []

    @abstractmethod
    async def read(self, ctx: ResourceContext) -> StateType | None: ...
