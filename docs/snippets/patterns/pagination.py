"""
Pagination pattern examples.

This snippet demonstrates common pagination patterns:
- Offset-based pagination
- Cursor-based pagination
- Page-based pagination
- Fetching all pages

Used in: guides showing how to handle paginated API responses.
"""

import httpx

from pyvider.resources.context import ResourceContext


# --8<-- [start:offset_pagination]
async def fetch_all_offset_pagination(
    ctx: ResourceContext,
    base_url: str,
    limit: int = 100,
) -> list[dict]:
    """Fetch all items using offset-based pagination."""
    all_items = []
    offset = 0

    async with httpx.AsyncClient() as client:
        while True:
            # Fetch page
            response = await client.get(
                base_url,
                params={"limit": limit, "offset": offset},
                timeout=10.0,
            )
            response.raise_for_status()

            data = response.json()
            items = data.get("items", [])

            if not items:
                # No more items
                break

            all_items.extend(items)
            ctx.add_info(f"Fetched {len(items)} items (total: {len(all_items)})")

            # Check if there are more pages
            total = data.get("total")
            if total and len(all_items) >= total:
                break

            offset += limit

    return all_items


# --8<-- [end:offset_pagination]


# --8<-- [start:cursor_pagination]
async def fetch_all_cursor_pagination(
    ctx: ResourceContext,
    base_url: str,
    page_size: int = 100,
) -> list[dict]:
    """Fetch all items using cursor-based pagination."""
    all_items = []
    cursor = None

    async with httpx.AsyncClient() as client:
        while True:
            # Build params
            params = {"page_size": page_size}
            if cursor:
                params["cursor"] = cursor

            # Fetch page
            response = await client.get(
                base_url,
                params=params,
                timeout=10.0,
            )
            response.raise_for_status()

            data = response.json()
            items = data.get("items", [])

            if not items:
                break

            all_items.extend(items)
            ctx.add_info(f"Fetched {len(items)} items (total: {len(all_items)})")

            # Get next cursor
            cursor = data.get("next_cursor")
            if not cursor:
                # No more pages
                break

    return all_items


# --8<-- [end:cursor_pagination]


# --8<-- [start:page_pagination]
async def fetch_all_page_pagination(
    ctx: ResourceContext,
    base_url: str,
    per_page: int = 100,
) -> list[dict]:
    """Fetch all items using page-based pagination."""
    all_items = []
    page = 1

    async with httpx.AsyncClient() as client:
        while True:
            # Fetch page
            response = await client.get(
                base_url,
                params={"page": page, "per_page": per_page},
                timeout=10.0,
            )
            response.raise_for_status()

            data = response.json()
            items = data.get("items", [])

            if not items:
                break

            all_items.extend(items)
            ctx.add_info(f"Fetched page {page} ({len(items)} items)")

            # Check if there are more pages
            total_pages = data.get("total_pages")
            if total_pages and page >= total_pages:
                break

            # Or check if this was the last page
            has_next = data.get("has_next", False)
            if not has_next:
                break

            page += 1

    return all_items


# --8<-- [end:page_pagination]


# --8<-- [start:link_header_pagination]
async def fetch_all_link_header_pagination(
    ctx: ResourceContext,
    base_url: str,
) -> list[dict]:
    """Fetch all items using Link header pagination (GitHub style)."""
    all_items = []
    url = base_url

    async with httpx.AsyncClient() as client:
        while url:
            # Fetch page
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()

            items = response.json()
            if not items:
                break

            all_items.extend(items)
            ctx.add_info(f"Fetched {len(items)} items (total: {len(all_items)})")

            # Parse Link header for next URL
            url = None
            link_header = response.headers.get("Link")
            if link_header:
                # Parse: <https://api.example.com/items?page=2>; rel="next"
                for link in link_header.split(","):
                    if 'rel="next"' in link:
                        url = link.split(";")[0].strip("<>")
                        break

    return all_items


# --8<-- [end:link_header_pagination]


# --8<-- [start:data_source_pagination]
import attrs

from pyvider.data_sources import BaseDataSource


@attrs.define
class ItemsConfig:
    """Configuration for items data source."""

    filter: str | None = None
    limit: int | None = None


@attrs.define
class ItemsData:
    """Items data returned to Terraform."""

    id: str
    items: list[dict]
    total_count: int


class ItemsDataSource(BaseDataSource):
    """Example data source that handles pagination internally."""

    config_class = ItemsConfig
    state_class = ItemsData

    async def read(self, ctx: ResourceContext) -> ItemsData | None:
        """Read all items, handling pagination automatically."""
        if not ctx.config:
            return None

        # Fetch all items using pagination
        all_items = await fetch_all_cursor_pagination(
            ctx,
            "https://api.example.com/items",
            page_size=100,
        )

        # Apply filtering if requested
        if ctx.config.filter:
            all_items = [item for item in all_items if self._matches_filter(item, ctx.config.filter)]

        # Apply limit if requested
        if ctx.config.limit:
            all_items = all_items[: ctx.config.limit]

        return ItemsData(
            id="items",
            items=all_items,
            total_count=len(all_items),
        )

    def _matches_filter(self, item: dict, filter_expr: str) -> bool:
        """Check if item matches filter (example)."""
        return True  # Implement actual filtering logic


# --8<-- [end:data_source_pagination]
