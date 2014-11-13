# -*- coding: utf-8 -*-
"""
pyqode.python is an extension of pyqode.core that brings support
for the python programming language. It provides a set of additional modes and
panels for the frontend and a series of worker for the backend (code
completion, documentation lookups, code linters, and so on...).

"""
__version__ = '2.4.dev'

try:
    # load pyqode.python resources (code completion icons)
    from pyqode.python._forms import pyqode_python_icons_rc  # DO NOT REMOVE!!!
except ImportError:
    # PyQt/PySide might not be available for the interpreter that run the
    # backend
    pass
