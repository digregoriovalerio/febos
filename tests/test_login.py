import pytest
import respx
from httpx import HTTPStatusError, Response

from febos.endpoint import FebosEndpoint
from febos.error import AuthenticationError
from febos.login import LoginEndpoint, LoginPostResponse

LOGIN_URL = f"{FebosEndpoint.API_URL}{LoginEndpoint.URL}"


@respx.mock
def test_login_post_success(client, mock_login_response):
    auth_token = "fake-token"
    route = respx.post(LOGIN_URL).mock(
        return_value=Response(
            200, json=mock_login_response, headers={"Authorization": auth_token}
        )
    )
    endpoint = LoginEndpoint(username="testuser", password="password123")
    response = endpoint.post(client=client)
    assert route.called
    assert isinstance(response, LoginPostResponse)
    assert client.get_token() == auth_token
    assert response.username == "testuser"


@respx.mock
def test_login_post_missing_token(client, mock_login_response):
    respx.post(LOGIN_URL).mock(return_value=Response(200, json=mock_login_response))
    endpoint = LoginEndpoint(username="user", password="pass")
    with pytest.raises(
        AuthenticationError, match="Missing authorization token in response"
    ):
        endpoint.post(client=client)


@respx.mock
def test_login_post_http_error(client):
    respx.post(LOGIN_URL).mock(return_value=Response(401))
    endpoint = LoginEndpoint(username="wrong", password="wrong")
    with pytest.raises(HTTPStatusError):
        endpoint.post(client=client)
