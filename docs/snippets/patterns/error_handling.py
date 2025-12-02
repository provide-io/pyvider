"""
Error handling pattern examples.

This snippet demonstrates common error handling patterns:
- HTTP error handling with httpx
- Retries with exponential backoff
- User-friendly error messages
- Error diagnostics with ResourceContext

Used in: guides showing error handling best practices.
"""

import httpx

from pyvider.resources.context import ResourceContext


# --8<-- [start:basic_http_errors]
async def handle_http_errors_basic(ctx: ResourceContext, url: str) -> dict | None:
    """Basic HTTP error handling."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                ctx.add_warning(f"Resource not found: {url}")
                return None
            elif e.response.status_code >= 500:
                ctx.add_error(f"Server error: {e.response.status_code}")
                raise
            else:
                ctx.add_error(f"HTTP error: {e.response.status_code}")
                raise

        except httpx.RequestError as e:
            ctx.add_error(f"Request failed: {e!s}")
            raise


# --8<-- [end:basic_http_errors]


# --8<-- [start:retry_pattern]
import asyncio


async def fetch_with_retry(
    ctx: ResourceContext,
    url: str,
    max_retries: int = 3,
    base_delay: float = 1.0,
) -> dict | None:
    """Fetch with exponential backoff retry."""
    last_error = None

    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10.0)
                response.raise_for_status()
                return response.json()

        except httpx.HTTPStatusError as e:
            # Don't retry 4xx errors (client errors)
            if 400 <= e.response.status_code < 500:
                ctx.add_error(f"Client error: {e.response.status_code}")
                raise

            last_error = e
            if attempt < max_retries - 1:
                delay = base_delay * (2**attempt)  # Exponential backoff
                ctx.add_warning(
                    f"Request failed (attempt {attempt + 1}/{max_retries}), retrying in {delay}s..."
                )
                await asyncio.sleep(delay)

        except httpx.RequestError as e:
            last_error = e
            if attempt < max_retries - 1:
                delay = base_delay * (2**attempt)
                ctx.add_warning(
                    f"Request failed (attempt {attempt + 1}/{max_retries}), retrying in {delay}s..."
                )
                await asyncio.sleep(delay)

    # All retries exhausted
    ctx.add_error(f"Failed after {max_retries} attempts: {last_error}")
    raise last_error


# --8<-- [end:retry_pattern]


# --8<-- [start:user_friendly_errors]
async def create_with_friendly_errors(ctx: ResourceContext, name: str) -> dict:
    """Create resource with user-friendly error messages."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.example.com/resources",
                json={"name": name},
                timeout=10.0,
            )
            response.raise_for_status()
            return response.json()

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 409:
            # Conflict - resource already exists
            ctx.add_error(
                f"Resource '{name}' already exists. Choose a different name or import the existing resource."
            )
        elif e.response.status_code == 403:
            # Forbidden - permissions issue
            ctx.add_error(
                "Permission denied. Ensure your API credentials have "
                "permission to create resources in this project."
            )
        elif e.response.status_code == 422:
            # Validation error
            error_details = e.response.json().get("errors", [])
            ctx.add_error(f"Validation failed: {', '.join(error_details)}")
        else:
            # Generic error
            ctx.add_error(
                f"Failed to create resource: HTTP {e.response.status_code}. "
                f"Check API documentation for details."
            )
        raise

    except httpx.RequestError as e:
        ctx.add_error(
            f"Unable to connect to API server: {e!s}. "
            "Check your network connection and API endpoint configuration."
        )
        raise


# --8<-- [end:user_friendly_errors]


# --8<-- [start:context_diagnostics]
from pyvider.resources import BaseResource, ResourceContext


class ExampleResource(BaseResource):
    """Example showing ResourceContext diagnostics usage."""

    async def _create_apply(self, ctx: ResourceContext) -> tuple[dict | None, None]:
        """Create with comprehensive error handling."""
        if not ctx.config:
            return None, None

        # Add informational diagnostics
        ctx.add_info("Starting resource creation...")

        # Validate prerequisites
        if not self._check_prerequisites(ctx.config):
            ctx.add_error("Prerequisites not met. Ensure dependencies are configured.")
            return None, None

        # Add warnings for potentially risky operations
        if ctx.config.get("public_access"):
            ctx.add_warning(
                "Public access is enabled. Ensure this is intentional as it "
                "may expose your resource to the internet."
            )

        try:
            # Perform operation
            result = await self._perform_create(ctx)
            ctx.add_info("Resource created successfully")
            return result, None

        except ValueError as e:
            ctx.add_error(f"Invalid configuration: {e!s}")
            return None, None

        except PermissionError as e:
            ctx.add_error(f"Permission denied: {e!s}")
            return None, None

        except Exception as e:
            ctx.add_error(f"Unexpected error: {e!s}")
            raise

    def _check_prerequisites(self, config) -> bool:
        """Check prerequisites (example)."""
        return True

    async def _perform_create(self, ctx: ResourceContext) -> dict:
        """Perform creation (example)."""
        return {}


# --8<-- [end:context_diagnostics]
