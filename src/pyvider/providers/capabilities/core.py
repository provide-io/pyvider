from pyvider.capabilities import BaseCapability, register_capability
from pyvider.schema import PvsAttribute


@register_capability("core")
class CoreProviderCapability(BaseCapability):
    """
    The built-in 'core' capability for the Pyvider provider.

    This capability provides the foundational, empty schema block that
    other capabilities can extend. Its contribution is an empty dictionary,
    making it a neutral identity element in the schema composition process.
    """

    @staticmethod
    def get_schema_contribution() -> dict[str, PvsAttribute]:
        """Contributes the base provider attributes (none in this case)."""
        return {}
