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
from io import StringIO, BytesIO
import logging
import sys
from pcef.core import CheckerMode, CheckerMessage
from pcef.core import MSG_STATUS_ERROR, MSG_STATUS_WARNING
from pcef.qt import QtGui


class PEP8CheckerMode(CheckerMode):
    DESCRIPTION = "Check python code for PEP8 issues"
    IDENTIFIER = "pep8Checker"

    def __init__(self):
        CheckerMode.__init__(self, clearOnRequest=False)

    def _onInstall(self, editor):
        CheckerMode._onInstall(self, editor)
        try:
            import pep8
        except ImportError:
            logging.warning("Cannot import pep8.py, PEP8CheckerMode disabled")
            self.enabled = False
        else:
            logging.debug("pep8.py found!")

    def run(self, document, filePath):
        assert isinstance(document, QtGui.QTextDocument)
        old_stdout = sys.stdout
        if sys.version_info[0] == 3:
            sys.stdout = mystdout = StringIO()
        else:
            sys.stdout = mystdout = BytesIO()
        self.clearMessagesRequested.emit()
        try:
            self.check(document.toPlainText().splitlines(True), filePath)
            sys.stdout = old_stdout
            self.analyse(mystdout.getvalue().splitlines())
        except TypeError:
            print(document.toPlainText().splitlines(True), filePath)
            pass

    def analyse(self, lines):
        for line in lines:
            tokens = line.split(":")
            nbTokens = len(tokens)
            msg = tokens[nbTokens-1]
            status = MSG_STATUS_WARNING
            if msg.startswith("E"):
                MSG_STATUS_ERROR
            try:
                line = int(tokens[nbTokens-3])
            except IndexError:
                return
            except ValueError:
                return
            self.addMessageRequested.emit(CheckerMessage(msg, status, line))

    def check(self, lines, filename):
        """
        Checks the python source code using PEP8 checker.

        :param codeString: The code string to check

        :param filename;

        .. note: This is a modified version of the check function found in the
                 pyFlakes script.
        """
        import pep8
        pep8style = pep8.StyleGuide(parse_argv=False, config_file=True)
        pep8style.input_file(filename, lines=lines)
