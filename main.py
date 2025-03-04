""" Example application """

import sys
import logging
from src.febos.api import FebosApi

LOGGER = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s] [%(funcName)s()] %(message)s"
logging.basicConfig(format=FORMAT)
LOGGER.setLevel(logging.DEBUG)

def main(username, password):
    api = FebosApi(username, password)
    login = api.login()
    LOGGER.info("Logged in")
    installations = login.installationIdList
    groups = set()
    devices = []
    resources = {}
    for installation_id in installations:
        page_config = api.page_config(installation_id)
        for device in page_config.deviceMap.values():
            devices.append(device.id)
            get_febos_slave = api.get_febos_slave(installation_id, device.id)
            for slave in get_febos_slave:
                for k in slave.__dict__:
                    if k in ["temp", "setTemp", "callTemp", "humid", "callHumid", "confort", "stagione"]:
                        key = f"{installation_id}_{device.id}_{slave.indirizzoSlave}_{k.lower()}"
                        resources[key] = getattr(slave, k)
            for page in page_config.pageMap.values():
                for tab in page.tabList:
                    for widget in tab.widgetList:
                        for group in widget.widgetInputGroupList:
                            groups.add(group.inputGroupGetCode)
                            for resource in group.inputList:
                                key = f"{installation_id}_{resource.deviceId}_{resource.thingId}_{resource.code}"
                                resources[key] = None
    for installation_id in installations:
        realtime_data = api.realtime_data(installation_id, groups)
        for entry in realtime_data:
            for code, value in entry.data.items():
                key = f"{installation_id}_{entry.deviceId}_{entry.thingId}_{code}"
                if key in resources:
                    resources[key] = value.i
                else:
                    LOGGER.warning(f"Key not found: {key}")
        for device_id in devices:
            get_febos_slave = api.get_febos_slave(installation_id, device_id)
            for slave in get_febos_slave:
                for k in slave.__dict__:
                    if k in ["temp", "setTemp", "callTemp", "humid", "callHumid", "confort", "stagione"]:
                        key = f"{installation_id}_{device_id}_{slave.indirizzoSlave}_{k.lower()}"
                        if key in resources:
                            resources[key] = getattr(slave, k)
                        else:
                            LOGGER.warning(f"Key not found: {key}")
    LOGGER.info(f"{len(login.installationIdList)} installations loaded")
    LOGGER.info(f"{len(resources)} resources loaded")
    for key, value in resources.items():
        LOGGER.debug(f"[RESOURCE] KEY = {key}, VALUE = {value}")

if __name__ == "__main__":
    main(*sys.argv[1:])
