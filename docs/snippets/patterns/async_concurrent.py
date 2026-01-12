"""
Async and concurrent operation pattern examples.

This snippet demonstrates:
- Concurrent API calls with asyncio.gather
- Async resource operations
- Parallel resource creation
- Error handling in concurrent operations

Used in: guides showing async/concurrent patterns.
"""

import asyncio

import httpx

from pyvider.resources import BaseResource, ResourceContext


# --8<-- [start:concurrent_api_calls]
async def fetch_multiple_resources_concurrent(
    ctx: ResourceContext,
    resource_ids: list[str],
) -> list[dict]:
    """Fetch multiple resources concurrently."""
    async with httpx.AsyncClient() as client:

        async def fetch_one(resource_id: str) -> dict:
            """Fetch a single resource."""
            response = await client.get(
                f"https://api.example.com/resources/{resource_id}",
                timeout=10.0,
            )
            response.raise_for_status()
            return response.json()

        # Fetch all concurrently
        ctx.add_info(f"Fetching {len(resource_ids)} resources concurrently...")
        results = await asyncio.gather(*[fetch_one(rid) for rid in resource_ids])
        ctx.add_info(f"Fetched {len(results)} resources")

        return results


# --8<-- [end:concurrent_api_calls]


# --8<-- [start:concurrent_with_error_handling]
async def fetch_multiple_with_error_handling(
    ctx: ResourceContext,
    resource_ids: list[str],
) -> list[dict | None]:
    """Fetch multiple resources concurrently with error handling."""
    async with httpx.AsyncClient() as client:

        async def fetch_one_safe(resource_id: str) -> dict | None:
            """Fetch a single resource, returning None on error."""
            try:
                response = await client.get(
                    f"https://api.example.com/resources/{resource_id}",
                    timeout=10.0,
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                ctx.add_warning(f"Failed to fetch {resource_id}: {e}")
                return None

        # Fetch all concurrently (won't fail if some requests fail)
        results = await asyncio.gather(
            *[fetch_one_safe(rid) for rid in resource_ids],
            return_exceptions=False,  # Handle errors in fetch_one_safe
        )

        # Filter out None values if needed
        successful = [r for r in results if r is not None]
        ctx.add_info(f"Successfully fetched {len(successful)}/{len(resource_ids)} resources")

        return results


# --8<-- [end:concurrent_with_error_handling]


# --8<-- [start:parallel_resource_operations]
import attrs


@attrs.define
class MultiConfig:
    """Configuration for creating multiple resources."""

    names: list[str]


@attrs.define
class MultiState:
    """State tracking multiple resources."""

    id: str
    resource_ids: list[str]


class MultiResourceCreator(BaseResource):
    """Example: Create multiple API resources concurrently."""

    config_class = MultiConfig
    state_class = MultiState

    async def _create_apply(self, ctx: ResourceContext) -> tuple[MultiState | None, None]:
        """Create multiple resources concurrently."""
        if not ctx.config:
            return None, None

        async with httpx.AsyncClient() as client:

            async def create_one(name: str) -> str:
                """Create a single resource and return its ID."""
                response = await client.post(
                    "https://api.example.com/resources",
                    json={"name": name},
                    timeout=10.0,
                )
                response.raise_for_status()
                data = response.json()
                return data["id"]

            # Create all resources concurrently
            ctx.add_info(f"Creating {len(ctx.config.names)} resources...")
            resource_ids = await asyncio.gather(*[create_one(name) for name in ctx.config.names])
            ctx.add_info(f"Created {len(resource_ids)} resources")

            return (
                MultiState(
                    id="multi-resource",
                    resource_ids=resource_ids,
                ),
                None,
            )

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        """Delete multiple resources concurrently."""
        if not ctx.state:
            return

        async with httpx.AsyncClient() as client:

            async def delete_one(resource_id: str) -> None:
                """Delete a single resource."""
                await client.delete(
                    f"https://api.example.com/resources/{resource_id}",
                    timeout=10.0,
                )

            # Delete all resources concurrently
            ctx.add_info(f"Deleting {len(ctx.state.resource_ids)} resources...")
            await asyncio.gather(
                *[delete_one(rid) for rid in ctx.state.resource_ids],
                return_exceptions=True,  # Continue even if some deletions fail
            )
            ctx.add_info("Deletion complete")


# --8<-- [end:parallel_resource_operations]


# --8<-- [start:semaphore_rate_limiting]
async def fetch_with_rate_limit(
    ctx: ResourceContext,
    resource_ids: list[str],
    max_concurrent: int = 5,
) -> list[dict]:
    """Fetch resources concurrently with rate limiting."""
    # Limit concurrent requests using a semaphore
    semaphore = asyncio.Semaphore(max_concurrent)

    async with httpx.AsyncClient() as client:

        async def fetch_one(resource_id: str) -> dict:
            """Fetch with rate limiting."""
            async with semaphore:  # Acquire semaphore
                ctx.add_info(f"Fetching {resource_id}...")
                response = await client.get(
                    f"https://api.example.com/resources/{resource_id}",
                    timeout=10.0,
                )
                response.raise_for_status()
                return response.json()

        # Fetch all (but only max_concurrent at a time)
        results = await asyncio.gather(*[fetch_one(rid) for rid in resource_ids])

        return results


# --8<-- [end:semaphore_rate_limiting]


# --8<-- [start:async_timeout]
async def fetch_with_timeout(
    ctx: ResourceContext,
    resource_id: str,
    timeout_seconds: float = 30.0,
) -> dict | None:
    """Fetch resource with overall timeout."""
    try:
        async with asyncio.timeout(timeout_seconds):
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://api.example.com/resources/{resource_id}",
                    timeout=10.0,  # Request timeout
                )
                response.raise_for_status()
                return response.json()

    except TimeoutError:
        ctx.add_error(f"Operation timed out after {timeout_seconds}s")
        return None


# --8<-- [end:async_timeout]


# --8<-- [start:streaming_operations]
async def process_items_in_batches(
    ctx: ResourceContext,
    items: list[dict],
    batch_size: int = 10,
) -> None:
    """Process items in batches to avoid overwhelming the API."""
    total = len(items)

    for i in range(0, total, batch_size):
        batch = items[i : i + batch_size]
        ctx.add_info(f"Processing batch {i // batch_size + 1} ({len(batch)} items)...")

        # Process batch concurrently
        async with httpx.AsyncClient() as client:
            tasks = [
                client.post(
                    "https://api.example.com/process",
                    json=item,
                    timeout=10.0,
                )
                for item in batch
            ]
            await asyncio.gather(*tasks)

        ctx.add_info(f"Completed batch ({i + len(batch)}/{total} items processed)")


# --8<-- [end:streaming_operations]
