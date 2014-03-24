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
import pyqode.core
from pyqode.core import logger
from pyqode.core.api import client
from pyqode.core.editor import Mode
from pyqode.core.api.system import DelayJobRunner
from pyqode.python.workers import Definition, defined_names
from PyQt4 import QtCore


class DocumentAnalyserMode(Mode, QtCore.QObject):
    """
    This mode analyses the structure of a document (a tree of
    :class:`pyqode.python.modes.document_analyser.Definition`.

    :attr:pyqode.python.DocumentAnalyserMode.documentChanged` is emitted
    whenever the document structure changed.

    To keep good performances, the analysis task is run when the application is
    idle for more than 1 second (by default).
    """
    IDENTIFIER = "documentAnalyserMode"
    DESCRIPTION = "Analysis the document structure on the fly"

    #: Signal emitted when the document structure changed.
    documentChanged = QtCore.pyqtSignal()

    def __init__(self, delay=1000):
        Mode.__init__(self)
        QtCore.QObject.__init__(self)
        self._jobRunner = DelayJobRunner(self, nb_threads_max=1, delay=delay)
        #: The list of results (elements might have children; this is actually
        #: a tree).
        self.results = []

    def _on_state_changed(self, state):
        if state:
            self.editor.blockCountChanged.connect(self._on_line_count_changed)
            self.editor.new_text_set.connect(self._run_analysis)
        else:
            self.editor.blockCountChanged.disconnect(
                self._on_line_count_changed)
            self.editor.new_text_set.disconnect(self._run_analysis)

    def _on_line_count_changed(self, e):
        self._jobRunner.request_job(self._run_analysis, False)

    def _run_analysis(self):
        if self.editor.toPlainText():
            request_data = {
                'code': self.editor.toPlainText(),
                'path': self.editor.file_path,
                'encoding': self.editor.file_encoding
            }
            try:
                self.editor.request_work(defined_names, request_data,
                                         on_receive=self._on_results_available)
            except client.NotConnectedError:
                pass
        else:
            self.results = []
            self.documentChanged.emit()

    def _on_results_available(self, status, results):
        if status:
            if results is not None:
                results = [Definition().from_dict(ddict) for ddict in results]
                self.results = results
                logger.debug("Document structure changed")
            else:
                self.results = []
            self.documentChanged.emit()

    @property
    def flattend_results(self):
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
