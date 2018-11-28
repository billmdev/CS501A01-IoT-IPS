import datetime
import json
import sys


def analyze_file(fname, port):
    lines = []
    with open(fname, 'r') as f:
        for line in f:
            try:
                lines.append(json.loads(line))
            except:
                pass
    macs_to_add = []
    for data in lines:
        for c in data['cellphones']:
            if c['rssi'] > -80 and c['mac'] not in macs_to_add:
                macs_to_add.append(c['mac'])
    mac_data = {mac: {'y': []} for mac in macs_to_add}
    num = {'x': [], 'y': []}
    for data in lines:
        rssi = {}
        for mac in macs_to_add:
            rssi[mac] = -100
            for c in data['cellphones']:
                if c['mac'] in rssi:
                    rssi[c['mac']] = c['rssi']
        for mac in mac_data:
            mac_data[mac]['y'].append(str(rssi[mac] + 100))
        num['x'].append("'" + datetime.datetime.fromtimestamp(
            data['time']).isoformat().split('.')[0].replace('T', ' ') + "'")
        num['y'].append(str(len(data['cellphones'])))

    mac_names = copy.deepcopy(macs_to_add)
    for i, mac in enumerate(mac_names):
        mac_names[i] = 'mac' + mac.replace(':', '')

    