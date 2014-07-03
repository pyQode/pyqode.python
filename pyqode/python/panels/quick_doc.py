# -*- coding: utf-8 -*-
"""
Contains the quick documentation panel
"""
from docutils.core import publish_parts
from pyqode.core.qt import QtGui, QtWidgets
from pyqode.core.api import Panel, TextHelper
from pyqode.core.api.utils import drift_color
from pyqode.python.backend.workers import quick_doc


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

    def __init__(self):
        super(QuickDocPanel, self).__init__()
        # layouts
        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)
        child_layout = QtWidgets.QVBoxLayout()

        # A QTextEdit to show the doc
        self.text_edit = QtWidgets.QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setAcceptRichText(True)
        layout.addWidget(self.text_edit)

        # A QPushButton (inside a child layout for a better alignment)
        # to close the panel
        self.bt_close = QtWidgets.QPushButton()
        self.bt_close.setIcon(QtGui.QIcon.fromTheme(
            "application-exit", QtGui.QIcon(":/pyqode-icons/rc/close.png")))
        self.bt_close.clicked.connect(self.hide)
        child_layout.addWidget(self.bt_close)
        child_layout.addStretch()
        layout.addLayout(child_layout)

        # Action
        self.action_quick_doc = QtWidgets.QAction("Show documentation", self)
        self.action_quick_doc.setShortcut("Alt+Q")

        self.action_quick_doc.triggered.connect(
            self._on_action_quick_doc_triggered)

    def _reset_stylesheet(self):
        highlight = drift_color(self.editor.palette().window().color())
        stylesheet = self.STYLESHEET % {
            "tooltip": self.editor.palette().toolTipBase().color().name(),
            "bck": self.editor.palette().window().color().name(),
            "color": self.editor.palette().windowText().color().name(),
            "highlight": highlight.name()}
        self.setStyleSheet(stylesheet)

    def on_install(self, editor):
        super(QuickDocPanel, self).on_install(editor)
        self._reset_stylesheet()
        self.setVisible(False)

    def on_state_changed(self, state):
        super().on_state_changed(state)
        if state:
            self.editor.add_action(self.action_quick_doc)
        else:
            self.editor.remove_action(self.action_quick_doc)

    def refresh_style(self):
        self._reset_stylesheet()

    def _on_action_quick_doc_triggered(self):
        tc = TextHelper(self.editor).word_under_cursor(select_whole_word=True)
        request_data = {
            'code': self.editor.toPlainText(),
            'line': tc.blockNumber() + 1,
            'column': tc.columnNumber(),
            'path': self.editor.file.path,
            'encoding': self.editor.file.encoding
        }
        self.editor.backend.send_request(
            quick_doc, request_data, on_receive=self._on_results_available)

    def _on_results_available(self, status, results):
        if status:
            self.setVisible(True)
            if results:
                if len(results) and results[0] != "":
                    string = "\n\n".join(results)
                    string = publish_parts(
                        string, writer_name='html',
                        settings_overrides={'output_encoding': 'unicode'})[
                            'html_body']
                    string = string.replace('colspan="2"', 'colspan="0"')
                    string = string.replace("<th ", '<th align="left" ')
                    string = string.replace(
                        '</tr>\n<tr class="field"><td>&nbsp;</td>', '')
                    if string:
                        skip_error_msg = False
                        print(string)
                        lines = []
                        for l in string.splitlines():
                            if (l.startswith('<div class="system-message"') or
                                    l.startswith(
                                        '<div class="last system-message"')):
                                skip_error_msg = True
                                continue
                            if skip_error_msg:
                                if l.endswith('</div>'):
                                    skip_error_msg = False
                            else:
                                lines.append(l)
                        self.text_edit.setText('\n'.join(lines))
                        return
            self.text_edit.setText("Documentation not found")
