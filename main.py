"""Interactive CLI client for Febos API.

A command-line interface where users can authenticate and run various API commands.
Type 'help' for a list of available commands.
"""

import logging
from datetime import datetime

from febos.client import FebosClient
from febos.error import AuthenticationError, FebosError
from febos.get_data_analysis import GetDataAnalysisEndpoint
from febos.get_febos_slave import GetFebosSlaveEndpoint
from febos.get_historical_data import GetHistoricalDataEndpoint
from febos.get_language import GetLanguageEndpoint
from febos.installation import InstallationEndpoint
from febos.login import LoginEndpoint
from febos.page_config import PageConfigEndpoint
from febos.realtime_data import RealtimeDataEndpoint

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s",
)

LOGGER = logging.getLogger(__name__)


class FebosSession:
    """Interactive session manager for Febos API."""

    def __init__(self):
        """Initialize session with no client (unauthenticated)."""
        self.client = FebosClient()
        self.authenticated = False

    def get_authenticated_client(self) -> FebosClient:
        """Retrieve the authenticated client or raise an error if not authenticated."""
        if self.authenticated:
            return self.client
        raise FebosError("Not authenticated. Use 'login <username> <password>' first.")

    def cmd_help(self, *args):
        """Display available commands."""
        help_text = """
Available commands:

  help                                   - Show this help message
  exit, quit                             - Exit the session
  
Authentication:
  login <username> <password>            - Authenticate with Febos API

Installation:
  installation [pageStart] [pageItems]   - List installations (optional pagination)

Page Configuration:
  pageconfig <installation_id>           - Get page config for installation

Real-time Data:
  realtimeget <installation_id> <input_group_list>  - Get real-time data
  realtimepost <installation_id> <input_group_list> <json_data>         - Post real-time data

Slave Device:
  slave <installation_id> <device_id>    - Get slave device data

Language:
  language <installation_id> <device_id> - Get device language

Data Analysis:
  dataanalysis <installation_id> <device_id> [from_ts] [to_ts] - Get data analysis rows
                                            (timestamps: "YYYY-MM-DD HH:MM:SS", defaults to today)

Historical Data:
  historicaldata <installation_id> <input_group_list> <time_from> <time_to>
                                         - Get historical time-series data
                                           (timestamps: "YYYY-MM-DD HH:MM:SS")
"""
        print(help_text)

    def cmd_exit(self, *args):
        """Exit the session."""
        print("Goodbye!")
        raise KeyboardInterrupt

    def cmd_quit(self, *args):
        """Exit the session (alias for exit)."""
        return self.cmd_exit(*args)

    def cmd_login(self, *args):
        """Authenticate with username and password."""
        if len(args) < 2:
            print("Usage: login <username> <password>")
            return

        username, password = args[0], args[1]
        try:
            login_endpoint = LoginEndpoint(username=username, password=password)
            response = login_endpoint.post(client=self.client)
            self.authenticated = True
            print(f"✓ Logged in as: {response.username}")
            print(f"  Installations: {response.installationIdList}")
        except AuthenticationError as e:
            print(f"✗ Authentication failed: {e}")
        except Exception as e:
            print(f"✗ Error: {e}")

    def cmd_installation(self, *args):
        """List installations."""
        try:
            page_start = int(args[0]) if len(args) > 0 else 1
            page_items = int(args[1]) if len(args) > 1 else 500000
            endpoint = InstallationEndpoint(
                pageStart=page_start, pageItems=page_items
            )
            response = endpoint.get(client=self.get_authenticated_client())
            if not response.root:
                print("No installations found.")
                return
            for inst in response.root:
                print(f"  ID: {inst.id:6} | Name: {inst.name:30} | Label: {inst.label}")
        except Exception as e:
            print(f"✗ Error: {e}")

    def cmd_pageconfig(self, *args):
        """Get page configuration for an installation."""
        if len(args) < 1:
            print("Usage: pageconfig <installation_id>")
            return
        try:
            installation_id = int(args[0])
            endpoint = PageConfigEndpoint(installation_id=installation_id)
            response = endpoint.get(client=self.get_authenticated_client())
            print(f"Installation: {response.installation.name} (ID: {response.installation.id})")
            print(f"  Devices: {len(response.deviceMap)}")
            print(f"  Pages: {len(response.pageMap)}")
            print(f"  Things: {len(response.thingMap)}")
            if response.deviceMap:
                print("  Device IDs:", ", ".join(str(d.id) for d in response.deviceMap.values()))
        except ValueError:
            print("Installation ID must be an integer.")
        except Exception as e:
            print(f"✗ Error: {e}")

    def cmd_realtimeget(self, *args):
        """Get real-time data for input groups."""
        if len(args) < 2:
            print("Usage: realtimeget <installation_id> <input_group_list>")
            print("  input_group_list: comma-separated group codes (e.g., 'group1,group2')")
            return
        try:
            installation_id = int(args[0])
            input_group_list = args[1].split(",")
            endpoint = RealtimeDataEndpoint(
                installation_id=installation_id,
                input_group_list=input_group_list,
            )
            response = endpoint.get(client=self.get_authenticated_client())
            print(f"Real-time data ({len(response.root)} entries):")
            for entry in response.root:
                print(f"  Device {entry.deviceId}, Group {entry.groupCode}:")
                for code, value in entry.data.items():
                    print(f"    {code}: {value.i}")
        except ValueError:
            print("Installation ID must be an integer.")
        except Exception as e:
            print(f"✗ Error: {e}")

    def cmd_realtimepost(self, *args):
        """Post real-time data for input groups."""
        if len(args) < 3:
            print("Usage: realtimepost <installation_id> <input_group_list> <json_data>")
            print("  Example: realtimepost 101 group1,group2 '{\"data\":{\"temp\":{\"i\":22.5}},\"deviceId\":789,\"groupCode\":\"F_GENERAL\",\"thingId\":10}'")
            return
        print("✗ Post real-time data not yet implemented in CLI")

    def cmd_slave(self, *args):
        """Get slave device data."""
        if len(args) < 2:
            print("Usage: slave <installation_id> <device_id>")
            return
        try:
            installation_id = int(args[0])
            device_id = int(args[1])
            endpoint = GetFebosSlaveEndpoint(
                installation_id=installation_id, device_id=device_id
            )
            response = endpoint.get(client=self.get_authenticated_client())
            print(f"Slave device data ({len(response.root)} entries):")
            for slave in response.root:
                print(f"  Slave: {slave.nomeSlave} (Addr: {slave.indirizzoSlave})")
                print(f"    Temperature: {slave.temp}°C (Set: {slave.setTemp}, Call: {slave.callTemp})")
                print(f"    Humidity: {slave.humid}% (Call: {slave.callHumid})")
                print(f"    Comfort: {slave.confort} | Season: {slave.stagione}")
                print(f"    Status: {slave.statusSlave}")
        except ValueError:
            print("Installation ID and Device ID must be integers.")
        except Exception as e:
            print(f"✗ Error: {e}")

    def cmd_language(self, *args):
        """Get device language setting."""
        if len(args) < 2:
            print("Usage: language <installation_id> <device_id>")
            return
        try:
            installation_id = int(args[0])
            device_id = int(args[1])
            endpoint = GetLanguageEndpoint(
                installation_id=installation_id, device_id=device_id
            )
            response = endpoint.get(client=self.get_authenticated_client())
            print(f"Device language:")
            print(f"  ID: {response.ID_language}")
            print(f"  Retrieved at: {response.ts}")
        except ValueError:
            print("Installation ID and Device ID must be integers.")
        except Exception as e:
            print(f"✗ Error: {e}")

    def cmd_dataanalysis(self, *args):
        """Get data analysis rows for a device."""
        if len(args) < 2:
            print("Usage: dataanalysis <installation_id> <device_id> [from_ts] [to_ts]")
            print("  from_ts/to_ts format: YYYY-MM-DD HH:MM:SS (defaults to today 00:00:00 to 23:59:00)")
            return
        try:
            installation_id = int(args[0])
            device_id = int(args[1])
            from_ts = args[2] if len(args) > 2 else None
            to_ts = args[3] if len(args) > 3 else None

            if from_ts is None or to_ts is None:
                today = datetime.now().date()
                from_ts = f"{today} 00:00:00"
                to_ts = f"{today} 23:59:00"

            endpoint = GetDataAnalysisEndpoint(
                installation_id=installation_id,
                device_id=device_id,
                from_ts=from_ts,
                to_ts=to_ts,
            )
            response = endpoint.get(client=self.get_authenticated_client())
            print(f"Data analysis rows ({len(response.root)} entries):")
            for entry in response.root:
                row_data = entry.model_dump()
                ts = row_data.pop("ts")
                print(f"  [{ts}]:")
                for key, value in sorted(row_data.items()):
                    print(f"    {key}: {value}")
        except ValueError:
            print("Installation ID and Device ID must be integers.")
        except Exception as e:
            print(f"✗ Error: {e}")

    def cmd_historicaldata(self, *args):
        """Get historical time-series data for input groups."""
        if len(args) < 4:
            print("Usage: historicaldata <installation_id> <input_group_list> <time_from> <time_to>")
            print("  input_group_list: comma-separated codes (e.g., 'FB-GRAPH-DATA@D9551@T31115')")
            print("  time_from/time_to: YYYY-MM-DD HH:MM:SS")
            return
        try:
            installation_id = int(args[0])
            input_group_list = args[1]
            time_from = args[2]
            time_to = args[3]

            endpoint = GetHistoricalDataEndpoint(
                installation_id=installation_id,
                input_group_list=input_group_list,
                time_from=time_from,
                time_to=time_to,
            )
            response = endpoint.get(client=self.get_authenticated_client())
            print(f"Historical data ({len(response.root)} entries):")
            for entry in response.root:
                print(f"  Device {entry.deviceId}, Thing {entry.thingId}, Group: {entry.groupCode}")
                print(f"    Input codes: {', '.join(ic.code for ic in entry.inputArray)}")
                print(f"    Data points: {len(entry.data)}")
                for point in entry.data:
                    values_str = ", ".join(point.vs)
                    print(f"      [{point.ts}]: {values_str}")
        except ValueError:
            print("Installation ID must be an integer.")
        except Exception as e:
            print(f"✗ Error: {e}")

    def dispatch(self, line: str):
        """Dispatch a command line to the appropriate handler."""
        parts = line.strip().split()
        if not parts:
            return

        cmd = parts[0].lower()
        args = parts[1:]

        # Map commands to methods
        command_map = {
            "help": self.cmd_help,
            "exit": self.cmd_exit,
            "quit": self.cmd_quit,
            "login": self.cmd_login,
            "installation": self.cmd_installation,
            "pageconfig": self.cmd_pageconfig,
            "realtimeget": self.cmd_realtimeget,
            "realtimepost": self.cmd_realtimepost,
            "slave": self.cmd_slave,
            "language": self.cmd_language,
            "dataanalysis": self.cmd_dataanalysis,
            "historicaldata": self.cmd_historicaldata,
        }

        if cmd in command_map:
            try:
                command_map[cmd](*args)
            except FebosError as e:
                print(f"✗ {e}")
            except KeyboardInterrupt:
                raise
        else:
            print(f"Unknown command: '{cmd}'. Type 'help' for available commands.")


def main():
    """Main CLI loop."""
    session = FebosSession()
    print("=" * 60)
    print("  Febos Interactive CLI")
    print("=" * 60)
    print("Type 'help' for available commands or 'login <username> <password>' to start.")
    print()

    try:
        while True:
            try:
                prompt = "febos> "
                line = input(prompt).strip()
                if line:
                    session.dispatch(line)
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
