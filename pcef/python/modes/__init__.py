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
from pcef.python.modes.pep8_checker import PEP8CheckerMode
from pcef.python.modes.indenter import PyAutoIndentMode
from pcef.python.modes.pyflakes_checker import PyFlakesCheckerMode
from pcef.python.modes.folder import PyFolderMode
from pcef.python.modes.syntax_highlighter import PyHighlighterMode


__all__ = ["PEP8CheckerMode", "PyAutoIndentMode", "PyFlakesCheckerMode",
           "PyFolderMode", "PyHighlighterMode"]
