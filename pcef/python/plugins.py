"""
This file contains all the PCEF QtDesigner plugins.

Installation:
==================

run designer.pyw (Qt Designer must be installed on your system and must be
in your path on Windows)
"""
# This only works with PyQt, PySide does not support the QtDesigner module
import os
import PyQt4
import pcef.python
from pcef.core.plugins import QCodeEditPlugin
from PyQt4.QtGui import QApplication

os.environ.setdefault("QT_API", "PyQt")


class QPythonCodeEditPlugin(QCodeEditPlugin):
    _module = 'pcef'        # path to the widget's module
    _class = 'QPythonCodeEdit'    # name of the widget class
    _name = "QPythonCodeEdit"
    _icon = None

    def createWidget(self, parent):
        return pcef.python.QPythonCodeEdit(parent)
