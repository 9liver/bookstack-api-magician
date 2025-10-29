"""Custom exceptions for BookStack API."""


class BookStackAPIError(Exception):
    """Base exception for BookStack API errors."""

    def __init__(self, message, status_code=None, response=None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class AuthenticationError(BookStackAPIError):
    """Exception raised for authentication errors."""
    pass


class ResourceNotFoundError(BookStackAPIError):
    """Exception raised when a resource is not found."""
    pass


class ValidationError(BookStackAPIError):
    """Exception raised for validation errors."""
    pass


class PermissionError(BookStackAPIError):
    """Exception raised for permission errors."""
    pass


class RateLimitError(BookStackAPIError):
    """Exception raised when API rate limit is exceeded."""
    pass
