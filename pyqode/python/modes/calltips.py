#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2013 Colin Duquesnoy
#
# This file is part of pyQode.
#
# pyQode is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# pyQode is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with pyQode. If not, see http://www.gnu.org/licenses/.
#
"""
Contains the JediCompletionProvider class implementation.
"""
import jedi
from pyqode.core import Mode, DelayJobRunner, logger, constants
from pyqode.core import CodeCompletionMode
from pyqode.qt import QtCore, QtGui


class CalltipsWorker(object):
    def __init__(self, code, line, col, path, encoding):
        self.code = code
        self.line = line
        self.col = col
        self.path = path
        self.encoding = encoding

    def __call__(self, *args, **kwargs):
        script = jedi.Script(self.code, self.line, self.col, self.path,
                             self.encoding)
        c = script.get_in_function_call()
        if c:
            results = [str(c.module.name), str(c.call_name),
                       [str(p.token_list[0]) for p in c.params], c.index,
                       c.bracket_start]
            return results
        return []


class CalltipsMode(Mode, QtCore.QObject):
    IDENTIFIER = "calltipsMode"
    DESCRIPTION = "Provides functions calltips using the jedi library"

    tooltipDisplayRequested = QtCore.Signal(object, int)
    tooltipHideRequested = QtCore.Signal()

    def __init__(self):
        Mode.__init__(self)
        QtCore.QObject.__init__(self)
        self.__jobRunner = DelayJobRunner(self, nbThreadsMax=1, delay=700)
        self.tooltipDisplayRequested.connect(self.__displayTooltip)
        self.tooltipHideRequested.connect(QtGui.QToolTip.hideText)

    def _onStateChanged(self, state):
        if state:
            self.editor.keyReleased.connect(self.__onKeyReleased)
            CodeCompletionMode.SERVER.signals.workCompleted.connect(
                self.__onWorkFinished)
        else:
            CodeCompletionMode.SERVER.signals.workCompleted.disconnect(
                self.__onWorkFinished)

    def __onKeyReleased(self, event):
        if (event.key() == QtCore.Qt.Key_ParenLeft or
                event.key() == QtCore.Qt.Key_Comma or
                event.key() == QtCore.Qt.Key_Space):
            tc = self.editor.textCursor()
            line = tc.blockNumber() + 1
            col = tc.columnNumber()
            fn = self.editor.filePath
            encoding = self.editor.fileEncoding
            source = self.editor.toPlainText()
            self.__requestCalltip(source, line, col, fn, encoding)
        else:
            QtGui.QToolTip.hideText()

    def __requestCalltip(self, *args):
        logger.debug("Calltip requested")
        worker = CalltipsWorker(*args)
        CodeCompletionMode.SERVER.requestWork(self, worker)

    def __onWorkFinished(self, caller_id, worker, results):
        if caller_id == id(self) and isinstance(worker, CalltipsWorker):
            if results:
                call = {"call.module.name": results[0],
                        "call.call_name": results[1],
                        "call.params": results[2],
                        "call.index": results[3],
                        "call.bracket_start": results[4]}
                self.tooltipDisplayRequested.emit(call, worker.col)

    def __isLastCharEndOfWord(self):
        try:
            tc = self.editor.selectWordUnderCursor()
            tc.setPosition(tc.position())
            tc.movePosition(tc.StartOfLine, tc.KeepAnchor)
            l = tc.selectedText()
            lastChar = l[len(l) - 1]
            seps = constants.WORD_SEPARATORS
            symbols = [",", " ", "("]
            return lastChar in seps and not lastChar in symbols
        except IndexError:
            return False

    def __displayTooltip(self, call, col):
        if not call or self.__isLastCharEndOfWord():
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
        charWidth = self.editor.fontMetrics().width('A')
        w_offset = (col - call['call.bracket_start'][1]) * charWidth
        position = QtCore.QPoint(
            self.editor.cursorRect().x() - w_offset,
            self.editor.cursorRect().y())
        position = self.editor.mapToGlobal(position)
        # show tooltip
        QtGui.QToolTip.showText(position, calltip, self.editor)
