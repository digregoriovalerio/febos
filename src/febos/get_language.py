"""Endpoint model for retrieving device language settings."""

from typing import ClassVar

from febos.client import FebosClient
from febos.data_model import GetLanguageGetResponse
from febos.endpoint import FebosEndpoint


class GetLanguageEndpoint(FebosEndpoint):
    """Endpoint for retrieving device language.

    Performs a GET against the Febos API to retrieve the current language
    setting for a given installation/device. The response typically contains
    a timestamp and an `ID_language` value.

    Attributes:
        installation_id: ID of the installation.
        device_id: ID of the device.
    """

    URL: ClassVar[str] = (
        "/v2/emmeti/{installation_id}/{device_id}/febos-data/get-language"
    )
    REFERER: ClassVar[str] = "/page/FBDEVLIST"

    installation_id: int
    device_id: int

    def get(self, client: FebosClient) -> GetLanguageGetResponse:
        """Get language information for the device.

        Returns:
            GetLanguageGetResponse with `ts` and `ID_language` fields.
        """
        response = super().get(client=client)
        return GetLanguageGetResponse.model_validate(response.json())
