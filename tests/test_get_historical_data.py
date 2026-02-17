import pytest
import respx
from httpx import Response

from febos.endpoint import FebosEndpoint
from febos.get_historical_data import GetHistoricalDataEndpoint

GET_HISTORICAL_DATA_URL = f"{FebosEndpoint.API_URL}{GetHistoricalDataEndpoint.URL}"


@respx.mock
def test_get_historical_data_success(client, mock_get_historical_data_response):
    url = GET_HISTORICAL_DATA_URL.format(installation_id=7593)
    route = respx.get(url).mock(
        return_value=Response(200, json=mock_get_historical_data_response)
    )
    endpoint = GetHistoricalDataEndpoint(
        installation_id=7593,
        input_group_list="FB-GRAPH-DATA@D9551@T31115",
        time_from="2026-02-11 00:00:00",
        time_to="2026-02-11 23:59:59",
    )
    response = endpoint.get(client=client)
    assert route.called
    assert len(response.root) == len(mock_get_historical_data_response)
    assert response.root[0].deviceId == mock_get_historical_data_response[0]["deviceId"]
    assert response.root[0].thingId == mock_get_historical_data_response[0]["thingId"]
    assert len(response.root[0].data) == len(
        mock_get_historical_data_response[0]["data"]
    )


@respx.mock
def test_get_historical_data_http_error(client):
    url = GET_HISTORICAL_DATA_URL.format(installation_id=7593)
    respx.get(url).mock(return_value=Response(401))
    endpoint = GetHistoricalDataEndpoint(
        installation_id=7593,
        input_group_list="FB-GRAPH-DATA@D9551@T31115",
        time_from="2026-02-11 00:00:00",
        time_to="2026-02-11 23:59:59",
    )
    with pytest.raises(Exception):
        endpoint.get(client=client)
