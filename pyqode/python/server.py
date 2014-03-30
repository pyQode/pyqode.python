#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Server main script customised for pyqode.python.

Users of pyqode.python can directly use this script. If you need to append
directories to sys.path, use the '-s' command line arguments, e.g.::

    python server.py 8080 -s /home/your_name/MyProj /home/your_name/MyLib


The server can be run with a custom python interpreter, this is needed if you
want to support python 2 syntax or virtualenv. This means that pyqode.core,
pyqode.python and all their pure python dependencies (not PyQt) must be
installed in the targeted env (virtualenv or python2 site package). Another
option is to bundle all dependencies in a zip archive that the server will
append to sys path, that way you don't clutter the use1r env with IDE specific
package but you have to write a new server to do that.

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
