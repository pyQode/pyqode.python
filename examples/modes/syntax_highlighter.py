"""
Minimal example showing the use of the PythonSH mode.
"""
import logging
logging.basicConfig(level=logging.DEBUG)
import sys

from pyqode.qt import QtWidgets
from pyqode.core.api import CodeEdit, ColorScheme
from pyqode.python.backend import server
from pyqode.python.modes import PythonSH


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    editor = CodeEdit()
    editor.backend.start(server.__file__)
    editor.resize(800, 600)
    # add a native python syntax highlighter
    sh = editor.modes.append(PythonSH(editor.document()))
    # change its color scheme (from pygments)
    sh.color_scheme = ColorScheme('monokai')
    editor.show()
    editor.file.open(__file__)
    app.exec_()
    editor.close()
    del editor
    del app
