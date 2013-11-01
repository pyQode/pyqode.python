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
Contains python specific modes
"""
from pyqode.python.modes.autocomplete import PyAutoCompleteMode
from pyqode.python.modes.calltips import CalltipsMode
from pyqode.python.modes.code_completion import PyCodeCompletionMode
from pyqode.python.modes.code_completion import JediCompletionProvider
from pyqode.python.modes.comments import CommentsMode
from pyqode.python.modes.pep8_checker import PEP8CheckerMode
from pyqode.python.modes.autoindent import PyAutoIndentMode
from pyqode.python.modes.indenter import PyIndenterMode
from pyqode.python.modes.pyflakes_checker import PyFlakesCheckerMode
from pyqode.python.modes.syntax_highlighter import PyHighlighterMode
from pyqode.python.modes.syntax_highlighter import DEFAULT_DARK_STYLES
from pyqode.python.modes.syntax_highlighter import DEFAULT_LIGHT_STYLES
from pyqode.python.modes.goto_assignements import GoToAssignmentsMode
from pyqode.python.modes.document_analyser import DocumentAnalyserMode


__all__ = ["PyAutoCompleteMode", "CalltipsMode", "PyCodeCompletionMode",
           "JediCompletionProvider", "PEP8CheckerMode", "GoToAssignmentsMode",
           "PyAutoIndentMode", "PyFlakesCheckerMode", "PyIndenterMode",
           "CommentsMode", "PyHighlighterMode", "DEFAULT_DARK_STYLES",
           "DEFAULT_LIGHT_STYLES"]
