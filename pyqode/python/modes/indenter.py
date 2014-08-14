# -*- coding: utf-8 -*-
"""
Contains the python indenter.
"""
from pyqode.qt import QtGui
from pyqode.core.modes import IndenterMode


class PyIndenterMode(IndenterMode):
    """
    Implements python specific indentation, tab/back-tab always
    indents/unindents the **whole** line. This replace the default IndenterMode
    which we found to be better suited for python code editing.
    """
    def indent(self):
        """
        Performs an indentation
        """
        cursor = self.editor.textCursor()
        assert isinstance(cursor, QtGui.QTextCursor)
        if not cursor.hasSelection():
            cursor.select(cursor.LineUnderCursor)
        if cursor.hasSelection():
            self.indent_selection(cursor)
        else:
            # simply insert indentation at the cursor position
            tab_len = self.editor.tab_length
            cursor.beginEditBlock()
            if self.editor.use_spaces_instead_of_tabs:
                cursor.insertText(tab_len * " ")
            else:
                cursor.insertText('\t')
            cursor.endEditBlock()
            self.editor.setTextCursor(cursor)

    def unindent(self):
        """
        Performs an un-indentation
        """
        cursor = self.editor.textCursor()
        assert isinstance(cursor, QtGui.QTextCursor)
        if not cursor.hasSelection():
            cursor.select(cursor.LineUnderCursor)
        self.unindent_selection(cursor)
