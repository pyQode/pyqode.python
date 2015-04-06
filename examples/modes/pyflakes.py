"""
Minimal example showing the use of the FrostedCheckerMode.

We use Frosted (a fork of pyFlakes) that provides an easier API for running
pyFlakes on strings (instead of files).
"""
import logging
from pyqode.core.panels import CheckerPanel

logging.basicConfig(level=logging.DEBUG)
import sys

from pyqode.qt import QtWidgets
from pyqode.core.api import CodeEdit
from pyqode.python.backend import server
from pyqode.python.modes import PyFlakesChecker, PythonSH


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    editor = CodeEdit()
    editor.backend.start(server.__file__)
    editor.resize(800, 600)
    print(editor.modes.append(PyFlakesChecker()))
    editor.modes.append(PythonSH(editor.document()))  # looks better
    editor.panels.append(CheckerPanel())
    editor.show()
    editor.setPlainText('print("foo\n', 'text/x-python', 'utf-8')
    app.exec_()
    editor.close()
    del editor
    del app
