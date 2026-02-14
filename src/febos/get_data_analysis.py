"""Endpoint model for retrieving data analysis rows for a device."""

from typing import ClassVar, Optional

from febos.client import FebosClient
from febos.data_model import GetDataAnalysisGetResponse
from febos.endpoint import FebosEndpoint


class GetDataAnalysisEndpoint(FebosEndpoint):
    """Endpoint for retrieving data analysis rows for a device.

    Performs a GET against the Febos API returning a list of timestamped
    measurements keyed by input codes (e.g. `R8765`, `R8766`). The endpoint
    accepts `from` and `to` query parameters to limit the time range.

    Attributes:
        installation_id: Installation id placeholder for the URL.
        device_id: Device id placeholder for the URL.
        from_ts: Optional start timestamp string for the `from` query param.
        to_ts: Optional end timestamp string for the `to` query param.
    """

    URL: ClassVar[str] = (
        "/v2/emmeti/{installation_id}/{device_id}/febos-data/get-data-analysis"
    )
    REFERER: ClassVar[str] = "/page/FBDEVLIST"

    installation_id: int
    device_id: int
    from_ts: Optional[str] = None
    to_ts: Optional[str] = None

    def get(self, client: FebosClient) -> GetDataAnalysisGetResponse:
        """Get data analysis rows for the configured time range.

        Returns:
            GetDataAnalysisGetResponse: list-like root model with entries.
        """
        params = {}
        if self.from_ts is not None:
            params["from"] = self.from_ts
        if self.to_ts is not None:
            params["to"] = self.to_ts

        response = super().get(client=client, params=params)
        return GetDataAnalysisGetResponse.model_validate(response.json())
