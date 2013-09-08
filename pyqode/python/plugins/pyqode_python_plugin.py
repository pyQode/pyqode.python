#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#The MIT License (MIT)
#
#Copyright (c) <2013> <Colin Duquesnoy and others, see AUTHORS.txt>
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
