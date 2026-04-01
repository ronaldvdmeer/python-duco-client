# Error Handling

All exceptions inherit from `DucoError` and are exported from the top-level package.

## Exception hierarchy

```
DucoError                   — base for all library errors
  DucoConnectionError       — network unreachable / timeout
  DucoRateLimitError        — API write rate limit exceeded
```

## Importing exceptions

```python
from duco import (
    DucoError,
    DucoConnectionError,
    DucoRateLimitError,
)
```

## Basic error handling

```python
from duco import DucoClient, DucoError

try:
    board = await client.async_get_board_info()
except DucoError as err:
    print(f"Duco error: {err}")
```

## Handling specific errors

```python
from duco import DucoConnectionError, DucoRateLimitError

try:
    await client.async_set_ventilation_state(1, "MAN2")

except DucoConnectionError:
    # Box unreachable — check network / IP address
    print("Could not reach the Duco box")

except DucoRateLimitError as err:
    # Write rate limit exceeded
    print(f"Rate limit exceeded ({err.remaining} requests remaining)")
```

## Rate limiting

The Duco API enforces a write request rate limit. The current remaining count can be checked with:

```python
remaining = await client.async_get_write_req_remaining()
```

When a write request is refused due to the rate limit, `DucoRateLimitError` is raised. The `remaining` attribute contains the number of requests left, or `None` if unknown.
