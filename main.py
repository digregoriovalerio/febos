from .src.febos.api import FebosApi


def main():
    def get_inputs(cfg):
        inputs = {}
        for _, page in cfg.get('pageMap', {}).items():
            for tab in page.get('tabList', []):
                for widget in tab.get('widgetList', []):
                    for group in widget.get('widgetInputGroupList', []):
                        for input in group.get('inputList', []):
                            inputs[input['code']] = input
        return inputs

    def get_input_groups(cfg):
        config.get('pageMap', {}).get('FBDEVLIST', {}).get(
            'inputGroupGetCodeList', [])
        groups = set()
        for _, page in cfg.get('pageMap', {}).items():
            groups = groups.union(set(page.get('inputGroupGetCodeList', [])))
        return groups
    api = FebosApi()
    login = api.login("emt-220209004020", "bg2TnDA=Kp")
    for installation_id in login.get('installationIdList', []):
        print(f"Installation {installation_id}:")
        config = api.page_config(installation_id)
        inputs = get_inputs(config)
        groups = get_input_groups(config)
        for _, device in config.get('deviceMap', {}).items():
            if 'id' in device:
                print(
                    f"- DEVICE: {config['deviceMap'][str(device['id'])]['name']}:")
                data = api.realtime_data(installation_id, list(groups))
                print(f"\t* Master:")
                for entry in data:
                    print(f'\t  Group: {entry["groupCode"]}')
                    print(
                        f"\t  Thing: {config['thingMap'][str(entry['thingId'])]['name']}:")
                    print(f'\t  Data:')
                    for k, v in entry["data"].items():
                        if k in inputs:
                            print(
                                f"\t  - {inputs[k]['label']}: {v['i']} {inputs[k].get('measUnit', '')} [{inputs[k].get('inputType', '')}]")
                slaves = api.get_febos_slave(installation_id, device['id'])
                print(f"\t  Slaves:")
                for slave in slaves:
                    print(f"\t  - {slave["indirizzoSlave"]}: {slave["temp"]/10} °C, {slave["humid"]}% ({slave["setTemp"]/10} °C)")


if __name__ == '__main__':
    main()
