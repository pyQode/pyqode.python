"""
This simple example shows you how to use the pre-configured python editor.
"""
import logging
logging.basicConfig()
# optionally, set the qt api to use (in ['pyqt4', 'pyqt5', 'pyside'])
# import os; os.environ['QT_API'] = 'pyside'
import sys
from pyqode.qt import QtWidgets
from pyqode.python.backend import server
from pyqode.python.widgets import PyCodeEdit
from pyqode.python.widgets import code_edit


app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
editor = PyCodeEdit(server_script=server.__file__)
# show the PyCodeEdit module in the editor
editor.file.open(code_edit.__file__.replace('.pyc', '.py'))
window.setCentralWidget(editor)
window.show()
app.exec_()
