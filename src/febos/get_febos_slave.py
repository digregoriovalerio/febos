"""Endpoint model for retrieving Febos slave device data."""

from typing import ClassVar

from febos.client import FebosClient
from febos.data_model import GetFebosSlaveGetResponse
from febos.endpoint import FebosEndpoint


class GetFebosSlaveEndpoint(FebosEndpoint):
    """Endpoint for retrieving Febos slave device data.

    Fetches slave device information such as temperature, humidity and
    device settings for a specific `installation_id` and `device_id`.

    Attributes:
        installation_id: ID of the installation.
        device_id: ID of the device.

        Notes:
                - Path placeholders in `URL` (e.g. `{installation_id}`, `{device_id}`)
                    are filled automatically from the endpoint model's fields by the
                    base class (it uses `self.model_dump()` when formatting the URL).
                    Call `super().get()` directly; include query parameters with
                    `params={...}` and request bodies with `json=...`.
    """

    URL: ClassVar[str] = (
        "/v2/emmeti/{installation_id}/{device_id}/febos-data/get-febos-slave"
    )
    REFERER: ClassVar[str] = "/page/FBDEVLIST"

    installation_id: int
    device_id: int

    def get(self, client: FebosClient) -> GetFebosSlaveGetResponse:
        """Get Febos slave device data.

        Returns:
            GetFebosSlaveGetResponse containing slave device information.

        Raises:
            HTTPStatusError: If HTTP request fails.
        """
        response = super().get(client=client)
        return GetFebosSlaveGetResponse.model_validate(response.json())
