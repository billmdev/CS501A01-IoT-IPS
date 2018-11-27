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
