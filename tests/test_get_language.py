import pytest
import respx
from httpx import Response

from febos.endpoint import FebosEndpoint
from febos.get_language import GetLanguageEndpoint

GET_LANGUAGE_URL = f"{FebosEndpoint.API_URL}{GetLanguageEndpoint.URL}"


@respx.mock
def test_get_language_get_success(client, mock_get_language_response):
    url = GET_LANGUAGE_URL.format(installation_id=100, device_id=789)
    route = respx.get(url).mock(
        return_value=Response(200, json=mock_get_language_response)
    )
    endpoint = GetLanguageEndpoint(installation_id=100, device_id=789)
    response = endpoint.get(client=client)
    assert route.called
    assert response.ID_language == mock_get_language_response["ID_language"]
    assert response.ts == mock_get_language_response["ts"]


@respx.mock
def test_get_language_get_http_error(client):
    url = GET_LANGUAGE_URL.format(installation_id=100, device_id=789)
    respx.get(url).mock(return_value=Response(401))
    endpoint = GetLanguageEndpoint(installation_id=100, device_id=789)
    with pytest.raises(Exception):
        endpoint.get(client=client)
