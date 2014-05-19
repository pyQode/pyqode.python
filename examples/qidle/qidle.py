#! /usr/bin/python3
# -*- coding: utf-8 -*-
import logging
import sys
filename = None
if sys.platform == 'win32':
    filename = 'qidle.log'
logging.basicConfig(level=logging.INFO, filename=filename)
from qidle import main


if __name__ == '__main__':
    main()
