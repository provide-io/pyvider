from __future__ import annotations

from typing import TYPE_CHECKING, Any

from attrs import define, field
from provide.foundation import logger

from pyvider.common.context import BaseContext

if TYPE_CHECKING:
    from pyvider.providers.base import BaseProvider


@define
class ProviderContext(BaseContext):
    """
    Holds the configured state of the provider. Inherits diagnostic
    reporting capabilities from BaseContext.
    """

    config: Any = field()
    provider: BaseProvider | None = field(default=None, init=False)

    def __attrs_post_init__(self) -> None:
        logger.info("ProviderContext initialized", config_type=type(self.config).__name__)
