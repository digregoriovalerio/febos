"""Python API client for the EmmeTI Febos webapp.

This package provides a small synchronous client and typed endpoint models
for interacting with EmmeTI's Febos frontend API. Create a `FebosClient`,
instantiate endpoint models (e.g., `GetDataAnalysisEndpoint`, `LoginEndpoint`)
with that client and call `get()`/`post()` to perform requests.
"""

from febos.client import FebosClient
from febos.data_model import (DataAnalysisEntry, Device,
                              GetDataAnalysisGetResponse,
                              GetFebosSlaveGetResponse, GetLanguageGetResponse,
                              HistoricalDataEntry, HistoricalDataGetResponse,
                              HistoricalDataPoint, Input, InputCode,
                              InputGroup, Installation,
                              InstallationGetResponse, LoginPostResponse, Page,
                              PageConfigGetResponse, RealtimeData,
                              RealtimeDataGetResponse,
                              RealtimeDataPostResponse, Slave, Tab, Thing,
                              Value, Widget)
from febos.error import AuthenticationError, FebosError
from febos.get_data_analysis import GetDataAnalysisEndpoint
from febos.get_febos_slave import GetFebosSlaveEndpoint
from febos.get_historical_data import GetHistoricalDataEndpoint
from febos.get_language import GetLanguageEndpoint
from febos.installation import InstallationEndpoint
from febos.login import LoginEndpoint
from febos.page_config import PageConfigEndpoint
from febos.realtime_data import RealtimeDataEndpoint

__version__ = "1.0.0"

__all__ = [
    "FebosClient",
    "AuthenticationError",
    "FebosError",
    "GetDataAnalysisEndpoint",
    "GetFebosSlaveEndpoint",
    "GetHistoricalDataEndpoint",
    "GetLanguageEndpoint",
    "InstallationEndpoint",
    "LoginEndpoint",
    "PageConfigEndpoint",
    "RealtimeDataEndpoint",
    "Slave",
    "GetFebosSlaveGetResponse",
    "Installation",
    "InstallationGetResponse",
    "LoginPostResponse",
    "Device",
    "Input",
    "InputGroup",
    "Widget",
    "Tab",
    "Page",
    "Thing",
    "PageConfigGetResponse",
    "Value",
    "RealtimeData",
    "RealtimeDataGetResponse",
    "RealtimeDataPostResponse",
    "GetLanguageGetResponse",
    "DataAnalysisEntry",
    "GetDataAnalysisGetResponse",
    "InputCode",
    "HistoricalDataPoint",
    "HistoricalDataEntry",
    "HistoricalDataGetResponse",
]
