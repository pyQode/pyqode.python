"""
Minimal example showing the use of the PEP8CheckerMode.
"""
import logging
logging.basicConfig(level=logging.DEBUG)
import sys

from pyqode.qt import QtWidgets
from pyqode.core.api import CodeEdit
from pyqode.core.panels import CheckerPanel
from pyqode.python.backend import server
from pyqode.python.modes import PEP8CheckerMode, PythonSH


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    editor = CodeEdit()
    editor.backend.start(server.__file__)
    editor.resize(800, 600)
    print(editor.modes.append(PEP8CheckerMode()))
    editor.modes.append(PythonSH(editor.document()))  # looks better
    editor.panels.append(CheckerPanel())
    editor.show()
    editor.setPlainText('class Foo:\n\n\ndef __init__(self):\n\npass',
                        'text/x-python', 'utf-8')
    app.exec_()
    editor.close()
    del editor
    del app
