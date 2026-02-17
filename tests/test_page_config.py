import pytest
import respx
from httpx import HTTPStatusError, Response

from febos.endpoint import FebosEndpoint
from febos.page_config import PageConfigEndpoint

PAGE_CONFIG_URL = f"{FebosEndpoint.API_URL}{PageConfig.URL}"


@respx.mock
def test_page_config_get_success(client, mock_page_config_response):
    url = PAGE_CONFIG_URL.format(installation_id=100)
    route = respx.get(url).mock(
        return_value=Response(200, json=mock_page_config_response)
    )
    endpoint = PageConfigEndpoint(installation_id=100)
    response = endpoint.get(client=client)
    assert route.called
    assert response.installation.id == 100
    assert "789" in response.deviceMap
    assert respx.calls.last.request.url.params["web"] == "false"


@respx.mock
def test_page_config_get_auth_error(client):
    url = PAGE_CONFIG_URL.format(installation_id=100)
    respx.get(url).mock(return_value=Response(401))
    endpoint = PageConfigEndpoint(installation_id=100)
    with pytest.raises(HTTPStatusError):
        endpoint.get(client=client)
