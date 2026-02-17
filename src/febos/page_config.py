"""Endpoint model for fetching page and device configuration."""

from typing import ClassVar

from febos.client import FebosClient
from febos.data_model import PageConfigGetResponse
from febos.endpoint import FebosEndpoint


class PageConfigEndpoint(FebosEndpoint):
    """Endpoint for retrieving page and device configuration.

    Fetches pages, devices and input groups for a particular installation.

    Attributes:
        installation_id: ID of the installation to get configuration for.

        Notes:
                - Path placeholders in `URL` (e.g. `{installation_id}`) are filled
                    automatically from the endpoint model's fields (via
                    `self.model_dump()`). Call `super().get(params={...})` to include
                    query parameters.
                - This endpoint sets `web=false` by default when requesting data.
    """

    URL: ClassVar[str] = "/v1/installation/{installation_id}/page-config"
    REFERER: ClassVar[str] = "/page/FBDEVLIST"

    installation_id: int

    def get(self, client: FebosClient) -> PageConfigGetResponse:
        """Get page configuration for installation.

        Returns:
            PageConfigGetResponse containing pages, devices, and input groups.

        Raises:
            HTTPStatusError: If HTTP request fails.
        """
        response = super().get(client=client, params={"web": "false"})
        return PageConfigGetResponse.model_validate(response.json())
