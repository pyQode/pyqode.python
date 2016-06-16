from pyqode.qt import QtWidgets
from pyqode.python.widgets import PyConsole


app = QtWidgets.QApplication([])
console = PyConsole(color_scheme='qt')
console.resize(800, 600)
# console.change_interpreter('python2')
console.show()

app.exec_()
