#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from pyvider.resources.base import BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.schema import PvsSchema

DataSourceType = TypeVar("DataSourceType")
StateType = TypeVar("StateType")
ConfigType = TypeVar("ConfigType")


class BaseDataSource(ABC, Generic[DataSourceType, StateType, ConfigType]):
    """Base class for read-only data sources.

    ``config_class`` and ``state_class`` must be ``attrs`` classes
    (decorated with ``@attrs.define`` / ``@attrs.frozen``). The framework
    introspects them via ``attrs.fields()`` during cty ↔ Python
    conversion; plain ``dataclasses`` or other class flavors will not
    round-trip correctly. See ``BaseResource`` for the full rationale.
    The validator in ``cty_to_attrs_instance`` raises
    ``FrameworkConfigurationError`` up front on misuse.
    """

    config_class: type[ConfigType] | None = None
    state_class: type[StateType]

    @classmethod
    @abstractmethod
    def get_schema(cls) -> PvsSchema: ...

    @classmethod
    def from_cty(cls, *args: Any, **kwargs: Any) -> Any:
        # Delegate to the common helper method on BaseResource
        return BaseResource.from_cty(*args, **kwargs)

    async def validate(self, config: ConfigType | None) -> list[str]:
        """
        Runs custom validation logic for the data source's configuration.
        This is the template method that calls the developer-implemented hook.
        """
        if config is None:
            return []
        return await self._validate_config(config)

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


# 🐍🏗️🔚
