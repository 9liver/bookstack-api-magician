"""BookStack API Magician - A comprehensive Python client for BookStack API."""

from .client import BookStackClient
from .exceptions import (
    BookStackAPIError,
    AuthenticationError,
    ResourceNotFoundError,
    ValidationError,
)

__version__ = "1.0.0"
__all__ = [
    "BookStackClient",
    "BookStackAPIError",
    "AuthenticationError",
    "ResourceNotFoundError",
    "ValidationError",
]
