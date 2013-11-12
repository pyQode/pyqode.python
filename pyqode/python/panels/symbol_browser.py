"""
SymbolBrowserPanel
"""
import pyqode.core
from pyqode.qt import QtGui, QtCore


class SymbolBrowserPanel(pyqode.core.Panel):
    """
    Show a combo box with the file definitions.

    Allow quick navigation in the file and sync with the cursor
    position.
    """

    IDENTIFIER = "symbolBrowserPanel"
    DESCRIPTION = __doc__

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
        super(SymbolBrowserPanel, self)._onStateChanged(state)
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
            self.comboBox.addItem(QtGui.QIcon(d.icon), d.name, d)
        self._definitions = definitions
        self._syncComboBox(self.editor.cursorPosition[0])

    @QtCore.Slot(int)
    def _onDefinitionActivated(self, index):
        definition = self.comboBox.itemData(index)
        if definition:
            self.editor.gotoLine(definition.line, column=definition.column)

    def _syncComboBox(self, line):
        i = -1
        for i, d in enumerate(reversed(self._definitions)):
            if d.line <= line:
                break
        if i >= 0:
            index = len(self._definitions) - i
            self.comboBox.setCurrentIndex(index)

    def _onCursorPositionChanged(self):
        line = self.editor.cursorPosition[0]
        if self._prevLine != line:
            self._syncComboBox(line)
        self._prevLine = line
