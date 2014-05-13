# -*- coding: utf-8 -*-
"""
Contains the python indenter.
"""
from PyQt4 import QtGui
from pyqode.core.frontend.modes import IndenterMode
from pyqode.core import settings


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
        if cursor.hasSelection():
            self.indent_selection(cursor)
        else:
            # simply insert indentation at the cursor position
            tab_len = settings.tab_length
            cursor.beginEditBlock()
            if settings.use_spaces_instead_of_tabs:
                cursor.insertText(tab_len * " ")
            else:
                cursor.insertText('\t')
            cursor.endEditBlock()
            self.editor.setTextCursor(cursor)

    def unindent(self):
        cursor = self.editor.textCursor()
        assert isinstance(cursor, QtGui.QTextCursor)
        if not cursor.hasSelection():
            cursor.select(cursor.LineUnderCursor)
        self.unindent_selection(cursor)
