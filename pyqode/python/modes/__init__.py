# -*- coding: utf-8 -*-
"""
Contains python specific modes
"""
from pyqode.python.modes.autocomplete import PyAutoCompleteMode
from pyqode.python.modes.calltips import CalltipsMode
from pyqode.python.modes.comments import CommentsMode
from pyqode.python.modes.pep8_checker import PEP8CheckerMode
from pyqode.python.modes.autoindent import PyAutoIndentMode
from pyqode.python.modes.indenter import PyIndenterMode
from pyqode.python.modes.frosted_checker import FrostedCheckerMode
from pyqode.python.modes.syntax_highlighter import PyHighlighterMode
from pyqode.python.modes.syntax_highlighter import DEFAULT_DARK_STYLES
from pyqode.python.modes.syntax_highlighter import DEFAULT_LIGHT_STYLES
from pyqode.python.modes.goto_assignements import GoToAssignmentsMode
from pyqode.python.modes.document_analyser import DocumentAnalyserMode


__all__ = ["PyAutoCompleteMode", "CalltipsMode", "PEP8CheckerMode",
           "GoToAssignmentsMode", "PyAutoIndentMode", "FrostedCheckerMode",
           "PyIndenterMode", "CommentsMode", "PyHighlighterMode",
           "DEFAULT_DARK_STYLES", "DEFAULT_LIGHT_STYLES"]
