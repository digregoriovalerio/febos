"""Endpoint model for accessing and submitting real-time device data.

Provides small convenience methods to `get()` and `post()` current values.
"""

from typing import ClassVar, List

from febos.client import FebosClient
from febos.data_model import RealtimeData as RealtimeDataModel
from febos.data_model import RealtimeDataGetResponse, RealtimeDataPostResponse
from febos.endpoint import FebosEndpoint


class RealtimeDataEndpoint(FebosEndpoint):
    """Endpoint for accessing and submitting real-time device data.

    Provides `get()` to fetch current sensor values for a set of input
    groups and `post()` to submit real-time measurements.

    Attributes:
        installation_id: ID of the installation.
        input_group_list: List of input group codes to query.

    Notes:
        - `get()` sends `input_group_list` as a comma-separated query
          parameter.
        - `post()` accepts a `RealtimeData` model and sends it as JSON
          in the request body.
    """

    URL: ClassVar[str] = "/v2/emmeti/{installation_id}/realtime-data"
    REFERER: ClassVar[str] = "/page/FBDEVLIST"

    installation_id: int
    input_group_list: List[str]

    def get(self, client: FebosClient) -> RealtimeDataGetResponse:
        """Get real-time data for input groups.

        Returns:
            RealtimeDataGetResponse containing sensor values and timestamps.

        Raises:
            HTTPStatusError: If HTTP request fails.
        """
        response = super().get(
            client=client, params={"input_group_list": ",".join(self.input_group_list)}
        )
        return RealtimeDataGetResponse.model_validate(response.json())

    def post(
        self, client: FebosClient, data: RealtimeDataModel
    ) -> RealtimeDataPostResponse:
        """Post real-time data for input groups.

        Args:
            data: Real-time data to post.

        Returns:
            RealtimeDataPostResponse indicating success or failure.

        Raises:
            HTTPStatusError: If HTTP request fails.
        """
        response = super().post(
            client=client,
            params={"input_group_list": ",".join(self.input_group_list)},
            json=data.model_dump(),
        )
        return RealtimeDataPostResponse.model_validate(response.json())
