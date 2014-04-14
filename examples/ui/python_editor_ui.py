# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'python_editor.ui'
#
# Created: Mon Apr 14 21:15:15 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1078, 831)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setSpacing(1)
        self.gridLayout.setMargin(1)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.editor = QPythonCodeEdit(self.centralwidget)
        self.editor.setObjectName(_fromUtf8("editor"))
        self.gridLayout.addWidget(self.editor, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1078, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuSettings = QtGui.QMenu(self.menubar)
        self.menuSettings.setObjectName(_fromUtf8("menuSettings"))
        self.menuPanels = QtGui.QMenu(self.menuSettings)
        self.menuPanels.setObjectName(_fromUtf8("menuPanels"))
        self.menuModes = QtGui.QMenu(self.menuSettings)
        self.menuModes.setObjectName(_fromUtf8("menuModes"))
        self.menuStyle = QtGui.QMenu(self.menuSettings)
        self.menuStyle.setObjectName(_fromUtf8("menuStyle"))
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionOpen = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("document-open"))
        self.actionOpen.setIcon(icon)
        self.actionOpen.setIconVisibleInMenu(True)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setEnabled(False)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("document-save"))
        self.actionSave.setIcon(icon)
        self.actionSave.setIconVisibleInMenu(True)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionPanel = QtGui.QAction(MainWindow)
        self.actionPanel.setObjectName(_fromUtf8("actionPanel"))
        self.actionModes = QtGui.QAction(MainWindow)
        self.actionModes.setObjectName(_fromUtf8("actionModes"))
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionLight = QtGui.QAction(MainWindow)
        self.actionLight.setCheckable(True)
        self.actionLight.setObjectName(_fromUtf8("actionLight"))
        self.actionDark = QtGui.QAction(MainWindow)
        self.actionDark.setCheckable(True)
        self.actionDark.setObjectName(_fromUtf8("actionDark"))
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuStyle.addAction(self.actionLight)
        self.menuStyle.addAction(self.actionDark)
        self.menuSettings.addAction(self.menuPanels.menuAction())
        self.menuSettings.addAction(self.menuModes.menuAction())
        self.menuSettings.addAction(self.menuStyle.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionSave)

        self.retranslateUi(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "pyQode - Python Editor", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings", None))
        self.menuPanels.setTitle(_translate("MainWindow", "Panels", None))
        self.menuModes.setTitle(_translate("MainWindow", "Modes", None))
        self.menuStyle.setTitle(_translate("MainWindow", "Style", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.actionOpen.setText(_translate("MainWindow", "Open", None))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O", None))
        self.actionSave.setText(_translate("MainWindow", "Save", None))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S", None))
        self.actionPanel.setText(_translate("MainWindow", "Panel", None))
        self.actionModes.setText(_translate("MainWindow", "Modes", None))
        self.actionAbout.setText(_translate("MainWindow", "About", None))
        self.actionLight.setText(_translate("MainWindow", "Light", None))
        self.actionDark.setText(_translate("MainWindow", "Dark", None))

from pyqode.python.editor import QPythonCodeEdit
from . import editor_rc