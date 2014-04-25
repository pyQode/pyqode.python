#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integrates the generic editor using the pyQode qt designer plugin.
"""
import logging
import os
import sys

from PyQt4 import QtCore, QtGui

from pyqode.core import frontend
from pyqode.python.backend import server

from ui.python_editor_ui import Ui_MainWindow


class PythonEditorWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # starts pyqode server
        frontend.start_server(self.editor, server.__file__)

        # Setup menus
        mnu = QtGui.QMenu("Edit", self.menubar)
        mnu.addActions(self.editor.actions())
        self.menubar.addMenu(mnu)
        self.setupStylesMenu()
        self.setupModesMenu()
        self.setupPanelsMenu()
        self.setupPanelsMenu()

        # connect to editor signals
        self.editor.dirty_changed.connect(self.actionSave.setEnabled)
        self.actionSave.triggered.connect(self.save)
        self.actionOpen.triggered.connect(self.on_actionOpen_triggered)

        # handle assignment that are out of the current document
        frontend.get_mode(
            self.editor, 'GoToAssignmentsMode').outOfDocument.connect(
            self.onOutOfDocument)

        # open ourself
        frontend.open_file(self.editor, __file__)

    def setupStylesMenu(self):
        group = QtGui.QActionGroup(self)
        group.addAction(self.actionLight)
        self.actionLight.setChecked(True)
        self.acceptDrops()
        group.addAction(self.actionDark)
        group.triggered.connect(self.changeStyle)

    def setupModesMenu(self):
        for k, v in sorted(frontend.get_modes(self.editor).items()):
            a = QtGui.QAction(self.menuModes)
            a.setText(k)
            a.setCheckable(True)
            a.setChecked(True)
            a.changed.connect(self.onModeCheckStateChanged)
            a.mode = v
            self.menuModes.addAction(a)

    def setupPanelsMenu(self):
        for zones, panel_dic in sorted(frontend.get_panels(
                self.editor).items()):
            for k, v in panel_dic.items():
                a = QtGui.QAction(self.menuModes)
                a.setText(k)
                a.setCheckable(True)
                a.setChecked(True)

                a.changed.connect(self.onPanelCheckStateChanged)
                a.panel = v
                self.menuPanels.addAction(a)

    @QtCore.pyqtSlot(object)
    def onOutOfDocument(self, definition):
        QtGui.QMessageBox.warning(self, "Out of document",
                                  "%s is defined out of the current document. "
                                  "An IDE will typically open a new tab." %
                                  definition.full_name)

    @QtCore.pyqtSlot()
    def changeStyle(self):
        if self.actionLight.isChecked():
            self.editor.use_white_style()
        elif self.actionDark.isChecked():
            self.editor.use_dark_style()

    @QtCore.pyqtSlot()
    def on_actionOpen_triggered(self):
        filePath = QtGui.QFileDialog.getOpenFileName(
            self, "Choose a file", os.path.expanduser("~"))
        if filePath:
            frontend.open_file(self.editor, filePath)

    @QtCore.pyqtSlot()
    def onPanelCheckStateChanged(self):
        action = self.sender()
        action.panel.enabled = action.isChecked()

    @QtCore.pyqtSlot()
    def onModeCheckStateChanged(self):
        action = self.sender()
        action.get_mode.enabled = action.isChecked()

    @QtCore.pyqtSlot()
    def save(self):
        frontend.save_to_file(self.editor)


def main():
    logging.basicConfig(level=logging.INFO)
    app = QtGui.QApplication(sys.argv)
    win = PythonEditorWindow()
    win.show()
    app.exec_()
    frontend.stop_server(win.editor)
    del win
    del app


if __name__ == "__main__":
    main()
