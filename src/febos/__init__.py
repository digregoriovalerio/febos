"""Python API client for the EmmeTI Febos webapp.

This package provides a small synchronous client and typed endpoint models
for interacting with EmmeTI's Febos frontend API. Create a `FebosClient`,
instantiate endpoint models with that client and call `get()`/`post()` to
perform requests.
"""

from febos.client import FebosClient
from febos.error import AuthenticationError, FebosError
from febos.get_data_analysis import GetDataAnalysis
from febos.get_febos_slave import GetFebosSlave
from febos.get_historical_data import GetHistoricalData
from febos.get_language import GetLanguage
from febos.installation import Installation
from febos.login import Login
from febos.page_config import PageConfig
from febos.realtime_data import RealtimeData

__version__ = "1.0.0"

__all__ = [
    "FebosClient",
    "AuthenticationError",
    "FebosError",
    "GetDataAnalysis",
    "GetFebosSlave",
    "GetHistoricalData",
    "GetLanguage",
    "Installation",
    "Login",
    "PageConfig",
    "RealtimeData",
]
