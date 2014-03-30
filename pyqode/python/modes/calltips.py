# -*- coding: utf-8 -*-
"""
Contains the JediCompletionProvider class implementation.
"""
import os
from pyqode.core import logger
from pyqode.core.api import constants
from pyqode.core.editor import Mode
from pyqode.core.api.system import DelayJobRunner
from pyqode.python import workers
from PyQt4 import QtCore, QtGui


class CalltipsMode(Mode, QtCore.QObject):
    """
    This mode shows function/method call tips in a QToolTip using
    :meth:`jedi.Script.call_signatures`.
    """
    tooltipDisplayRequested = QtCore.pyqtSignal(object, int)
    tooltipHideRequested = QtCore.pyqtSignal()

    def __init__(self):
        Mode.__init__(self)
        QtCore.QObject.__init__(self)
        self.__jobRunner = DelayJobRunner(self, nb_threads_max=1, delay=700)
        self.tooltipDisplayRequested.connect(self._display_tooltip)
        self.tooltipHideRequested.connect(QtGui.QToolTip.hideText)
        self.__requestCnt = 0

    def _on_state_changed(self, state):
        if "PYQODE_NO_COMPLETION_SERVER" not in os.environ:
            if state:
                self.editor.key_released.connect(self._on_key_released)

    def _on_key_released(self, event):
        if (event.key() == QtCore.Qt.Key_ParenLeft or
                event.key() == QtCore.Qt.Key_Comma):
            tc = self.editor.textCursor()
            line = tc.blockNumber() + 1
            col = tc.columnNumber()
            fn = self.editor.file_path
            encoding = self.editor.file_encoding
            source = self.editor.toPlainText()
            # jedi has a bug if the statement has a closing parenthesis
            # remove it!
            lines = source.splitlines()
            l = lines[line - 1].rstrip()
            if l.endswith(")"):
                lines[line - 1] = l[:-1]
            source = "\n".join(lines)
            self._request_calltip(source, line, col, fn, encoding)

    def _request_calltip(self, source, line, col, fn, encoding):
        if self.__requestCnt == 0:
            self.__requestCnt += 1
            logger.debug("Calltip requested")
            self.editor.request_work(
                workers.calltips,
                {'code': source, 'line': line, 'column': col, 'path': None,
                 'encoding': encoding}, on_receive=self._on_results_available)

    def _on_results_available(self, status, results):
        if status:
            logger.debug("Calltip request finished")
            self.__requestCnt -= 1
            if results:
                call = {"call.module.name": results[0],
                        "call.call_name": results[1],
                        "call.params": results[2],
                        "call.index": results[3],
                        "call.bracket_start": results[4]}
                self.tooltipDisplayRequested.emit(call, results[5])

    def _is_last_chard_end_of_word(self):
        try:
            tc = self.editor.select_word_under_cursor()
            tc.setPosition(tc.position())
            tc.movePosition(tc.StartOfLine, tc.KeepAnchor)
            l = tc.selectedText()
            last_char = l[len(l) - 1]
            seps = constants.WORD_SEPARATORS
            symbols = [",", " ", "("]
            return last_char in seps and last_char not in symbols
        except IndexError:
            return False

    def _display_tooltip(self, call, col):
        if not call or self._is_last_chard_end_of_word():
            return
        # create a formatted calltip (current index appear in bold)
        calltip = "<nobr>{0}.{1}(".format(call['call.module.name'],
                                          call['call.call_name'])
        for i, param in enumerate(call['call.params']):
            if i != 0:
                calltip += ", "
            if i == call['call.index']:
                calltip += "<b>"
            calltip += param
            if i == call['call.index']:
                calltip += "</b>"
        calltip += ')</nobr>'
        # set tool tip position at the start of the bracket
        char_width = self.editor.fontMetrics().width('A')
        w_offset = (col - call['call.bracket_start'][1]) * char_width
        position = QtCore.QPoint(
            self.editor.cursorRect().x() - w_offset,
            self.editor.cursorRect().y() + 35)
        position = self.editor.mapToGlobal(position)
        # show tooltip
        QtGui.QToolTip.showText(position, calltip, self.editor)
