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
import argparse
import sys


if __name__ == '__main__':
    """
    Server process' entry point
    """
    # setup argument parser and parse command line args
    parser = argparse.ArgumentParser()
    parser.add_argument("port", help="the local tcp port to use to run "
                        "the server")
    parser.add_argument('-s', '--syspath', nargs='*')
    args = parser.parse_args()

    # add user paths to sys.path
    if args.syspath:
        for path in args.syspath:
            print('append path %s to sys.path\n' % path)
            sys.path.append(path)

    from pyqode.core import backend
    from pyqode.python.backend.workers import JediCompletionProvider

    # setup completion providers
    backend.CodeCompletionWorker.providers.append(JediCompletionProvider())
    backend.CodeCompletionWorker.providers.append(
        backend.DocumentWordsProvider())

    # starts the server
    backend.serve_forever(args)
