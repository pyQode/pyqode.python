# -*- coding: utf-8 -*-
#
#The MIT License (MIT)
#
#Copyright (c) <2013-2014> <Colin Duquesnoy and others, see AUTHORS.txt>
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
        if definitions:
            self.comboBox.addItem(" < Select a symbol >")
        else:
            self.comboBox.addItem("No symbols")
        for d in definitions:
            try:
                self.comboBox.addItem(QtGui.QIcon(d.icon), d.name, d)
            except TypeError:
                pass  # skip anonym elements, sometimes jedi fail to
                      # to get a variable name and return a list instead
                      # of a string.
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
