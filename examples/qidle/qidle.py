#! /usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from qidle import main
import logging

if __name__ == '__main__':
    filename = None
    if sys.platform == 'win32':
        filename = 'qidle.log'
    logging.basicConfig(level=logging.INFO, filename=filename)
    main()
