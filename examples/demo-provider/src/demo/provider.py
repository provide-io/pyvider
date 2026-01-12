"""
Demo Provider - Main Provider Configuration
"""

from pyvider.providers import BaseProvider, ProviderMetadata, register_provider
from pyvider.schema import PvsSchema, a_bool, a_num, a_str, s_provider


@register_provider("demo")
class DemoProvider(BaseProvider):
    """
    Demo infrastructure provider showcasing Pyvider capabilities.

    This provider simulates managing servers and demonstrates:
    - Configuration management
    - Resource lifecycle
    - Data source queries
    - Custom functions
    """

    def __init__(self) -> None:
        super().__init__(
            metadata=ProviderMetadata(
                name="demo",
                version="1.0.0",
                protocol_version="6",
            )
        )

    @classmethod
    def get_schema(cls) -> PvsSchema:
        """Define provider configuration schema"""
        return s_provider(
            {
                "api_url": a_str(
                    required=False,
                    description="API endpoint URL for the demo service",
                ),
                "api_token": a_str(
                    required=False,
                    sensitive=True,
                    description="API authentication token",
                ),
                "timeout": a_num(
                    required=False,
                    description="Request timeout in seconds",
                ),
                "debug": a_bool(
                    required=False,
                    description="Enable debug logging",
                ),
            }
        )
