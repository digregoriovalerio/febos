import pytest

from febos.client import FebosClient


@pytest.fixture
def client():
    c = FebosClient()
    c.set_token("fake-token")
    return c


@pytest.fixture
def mock_login_response():
    return {
        "authList": ["ADMIN"],
        "creationDate": "2024-01-01T00:00:00Z",
        "email": "test@example.com",
        "enabled": True,
        "id": 1,
        "installationIdList": [101],
        "name": "Test User",
        "profileId": 1,
        "profileName": "SuperAdmin",
        "tenantId": 1,
        "tenantName": "Main Tenant",
        "username": "testuser",
    }


@pytest.fixture
def mock_installation_response():
    return [
        {
            "adminUserId": 1,
            "adminUserName": "Admin",
            "code": "XYZ",
            "codeName": "CodeName",
            "finalUserId": [10, 11],
            "finalUserName": ["testuser"],
            "id": 100,
            "label": "Label1",
            "name": "Inst1",
            "numAlarm": 0,
            "numController": 1,
            "numDisconnected": 0,
            "tagSet": ["tag1"],
            "tenantId": 1,
            "tenantName": "Tenant1",
        }
    ]


@pytest.fixture
def mock_page_config_response():
    return {
        "deviceMap": {
            "789": {
                "id": 789,
                "name": "Device1",
                "code": "D1",
                "codeName": "CN1",
                "controllerCode": "CC1",
                "controllerId": 1,
                "controllerName": "C1",
                "deviceCategory": "CAT1",
                "deviceTypeCode": "T1",
                "deviceTypeId": 1,
                "deviceTypeName": "Type1",
                "enabled": True,
                "installationCode": "I1",
                "installationId": 100,
                "installationName": "Inst1",
                "label": "L1",
                "modelCode": "M1",
                "modelId": 1,
                "modelName": "Mod1",
                "ord": 1,
                "tenantId": 1,
                "tenantName": "T1",
            }
        },
        "installation": {
            "id": 100,
            "name": "Inst1",
            "code": "XYZ",
            "codeName": "CN1",
            "label": "L1",
            "tagSet": [],
            "tenantId": 1,
            "tenantName": "T1",
        },
        "pageMap": {},
        "thingMap": {},
    }


@pytest.fixture
def mock_realtime_data_response():
    return [
        {
            "data": {"temp": {"i": 22.5}},
            "deviceId": 789,
            "groupCode": "F_GENERAL",
            "thingId": 10,
            "ts": "2024-01-01T12:00:00Z",
        }
    ]


@pytest.fixture
def mock_slave_response():
    return [
        {
            "callHumid": 0,
            "callTemp": 1,
            "centrallizato": 1,
            "confort": 20,
            "humid": 50,
            "indirizzoSlave": "01",
            "nomeSlave": "Living",
            "setTemp": 21,
            "stagione": 1,
            "statusSlave": "ON",
            "temp": 22,
        }
    ]


@pytest.fixture
def mock_get_language_response():
    return {"ts": "2026-02-11 22:02:50", "ID_language": "1"}


@pytest.fixture
def mock_get_data_analysis_response():
    return [
        {
            "ts": "2026-02-11 23:33:43",
            "R8765": "0",
            "R8766": "0",
            "R8767": "0",
            "R8768": "0",
            "R8769": "0",
            "R8770": "0",
            "R8771": "0",
            "R8772": "0",
            "R8773": "0",
            "R8774": "---",
        },
        {
            "ts": "2026-02-11 00:03:18",
            "R8765": "0",
            "R8766": "0",
            "R8767": "0",
            "R8768": "0",
            "R8769": "0",
            "R8770": "0",
            "R8771": "0",
            "R8772": "0",
            "R8773": "0",
            "R8774": "---",
        },
    ]


@pytest.fixture
def mock_get_historical_data_response():
    return [
        {
            "deviceId": 9551,
            "thingId": 31115,
            "groupCode": "FB-GRAPH-DATA@D9551@T31115",
            "inputArray": [
                {"code": "R8750"},
                {"code": "R8751"},
                {"code": "R8752"},
                {"code": "R8753"},
                {"code": "R8754"},
            ],
            "data": [
                {
                    "ts": "2026-02-11T01:03:18",
                    "vs": ["194", "74", "146", "48", "205"],
                },
                {
                    "ts": "2026-02-11T01:08:18",
                    "vs": ["193", "74", "145", "48", "205"],
                },
                {
                    "ts": "2026-02-11T23:33:43",
                    "vs": ["195", "76", "151", "48", "205"],
                },
            ],
        }
    ]
