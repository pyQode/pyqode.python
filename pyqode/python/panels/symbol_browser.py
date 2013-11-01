"""
SymbolBrowserPanel
"""
import pyqode.core
from pyqode.qt import QtGui




class SymbolBrowserPanel(pyqode.core.Panel):
    def __init__(self):
        super(SymbolBrowserPanel, self).__init__()
        layout = QtGui.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.comboBox = QtGui.QComboBox()
        layout.addWidget(self.comboBox)
        self.setLayout(layout)
        self.comboBox.addItem("<Select a symbol>")

    def _onInstall(self, editor):
        super(SymbolBrowserPanel, self)._onInstall(editor)
        self.comboBox.setFont(self.editor.font())
