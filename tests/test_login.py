import pytest
import respx
from httpx import HTTPStatusError, Response

from febos.endpoint import FebosEndpoint
from febos.error import AuthenticationError
from febos.login import Login, LoginPostResponse

LOGIN_URL = f"{FebosEndpoint.API_URL}{Login.URL}"


@respx.mock
def test_login_post_success(client, mock_login_response):
    auth_token = "fake-token"
    route = respx.post(LOGIN_URL).mock(
        return_value=Response(
            200, json=mock_login_response, headers={"Authorization": auth_token}
        )
    )
    endpoint = Login(client=client, username="testuser", password="password123")
    response = endpoint.post()
    assert route.called
    assert isinstance(response, LoginPostResponse)
    assert endpoint._client.auth.token == auth_token
    assert response.username == "testuser"


@respx.mock
def test_login_post_missing_token(client, mock_login_response):
    respx.post(LOGIN_URL).mock(return_value=Response(200, json=mock_login_response))
    endpoint = Login(client=client, username="user", password="pass")
    with pytest.raises(
        AuthenticationError, match="Missing authorization token in response"
    ):
        endpoint.post()


@respx.mock
def test_login_post_http_error(client):
    respx.post(LOGIN_URL).mock(return_value=Response(401))
    endpoint = Login(client=client, username="wrong", password="wrong")
    with pytest.raises(HTTPStatusError):
        endpoint.post()
