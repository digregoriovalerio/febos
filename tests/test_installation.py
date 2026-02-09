import pytest
import respx
from httpx import HTTPStatusError, Response
from pydantic import ValidationError

from febos.endpoint import FebosEndpoint
from febos.installation import Installation, InstallationGetResponse

INSTALLATION_URL = f"{FebosEndpoint.API_URL}{Installation.URL}"


@respx.mock
def test_installation_get_success(client, mock_installation_response):
    route = respx.get(INSTALLATION_URL).mock(
        return_value=Response(200, json=mock_installation_response)
    )
    endpoint = Installation(client=client, pageStart=1, pageItems=10)
    response = endpoint.get()
    request = route.calls.last.request
    assert route.called
    assert isinstance(response, InstallationGetResponse)
    assert len(response.root) == 1
    assert len(response.root[0].finalUserName) == 1
    assert response.root[0].finalUserName[0] == "testuser"
    assert "pageStart" in request.url.params
    assert request.url.params["pageStart"] == "1"
    assert "pageItems" in request.url.params
    assert request.url.params["pageItems"] == "10"


@respx.mock
def test_installation_get_invalid_json(client):
    respx.get(INSTALLATION_URL).mock(
        return_value=Response(200, json=[{"error": "invalid data"}])
    )
    endpoint = Installation(client=client, pageStart=1, pageItems=10)
    with pytest.raises(ValidationError):
        endpoint.get()


@respx.mock
def test_installation_get_http_error(client):
    respx.get(INSTALLATION_URL).mock(return_value=Response(500))
    endpoint = Installation(client=client, pageStart=1, pageItems=10)
    with pytest.raises(HTTPStatusError):
        endpoint.get()
