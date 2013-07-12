#!/usr/bin/env python3
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
import os
import sys
os.environ.setdefault("QT_API", "PyQt")
from pcef.qt import QtCore, QtGui
from pcef.core import FoldingIndicator
if sys.version_info[0] == 3:
    from examples.gui_integration.ui.python_editor_ui3 import Ui_MainWindow
    logging.info("Using python3")
else:
    from examples.gui_integration.ui.python_editor_ui import Ui_MainWindow
    logging.info("Using python2")
 

class PythonEditorWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.editor.foldingPanel.addIndicator(FoldingIndicator(22, 30))
        self.editor.dirtyChanged.connect(self.actionSave.setEnabled)
        self.actionSave.triggered.connect(self.editor.saveToFile)
        mnu = QtGui.QMenu("Edit", self.menubar)
        mnu.addActions(self.editor.actions())
        self.menubar.addMenu(mnu)
        # Add modes to the modes menu
        for k, v in self.editor.modes().items():
            a = QtGui.QAction(self.menuModes)
            a.setText(k)
            a.setCheckable(True)
            a.setChecked(True)
            a.changed.connect(self.onModeCheckStateChanged)
            a.mode = v
            self.menuModes.addAction(a)
        # Add panels to the panels menu
        for zones, panel_dic in self.editor.panels().items():
            for k, v in panel_dic.items():
                a = QtGui.QAction(self.menuModes)
                a.setText(k)
                a.setCheckable(True)
                a.setChecked(True)
                a.changed.connect(self.onPanelCheckStateChanged)
                a.panel = v
                self.menuPanels.addAction(a)
        try:
            self.editor.openFile(__file__)
        except (OSError, IOError) as e:
            pass
        except AttributeError:
            pass
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
    app.exec_()

if __name__ == "__main__":
    main()


