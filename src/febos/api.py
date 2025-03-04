from requests import Session
from requests.auth import AuthBase

from .errors import ApiError, AuthenticationError


class BearerAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


class FebosApi(Session):
    BASE_URL = f"https://emmeti.aq-iot.net"
    APP_URL = f"{BASE_URL}/aq-iot-app-emmeti"
    API_URL = f"{BASE_URL}/aq-iot-server-frontend-ha/api"

    def __init__(self, username, password):
        super().__init__()
        self.auth = None
        self.login_data = None
        self.username = username
        self.password = password

    def _handle_error(self, response):
        if response.status_code == 401:
            raise AuthenticationError(response)
        elif response.status_code != 200:
            raise ApiError(response)

    def login(self):
        self.login_data = None
        response = self.post(
            url=f"{self.API_URL}/v1/auth/login",
            headers={
                "Accept": "application/json, text/plain, */*",
                "Content-Type": "application/json",
                "Referer": f"{self.APP_URL}/auth/login",
            },
            json={"username": self.username, "password": self.password},
        )
        if not response or response.status_code != 200:
            raise self._handle_error(response)
        self.auth = BearerAuth(response.headers.get("authorization"))
        self.login_data = response.json()
        return self.login_data

    def installation(self, pageStart=1, pageItems=500000):
        response = self.get(
            url=f"{self.API_URL}/v1/installation?pageStart={pageStart}&pageItems={pageItems}",
            headers={
                "Accept": "application/json, text/plain, */*",
                "Referer": f"{self.APP_URL}/auth/installation-list",
            },
        )
        if not response or response.status_code != 200:
            raise self._handle_error(response)
        return response.json()

    def page_config(self, installation_id):
        response = self.get(
            url=f"{self.API_URL}/v1/installation/{installation_id}/page-config?web=false",
            headers={
                "Accept": "application/json, text/plain, */*",
                "Referer": f"{self.APP_URL}/page/FBDEVLIST",
            },
        )
        if not response or response.status_code != 200:
            raise self._handle_error(response)
        return response.json()

    def get_febos_slave(self, installation_id, device_id):
        response = self.get(
            url=f"{self.API_URL}/v2/emmeti/{installation_id}/{device_id}/febos-data/get-febos-slave",
            headers={
                "Accept": "application/json, text/plain, */*",
                "Referer": f"{self.APP_URL}/page/FBDEVLIST",
            },
        )
        if not response or response.status_code != 200:
            raise self._handle_error(response)
        return response.json()

    def realtime_data(self, installation_id, input_group_list):
        if input_group_list is None or len(input_group_list) == 0:
            return ValueError(input_group_list)
        response = self.get(
            url=f"{self.API_URL}/v2/emmeti/{installation_id}/realtime-data?input_group_list={','.join(input_group_list)}",
            headers={
                "Accept": "application/json, text/plain, */*",
                "Referer": f"{self.APP_URL}/page/FBDEVLIST",
            },
        )
        if not response or response.status_code != 200:
            raise self._handle_error(response)
        return response.json()
