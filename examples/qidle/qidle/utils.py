# -*- coding: utf-8 -*-
from glob import glob
import os
import platform


def get_interpreters():
    if platform.system().lower() == 'linux':
        executables = [os.path.join('/usr/bin/', exe)
                       for exe in ['python2', 'python3']
                       if os.path.exists(os.path.join('/usr/bin/', exe))]
    else:
        executables = set()
        paths = os.environ['PATH'].split(';')
        for path in paths:
            if 'python' in path.lower():
                if 'scripts' in path.lower():
                     path = os.path.abspath(os.path.join(path, os.pardir))
                executables.add(os.path.join(path, 'python.exe'))
    return executables
