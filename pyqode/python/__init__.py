# -*- coding: utf-8 -*-
"""
pyqode.python is an extension of pyqode.core that brings support
for the python programming language. It does so by providing a set
of additional modes and panels for the frontend and by supplying
dedicated workers for the backend.

"""
__version__ = '2.4.dev'

try:
    # load pyqode.python resources (code completion icons)
    from pyqode.python._forms import pyqode_python_icons_rc  # DO NOT REMOVE!!!
except ImportError:
    # PyQt/PySide might not be available for the interpreter that run the
    # backend
    pass
