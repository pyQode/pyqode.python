# -*- coding: utf-8 -*-
"""
SymbolBrowserPanel
"""
import logging
from pyqode.core.frontend import Panel
from pyqode.core import frontend
from PyQt4 import QtGui, QtCore


def _logger():
    return logging.getLogger(__name__)


class SymbolBrowserPanel(Panel):
    """
    Show a combo box with the file definitions.

    Allow quick navigation in the file and sync with the cursor
    position.
    """

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
                frontend.get_mode(
                    self.editor,
                    'DocumentAnalyserMode').documentChanged.connect(
                    self._on_document_changed)
            except KeyError:
                _logger().warning("No DocumentAnalyserMode found, install it "
                                  "before SymbolBrowserPanel!")
        else:
            self.editor.cursorPositionChanged.disconnect(
                self._on_cursor_pos_changed)
            try:
                frontend.get_mode(
                    self.editor,
                    'DocumentAnalyserMode').documentChanged.disconnect(
                    self._on_document_changed)
            except KeyError:
                _logger().warning("No DocumentAnalyserMode found, install it "
                                  "before SymbolBrowserPanel!")

    def _on_document_changed(self):
        try:
            mode = frontend.get_mode(self.editor, 'DocumentAnalyserMode')
        except KeyError:
            definitions = []
        else:
            definitions = mode.flattened_results
        self.combo_box.clear()
        if definitions:
            self.combo_box.addItem(" < Select a symbol >")
        else:
            self.combo_box.addItem("No symbols")
        for d in definitions:
            try:
                self.combo_box.addItem(QtGui.QIcon(d.icon), d.name, d)
            except TypeError:
                # skip un-named elements, sometimes jedi fail to
                # to get a variable name and return a list instead
                # of a string.
                pass
        self._definitions = definitions
        self._sync_combo_box(frontend.current_line_nbr(self.editor))

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
        line = frontend.current_line_nbr(self.editor)
        if self._prevLine != line:
            self._sync_combo_box(line)
        self._prevLine = line
