#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# PCEF - Python/Qt Code Editing Framework
# Copyright 2013, Colin Duquesnoy <colin.duquesnoy@gmail.com>
#
# This software is released under the LGPLv3 license.
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""
Integrates the generic editor using the pcef qt designer plugin.
"""
import logging
logging.basicConfig(level=logging.INFO)
import sys
from pcef.qt import QtCore, QtGui
from ui import loadUi


class PythonEditorWindow(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        loadUi("python_editor.ui", self, rcFilename="examples.qrc")
        if QtGui.QIcon.hasThemeIcon("document-save"):
            self.actionSave.setIcon(QtGui.QIcon.fromTheme("document-save"))
        if QtGui.QIcon.hasThemeIcon("document-open"):
            self.actionOpen.setIcon(QtGui.QIcon.fromTheme("document-open"))
        mnu = QtGui.QMenu("Edit", self.menubar)
        mnu.addActions(self.editor.actions())
        self.menubar.addMenu(mnu)
        self.setupStylesMenu()
        self.setupModesMenu()
        self.setupPanelsMenu()
        try:
            self.editor.openFile(__file__)
        except (OSError, IOError):
            pass
        except AttributeError:
            pass

    def setupStylesMenu(self):
        group = QtGui.QActionGroup(self)
        group.addAction(self.actionLight)
        self.actionLight.setChecked(True)
        group.addAction(self.actionDark)
        group.triggered.connect(self.changeStyle)

    def setupModesMenu(self):
        for k, v in self.editor.modes().items():
            a = QtGui.QAction(self.menuModes)
            a.setText(k)
            a.setCheckable(True)
            a.setChecked(True)
            a.changed.connect(self.onModeCheckStateChanged)
            a.mode = v
            self.menuModes.addAction(a)

    def setupPanelsMenu(self):
        for zones, panel_dic in self.editor.panels().items():
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
