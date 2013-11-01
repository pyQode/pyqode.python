"""
SymbolBrowserPanel
"""
import pyqode.core
from pyqode.qt import QtGui, QtCore


class SymbolBrowserPanel(pyqode.core.Panel):
    def __init__(self):
        super(SymbolBrowserPanel, self).__init__()
        self._prevLine = -1
        self._definitions = []
        layout = QtGui.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.comboBox = QtGui.QComboBox()
        self.comboBox.setSizeAdjustPolicy(self.comboBox.AdjustToMinimumContentsLength)
        self.comboBox.activated.connect(self._onDefinitionActivated)
        layout.addWidget(self.comboBox)
        self.setLayout(layout)
        self.comboBox.addItem("Loading symbols...")

    def _onStateChanged(self, state):
        if state:
            self.editor.cursorPositionChanged.connect(
                self._onCursorPositionChanged)
            try:
                self.editor.documentAnalyserMode.documentChanged.connect(
                    self._onDocumentChanged)
            except AttributeError:
                pyqode.core.logger.warning("DocumentAnalyserMode, install it "
                                           "before SymbolBrowserPanel!")
        else:
            self.editor.cursorPositionChanged.disconnect(
                self._onCursorPositionChanged)
            try:
                self.editor.documentAnalyserMode.documentChanged.disconnect(
                    self._onDocumentChanged)
            except AttributeError:
                pyqode.core.logger.warning("DocumentAnalyserMode, install it "
                                           "before SymbolBrowserPanel!")

    def _onDocumentChanged(self):
        definitions = self.editor.documentAnalyserMode.flattenedResults
        self.comboBox.clear()
        self.comboBox.addItem(" < Select a symbol >")
        for d in definitions:
            if isinstance(d.full_name, list):
                d.full_name = d.name
            self.comboBox.addItem(QtGui.QIcon(d.icon), d.full_name, d)
        self._definitions = definitions

    @QtCore.Slot(int)
    def _onDefinitionActivated(self, index):
        definition = self.comboBox.itemData(index)
        if definition:
            self.editor.gotoLine(definition.line, column=definition.column)

    def _onCursorPositionChanged(self):
        line = self.editor.cursorPosition[0]
        if self._prevLine != line:
            i = -1
            for i, d in enumerate(reversed(self._definitions)):
                if d.line <= line:
                    break
            if i >= 0:
                self.comboBox.setCurrentIndex(len(self._definitions) - i)
        self._prevLine = line
