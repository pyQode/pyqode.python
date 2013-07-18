#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# PCEF - Python/Qt Code Editing Framework
# Copyright 2013, Colin Duquesnoy <colin.duquesnoy@gmail.com>
#
# This software is released under the LGPLv3 license.
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""
This module contains the pyFlakes checker mode
"""
import logging
import _ast
from pcef.core import CheckerMode, CheckerMessage
from pcef.core import MSG_STATUS_ERROR, MSG_STATUS_INFO, MSG_STATUS_WARNING
from pcef.qt import QtCore, QtGui


class PyFlakesCheckerMode(CheckerMode):
    DESCRIPTION = "Check python code using pyFlakes"
    IDENTIFIER = "pyFlakesChecker"

    def install(self, editor):
        CheckerMode.install(self, editor)
        try:
            import pyflakes
        except ImportError:
            logging.warning("Cannot import PyFlakes, PyFlakesCheckerMode "
                            "disabled")
            self.enabled = False
        else:
            logging.debug("PyFlakes found!")

    def run(self, document, filePath):
        assert isinstance(document, QtGui.QTextDocument)
        self.check(document.toPlainText(), filePath)

    def check(self, codeString, filename):
        """
        Checks the python source code using PyFlakes checker.

        :param codeString: The code string to check

        :param filename;

        .. note: This is a modified version of the check function found in the
                 pyFlakes script.
        """
        # First, compile into an AST and handle syntax errors.
        try:
            tree = compile(codeString.encode(self.editor.fileEncoding),
                           filename, "exec", _ast.PyCF_ONLY_AST)
        except SyntaxError as value:
                msg = value.args[0]
                print(msg)
                (lineno, offset, text) = value.lineno, value.offset, value.text
                # If there's an encoding problem with the file, the text is None
                if text is None:
                    # Avoid using msg, since for the only known case, it
                    # contains a bogus message that claims the encoding the
                    # file declared was unknown.s
                    logging.warning("%s: problem decoding source" % filename)
                else:
                    self.addMessageRequested.emit(
                        CheckerMessage(msg, MSG_STATUS_ERROR, lineno))
                return 1
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
                self.addMessageRequested.emit(CheckerMessage(msg, status, line))
            return len(w.messages)
