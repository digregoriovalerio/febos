from __future__ import annotations

from typing import List, Any

from requests import Session
from requests.auth import AuthBase

from .errors import ApiError, AuthenticationError
from pydantic import BaseModel, root_validator
from datetime import datetime
from pydantic_core import from_json
from requests.models import Response

from pydantic_core._pydantic_core import ValidationError

class LoginResponse(BaseModel):
    """Login response."""
    authList: List[str]
    creationDate: datetime
    email: str
    enabled: bool
    id: int
    installationIdList: List[int]
    name: str
    profileId: int
    profileName: str
    tenantId: int
    tenantName: str
    username: str

    @staticmethod
    def from_json(json_data: dict[str, Any]) -> LoginResponse:
        return LoginResponse.model_validate(json_data)


class InstallationData(BaseModel):
    """Installation Data."""
    adminUserId: int
    adminUserName: str
    code: str
    codeName: str
    finalUserId: List[int]
    finalUserName: List[str]
    id: int
    label: str
    name: str
    numAlarm: int
    numController: int
    numDisconnected: int
    tagSet: List[str]
    tenantId: int
    tenantName: str


class InstallationResponse:
    """Installation response."""

    @staticmethod
    def from_json(json_data: dict[str, Any]) -> List[InstallationData]:
        return list([InstallationData.model_validate(i) for i in json_data])


class Installation(BaseModel):
    """Installation Data."""
    code: str
    codeName: str
    id: int
    label: str
    name: str
    tagSet: List[str]
    tenantId: int
    tenantName: str


class Device(BaseModel):
    """Device Data."""
    code: str
    codeName: str
    controllerCode: str
    controllerId: int
    controllerName: str
    deviceCategory: str
    deviceTypeCode: str
    deviceTypeId: int
    deviceTypeName: str
    enabled: bool
    id: int
    installationCode: str
    installationId: int
    installationName: str
    label: str
    modelCode: str
    modelId: int
    modelName: str
    name: str
    ord: int
    tenantId: int
    tenantName: str


class Thing(BaseModel):
    """Thing Data."""
    address: str
    code: str
    codeName: str
    deviceId: int
    id: int
    label: str
    modelCode: str
    modelId: int
    modelName: str
    name: str
    ord: int
    tenantId: int
    tenantName: str
    thingTypeCode: str
    thingTypeName: str


class Input(BaseModel):
    """Input Data."""
    authGet: str = None
    category: str
    clientName: str
    code: str
    codeName: str
    dataOffset: int
    defaultIntValue: int = None
    description: str = None
    deviceId: int
    deviceModelId: int
    display: bool = None
    enabled: bool = None
    id: int
    inputOptionDtoList: List[Any]
    inputType: str
    label: str
    max: int = None
    measUnit: str = None
    min: int = None
    name: str
    nullValue: str = None
    ord: int
    parameterEditorType: str = None
    saveHistory: bool
    scale: int = None
    thingId: int
    thingModelId: int
                                                                                                                                         
    @root_validator(skip_on_failure=True)
    def _remove_age_if_none(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        for k in list(values.keys()):
            if values[k] is None:
                del values[k]
        return values


class InputGroup(BaseModel):
    """InputGroup Data."""
    deviceId: int
    inputGroupCode: str
    inputGroupGetCode: str
    inputGroupId: int
    inputList: List[Input]
    ord: int
    thingId: int


class Widget(BaseModel):
    """Widget Data."""
    code: str
    defaultDeviceId: int
    defaultThingId: int
    id: int
    inputGroupGetCodeList: List[str]
    label: str
    name: str
    ord: int
    tabId: int
    widgetInputGroupList: List[InputGroup]


class Tab(BaseModel):
    """Tab Data."""
    code: str
    id: int
    inputGroupGetCodeMap: dict[str, List[str]]
    label: str
    name: str
    ord: int
    pageId: int
    widgetList: List[Widget]


class Page(BaseModel):
    """Page Data."""
    code: str
    codeName: str
    id: int
    inputGroupGetCodeList: List[str]
    label: str
    name: str
    ord: int
    pageType: str
    tabList: List[Tab]


class PageConfigResponse(BaseModel):
    """Page Config response."""
    deviceMap: dict[str, Device]
    installation: Installation
    pageMap: dict[str, Page]
    thingMap: dict[str, Thing]
    
    @staticmethod
    def from_json(json_data: dict[str, Any]) -> PageConfigResponse:
        return PageConfigResponse.model_validate(json_data)


class Slave(BaseModel):
    """Slave Data."""
    callHumid: int
    callTemp: int
    centrallizato: int
    confort: int
    humid: int
    indirizzoSlave: str
    nomeSlave: str
    setTemp: int
    stagione: int
    statusSlave: str
    temp: int


class GetFebosSlaveResponse:
    """Get Febos Slave response."""
    
    @staticmethod
    def from_json(json_data: dict[str, Any]) -> List[Slave]:
        return list([Slave.model_validate(slave) for slave in json_data])


class Value(BaseModel):
    """Value data."""
    i: Any


class RealtimeData(BaseModel):
    """Realtime data."""
    data: dict[str, Value]
    deviceId: int
    groupCode: str
    thingId: int
    ts: datetime


class RealtimeDataResponse:
    """Realtime Data response."""
    
    @staticmethod
    def from_json(json_data: dict[str, Any]) -> List[RealtimeData]:
        return list([RealtimeData.model_validate(data) for data in json_data])


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

    def __init__(self, username: str, password: str):
        super().__init__()
        self.auth = None
        self.username = username
        self.password = password

    def _handle_error(self, response: Response) -> None:
        if response.status_code == 401:
            raise AuthenticationError(response)
        elif response.status_code != 200:
            raise ApiError(response)

    def login(self) -> LoginResponse:
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
        return LoginResponse.from_json(response.json())

    def installation(self, pageStart: int = 1, pageItems: int = 500000) -> List[InstallationData]:
        response = self.get(
            url=f"{self.API_URL}/v1/installation?pageStart={pageStart}&pageItems={pageItems}",
            headers={
                "Accept": "application/json, text/plain, */*",
                "Referer": f"{self.APP_URL}/auth/installation-list",
            },
        )
        if not response or response.status_code != 200:
            raise self._handle_error(response)
        return InstallationResponse.from_json(response.json())

    def page_config(self, installation_id: int) -> PageConfigResponse:
        response = self.get(
            url=f"{self.API_URL}/v1/installation/{installation_id}/page-config?web=false",
            headers={
                "Accept": "application/json, text/plain, */*",
                "Referer": f"{self.APP_URL}/page/FBDEVLIST",
            },
        )
        if not response or response.status_code != 200:
            raise self._handle_error(response)
        return PageConfigResponse.from_json(response.json())

    def get_febos_slave(self, installation_id: int, device_id: int) -> List[Slave]:
        response = self.get(
            url=f"{self.API_URL}/v2/emmeti/{installation_id}/{device_id}/febos-data/get-febos-slave",
            headers={
                "Accept": "application/json, text/plain, */*",
                "Referer": f"{self.APP_URL}/page/FBDEVLIST",
            },
        )
        if not response or response.status_code != 200:
            raise self._handle_error(response)
        return GetFebosSlaveResponse.from_json(response.json())

    def realtime_data(self, installation_id: int, input_group_list: List[str]) -> List[RealtimeData]:
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
        return RealtimeDataResponse.from_json(response.json())
