#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# PCEF
# Copyright 2013, Colin Duquesnoy <colin.duquesnoy@gmail.com>
#
# This software is released under the LGPLv3 license.
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""
Contains python specific modes
"""
from pcef.python.modes.calltips import CalltipsMode
from pcef.python.modes.code_completion import JediCompletionProvider
from pcef.python.modes.pep8_checker import PEP8CheckerMode
from pcef.python.modes.indenter import PyAutoIndentMode
from pcef.python.modes.pyflakes_checker import PyFlakesCheckerMode
from pcef.python.modes.folder import FolderMode
from pcef.python.modes.syntax_highlighter import PyHighlighterMode
from pcef.python.modes.syntax_highlighter import DEFAULT_DARK_STYLES
from pcef.python.modes.syntax_highlighter import DEFAULT_LIGHT_STYLES


__all__ = ["CalltipsMode", "JediCompletionProvider", "PEP8CheckerMode",
           "PyAutoIndentMode", "PyFlakesCheckerMode", "FolderMode",
           "PyHighlighterMode", "DEFAULT_DARK_STYLES", "DEFAULT_LIGHT_STYLES"]
