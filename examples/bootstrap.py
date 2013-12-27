#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#The MIT License (MIT)
#
#Copyright (c) <2013> <Colin Duquesnoy and others, see AUTHORS.txt>
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.
#
"""
Simple example on how to use a Bootstrapper to preload modules at startup and
show a splash screen while preloading.
"""
import sys
import logging
logging.basicConfig(level=logging.INFO)
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
    main()
