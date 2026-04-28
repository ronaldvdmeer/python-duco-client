"""Exceptions for the Duco ventilation API client."""

from __future__ import annotations


class DucoError(Exception):
    """Base exception for Duco API errors."""


class DucoConnectionError(DucoError):
    """Exception raised when the Duco box is unreachable."""


class DucoAuthenticationError(DucoError):
    """Exception raised when the API key cannot be generated or is rejected."""


class DucoRateLimitError(DucoError):
    """Exception raised when the API write rate limit is exceeded.

    Attributes:
        remaining: Number of write requests remaining, or ``None`` if unknown.

    """

    def __init__(self, remaining: int | None = None) -> None:
        self.remaining = remaining
        message = "Duco API write rate limit exceeded"
        if remaining is not None:
            message += f" ({remaining} requests remaining)"
        super().__init__(message)
