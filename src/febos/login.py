from typing import ClassVar

from febos.data_model import LoginPostResponse
from febos.endpoint import FebosEndpoint
from febos.error import AuthenticationError


class Login(FebosEndpoint):
    """Endpoint for user authentication.

    Authenticates a user using `username` and `password` and stores the
    returned bearer token on the provided `FebosClient` instance.

    Attributes:
        username: Username for authentication.
        password: Password for authentication.

    Usage:
        - Calls `super().post(json=self.model_dump())` to send credentials as
          a JSON body to the server.
        - Expects the server to set an `Authorization` header on success; the
          header value is stored into the client's auth token.
    """

    URL: ClassVar[str] = "/v1/auth/login"
    REFERER: ClassVar[str] = "/auth/login"

    username: str
    password: str

    def post(self) -> LoginPostResponse:
        """Authenticate user and set bearer token.
        
        Returns:
            LoginPostResponse containing user information and auth details.
            
        Raises:
            AuthenticationError: If authorization token is missing from response.
            HTTPStatusError: If HTTP request fails.
        """
        response = super().post(
            json=self.model_dump(),
        )
        token = response.headers.get("Authorization")
        if not token:
            raise AuthenticationError("Missing authorization token in response")
        self._client.set_token(token)
        return LoginPostResponse.model_validate(response.json())
