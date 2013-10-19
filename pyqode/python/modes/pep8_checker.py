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
from pyqode.core import CheckerMode, CheckerMessage, logger
from pyqode.core import MSG_STATUS_WARNING

try:
    import pep8

    class CustomReport(pep8.StandardReport):
        """
        Custom report used to get the pep8 results as a list of string. This
        is easier to handler then retrieving the stdout and parsing.
        """

        def get_file_results(self):
            self._deferred_print.sort()
            return self._deferred_print

    class CustomChecker(pep8.Checker):
        """
        Custom Checker with our Custom report.
        """
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
    """
    This functions is run in a background process to check the code against
    PEP8 using pep8.py.
    """
    import pep8
    # setup our custom style guide with our custom checker which returns a list
    # of strings instread of spitting the results at stdout
    pep8style = pep8.StyleGuide(parse_argv=False, config_file=True,
                                checker_class=CustomChecker)
    results = pep8style.input_file(filePath, lines=code.splitlines(True))
    messages = []
    for line_number, offset, code, text, doc in results:
        messages.append(CheckerMessage(
            text, MSG_STATUS_WARNING, line_number))
    q.put(messages)


class PEP8CheckerMode(CheckerMode):
    """
    This checker mode runs pep8.py on the fly to check your python style.
    """
    #: Mode description
    DESCRIPTION = "Check python code for PEP8 issues"
    #: Mode identifier
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
