# How to Handle Pagination

Handle paginated API responses in data sources to fetch large result sets efficiently.

---

## Basic Pagination Pattern

```python
import attrs
import httpx
from pyvider.data_sources import register_data_source, BaseDataSource
from pyvider.schema import s_data_source, a_str, a_num, a_list, PvsSchema

@attrs.define
class PaginatedQueryConfig:
    endpoint: str
    limit: int = 100  # Max results to fetch

@attrs.define
class PaginatedQueryData:
    id: str
    items: list[dict]
    total_fetched: int
    has_more: bool

@register_data_source("paginated_query")
class PaginatedQuery(BaseDataSource):
    config_class = PaginatedQueryConfig
    state_class = PaginatedQueryData

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_data_source({
            "endpoint": a_str(required=True),
            "limit": a_num(default=100),
            "id": a_str(computed=True),
            "items": a_list(a_map(a_str()), computed=True),
            "total_fetched": a_num(computed=True),
            "has_more": a_bool(computed=True),
        })

    async def read(self, config: PaginatedQueryConfig) -> PaginatedQueryData:
        all_items = []
        page = 1
        has_more = True

        async with httpx.AsyncClient() as client:
            while has_more and len(all_items) < config.limit:
                response = await client.get(
                    f"https://api.example.com{config.endpoint}",
                    params={"page": page, "per_page": 100}
                )
                data = response.json()

                all_items.extend(data["items"])
                has_more = data.get("has_more", False)
                page += 1

                # Stop if we have enough
                if len(all_items) >= config.limit:
                    break

        return PaginatedQueryData(
            id=f"{config.endpoint}:{config.limit}",
            items=all_items[:config.limit],
            total_fetched=len(all_items[:config.limit]),
            has_more=has_more,
        )
```

---

## Token-Based Pagination

Many APIs use cursor/token-based pagination:

```python
async def read(self, config: Config) -> Data:
    all_items = []
    next_token = None

    async with httpx.AsyncClient() as client:
        while len(all_items) < config.limit:
            params = {"limit": min(100, config.limit - len(all_items))}
            if next_token:
                params["next_token"] = next_token

            response = await client.get(
                f"https://api.example.com{config.endpoint}",
                params=params
            )
            data = response.json()

            all_items.extend(data["items"])
            next_token = data.get("next_token")

            # No more pages
            if not next_token:
                break

    return Data(
        id=f"{config.endpoint}:{config.limit}",
        items=all_items,
        total_fetched=len(all_items),
    )
```

---

## Offset-Based Pagination

Traditional offset/limit pagination:

```python
async def read(self, config: Config) -> Data:
    all_items = []
    offset = 0
    page_size = 100

    async with httpx.AsyncClient() as client:
        while len(all_items) < config.limit:
            fetch_size = min(page_size, config.limit - len(all_items))

            response = await client.get(
                f"https://api.example.com{config.endpoint}",
                params={"offset": offset, "limit": fetch_size}
            )
            data = response.json()

            items = data.get("items", [])
            if not items:
                break  # No more results

            all_items.extend(items)
            offset += len(items)

            # Got fewer than requested = last page
            if len(items) < fetch_size:
                break

    return Data(
        id=f"{config.endpoint}:{config.limit}",
        items=all_items,
        total_fetched=len(all_items),
    )
```

---

## Link Header Pagination

Some APIs use HTTP Link headers (like GitHub):

```python
import httpx
from urllib.parse import parse_qs, urlparse

async def read(self, config: Config) -> Data:
    all_items = []
    url = f"https://api.example.com{config.endpoint}"

    async with httpx.AsyncClient() as client:
        while url and len(all_items) < config.limit:
            response = await client.get(url, params={"per_page": 100})
            data = response.json()

            all_items.extend(data)

            # Parse Link header for next page
            link_header = response.headers.get("Link", "")
            url = None
            for link in link_header.split(","):
                if 'rel="next"' in link:
                    url = link.split(";")[0].strip("<> ")
                    break

            if len(all_items) >= config.limit:
                break

    return Data(
        id=f"{config.endpoint}:{config.limit}",
        items=all_items[:config.limit],
        total_fetched=len(all_items[:config.limit]),
    )
```

---

## Parallel Pagination

Fetch multiple pages concurrently (be careful with rate limits):

