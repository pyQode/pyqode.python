"""
This is a simple test script to that is meant to be run by Travis CI to ensure
everything works properly foreach bindings on each supported python
version (2.7, 3.2, 3.3).

It runs a QApplication and shows a QPythonCodeEdit for 500ms.
"""
import sys
from pcef.qt import QtCore, QtGui
from pcef.python import QPythonCodeEdit


def leave():
    app = QtGui.QApplication.instance()
    app.exit(0)


def main():
    app = QtGui.QApplication(sys.argv)
    editor = QPythonCodeEdit()
    editor.show()
    editor.openFile(__file__)
    QtCore.QTimer.singleShot(7000, leave)
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
