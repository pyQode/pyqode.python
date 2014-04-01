#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integrates the generic editor using the pyQode qt designer plugin.
"""
import logging
logging.basicConfig(level=logging.INFO)
import os
import sys
from PyQt4 import QtCore, QtGui
from ui.python_editor_ui import Ui_MainWindow

from pyqode.core import client


class PythonEditorWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.editor.start_server(args=['-s', os.getcwd()])
        self.actionOpen.setIcon(
            QtGui.QIcon.fromTheme(
                "document-open", QtGui.QIcon(":/example_icons/rc/folder.png")))
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
        self.editor.get_mode('GoToAssignmentsMode').outOfDocument.connect(
            self.onOutOfDocument)

        # open ourself
        self.editor.open_file(__file__)

    def onOutOfDocument(self, definition):
        QtGui.QMessageBox.warning(self, "Out of document",
                                  "%s is defined out of the current document. "
                                  "An IDE will typically open a new tab." %
                                  definition.full_name)

    def setupStylesMenu(self):
        group = QtGui.QActionGroup(self)
        group.addAction(self.actionLight)
        self.actionLight.setChecked(True)
        self.acceptDrops()
        group.addAction(self.actionDark)
        group.triggered.connect(self.changeStyle)

    def setupModesMenu(self):
        for k, v in sorted(self.editor.get_modes().items()):
            a = QtGui.QAction(self.menuModes)
            a.setText(k)
            a.setCheckable(True)
            a.setChecked(True)
            a.changed.connect(self.onModeCheckStateChanged)
            a.mode = v
            self.menuModes.addAction(a)

    def setupPanelsMenu(self):
        for zones, panel_dic in sorted(self.editor.get_panels().items()):
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
            self.editor.use_white_style()
        elif action == self.actionDark:
            self.editor.use_dark_style()

    @QtCore.pyqtSlot()
    def on_actionOpen_triggered(self):
        filePath = QtGui.QFileDialog.getOpenFileName(
            self, "Choose a file", os.path.expanduser("~"))
        if filePath:
            self.editor.open_file(filePath)

    def onPanelCheckStateChanged(self):
        action = self.sender()
        action.panel.enabled = action.isChecked()

    def onModeCheckStateChanged(self):
        action = self.sender()
        action.get_mode.enabled = action.isChecked()


def main():
    app = QtGui.QApplication(sys.argv)
    win = PythonEditorWindow()
    win.show()
    app.exec_()
    client.stop_server(win.editor)
    del win
    del app

if __name__ == "__main__":
    main()
