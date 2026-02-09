from abc import ABC
from typing import Any, ClassVar, Dict, Optional

from httpx import Response
from pydantic import BaseModel, PrivateAttr

from febos.client import FebosClient


class FebosEndpoint(ABC, BaseModel):
    """Base class for EmmeTI Febos API endpoints.

    Provides common HTTP request functionality with automatic error handling
    and proper header configuration. Subclasses declare `URL` and `REFERER`
    as `ClassVar[str]` values. Endpoint instances are Pydantic models holding
    any request-specific fields (e.g. `installation_id`, `device_id`).

    Class Attributes:
        APP_URL: Base URL path for the application.
        API_URL: Base URL path for the API.
        URL: Endpoint-specific URL path (must be set by subclasses).
        REFERER: Endpoint-specific referer header (must be set by subclasses).

    Notes:
        - `get()` and `post()` convenience methods call `_call()` which
          forwards keyword arguments directly to the underlying httpx client.
                - Path placeholders in `URL` are formatted using the endpoint model
                    values (via `self.model_dump()`). For example, if the model has
                    `installation_id` and `device_id` fields they will be used to fill
                    `{installation_id}`/`{device_id}` in the `URL` automatically when
                    calling `get()` or `post()`.
        - To send a JSON body call `super().post(json=...)`.
        - To include query parameters pass `params={...}` to `get()`/`post()`.
    """
    
    APP_URL: ClassVar[str] = "/aq-iot-app-emmeti"
    API_URL: ClassVar[str] = "/aq-iot-server-frontend-ha/api"
    URL: ClassVar[str]  # Must be overridden in subclasses
    REFERER: ClassVar[str]  # Must be overridden in subclasses

    _client: FebosClient = PrivateAttr()

    def __init__(self, client: FebosClient, **kwargs: Any) -> None:
        """Initialize endpoint with HTTP client.
        
        Args:
            client: FebosClient instance for making HTTP requests.
            **kwargs: Additional model fields.
        """
        super().__init__(**kwargs)
        self._client = client

    def _call(
        self,
        headers: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Response:
        """Make HTTP request to the endpoint.
        
        Args:
            method: HTTP method (GET, POST, etc.).
            headers: Optional additional headers.
            params: Optional query parameters.
            **kwargs: URL format parameters.
            
        Returns:
            HTTP response object.
            
        Raises:
            HTTPStatusError: If response status indicates an error.
        """
        if headers is None:
            headers = {}

        response = self._client.request(
            url=f"{FebosEndpoint.API_URL}{self.URL}".format(**self.model_dump()),
            headers={"Referer": str(self._client.base_url) + self.APP_URL + self.REFERER} | headers,
            **kwargs
        )

        response.raise_for_status()
        return response

    def get(self, *args, **kwargs) -> Response:
        """Make GET request to endpoint.
        
        Returns:
            HTTP response object.
        """
        return self._call(method="GET", *args, **kwargs)

    def post(self, *args, headers: Optional[Dict[str, Any]] = None, **kwargs) -> Response:
        """Make POST request to endpoint.
        
        Args:
            headers: Optional additional headers.
            **kwargs: URL format and body parameters.
            
        Returns:
            HTTP response object.
        """
        if headers is None:
            headers = {}
        headers = {"Content-Type": "application/json"} | headers
        return self._call(method="POST", *args, headers=headers, **kwargs)
