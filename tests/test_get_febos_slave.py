import pytest
import respx
from httpx import HTTPStatusError, Response

from febos.endpoint import FebosEndpoint
from febos.get_febos_slave import GetFebosSlave

GET_FEBOS_SLAVE_URL = f"{FebosEndpoint.API_URL}{GetFebosSlave.URL}"


@respx.mock
def test_get_febos_slave_get_success(client, mock_slave_response):
    url = GET_FEBOS_SLAVE_URL.format(installation_id=100, device_id=200)
    route = respx.get(url).mock(return_value=Response(200, json=mock_slave_response))
    endpoint = GetFebosSlave(client=client, installation_id=100, device_id=200)
    response = endpoint.get()
    assert route.called
    assert response.root[0].nomeSlave == "Living"


@respx.mock
def test_get_febos_slave_get_http_error(client):
    url = GET_FEBOS_SLAVE_URL.format(installation_id=100, device_id=200)
    respx.get(url).mock(return_value=Response(401))
    endpoint = GetFebosSlave(client=client, installation_id=100, device_id=200)
    with pytest.raises(HTTPStatusError):
        endpoint.get()
