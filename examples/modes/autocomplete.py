"""
Minimal example showing the use of the PyAutoCompleteMode.
"""
import logging
logging.basicConfig(level=logging.DEBUG)
import sys

from pyqode.qt import QtWidgets
from pyqode.core.api import CodeEdit
from pyqode.python.backend import server
from pyqode.python.modes import PyAutoCompleteMode


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    editor = CodeEdit()
    editor.backend.start(server.__file__)
    editor.resize(800, 600)
    print(editor.modes.append(PyAutoCompleteMode()))
    editor.appendPlainText(
        '# Please press "("\n'
        'class Foo:\n'
        '    def bar')
    editor.show()
    app.exec_()
    editor.close()
    del editor
    del app
