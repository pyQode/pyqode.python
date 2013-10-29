"""
Simple example on how to use a Bootstrapper to preload modules at startup and
show a splash screen while preloading.
"""
import sys
import logging
import pyqode.core
import pyqode.python
from pyqode.qt import QtGui


def main():
    app = QtGui.QApplication(sys.argv)
    # create the bootstrapper
    bootstrapper = pyqode.python.Bootstrapper(["numpy", "pyqode.qt.QtGui",
                                               "pyqode.qt.QtCore"])

    splash = QtGui.QSplashScreen(QtGui.QPixmap(800, 600))
    bootstrapper.preLoadFinished.connect(splash.close)

    # bootstrap and show splash
    bootstrapper.bootstrap()
    splash.show()
    app.processEvents()

    # create the window and open a file
    window = QtGui.QMainWindow()
    bootstrapper.preLoadFinished.connect(window.show)
    editor = pyqode.python.QPythonCodeEdit()
    editor.openFile(__file__)
    window.setCentralWidget(editor)
    window.resize(800, 600)

    app.exec_()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
