import pytest
import respx
from httpx import Response

from febos.endpoint import FebosEndpoint
from febos.get_data_analysis import GetDataAnalysisEndpoint

GET_DATA_ANALYSIS_URL = f"{FebosEndpoint.API_URL}{GetDataAnalysisEndpoint.URL}"


@respx.mock
def test_get_data_analysis_success(client, mock_get_data_analysis_response):
    url = GET_DATA_ANALYSIS_URL.format(installation_id=7593, device_id=9551)
    route = respx.get(url).mock(
        return_value=Response(200, json=mock_get_data_analysis_response)
    )
    endpoint = GetDataAnalysisEndpoint(
        installation_id=7593,
        device_id=9551,
        from_ts="2026-02-11 00:00:00",
        to_ts="2026-02-11 23:59:00",
    )
    response = endpoint.get(client=client)
    assert route.called
    assert len(response.root) == len(mock_get_data_analysis_response)
    assert response.root[0].ts == mock_get_data_analysis_response[0]["ts"]


@respx.mock
def test_get_data_analysis_http_error(client):
    url = GET_DATA_ANALYSIS_URL.format(installation_id=7593, device_id=9551)
    respx.get(url).mock(return_value=Response(401))
    endpoint = GetDataAnalysisEndpoint(installation_id=7593, device_id=9551)
    with pytest.raises(Exception):
        endpoint.get(client=client)
