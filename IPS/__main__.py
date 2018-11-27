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