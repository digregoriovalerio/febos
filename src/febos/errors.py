"""Febos API exceptions."""


class FebosError(Exception):
    """Generic Febos API error."""

    def __init__(self, context):
        self.context = context

class AuthenticationError(FebosError):
    """Authentication error."""

class ApiError(FebosError):
    """Generic API error."""
