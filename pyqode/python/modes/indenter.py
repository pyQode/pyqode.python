# -*- coding: utf-8 -*-
"""
Contains the python indenter.
"""
from pyqode.core.modes import IndenterMode
from PyQt4 import QtGui


class PyIndenterMode(IndenterMode):
    """
    Implements python specific indentation, tab/back-tab always
    indents/unindents the **whole** line. This replace the default IndenterMode
    which we found to be better suited for python code editing.
    """

    def indent(self):
        cursor = self.editor.textCursor()
        assert isinstance(cursor, QtGui.QTextCursor)
        if not cursor.hasSelection():
            cursor.select(cursor.LineUnderCursor)
        self.indent_selection(cursor)

    def unindent(self):
        cursor = self.editor.textCursor()
        assert isinstance(cursor, QtGui.QTextCursor)
        if not cursor.hasSelection():
            cursor.select(cursor.LineUnderCursor)
        self.unindent_selection(cursor)
