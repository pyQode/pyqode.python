# -*- coding: utf-8 -*-
"""
This is a simple test script to that is meant to be run by Travis CI to ensure
everything works properly foreach bindings on each supported python
version (3.2, 3.3, 3.4).

It runs a QApplication and shows a QPythonCodeEdit for 500ms.
"""
import sys
from PyQt4 import QtCore, QtGui
from pyqode.core import client
from pyqode.python.editor import QPythonCodeEdit

import logging
logging.basicConfig(level=True)


def leave():
    app = QtGui.QApplication.instance()
    app.exit(0)


def test_editor():
    app = QtGui.QApplication(sys.argv)
    editor = QPythonCodeEdit()
    editor.show()
    editor.start_server()
    editor.open_file(__file__)
    QtCore.QTimer.singleShot(500, leave)
    app.exec_()
    client.stop_server()
    del editor
    del app
