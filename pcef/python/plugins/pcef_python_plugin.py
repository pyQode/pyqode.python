#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# PCEF - Python/Qt Code Editing Framework
# Copyright 2013, Colin Duquesnoy <colin.duquesnoy@gmail.com>
#
# This software is released under the LGPLv3 license.
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""
This file contains all the PCEF QtDesigner plugins.

Installation:
==================

run designer.pyw (Qt Designer must be installed on your system and must be
in your path on Windows)
"""
# This only works with PyQt, PySide does not support the QtDesigner module
import os
if not 'QT_API' in os.environ:
    os.environ.setdefault("QT_API", "PyQt")
import pcef.python

PLUGINS_TYPES = {'QPythonCodeEdit': pcef.python.QPythonCodeEdit}

try:
    from pcef.core.plugins.pcef_core_plugin import QCodeEditPlugin

    class QPythonCodeEditPlugin(QCodeEditPlugin):
        _module = 'pcef.python'        # path to the widget's module
        _class = 'QPythonCodeEdit'    # name of the widget class
        _name = "QPythonCodeEdit"
        _icon = None
        _type = pcef.python.QPythonCodeEdit

        def createWidget(self, parent):
            return pcef.python.QPythonCodeEdit(parent)
except ImportError:
    print("Cannot use pcef plugins without PyQt4")
