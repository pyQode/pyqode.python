"""
Minimal example showing the use of the CommentsMode.
"""
import logging
logging.basicConfig(level=logging.DEBUG)
import sys

from pyqode.qt import QtWidgets
from pyqode.core.api import CodeEdit
from pyqode.python.backend import server
from pyqode.python.modes import CommentsMode, PythonSH


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    editor = CodeEdit()
    editor.backend.start(server.__file__)
    editor.resize(800, 600)
    print(editor.modes.append(CommentsMode()))
    editor.modes.append(PythonSH(editor.document()))  # looks better
    editor.show()
    editor.appendPlainText(
'''# press Ctrl+/ to comment/uncomment selected text or the current line
class Foo:
    def bar(self):
        pass''')
    app.exec_()
    editor.close()
    del editor
    del app
