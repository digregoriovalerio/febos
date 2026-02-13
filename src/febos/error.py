"""Custom exceptions used by the Febos client."""

from typing import Optional


class FebosError(Exception):
    """Base exception for Febos API errors."""


class AuthenticationError(FebosError):
    """Raised when authentication fails.

    Attributes:
        message: Description of the authentication error.
    """

    def __init__(self, message: Optional[str] = None) -> None:
        """Initialize AuthenticationError.

        Args:
            message: Optional error message.
        """
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        """Return string representation of error."""
        return self.message or "Authentication failed"
