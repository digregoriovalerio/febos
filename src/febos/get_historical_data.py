"""
Get Historical Data Endpoint

Retrieves timestamped historical data points for specified input groups within a date range.

Usage:
    from febos import FebosClient, GetHistoricalDataEndpoint

    client = FebosClient(token='your_token')
    endpoint = GetHistoricalDataEndpoint(
        installation_id=7593,
        input_group_list='FB-GRAPH-DATA@D9551@T31115',
        time_from='2026-02-11 00:00:00',
        time_to='2026-02-11 23:59:59'
    )

    response = endpoint.get(client=client)
    for entry in response.root:
        print(f"Device: {entry.deviceId}, Thing: {entry.thingId}")
        for point in entry.data:
            print(f"  {point.ts}: {point.vs}")
"""

from typing import ClassVar

from febos.client import FebosClient
from febos.data_model import HistoricalDataGetResponse
from febos.endpoint import FebosEndpoint


class GetHistoricalDataEndpoint(FebosEndpoint):
    """Endpoint for retrieving historical time-series data.

    Retrieves timestamped historical data points for specified input groups
    within a date range. Returns arrays of values with one entry per input code.

    Attributes:
        installation_id: Installation id placeholder for the URL.
        input_group_list: Input group codes to query (query param).
        time_from: Start time string "YYYY-MM-DD HH:MM:SS" (query param).
        time_to: End time string "YYYY-MM-DD HH:MM:SS" (query param).

    Notes:
        - Path placeholders in `URL` (e.g. `{installation_id}`)
          are filled automatically from the endpoint model's fields by the
          base class (it uses `self.model_dump()` when formatting the URL).
          Call `super().get()` directly; include query parameters with
          `params={...}` and request bodies with `json=...`.
    """

    URL: ClassVar[str] = "/v2/emmeti/{installation_id}/historical-data"
    REFERER: ClassVar[str] = "/page/FBDEVLIST"

    installation_id: int
    input_group_list: str
    time_from: str
    time_to: str

    def get(self, client: FebosClient) -> HistoricalDataGetResponse:
        """Get historical data for the configured time range.

        Returns:
            HistoricalDataGetResponse: list-like root model with entries.
        """
        params = {
            "input_group_list": self.input_group_list,
            "time_from": self.time_from,
            "time_to": self.time_to,
        }
        response = super().get(client=client, params=params)
        return HistoricalDataGetResponse.model_validate(response.json())
