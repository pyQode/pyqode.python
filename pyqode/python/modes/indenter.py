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
Contains the python indenter.
"""
from pyqode.core import IndenterMode
from pyqode.qt import QtGui


class PyIndenterMode(IndenterMode):
    """
    Implements python specific indentation, tab/back-tab always
    indents/unindents the whole line.
    """

    def indent(self):
        cursor = self.editor.textCursor()
        assert isinstance(cursor, QtGui.QTextCursor)
        if not cursor.hasSelection():
            cursor.select(cursor.LineUnderCursor)
        self.indentSelection(cursor)

    def unIndent(self):
        cursor = self.editor.textCursor()
        assert isinstance(cursor, QtGui.QTextCursor)
        if not cursor.hasSelection():
            cursor.select(cursor.LineUnderCursor)
        self.unIndentSelection(cursor)