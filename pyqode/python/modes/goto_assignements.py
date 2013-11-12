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
Contains the go to assignments mode.
"""
import os
import jedi
from  pyqode.qt import QtCore, QtGui
from pyqode.core import Mode, CodeCompletionMode, logger


class Assignment(object):
    """
    Assignment definition.
    """
    def __init__(self, path, line, column, full_name):
        #: Module path
        self.module_path = path.replace(".pyc", ".py")
        #: Line number
        self.line = line
        #: Column number
        self.column = column
        #: Assignement full name
        self.full_name = full_name

    def __str__(self):
        if self.line and self.column:
            return "%s (%s, %s)" % (self.full_name, self.line, self.column)
        return self.full_name

    def __repr__(self):
        return "Definition(%r, %r, %r, %r)" % (self.module_path, self.line,
                                               self.column, self.full_name)


class _Worker(object):
        def __init__(self, code, line, column, path, encoding):
            self.code = code
            self.line = line
            self.col = column
            self.path = path
            self.encoding = encoding

        def __call__(self, *args):
            script = jedi.Script(self.code, self.line, self.col, self.path,
                                 self.encoding)
            try:
                definitions = script.goto_assignments()
            except jedi.api.NotFoundError:
                return []
            else:
                ret_val = [Assignment(d.module_path, d.line, d.column,
                                      d.full_name)
                           for d in definitions]
                return ret_val


class GoToAssignmentsMode(Mode, QtCore.QObject):
    """
    Goes to the assignments (using jedi.Script.goto_assignments). If there are
    more than one assignments, an input dialog is used to ask the user to
    choose the desired assignment.

    This mode will emit :attr:`pyqode.python.GoToAssignmentsMode.outOfDocument`
    if the definition can not be reached in the current document. IDEs will
    typically open a new editor tab and go to the definition.
    """
    IDENTIFIER = "gotoAssignmentsMode"
    DESCRIPTION = "Move the text cursor to the symbol assignments/definitions"

    #: Signal emitted when the definition cannot be reached in the current edit.
    outOfDocument = QtCore.Signal(Assignment)

    #: Signal emitted when no results could be found.
    noResultsFound = QtCore.Signal()

    def __init__(self):
        Mode.__init__(self)
        QtCore.QObject.__init__(self)
        self._pending = False
        self.actionGotoAssignments = QtGui.QAction("Go to assignments", self)
        self.actionGotoAssignments.setShortcut("F2")
        self.actionGotoAssignments.triggered.connect(self.requestGoTo)

    def _onInstall(self, editor):
        Mode._onInstall(self, editor)
        if CodeCompletionMode.SERVER:
            CodeCompletionMode.SERVER.signals.workCompleted.connect(
                self._onWorkFinished)

    def _onStateChanged(self, state):
        if state:
            assert hasattr(self.editor, "wordClickMode")
            self.editor.wordClickMode.wordClicked.connect(self.requestGoTo)
            self.sep = self.editor.addSeparator()
            self.editor.addAction(self.actionGotoAssignments)
            if hasattr(self.editor, "codeCompletionMode"):
                self.editor.codeCompletionMode.preLoadStarted.connect(
                    self._onPreloadStarted)
                self.editor.codeCompletionMode.preLoadCompleted.connect(
                    self._onPreloadCompleted)
        else:
            self.editor.wordClickMode.wordClicked.disconnect(self.requestGoTo)
            self.editor.removeAction(self.actionGotoAssignments)
            self.editor.removeAction(self.sep)
            if hasattr(self.editor, "codeCompletionMode"):
                self.editor.codeCompletionMode.preLoadStarted.disconnect(
                    self._onPreloadStarted)
                self.editor.codeCompletionMode.preLoadCompleted.disconnect(
                    self._onPreloadCompleted)

    def _onPreloadStarted(self):
        self.actionGotoAssignments.setDisabled(True)

    def _onPreloadCompleted(self):
        self.actionGotoAssignments.setEnabled(True)

    def requestGoTo(self, tc=None):
        """
        Request a go to assignment.

        :param tc: Text cursor which contains the text that we must look for
                   its assignment. Can be None to go to the text that is under
                   the text cursor.
        :type tc: QtGui.QTextCursor
        """
        if not tc:
            tc = self.editor.selectWordUnderCursor()
        if CodeCompletionMode.SERVER:
            self.editor.setCursor(QtCore.Qt.WaitCursor)
            if not self._pending:
                CodeCompletionMode.SERVER.requestWork(
                    self, _Worker(self.editor.toPlainText(),
                                  tc.blockNumber()+1, tc.columnNumber(),
                                  self.editor.filePath,
                                  self.editor.fileEncoding))
                self._pending = True

    def _goToDefinition(self, definition):
        pth = os.path.normpath(definition.module_path)
        fp = os.path.normpath(self.editor.filePath.replace(".pyc", ".py"))
        if definition.module_path == fp:
            line = definition.line
            col = definition.column
            logger.debug("Go to %s" % definition)
            self.editor.gotoLine(line, move=True, column=col)
        else:
            logger.debug("Out of doc: %s" % definition)
            self.outOfDocument.emit(definition)

    def _makeUnique(self, seq):
        """
        Not performant but works.
        """
        # order preserving
        checked = []
        for e in seq:
            present = False
            for c in checked:
                if str(c) == str(e):
                    present = True
                    break
            if not present:
                checked.append(e)
        return checked

    def _onWorkFinished(self, caller_id, worker, definitions):
        if caller_id == id(self) and isinstance(worker, _Worker):
            self.editor.setCursor(QtCore.Qt.IBeamCursor)
            self._pending = False
            definitions = self._makeUnique(definitions)
            logger.debug("Got %r" % definitions)
            if len(definitions) == 1:
                definition = definitions[0]
                self._goToDefinition(definition)
            elif len(definitions) > 1:
                logger.debug(
                    "More than 1 assignments in different modules, user "
                    "need to make a choice: %s" % definitions)
                def_str, result = QtGui.QInputDialog.getItem(
                    self.editor, "Choose a definition",
                    "Choose the definition you want to go to:",
                    [str(d) for d in definitions])
                if result:
                    for definition in definitions:
                        if str(definition) == def_str:
                            self._goToDefinition(definition)
                            return
            else:
                logger.info("GoToAssignments: No results found")
                self.noResultsFound.emit()
