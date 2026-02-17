"""HTTP client helpers for Febos.

This module provides `FebosClient`, a thin wrapper around `httpx.Client`,
and related utilities such as `BearerAuth` and request/response logging
helpers used by the package.
"""

import logging
import os
from typing import Generator, Optional

from httpx import Auth, Client, Request, Response, Timeout

LOGGER = logging.getLogger(__name__)


def log_request(request: Request) -> None:
    """Log HTTP request details.

    Args:
        request: The HTTP request object to log.
    """
    try:
        content = request.read().decode()
        LOGGER.debug(
            f"Request: {request.method} {request.url}\nHeaders: {dict(request.headers)}\nContent: {content}"
        )
    except Exception as e:
        LOGGER.error(f"Error logging request: {e}")


def log_response(response: Response) -> None:
    """Log HTTP response details.

    Args:
        response: The HTTP response object to log.
    """
    try:
        request = response.request
        content = response.read().decode()
        LOGGER.debug(
            f"Response: {response.status_code} {request.url}\nHeaders: {dict(request.headers)}\nContent: {content}"
        )
    except Exception as e:
        LOGGER.error(f"Error logging response: {e}")


class BearerAuth(Auth):
    """Bearer token authentication for HTTP requests.

    Attributes:
        token: Optional bearer token to include in Authorization header.
    """

    def __init__(self, token: Optional[str] = None) -> None:
        """Initialize BearerAuth.

        Args:
            token: Optional bearer token string.
        """
        self.token = token

    def auth_flow(self, request: Request) -> Generator[Request, Response, None]:
        """Apply bearer token to request.

        Args:
            request: The HTTP request to authenticate.

        Yields:
            The modified request with Authorization header if token is set.
        """
        if self.token:
            request.headers["Authorization"] = f"Bearer {self.token}"
        yield request


class FebosClient(Client):
    """HTTP client for EmmeTI Febos API.

    Extends httpx.Client with bearer token authentication and request/response logging.
    """

    def __init__(
        self,
        *args,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
        **kwargs,
    ) -> None:
        """Initialize FebosClient.

        Args:
            base_url: Base URL for API requests. Defaults to FEBOS_BASE_URL env var or EmmeTI production server.
            timeout: Request timeout in seconds. Defaults to 30.0.
            *args: Additional positional arguments passed to httpx.Client.
            **kwargs: Additional keyword arguments passed to httpx.Client.
        """
        if base_url is None:
            base_url = os.getenv("FEBOS_BASE_URL", "https://emmeti.aq-iot.net")

        super().__init__(
            *args,
            base_url=base_url,
            timeout=Timeout(timeout),
            headers={
                "Accept": "application/json, text/plain, */*",
            },
            **kwargs,
        )
        # Only add logging hooks if not already present to prevent duplicates
        if log_request not in self.event_hooks["request"]:
            self.event_hooks["request"].append(log_request)
        if log_response not in self.event_hooks["response"]:
            self.event_hooks["response"].append(log_response)

    def get_token(self) -> Optional[str]:
        """Get the bearer token for authentication.

        Returns:
            The bearer token to use for subsequent requests. None if not yet authenticated.
        """
        return getattr(self.auth, "token", None) if self.auth else None

    def set_token(self, token: str) -> None:
        """Set or update the bearer token for authentication.

        Args:
            token: The bearer token to use for subsequent requests.
        """
        self.auth = BearerAuth(token)
