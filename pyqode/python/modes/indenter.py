# -*- coding: utf-8 -*-
"""
Contains the python indenter.
"""
from pyqode.qt import QtGui
from pyqode.core.modes import IndenterMode


class PyIndenterMode(IndenterMode):
    """
    Implements python specific indentation, tab/back-tab always
    indents/unindents the **whole** line. This replace the default
    IndenterMode which we found to be better suited for python code editing.

    To use the default behaviour, just set the ``tab_always_indent`` property
    to False
    """
    @property
    def tab_always_indent(self):
        return self._tab_always_indent

    @tab_always_indent.setter
    def tab_always_indent(self, value):
        self._tab_always_indent = value

    def __init__(self):
        super(PyIndenterMode, self).__init__()
        self._tab_always_indent = None
        self.tab_always_indent = True

    def indent(self):
        """
        Performs an indentation
        """
        if not self.tab_always_indent:
            super(PyIndenterMode, self).indent()
        else:
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
        if self.tab_always_indent:
            cursor = self.editor.textCursor()
            p = cursor.position()
            assert isinstance(cursor, QtGui.QTextCursor)
            if not cursor.hasSelection():
                cursor.select(cursor.LineUnderCursor)
            self.unindent_selection(cursor)
            p -= self.editor.tab_length
            c = self.editor.textCursor()
            c.setPosition(p)
            self.editor.setTextCursor(c)
        else:
            super(PyIndenterMode, self).unindent()
