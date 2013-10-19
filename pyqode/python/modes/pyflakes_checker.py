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
This module contains the pyFlakes checker mode
"""
import _ast
from pyqode.core import CheckerMode, CheckerMessage, logger
from pyqode.core import MSG_STATUS_ERROR, MSG_STATUS_WARNING
from pyqode.core import CHECK_TRIGGER_TXT_SAVED


def pyflakesAnalysisProcess(q, codeString, filename, fileEncoding):
    """
    Function executed in background process to run the pyflakes on the
    codeString.
    """
    msgs = []
    # First, compile into an AST and handle syntax errors.
    if not codeString or not fileEncoding:
        return
    try:
        tree = compile(codeString.encode(fileEncoding),
                       filename, "exec", _ast.PyCF_ONLY_AST)
    except SyntaxError as value:
        msg = value.args[0]
        (lineno, offset, text) = value.lineno, value.offset, value.text
        # If there's an encoding problem with the file, the text is None
        if text is None:
            # Avoid using msg, since for the only known case, it
            # contains a bogus message that claims the encoding the
            # file declared was unknown.s
            logger.warning("%s: problem decoding source" % filename)
        else:
            msgs.append(
                CheckerMessage(msg, MSG_STATUS_ERROR, lineno))
    else:
        # Okay, it's syntactically valid.  Now check it.
        from pyflakes import checker, messages
        msg_types = {messages.UnusedImport: MSG_STATUS_WARNING,
                     messages.RedefinedWhileUnused: MSG_STATUS_WARNING,
                     messages.RedefinedInListComp: MSG_STATUS_WARNING,
                     messages.ImportShadowedByLoopVar: MSG_STATUS_WARNING,
                     messages.ImportStarUsed: MSG_STATUS_WARNING,
                     messages.UndefinedName: MSG_STATUS_ERROR,
                     messages.DoctestSyntaxError: MSG_STATUS_ERROR,
                     messages.UndefinedExport: MSG_STATUS_ERROR,
                     messages.UndefinedLocal:  MSG_STATUS_ERROR,
                     messages.DuplicateArgument: MSG_STATUS_WARNING,
                     messages.Redefined: MSG_STATUS_WARNING,
                     messages.LateFutureImport: MSG_STATUS_WARNING,
                     messages.UnusedVariable: MSG_STATUS_WARNING}
        w = checker.Checker(tree, filename)
        w.messages.sort(key=lambda msg: msg.lineno)
        for warning in w.messages:
            msg = warning.message % warning.message_args
            line = warning.lineno
            status = msg_types[type(warning)]
            msgs.append(CheckerMessage(msg, status, line))
    q.put(msgs)


class PyFlakesCheckerMode(CheckerMode):
    """
    This checker mode runs pyflakes on the fly to check your python syntax.
    """
    DESCRIPTION = "Check python code using pyFlakes"
    IDENTIFIER = "pyFlakesCheckerMode"

    def __init__(self):
        CheckerMode.__init__(self, pyflakesAnalysisProcess,
                             delay=1200,
                             clearOnRequest=False)

    def _onInstall(self, editor):
        """
        Checks for pyflakes support. Auto disable if pyflakes could not be
        imported
        """
        CheckerMode._onInstall(self, editor)
        try:
            import pyflakes
        except ImportError:
            logger.warning("Cannot import PyFlakes, PyFlakesCheckerMode "
                            "disabled")
            self.enabled = False
