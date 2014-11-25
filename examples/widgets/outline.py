"""
This example show you how to use the PyOuytlineTreeWidget to show the structure
of a python document.

The widget works in combination with a DocumentAnalyserMode. Such a mode must
be installed on the editor widget otherwise no data will be displayed.
"""
import sys
from pyqode.qt import QtCore, QtWidgets
from pyqode.core.api import code_edit
from pyqode.python.widgets import PyCodeEdit, PyOutlineTreeWidget


app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
editor = PyCodeEdit()
editor.file.open(code_edit.__file__)
window.setCentralWidget(editor)
window.resize(800, 600)
outline = PyOutlineTreeWidget()
outline.set_editor(editor)
dock_outline = QtWidgets.QDockWidget('Outline')
dock_outline.setWidget(outline)
window.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock_outline)
window.show()
app.exec_()