import pytest
import respx
from httpx import HTTPStatusError, Response

from febos.endpoint import FebosEndpoint
from febos.realtime_data import RealtimeDataEndpoint

REALTIME_DATA_URL = f"{FebosEndpoint.API_URL}{RealtimeDataEndpoint.URL}"


@respx.mock
def test_realtime_data_get_success(client, mock_realtime_data_response):
    url = REALTIME_DATA_URL.format(installation_id=100)
    route = respx.get(url).mock(
        return_value=Response(200, json=mock_realtime_data_response)
    )
    endpoint = RealtimeDataEndpoint(installation_id=100, input_group_list=["GR1", "GR2"])
    response = endpoint.get(client=client)
    assert route.called
    assert len(response.root) > 0
    assert "temp" in response.root[0].data
    assert response.root[0].data["temp"].i == 22.5


@respx.mock
def test_realtime_data_get_auth_error(client):
    url = REALTIME_DATA_URL.format(installation_id=100)
    respx.get(url).mock(return_value=Response(401))
    endpoint = RealtimeDataEndpoint(installation_id=100, input_group_list=["GR1", "GR2"])
    with pytest.raises(HTTPStatusError):
        endpoint.get(client=client)
