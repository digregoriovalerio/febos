"""Endpoint model for listing installations available to the user."""

from typing import ClassVar

from febos.client import FebosClient
from febos.data_model import InstallationGetResponse
from febos.endpoint import FebosEndpoint


class InstallationEndpoint(FebosEndpoint):
    """Endpoint for retrieving the installation list.

    Fetches available installations for the authenticated user. The
    endpoint model contains pagination fields which are included as query
    parameters when calling `get()` (the model is serialized via
    `self.model_dump()` and forwarded as `params`).

    Attributes:
        pageStart: Starting page number (default: 1).
        pageItems: Number of items per page (default: 500000).
    """

    URL: ClassVar[str] = "/v1/installation"
    REFERER: ClassVar[str] = "/auth/installation-list"

    pageStart: int = 1
    pageItems: int = 500000

    def get(self, client: FebosClient) -> InstallationGetResponse:
        """Get list of installations.

        Returns:
            InstallationGetResponse containing list of installations.

        Raises:
            HTTPStatusError: If HTTP request fails.
        """
        response = super().get(client=client, params=self.model_dump())
        return InstallationGetResponse.model_validate(response.json())
