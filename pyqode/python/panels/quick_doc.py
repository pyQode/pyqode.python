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
Contains the quick documentation panel
"""
from docutils.core import publish_parts
from PyQt4 import QtGui
from pyqode.core.editor import Panel
from pyqode.core.api.system import drift_color
from pyqode.python.workers import quick_doc


class QuickDocPanel(Panel):
    """
    This panel quickly shows the documentation of the symbol under
    cursor.
    """
    STYLESHEET = """

    QTextEdit
    {
        background-color: %(tooltip)s;
        color: %(color)s;
    }

    QPushButton
    {
        color: %(color)s;
        background-color: transparent;
        padding: 5px;
        border: none;
    }

    QPushButton:hover
    {
        background-color: %(highlight)s;
        border: none;
        border-radius: 5px;
        color: %(color)s;
    }

    QPushButton:pressed, QCheckBox:pressed
    {
        border: 1px solid %(bck)s;
    }

    QPushButton:disabled
    {
        color: %(highlight)s;
    }
    """

    _KEYS = ["panelBackground", "background", "panelForeground",
             "panelHighlight"]

    #: Mode identifier
    IDENTIFIER = "quickDocPanel"

    #: Mode description
    DESCRIPTION = __doc__

    def __init__(self):
        super(QuickDocPanel, self).__init__()
        # layouts
        layout = QtGui.QHBoxLayout()
        self.setLayout(layout)
        child_layout = QtGui.QVBoxLayout()

        # A QTextEdit to show the doc
        self.text_edit = QtGui.QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setAcceptRichText(True)
        layout.addWidget(self.text_edit)

        # A QPushButton (inside a child layout for a better alignment)
        # to close the panel
        self.bt_close = QtGui.QPushButton()
        self.bt_close.setIcon(QtGui.QIcon.fromTheme(
            "application-exit", QtGui.QIcon(":/pyqode-icons/rc/close.png")))
        self.bt_close.clicked.connect(self.hide)
        child_layout.addWidget(self.bt_close)
        child_layout.addStretch()
        layout.addLayout(child_layout)

        # Action
        self.action_quick_doc = QtGui.QAction("Show documentation", self)
        self.action_quick_doc.setShortcut("Alt+Q")

        self.action_quick_doc.triggered.connect(self._on_action_quick_doc_triggered)

    def _reset_stylesheet(self):
        highlight = drift_color(self.editor.palette().window().color())
        stylesheet = self.STYLESHEET % {
            "tooltip": self.editor.palette().toolTipBase().color().name(),
            "bck": self.editor.palette().window().color().name(),
            "color": self.editor.palette().windowText().color().name(),
            "highlight": highlight.name()}
        self.setStyleSheet(stylesheet)

    def _on_install(self, editor):
        super(QuickDocPanel, self)._on_install(editor)
        self._reset_stylesheet()
        self.setVisible(False)

    def _on_state_changed(self, state):
        super(QuickDocPanel, self)._on_state_changed(state)
        if state:
            self.editor.add_action(self.action_quick_doc)
        else:
            self.editor.remove_action(self.action_quick_doc)

    def _on_style_changed(self, section, key):
        super(QuickDocPanel, self)._on_style_changed(section, key)
        if key in self._KEYS or not key:
            self._reset_stylesheet()

    def _on_action_quick_doc_triggered(self):
        tc = self.editor.select_word_under_cursor(select_whole_word=True)
        request_data = {
            'code': self.editor.toPlainText(),
            'line': tc.blockNumber() + 1,
            'column': tc.columnNumber(),
            'path': self.editor.file_path,
            'encoding': self.editor.file_encoding
        }
        self.editor.request_work(quick_doc, request_data,
                                 on_receive=self._on_results_available)

    def _on_results_available(self, status, results):
        if status:
            self.setVisible(True)
            if results:
                if len(results) and results[0] != "":
                    string = "\n\n".join(results)
                    string = publish_parts(
                        string, writer_name='html',
                        settings_overrides=
                        {'output_encoding': 'unicode'})['html_body']
                    string = string.replace('colspan="2"', 'colspan="0"')
                    string = string.replace("<th ", '<th align="left" ')
                    string = string.replace(
                        '</tr>\n<tr class="field"><td>&nbsp;</td>', '')
                    if string:
                        self.text_edit.setText(string)

                else:
                    self.text_edit.setText("Documentation not found")
            else:
                self.text_edit.setText("Documentation not found")
