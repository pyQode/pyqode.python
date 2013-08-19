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
This module contains the pyFlakes checker mode
"""
from pyqode.core import CheckerMode, CheckerMessage, logger
from pyqode.core import MSG_STATUS_WARNING

try:
    import pep8

    class CustomReport(pep8.StandardReport):
        def get_file_results(self):
            self._deferred_print.sort()
            return self._deferred_print

    class CustomChecker(pep8.Checker):
        def __init__(self, *args, **kwargs):
            super(CustomChecker, self).__init__(
                *args, report=CustomReport(kwargs.pop("options")), **kwargs)
            pass

except ImportError:

    class CustomReport(object):
        pass

    class CustomChecker(object):
        pass


def pep8AnalysisProcess(q, code, filePath, fileEncoding):
    import pep8
    pep8style = pep8.StyleGuide(parse_argv=False, config_file=True,
                                checker_class=CustomChecker)
    results = pep8style.input_file(filePath, lines=code.splitlines(True))
    messages = []
    for line_number, offset, code, text, doc in results:
        messages.append(CheckerMessage(
            text, MSG_STATUS_WARNING, line_number))
    q.put(messages)


class PEP8CheckerMode(CheckerMode):
    DESCRIPTION = "Check python code for PEP8 issues"
    IDENTIFIER = "pep8CheckerMode"

    def __init__(self):
        CheckerMode.__init__(self, pep8AnalysisProcess, clearOnRequest=False)

    def _onInstall(self, editor):
        """
        Checks for pep8 support on install
        """
        CheckerMode._onInstall(self, editor)
        try:
            import pep8
        except ImportError:
            logger.warning("Cannot import pep8.py, PEP8CheckerMode disabled")
            self.enabled = False
