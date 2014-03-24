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
from pyqode.core import logger
from pyqode.core.editor import Panel
from PyQt4 import QtGui, QtCore


class SymbolBrowserPanel(Panel):
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
        self.combo_box = QtGui.QComboBox()
        self.combo_box.setSizeAdjustPolicy(
            self.combo_box.AdjustToMinimumContentsLength)
        self.combo_box.activated.connect(self._on_definition_activated)
        layout.addWidget(self.combo_box)
        self.setLayout(layout)
        self.combo_box.addItem("Loading symbols...")

    def _on_state_changed(self, state):
        super(SymbolBrowserPanel, self)._on_state_changed(state)
        if state:
            self.editor.cursorPositionChanged.connect(
                self._on_cursor_pos_changed)
            try:
                self.editor.documentAnalyserMode.documentChanged.connect(
                    self._on_document_changed)
            except AttributeError:
                logger.warning("DocumentAnalyserMode, install it "
                               "before SymbolBrowserPanel!")
        else:
            self.editor.cursorPositionChanged.disconnect(
                self._on_cursor_pos_changed)
            try:
                self.editor.documentAnalyserMode.documentChanged.disconnect(
                    self._on_document_changed)
            except AttributeError:
                logger.warning("DocumentAnalyserMode, install it "
                               "before SymbolBrowserPanel!")

    def _on_document_changed(self):
        definitions = self.editor.documentAnalyserMode.flattend_results
        self.combo_box.clear()
        if definitions:
            self.combo_box.addItem(" < Select a symbol >")
        else:
            self.combo_box.addItem("No symbols")
        for d in definitions:
            try:
                self.combo_box.addItem(QtGui.QIcon(d.icon), d.name, d)
            except TypeError:
                pass  # skip anonym elements, sometimes jedi fail to
                      # to get a variable name and return a list instead
                      # of a string.
        self._definitions = definitions
        self._sync_combo_box(self.editor.cursor_position[0])

    @QtCore.pyqtSlot(int)
    def _on_definition_activated(self, index):
        definition = self.combo_box.itemData(index)
        if definition:
            self.editor.goto_line(definition.line, column=definition.column)

    def _sync_combo_box(self, line):
        i = -1
        for i, d in enumerate(reversed(self._definitions)):
            if d.line <= line:
                break
        if i >= 0:
            index = len(self._definitions) - i
            self.combo_box.setCurrentIndex(index)

    def _on_cursor_pos_changed(self):
        line = self.editor.cursor_position[0]
        if self._prevLine != line:
            self._sync_combo_box(line)
        self._prevLine = line
