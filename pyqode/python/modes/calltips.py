#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#The MIT License (MIT)
#
#Copyright (c) <2013> <Colin Duquesnoy and others, see AUTHORS.txt>
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
Contains the JediCompletionProvider class implementation.
"""
import os
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
        import jedi
        script = jedi.Script(self.code, self.line, self.col, self.path,
                             self.encoding)
        signatures = script.call_signatures()
        for c in signatures:
            results = [str(c.module.name), str(c.call_name),
                       [str(p.token_list[0]) for p in c.params], c.index,
                       c.bracket_start, self.col]
            # seems like len of signatures is always 1 when getting calltips
            return results
        return []


class CalltipsMode(Mode, QtCore.QObject):
    """
    This mode shows function/method call tips in a QToolTip using
    :meth:`jedi.Script.call_signatures`.
    """
    #: Mode identifier
    IDENTIFIER = "calltipsMode"
    #: Mode description
    DESCRIPTION = "Provides functions calltips using the jedi library"

    tooltipDisplayRequested = QtCore.Signal(object, int)
    tooltipHideRequested = QtCore.Signal()

    def __init__(self):
        Mode.__init__(self)
        QtCore.QObject.__init__(self)
        self.__jobRunner = DelayJobRunner(self, nbThreadsMax=1, delay=700)
        self.tooltipDisplayRequested.connect(self.__displayTooltip)
        self.tooltipHideRequested.connect(QtGui.QToolTip.hideText)
        self.__requestCnt = 0

    def _onStateChanged(self, state):
        if not "PYQODE_NO_COMPLETION_SERVER" in os.environ:
            if state:
                self.editor.keyReleased.connect(self.__onKeyReleased)

                if CodeCompletionMode.SERVER:
                    CodeCompletionMode.SERVER.signals.workCompleted.connect(
                        self.__onWorkFinished)
            elif CodeCompletionMode.SERVER:
                CodeCompletionMode.SERVER.signals.workCompleted.disconnect(
                    self.__onWorkFinished)

    def __onKeyReleased(self, event):
        if (event.key() == QtCore.Qt.Key_ParenLeft or
                event.key() == QtCore.Qt.Key_Comma):
            tc = self.editor.textCursor()
            line = tc.blockNumber() + 1
            col = tc.columnNumber()
            fn = self.editor.filePath
            encoding = self.editor.fileEncoding
            source = self.editor.toPlainText()
            self.__requestCalltip(source, line, col, fn, encoding)

    def __requestCalltip(self, *args):
        if self.__requestCnt == 0:
            self.__requestCnt += 1
            logger.debug("Calltip requested")
            worker = CalltipsWorker(*args)
            CodeCompletionMode.SERVER.requestWork(self, worker)

    def __onWorkFinished(self, caller_id, worker, results):
        if caller_id == id(self) and isinstance(worker, CalltipsWorker):
            logger.debug("Calltip request finished")
            self.__requestCnt -= 1
            if results:
                call = {"call.module.name": results[0],
                        "call.call_name": results[1],
                        "call.params": results[2],
                        "call.index": results[3],
                        "call.bracket_start": results[4]}
                self.tooltipDisplayRequested.emit(call, results[5])

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
