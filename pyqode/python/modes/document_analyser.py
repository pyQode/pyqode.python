# -*- coding: utf-8 -*-
import logging
from pyqode.core import api
from pyqode.core.api import Mode
from pyqode.core.api import DelayJobRunner
from pyqode.core.backend import NotConnected
from pyqode.python.backend.workers import Definition, defined_names
from pyqode.qt import QtCore


def _logger():
    return logging.getLogger(__name__)


class DocumentAnalyserMode(Mode, QtCore.QObject):
    """
    This mode analyses the structure of a document (a tree of
    :class:`pyqode.python.backend.workers.Definition`.

    :attr:`pyqode.python.modes.DocumentAnalyserMode.document_changed`
    is emitted whenever the document structure changed.

    To keep good performances, the analysis task is run when the application is
    idle for more than 1 second (by default).
    """
    #: Signal emitted when the document structure changed.
    document_changed = QtCore.Signal()

    def __init__(self, delay=1000):
        Mode.__init__(self)
        QtCore.QObject.__init__(self)
        self._jobRunner = DelayJobRunner(delay=delay)
        #: The list of results (elements might have children; this is actually
        #: a tree).
        self.results = []

    def on_state_changed(self, state):
        if state:
            self.editor.blockCountChanged.connect(self._on_line_count_changed)
            self.editor.new_text_set.connect(self._run_analysis)
        else:
            self.editor.blockCountChanged.disconnect(
                self._on_line_count_changed)
            self.editor.new_text_set.disconnect(self._run_analysis)

    def _on_line_count_changed(self, e):
        self._jobRunner.request_job(self._run_analysis)

    def _run_analysis(self):
        if self.editor and self.editor.toPlainText() and self.editor.file:
            request_data = {
                'code': self.editor.toPlainText(),
                'path': self.editor.file.path,
                'encoding': self.editor.file.encoding
            }
            try:
                self.editor.backend.send_request(
                    defined_names, request_data,
                    on_receive=self._on_results_available)
            except NotConnected:
                QtCore.QTimer.singleShot(100, self._run_analysis)
        else:
            self.results = []
            self.document_changed.emit()

    def _on_results_available(self, status, results):
        if results:
            results = [Definition().from_dict(ddict) for ddict in results]
        self.results = results
        if self.results is not None:
            _logger().debug("Document structure changed")
            self.document_changed.emit()

    @property
    def flattened_results(self):
        """
        Flattens the document structure tree as a simple sequential list.
        """
        ret_val = []
        for d in self.results:
            ret_val.append(d)
            for sub_d in d.children:
                nd = Definition(sub_d.name, sub_d.icon, sub_d.line,
                                sub_d.column, sub_d.full_name)
                nd.name = "  " + nd.name
                nd.full_name = "  " + nd.full_name
                ret_val.append(nd)
        return ret_val
