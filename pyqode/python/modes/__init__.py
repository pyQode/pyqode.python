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
