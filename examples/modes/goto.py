"""
Minimal example showing the use of the GoToAssignmentsMode.
"""
import logging
logging.basicConfig(level=logging.DEBUG)
import sys

from pyqode.qt import QtWidgets
from pyqode.core.api import CodeEdit
from pyqode.python.backend import server
from pyqode.python.modes import GoToAssignmentsMode, PythonSH


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    editor = CodeEdit()
    editor.backend.start(server.__file__)
    editor.resize(800, 600)
    print(editor.modes.append(GoToAssignmentsMode()))
    editor.modes.append(PythonSH(editor.document()))  # looks better
    editor.show()
    editor.appendPlainText(
'''press_me = 10


def spam():
    # press Ctrl+Left click on ``press_me`` to go to its definition
    print(press_me)
''')
    app.exec_()
    editor.close()
    del editor
    del app
