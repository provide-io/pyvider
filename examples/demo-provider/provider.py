"""
Simple Demo Provider for Pyvider - Testing s_function

This demonstrates that s_function works with a real provider.
"""

from pyvider.functions import BaseFunction, FunctionParameter, FunctionReturnType
from pyvider.hub import register_function, register_resource
from pyvider.providers import BaseProvider
from pyvider.providers.decorators import register_provider
from pyvider.resources import BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.schema import PvsSchema, a_list, a_num, a_str, s_function, s_provider, s_resource


@register_provider(name="demo")
class DemoProvider(BaseProvider):
    """Demo provider to test s_function functionality."""

    @classmethod
    def get_schema(cls) -> PvsSchema:
        """Provider configuration schema."""
        return s_provider(
            attributes={
                "api_key": a_str(description="API key for authentication", required=False),
            }
        )

    async def configure(self, config: dict) -> None:
        """Configure the provider."""
        self.api_key = config.get("api_key", "demo-key")


@register_resource("demo_resource", component_of="demo")
class DemoResource(BaseResource):
    """Demo resource to test resource schema."""

    @classmethod
    def get_schema(cls) -> PvsSchema:
        """Resource schema."""
        return s_resource(
            attributes={
                "name": a_str(description="Resource name", required=True),
                "description": a_str(description="Resource description", required=False),
                "count": a_num(description="Resource count", required=False),
            }
        )

    async def create(self, ctx: ResourceContext) -> dict:
        """Create the resource."""
        return {"id": "demo-1", "name": ctx.config.get("name", "default")}

    async def read(self, ctx: ResourceContext) -> None:
        """Read the resource."""
        pass

    async def update(self, ctx: ResourceContext) -> dict:
        """Update the resource."""
        return ctx.state or {}

    async def delete(self, ctx: ResourceContext) -> None:
        """Delete the resource."""
        pass


@register_function("upper", component_of="demo")
class UpperFunction(BaseFunction):
    """Converts a string to uppercase - using s_function!"""

    name: str = "upper"
    summary: str = "Convert string to uppercase"
    description: str = "Takes a string and returns it in uppercase"

    @classmethod
    def get_schema(cls) -> PvsSchema:
        """Function schema using s_function."""
        return s_function(
            parameters=[
                a_str(description="Input string to convert"),
            ],
            return_type=a_str(description="Uppercase string"),
        )

    def get_parameters(self) -> list[FunctionParameter]:
        """Legacy method - return empty for now."""
        return []

    def get_return_type(self) -> FunctionReturnType:
        """Legacy method."""
        from pyvider.cty import CtyString

        return FunctionReturnType(type=CtyString())

    async def call(self, input_str: str) -> str:
        """Execute the function."""
        return input_str.upper()


@register_function("join_strings", component_of="demo")
class JoinFunction(BaseFunction):
    """Joins strings with a separator - using s_function!"""

    name: str = "join_strings"
    summary: str = "Join strings with separator"
    description: str = "Takes a list of strings and a separator, returns joined string"

    @classmethod
    def get_schema(cls) -> PvsSchema:
        """Function schema using s_function."""
        return s_function(
            parameters=[
                a_list(a_str(), description="Strings to join"),
                a_str(description="Separator character"),
            ],
            return_type=a_str(description="Joined string"),
        )

    def get_parameters(self) -> list[FunctionParameter]:
        """Legacy method."""
        return []

    def get_return_type(self) -> FunctionReturnType:
        """Legacy method."""
        from pyvider.cty import CtyString

        return FunctionReturnType(type=CtyString())

    async def call(self, strings: list[str], separator: str) -> str:
        """Execute the function."""
        return separator.join(strings)


@register_function("add", component_of="demo")
class AddFunction(BaseFunction):
    """Adds two numbers - using s_function!"""

    name: str = "add"
    summary: str = "Add two numbers"
    description: str = "Takes two numbers and returns their sum"

    @classmethod
    def get_schema(cls) -> PvsSchema:
        """Function schema using s_function."""
        return s_function(
            parameters=[
                a_num(description="First number"),
                a_num(description="Second number"),
            ],
            return_type=a_num(description="Sum of the numbers"),
        )

    def get_parameters(self) -> list[FunctionParameter]:
        """Legacy method."""
        return []

    def get_return_type(self) -> FunctionReturnType:
        """Legacy method."""
        from pyvider.cty import CtyNumber

        return FunctionReturnType(type=CtyNumber())

    async def call(self, a: float, b: float) -> float:
        """Execute the function."""
        return a + b


def main():
    """Main entry point for the provider."""
    from pyvider.cli import main as pyvider_main

    pyvider_main()


if __name__ == "__main__":
    main()


# 🐍🏗️🔚
