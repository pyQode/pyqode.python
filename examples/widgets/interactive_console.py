"""
This example show you how to use the PyInteractiveConsole. We run a python
script which raises an exception. The exception traceback will be highlighted
differently than the rest of the process output and each module file path are
clickable by the user. We open an editor to show the specified module at the
specified line.
"""
import os
import sys
from pyqode.core.api import TextHelper
from pyqode.qt import QtWidgets
from pyqode.python.widgets import PyInteractiveConsole, PyCodeEdit


editor_windows = []


def open_editor(path, line):
    global editor_windows
    print(path, line)
    editor = PyCodeEdit()
    # prevent the restoration of cursor position which will reset the position
    # we will set after opening the file
    editor.file.restore_cursor = False
    editor.file.open(path)
    TextHelper(editor).goto_line(line)
    editor.show()
    editor_windows.append(editor)


app = QtWidgets.QApplication(sys.argv)
console = PyInteractiveConsole()
console.open_file_requested.connect(open_editor)
console.start_process(sys.executable, [
    os.path.join(os.getcwd(), 'interactive_process.py')])
console.show()
app.exec_()
