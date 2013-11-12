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
Integrates the generic editor using the pyQode qt designer plugin and shows
how to preload a list of modules and show the corresponding notification.

Preload will speed up code completions with big modules but will take a few
seconds. During this time, most of the operations are unavailable (
code completion, go to assignment, doc,...)

Note that this time may be multiplied by a factor of 10 the very first time
you run a pyqode.python application (up to 1 or 2 minutes on a low performance
netbook!)
"""
import logging
logging.basicConfig(level=logging.DEBUG)
import os
import sys
from pyqode.qt import QtCore, QtGui
import pyqode.core
import pyqode.python
from ui.python_editor_ui import Ui_MainWindow


class PythonEditorWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.actionOpen.setIcon(
            QtGui.QIcon.fromTheme("document-open", QtGui.QIcon(
                ":/example_icons/rc/folder.png")))
        self.actionSave.setIcon(
            QtGui.QIcon.fromTheme("document-save", QtGui.QIcon(
                ":/example_icons/rc/document-save.png")))
        mnu = QtGui.QMenu("Edit", self.menubar)
        mnu.addActions(self.editor.actions())
        self.menubar.addMenu(mnu)
        self.setupStylesMenu()
        self.setupModesMenu()
        self.setupPanelsMenu()

        # handle assignement that are out of the current document
        self.editor.gotoAssignmentsMode.outOfDocument.connect(
            self.onOutOfDocument)
        # preload a set of modules and show the preload operation in the
        # PreLoadPanel
        self.editor.installPanel(pyqode.python.PreLoadPanel(),
                                 pyqode.core.PanelPosition.TOP)
        self.editor.setModulesToPreload(["sys", "os", "pyqode.qt.QtGui",
                                         "pyqode.qt.QtCore",
                                         "pyqode.qt.QtGui.QMainWindow"])
        try:
            self.editor.openFile(__file__)
        except (OSError, IOError):
            pass
        except AttributeError:
            pass

    def onOutOfDocument(self, definition):
        QtGui.QMessageBox.warning(self, "Out of document",
                                  "%s is defined out of the current document. "
                                  "An IDE will typically open a new tab." %
                                  definition.full_name)

    def setupStylesMenu(self):
        group = QtGui.QActionGroup(self)
        group.addAction(self.actionLight)
        self.actionLight.setChecked(True)
        group.addAction(self.actionDark)
        group.triggered.connect(self.changeStyle)

    def setupModesMenu(self):
        for k, v in sorted(self.editor.modes().items()):
            a = QtGui.QAction(self.menuModes)
            a.setText(k)
            a.setCheckable(True)
            a.setChecked(True)
            a.changed.connect(self.onModeCheckStateChanged)
            a.mode = v
            self.menuModes.addAction(a)

    def setupPanelsMenu(self):
        for zones, panel_dic in sorted(self.editor.panels().items()):
            for k, v in panel_dic.items():
                a = QtGui.QAction(self.menuModes)
                a.setText(k)
                a.setCheckable(True)
                a.setChecked(True)
                a.changed.connect(self.onPanelCheckStateChanged)
                a.panel = v
                self.menuPanels.addAction(a)

    def changeStyle(self, action):
        if action == self.actionLight:
            self.editor.useLightStyle()
        elif action == self.actionDark:
            self.editor.useDarkStyle()

    @QtCore.Slot()
    def on_actionOpen_triggered(self):
        filePath = QtGui.QFileDialog.getOpenFileName(
            self, "Choose a file", os.path.expanduser("~"))
        if os.environ['QT_API'] == 'PySide':
            if filePath[0]:
                self.editor.openFile(filePath[0])
        else:
            if filePath:
                self.editor.openFile(filePath)

    def onPanelCheckStateChanged(self):
        action = self.sender()
        action.panel.enabled = action.isChecked()

    def onModeCheckStateChanged(self):
        action = self.sender()
        action.mode.enabled = action.isChecked()


def main():
    app = QtGui.QApplication(sys.argv)
    win = PythonEditorWindow()
    win.show()
    print(win.editor.settings.dump())
    print(win.editor.style.dump())
    app.exec_()

if __name__ == "__main__":
    main()
