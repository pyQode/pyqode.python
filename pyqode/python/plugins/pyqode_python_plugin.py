#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2013 Colin Duquesnoy
#
# This file is part of pyQode.
#
# pyQode is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# pyQode is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with pyQode. If not, see http://www.gnu.org/licenses/.
#
"""
This file contains all the pyQode QtDesigner plugins.

Installation:
==================

run designer.pyw (Qt Designer must be installed on your system and must be
in your path on Windows)
"""
# This only works with PyQt, PySide does not support the QtDesigner module
import os
if not 'QT_API' in os.environ:
    os.environ.setdefault("QT_API", "PyQt")
import pyqode.python

PLUGINS_TYPES = {'QPythonCodeEdit': pyqode.python.QPythonCodeEdit}

try:
    from pyqode.core.plugins.pyqode_core_plugin import QCodeEditPlugin

    class QPythonCodeEditPlugin(QCodeEditPlugin):
        _module = 'pyqode.python'        # path to the widget's module
        _class = 'QPythonCodeEdit'    # name of the widget class
        _name = "QPythonCodeEdit"
        _icon = None
        _type = pyqode.python.QPythonCodeEdit

        def createWidget(self, parent):
            return pyqode.python.QPythonCodeEdit(parent)
except ImportError:
    print("Cannot use pyQode plugins without PyQt4")
