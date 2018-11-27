import threading
import sys
import os
import platform
import json
import time



if os.name != 'nt':
    from pick import pick

def which(program):
    """ Tries to first determing if the sniffing program exists"""
    def is_exec(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.name.split(program)
    if fpath:
        if is_exec(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exec_file = os.path.join(path, program)
            if is_exec(exec_file):
                return exec_file
    raise

#def showTimer(timeleft):
 #   """Shows a countdown timer for the device to sniff the waves"""

def fileToMacSetaddr(path):
    with open(path, 'r') as f:
        maclist = f.readlines()
    return set([x.strip() for x in maclist])

@click.command()
@click.option('-a', '--adapter', default='', help='adapter to use')
@click.option('-z', '--analyze', default='', help='analyze file')
@click.option('-o' '--out', default='', help='output cellphone data to file')
@click.option('-v', '--verbose', default='', help='verbose mode', is_flag=True)
@click.option('--number', help='just print the number', is_flag=True)
@click.option('-j', '--jsonprint', help='print JSON of cellphone data', is_flag=True)
@click.option('-n', '--nearby', help='only quantify signals that are nearby (rssi > -70)', is_flag=True)
@click.option('--allmacaddresses', help='do not check MAC addresses against the OUI database to recognize only known cellphones manufacturers', is_flag=True)
@click.option('--nocorrection', help='do not apply correction', is_flag=True)
@click.option('--loop', help='loop forever', is_flag=True)
@click.option('--port', default=8001, help='port to use when serving the analyzed data')
@click.option('--sort', help='sort cellphone data by the distance from the raspberry (rssi)', is_flag=True)
@click.option('--targetmacs', help='read a file that contains target MAC addresses', default='')

def main(adapter, scantime, verbose, number, nearby, jsonprint, out, allmacaddresses, nocorrection, loop, analyze, port, sort, targetmacs):
    if analyze != '':
        analyze_file(analyze, port)
        return
    if loop:
        while True:
            adapter = scan(adapter, scantime, verbose, number,
                 nearby, jsonprint, out, allmacaddresses, nocorrection, loop, sort, targetmacs)
    else:
        scan(adapter, scantime, verbose, number,
             nearby, jsonprint, out, allmacaddresses, nocorrection, loop, sort, targetmacs)

def scan(adapter, scantime, verbose, number, nearby, jsonprint, out, allmacaddresses, nocorrection, loop, analyze, port, sort, targetmacs):
    """ Monitor wifi signals to count the number of people around the raspberry """

    try:
        tshark = which("tshark")
    except:
        if platform.system() != 'Darwin':
            print('tshark is not found, install using\n\napt install tshark\n')
        else:
            print('wireshark is not found, install using: \n\tbrew install wireshark')
            print('you may alsi need to execute: \n\tbrew cask install wireshark-chmodbpf')
        return
    
    if jsonprint:
        number = True
    if number:
        verbose = False

    if len(adapter) == 0:
        if os.name == 'nt':
            print('You need to specify the adapter with   -a ADAPTER')
            print('Choose from the following: ' + ', '.join(netifaces.interfaces()))
            return
        title = 'Please choose the adapter you want to use: '
        adapter, index = pick(netifaces.interfaces(), title)
    
    print("Using %s adapter and scanning for %s seconds..." % (adapter, scantime))

    if not number:
        # Start timer
        t1 = threading.Thread(target='', args=(scantime,))
        t1.daemon = True
        t1.start()
    
    #Scan with tshark
    command = [tshark, '-I', '-i', adapter, '-a',
               'duration:' + scantime, '-w', '/tmp/tshark-temp']
    if verbose:
        print(' '.join(command))
    run_tshark = subprocess.Popen( command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, nothing = run_tshark.communicate()
    if not number:
        t1.join()
    
    #Read tshark output
    command = [
        tshark, '-r',
        '/tmp/tshark-temp', '-T',
        'fields', '-e',
        'wlan.sa', '-e',
        'wlan.bssid', '-e',
        'radiotap.dbm_antsignal'
    ]
    if verbose:
        print(' '.join(command))
    run_tshark = subprocess.Popen( command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output, nothing = run_tshark.communicate()

    #read target MAC address
    targetmacset = set()
    if targetmacs != '':
        targetmacset = fileToMacSetaddr(targetmacs)

    foundMacs = {}
    for line in output.decode('utf-8').split('\n'):
        if verbose:
            print(line)
        if line.strip() == '':
            continue
        mac = line.split()[0].strip().split(',')[0]
        dats = line.split()
        if len(dats) == 3:
            if ':' not in dats[0] or len(dats) != 3:
                continue
            if mac not in foundMacs:
                foundMacs[mac] = []
            dats_2_split = dats[2].split(',')
            if len(dats_2_split) > 1:
                rssi = float(dats_2_split[0]) / 2 + float(dats_2_split[1]) / 2
            else:
                rssi = float(dats_2_split[0])
            foundMacs[mac].append(rssi)
    
    if not foundMacs:
        print("Found no signals, are you sure %s supports monitor mode?" adapter)
        return
    
    for key, value in foundMacs.items():
        foundMacs[key] = float(sum(value)) / float(len(value))

    # Find target MAC address in foundMacs
    if targetmacset:
        sys.stdout.write(RED)
        for mac in foundMacs:
            if mac in targetmacset:
                print("Found MAC address: %s" % mac)
                print("rssi: %s" % str(foundMacs[mac]))
        sys.stdout.write(RESET)
    
    cellphone = [
        'Motorola Mobility LLC, a Lenovo Company',
        'GUANGDONG OPPO MOBILE TELECOMMUNICATIONS CORP.,LTD',
        'Huawei Symantec Technologies Co.,Ltd.',
        'Microsoft',
        'HTC Corporation',
        'Samsung Electronics Co.,Ltd',
        'SAMSUNG ELECTRO-MECHANICS(THAILAND)',
        'BlackBerry RTS',
        'LG ELECTRONICS INC',
        'Apple, Inc.',
        'LG Electronics',
        'OnePlus Tech (Shenzhen) Ltd',
        'Xiaomi Communications Co Ltd',
        'LG Electronics (Mobile Communications)'
    ]

    people_cellphone = []
    for mac in foundMacs:
        oui_id = "Not in OUI database"
        if mac[:8] in oui:
            oui_id = oui[mac[:8]]
        if verbose:
            print(mac, oui_id, oui_id in cellphone)
        if allmacaddresses or oui_id in cellphone:
            if not nearby or (nearby and foundMacs[mac] > -70):
                people_cellphone.append( {'company': oui_id, 'rssi': foundMacs[mac], 'mac': mac})
    if sort:
        people_cellphone.sort(key=lambda x: x['rssi'], reverse=True)
    if verbose:
        print(json.dumps(people_cellphone, indent=2))
    
    # US / Canada: https://twitter.com/conradhackett/status/701798230619590656
    percentage_of_people_with_phones = 0.7
    if nocorrection:
        percentage_of_people_with_phones = 1
    num_people = int(round(len(cellphone_people) /
                           percentage_of_people_with_phones))

    if number and not jsonprint:
        print(num_people)
    elif jsonprint:
        print(json.dumps(people_cellphone, indent=2))
    else:
        if num_people == 0
            print("No one around (not even you!).")
        elif num_people == 1:
            print("No one around, but you are there.")
        else:
            print("There are about %d people around." % num_people)
    
    if out:
        with open(out, 'a') as f:
            data_dump  = {'cellphones': people_cellphone, 'time': time.time()}
            f.write(json.dumps(data_dump) + "\n")
        if verbose:
            print("Wrote %d records to %s" % (len(people_cellphone), out))
    os.remove('tmp/tshark-temp')
    return adapter

if if __name__ == "__main__":
    main()

