"""Pydantic models for Febos API requests and responses.

This module contains typed models used to parse responses returned by the
Febos frontend API. Models are intentionally simple mappings of the JSON
structures returned by the server.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, RootModel


class Slave(BaseModel):
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


class GetFebosSlaveGetResponse(RootModel):
    root: List[Slave]


class Installation(BaseModel):
    code: str
    codeName: str
    id: int
    label: str
    name: str
    tagSet: List[str]
    tenantId: int
    tenantName: str
    adminUserId: Optional[int] = None
    adminUserName: Optional[str] = None
    finalUserId: Optional[List[int]] = None
    finalUserName: Optional[List[str]] = None
    numAlarm: Optional[int] = None
    numController: Optional[int] = None
    numDisconnected: Optional[int] = None


class InstallationGetResponse(RootModel):
    root: List[Installation]


class LoginPostResponse(BaseModel):
    authList: List[str]
    creationDate: str
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


class Device(BaseModel):
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


class Input(BaseModel):
    category: str
    clientName: str
    code: str
    codeName: str
    dataOffset: int
    deviceId: int
    deviceModelId: int
    id: int
    inputOptionDtoList: List[Any]
    inputType: str
    label: str
    name: str
    ord: int
    saveHistory: bool
    thingId: int
    thingModelId: int
    authGet: Optional[str] = None
    defaultIntValue: Optional[int] = None
    description: Optional[str] = None
    display: Optional[bool] = None
    enabled: Optional[bool] = None
    max: Optional[int] = None
    measUnit: Optional[str] = None
    min: Optional[int] = None
    nullValue: Optional[str] = None
    parameterEditorType: Optional[str] = None
    scale: Optional[int] = None


class InputGroup(BaseModel):
    deviceId: int
    inputGroupCode: str
    inputGroupGetCode: str
    inputGroupId: int
    inputList: List[Input]
    ord: int
    thingId: int


class Widget(BaseModel):
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
    code: str
    id: int
    inputGroupGetCodeMap: dict[str, List[str]]
    label: str
    name: str
    ord: int
    pageId: int
    widgetList: List[Widget]


class Page(BaseModel):
    code: str
    codeName: str
    id: int
    inputGroupGetCodeList: List[str]
    label: str
    name: str
    ord: int
    pageType: str
    tabList: List[Tab]


class Thing(BaseModel):
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


class PageConfigGetResponse(BaseModel):
    deviceMap: Dict[str, Device]
    installation: Installation
    pageMap: Dict[str, Page]
    thingMap: Dict[str, Thing]


class Value(BaseModel):
    i: Any


class RealtimeData(BaseModel):
    data: dict[str, Value]
    deviceId: int
    thingId: int
    ts: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%S.%f"
        )[:-3]
        + "Z"
    )


class RealtimeDataGetResponse(RootModel):
    root: List[RealtimeData]


class RealtimeDataPostResponse(BaseModel):
    errCode: int
    msg: str


class GetLanguageGetResponse(BaseModel):
    ts: str
    ID_language: str


class DataAnalysisEntry(BaseModel):
    ts: str
    model_config = {"extra": "allow"}


class GetDataAnalysisGetResponse(RootModel):
    root: List[DataAnalysisEntry]


class InputCode(BaseModel):
    code: str


class HistoricalDataPoint(BaseModel):
    ts: str
    vs: List[str]


class HistoricalDataEntry(BaseModel):
    deviceId: int
    thingId: int
    groupCode: str
    inputArray: List[InputCode]
    data: List[HistoricalDataPoint]


class HistoricalDataGetResponse(RootModel):
    root: List[HistoricalDataEntry]
