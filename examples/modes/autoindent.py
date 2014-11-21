"""
Minimal example showing the use of the AutoIndentMode.
"""
import logging
logging.basicConfig(level=logging.DEBUG)
import sys

from pyqode.qt import QtWidgets
from pyqode.core.api import CodeEdit
from pyqode.python.backend import server
from pyqode.core.modes import SymbolMatcherMode
from pyqode.python.modes import PyAutoIndentMode, PythonSH


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    editor = CodeEdit()
    editor.backend.start(server.__file__)
    editor.resize(800, 600)
    # PyAutoIndent needs the matcher mode and a syntax highlighter to work
    # properly
    editor.modes.append(PythonSH(editor.document()))
    editor.modes.append(SymbolMatcherMode())
    print(editor.modes.append(PyAutoIndentMode()))
    editor.show()
    editor.appendPlainText(
        'class Foo:')
    app.exec_()
    editor.close()
    del editor
    del app
