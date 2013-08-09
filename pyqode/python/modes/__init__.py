#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# pyQode - Python/Qt Code Editor widget
# Copyright 2013, Colin Duquesnoy <colin.duquesnoy@gmail.com>
#
# This software is released under the LGPLv3 license.
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""
Contains python specific modes
"""
from pyqode.python.modes.calltips import CalltipsMode
from pyqode.python.modes.code_completion import JediCompletionProvider
from pyqode.python.modes.pep8_checker import PEP8CheckerMode
from pyqode.python.modes.indenter import PyAutoIndentMode
from pyqode.python.modes.pyflakes_checker import PyFlakesCheckerMode
from pyqode.python.modes.syntax_highlighter import PyHighlighterMode
from pyqode.python.modes.syntax_highlighter import DEFAULT_DARK_STYLES
from pyqode.python.modes.syntax_highlighter import DEFAULT_LIGHT_STYLES


__all__ = ["CalltipsMode", "JediCompletionProvider", "PEP8CheckerMode",
           "PyAutoIndentMode", "PyFlakesCheckerMode",
           "PyHighlighterMode", "DEFAULT_DARK_STYLES", "DEFAULT_LIGHT_STYLES"]
