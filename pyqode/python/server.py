#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#The MIT License (MIT)
#
#Copyright (c) <2013-2014> <Colin Duquesnoy and others, see AUTHORS.txt>
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.
#
"""
Server main script customised for pyqode.python.

Users of pyqode.python can directly use this script. If you need to append
directories to sys.path, use the '-s' command line arguments, e.g.::

    python server.py 8080 -s /home/your_name/MyProj /home/your_name/MyLib

"""
import sys
from pyqode.core.api import code_completion
from pyqode.core.api import server
from pyqode.core.api import workers
from pyqode.python import code_completion as py_code_completion


if __name__ == '__main__':
    # setup argument parser and parse command line args
    parser = server.default_parser()
    parser.add_argument('-s', '--syspath', nargs='*')
    args = parser.parse_args()

    # add user paths to sys.path
    if args.syspath:
        for path in args.syspath:
            sys.path.insert(0, path)

    # setup completion providers
    workers.CodeCompletion.providers.append(py_code_completion.JediProvider())
    workers.CodeCompletion.providers.append(
        code_completion.DocumentWordsProvider())

    # starts the server
    server.run(args)
