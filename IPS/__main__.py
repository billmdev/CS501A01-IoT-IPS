import threading
import sys
import os
import platform
import json
import time



if os.name != 'nt':
    from pick import pick

def which(program):
    """ Tries to first determing if the program exists"""
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



