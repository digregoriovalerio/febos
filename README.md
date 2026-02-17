# febos
A Python API client for the [EmmeTI Febos webapp](https://emmeti.aq-iot.net/).

## Features

- 🔐 Bearer token authentication
- 📡 Real-time sensor data retrieval
- 🏢 Multi-installation support
- 🔍 Device and resource discovery
- ✅ Full type hints and docstrings
- 🧪 Comprehensive test suite with mocking
- 📝 Pydantic models for data validation

## Installation

```bash
pip install febos
```

## Quick Start

```python
from febos import FebosClient, Login, PageConfig, RealtimeData

# Initialize client and authenticate
client = FebosClient()
login = Login(client=client, username="your_username", password="your_password")
response = login.post()

# Access user information
print(f"Welcome {response.username}!")
print(f"Installations: {response.installationIdList}")

# Get installation configuration
config = PageConfig(client=client, installation_id=101).get()
print(f"Devices: {list(config.deviceMap.keys())}")

# Fetch real-time data
real_time = RealtimeData(
    client=client,
    installation_id=101,
    input_group_list=["group1", "group2"]
).get()

for entry in real_time.root:
    print(f"Device {entry.deviceId}: {entry.data}")
```

## API Reference

### Client Initialization

```python
from febos import FebosClient

# Use default EmmeTI production server
client = FebosClient()

# Or specify custom base URL
client = FebosClient(base_url="https://custom.server.com")

# Set custom timeout (default: 30 seconds)
client = FebosClient(timeout=60.0)
```

You can also configure the base URL via environment variable:

```bash
export FEBOS_BASE_URL="https://custom.example.com"
python your_script.py
```

### Authentication

```python
from febos import Login

login = Login(client=client, username="user", password="pass")
response = login.post()  # Returns LoginPostResponse

# Token is automatically set in client after successful login
# Token can also be set manually:
client.set_token("your_bearer_token")
```

### Available Endpoints

#### Login
Authenticate and retrieve user information.

```python
response = Login(client=client, username="user", password="pass").post()
```

#### Installation
Retrieve list of installations for the user.

```python
response = Installation(
    client=client,
    pageStart=1,
    pageItems=500000
).get()

for installation in response.root:
    print(f"Installation: {installation.name} (ID: {installation.id})")
```

#### PageConfig
Get page configuration and device information for an installation.

```python
response = PageConfig(client=client, installation_id=101).get()
print(f"Devices: {response.deviceMap}")
print(f"Pages: {response.pageMap}")
print(f"Things: {response.thingMap}")
```

#### RealtimeData
Fetch or post real-time sensor data.

```python
# Get real-time data
response = RealtimeData(
    client=client,
    installation_id=101,
    input_group_list=["group1", "group2"]
).get()

# Post real-time data
from febos.data_model import RealtimeData as RealtimeDataModel, Value

data = RealtimeDataModel(
    data={"temperature": Value(i=22.5)},
    deviceId=789,
    groupCode="F_GENERAL",
    thingId=10
)
response = realtime.post(data)
```

#### GetFebosSlave
Retrieve Febos slave device information.

```python
response = GetFebosSlave(
    client=client,
    installation_id=101,
    device_id=789
).get()

for slave in response.root:
    print(f"Slave: {slave.nomeSlave} - Temp: {slave.temp}°C")
```

#### GetLanguage
Retrieve the device language setting for a given installation and device.

```python
response = GetLanguage(
    client=client,
    installation_id=101,
    device_id=789,
).get()

print(f"Language ID: {response.ID_language} (retrieved at {response.ts})")
```

#### GetDataAnalysis
Retrieve daily analysis rows for a device between two timestamps.

```python
response = GetDataAnalysis(
    client=client,
    installation_id=7593,
    device_id=9551,
    from_ts="2026-02-11 00:00:00",
    to_ts="2026-02-11 23:59:00",
).get()

for row in response.root:
    print(row.ts, {k: v for k, v in row.model_dump().items() if k != "ts"})
```

#### GetHistoricalData
Retrieve historical time-series data for input groups within a date range.

```python
response = GetHistoricalData(
    client=client,
    installation_id=7593,
    input_group_list="FB-GRAPH-DATA@D9551@T31115",
    time_from="2026-02-11 00:00:00",
    time_to="2026-02-11 23:59:59",
).get()

for entry in response.root:
    print(f"Device {entry.deviceId}, Thing {entry.thingId}")
    print(f"  Codes: {', '.join(ic.code for ic in entry.inputArray)}")
    for point in entry.data:
        print(f"  [{point.ts}]: {', '.join(point.vs)}")
```

## Data Models

All responses are validated using Pydantic models:

- `LoginPostResponse` - User information and auth details
- `InstallationGetResponse` - List of installations
- `PageConfigGetResponse` - Page configuration with devices and things
- `RealtimeDataGetResponse` - Real-time sensor data
- `GetFebosSlaveGetResponse` - Slave device information
- `GetLanguageGetResponse` - Device language information
- `GetDataAnalysisGetResponse` - Daily analysis data
- `HistoricalDataGetResponse` - Historical time-series data

See [src/febos/data_model.py](src/febos/data_model.py) for complete model definitions.

## Error Handling

The library provides custom exceptions:

```python
from febos import AuthenticationError, FebosError

try:
    login = Login(client=client, username="wrong", password="wrong")
    login.post()
except AuthenticationError as e:
    print(f"Auth failed: {e.message}")
except FebosError as e:
    print(f"API error: {e}")
```

## Configuration

### Environment Variables

- **FEBOS_BASE_URL**: Base URL for the API (default: `https://emmeti.aq-iot.net`)

```bash
export FEBOS_BASE_URL="https://custom.server.com"
```

### Client Options

The `FebosClient` supports the following configuration options:

```python
client = FebosClient(
    base_url="https://custom.server.com",  # API base URL
    timeout=30.0,  # Request timeout in seconds
)
```

- **base_url**: API endpoint URL (can also be set via `FEBOS_BASE_URL` env var)
- **timeout**: Request timeout in seconds (default: 30.0)

## Logging

The library uses the standard Python logging module. Configure logging level in your application:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

Or use the CLI example's `--log-level` option:

```bash
python main.py <username> <password> --log-level DEBUG
```

## Development

### Install development dependencies

```bash
pip install -e "febos[dev]"
```

### Run tests

```bash
pytest tests/
```

### Run specific test

```bash
pytest tests/test_login.py::test_login_post_success -v
```

### Code formatting and linting

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
pylint src/febos

# Run with coverage
pytest --cov=febos tests/
```

## Example: Full Data Collection

See [main.py](main.py) for a complete example that:
1. Authenticates with credentials
2. Discovers all installations
3. Retrieves page configurations
4. Collects real-time data
5. Gathers slave device information

Run the example:

```bash
python main.py <username> <password>

# With custom logging level
python main.py <username> <password> --log-level DEBUG

# Available log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

## Requirements

- Python >= 3.10
- httpx >= 0.27.2
- pydantic >= 2.12.5
- coloredlogs >= 15.0

### Optional Dependencies

For development, install with:
```bash
pip install -e "febos[dev]"
```

This includes:
- black - Code formatter
- isort - Import sorter
- pylint - Code linter
- pytest-cov - Coverage reporting

## License

MIT - See LICENSE file for details

## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/digregoriovalerio/febos).