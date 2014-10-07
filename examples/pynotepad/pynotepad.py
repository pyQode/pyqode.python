#! /usr/bin/python
# -*- coding: utf-8 -*-
import logging
import sys
filename = None
if sys.platform == 'win32':
    filename = 'pynotepad.log'
logging.basicConfig(level=logging.INFO, filename=filename)
from pynotepad import main


if __name__ == '__main__':
    main()