```python
import asyncio

async def read(self, config: Config) -> Data:
    # Determine total pages needed
    pages_needed = (config.limit + 99) // 100  # Round up

    async with httpx.AsyncClient() as client:
        # Create tasks for each page
        tasks = [
            self._fetch_page(client, config.endpoint, page)
            for page in range(1, pages_needed + 1)
        ]

        # Fetch all pages concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Combine results
        all_items = []
        for result in results:
            if isinstance(result, Exception):
                continue  # Skip failed pages
            all_items.extend(result)

    return Data(
        id=f"{config.endpoint}:{config.limit}",
        items=all_items[:config.limit],
        total_fetched=len(all_items[:config.limit]),
    )

async def _fetch_page(
    self,
    client: httpx.AsyncClient,
    endpoint: str,
    page: int
) -> list[dict]:
    """Fetch a single page."""
    response = await client.get(
        f"https://api.example.com{endpoint}",
        params={"page": page, "per_page": 100}
    )
    data = response.json()
    return data.get("items", [])
```

---

## Rate Limiting

Handle API rate limits during pagination:

```python
import asyncio
from datetime import datetime, timedelta

class RateLimitedQuery(BaseDataSource):
    def __init__(self):
        super().__init__()
        self._last_request = None
        self._min_interval = timedelta(milliseconds=100)  # 10 req/sec

    async def _wait_for_rate_limit(self):
        """Ensure we don't exceed rate limit."""
        if self._last_request:
            elapsed = datetime.now() - self._last_request
            if elapsed < self._min_interval:
                wait_time = (self._min_interval - elapsed).total_seconds()
                await asyncio.sleep(wait_time)
        self._last_request = datetime.now()

    async def read(self, config: Config) -> Data:
        all_items = []
        page = 1

        async with httpx.AsyncClient() as client:
            while len(all_items) < config.limit:
                # Respect rate limit
                await self._wait_for_rate_limit()

                response = await client.get(
                    f"https://api.example.com{config.endpoint}",
                    params={"page": page, "per_page": 100}
                )

                # Handle 429 Too Many Requests
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", "60"))
                    await asyncio.sleep(retry_after)
                    continue  # Retry same page

                data = response.json()
                all_items.extend(data["items"])

                if not data.get("has_more"):
                    break

                page += 1

        return Data(
            id=f"{config.endpoint}:{config.limit}",
            items=all_items[:config.limit],
        )
```

---

## Error Handling

Handle pagination errors gracefully:

```python
async def read(self, config: Config) -> Data:
    all_items = []
    page = 1
    errors = []

    async with httpx.AsyncClient() as client:
        while page <= 10 and len(all_items) < config.limit:  # Max 10 pages
            try:
                response = await client.get(
                    f"https://api.example.com{config.endpoint}",
                    params={"page": page, "per_page": 100},
                    timeout=30.0  # Add timeout
                )
                response.raise_for_status()

                data = response.json()
                all_items.extend(data.get("items", []))

                if not data.get("has_more"):
                    break

                page += 1

            except httpx.HTTPError as e:
                errors.append(f"Page {page} failed: {e}")
                # Continue to next page instead of failing completely
                page += 1
                continue

            except Exception as e:
                errors.append(f"Unexpected error on page {page}: {e}")
                break  # Stop on unexpected errors

    return Data(
        id=f"{config.endpoint}:{config.limit}",
        items=all_items[:config.limit],
        total_fetched=len(all_items),
        errors=errors if errors else None,
    )
```

---

## Best Practices

### 1. Set Maximum Pages

Prevent infinite loops:

```python
async def read(self, config: Config) -> Data:
    max_pages = 100  # Safety limit
    page = 0

    while page < max_pages and len(all_items) < config.limit:
        # Fetch page
        page += 1
```

### 2. Respect User Limits

Don't fetch more than requested:

```python
while len(all_items) < config.limit:
    # Fetch only what's needed
    fetch_size = min(100, config.limit - len(all_items))
    ...
```

### 3. Return Partial Results

Don't fail if some pages error:

```python
async def read(self, config: Config) -> Data:
    all_items = []
    try:
        # Fetch pages
        ...
    except Exception as e:
        # Return what we got
        return Data(
            items=all_items,
            error=f"Partial results due to: {e}"
        )
```

### 4. Cache Expensive Queries

```python
from functools import lru_cache

@lru_cache(maxsize=32)
async def read(self, config: Config) -> Data:
    # Pagination results cached by config
    ...
```

### 5. Add Progress Logging

```python
import logging

async def read(self, config: Config) -> Data:
    logger = logging.getLogger(__name__)
    page = 1

    while ...:
        logger.info(f"Fetching page {page}, got {len(all_items)} items so far")
        page += 1
```

---

## See Also

- [Create a Data Source](create-data-source.md) - Data source basics
- [Building Your First Data Source](../../tutorials/building-your-first-data-source.md) - Tutorial
- [Data Source API Reference](../../reference/data-source-api.md) - Complete API
- [Testing Data Sources](../../guides/development/testing-providers.md) - Testing strategies
