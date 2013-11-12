# -*- coding: utf-8 -*-
#
#The MIT License (MIT)
#
#Copyright (c) <2013> <Colin Duquesnoy and others, see AUTHORS.txt>
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.
#
from pyqode.core import Mode
from pyqode.qt import QtGui, QtCore


class CommentsMode(Mode):
    """
    Mode that allow to comment/uncomment a set of lines using Ctrl+/.
    """
    IDENTIFIER = "commentsMode"
    DESCRIPTION = "Comments/uncomments a set of lines (Ctrl+/)"

    def __init__(self):
        super(CommentsMode, self).__init__()
        self.action = QtGui.QAction("Comment/Uncomment", self.editor)
        self.action.setShortcut("Ctrl+/")

    def _onStateChanged(self, state):
        """
        Called when the mode is activated/deactivated
        """
        if state:
            self.action.triggered.connect(self.comment)
            self.separator = self.editor.addSeparator()
            self.editor.addAction(self.action)
        else:
            self.editor.removeAction(self.action)
            self.editor.removeAction(self.separator)
            self.action.triggered.disconnect(self.comment)

    def comment(self):
        """
        Comments/Uncomments the selected lines or the current lines if there
        is no selection.
        """
        cursor = self.editor.textCursor()
        cursor.beginEditBlock()
        sel_start = cursor.selectionStart()
        sel_end = cursor.selectionEnd()
        reversed_selection = cursor.position() == sel_start
        has_selection = True
        if not cursor.hasSelection():
            cursor.select(QtGui.QTextCursor.LineUnderCursor)
            has_selection = False
        lines = cursor.selection().toPlainText().splitlines()
        nb_lines = len(lines)
        cursor.setPosition(sel_start)
        comment = False
        for i in range(nb_lines):
            cursor.movePosition(QtGui.QTextCursor.StartOfLine)
            cursor.movePosition(QtGui.QTextCursor.EndOfLine, cursor.KeepAnchor)
            line = cursor.selectedText().lstrip()
            indent = len(cursor.selectedText()) - len(line)
            if not line.startswith("#"):
                comment = True
                break
            # next line
            cursor.movePosition(QtGui.QTextCursor.EndOfLine)
            cursor.setPosition(cursor.position() + 1)
        cursor.setPosition(sel_start)
        for i in range(nb_lines):
            cursor.movePosition(QtGui.QTextCursor.StartOfLine)
            cursor.movePosition(QtGui.QTextCursor.EndOfLine, cursor.KeepAnchor)
            line = cursor.selectedText().lstrip()
            if line != "":
                cursor.movePosition(QtGui.QTextCursor.StartOfLine)
                # Uncomment
                if not comment:
                    cursor.setPosition(cursor.position() + indent)
                    cursor.movePosition(cursor.Right, cursor.KeepAnchor, 1)
                    cursor.insertText("")
                    if i == 0:
                        sel_start -= 1
                        sel_end -= 1
                    else:
                        sel_end -= 1
                # comment
                else:
                    cursor.movePosition(QtGui.QTextCursor.StartOfLine)
                    cursor.setPosition(cursor.position() + indent)
                    cursor.insertText("#")
                    if i == 0:
                        sel_start += 1
                        sel_end += 1
                    else:
                        sel_end += 1
            # next line
            cursor.movePosition(QtGui.QTextCursor.EndOfLine)
            cursor.setPosition(cursor.position() + 1)
        cursor.setPosition(sel_start + (1 if not comment else -1))
        cursor.setPosition(sel_start + (1 if not comment else -1))
        cursor.endEditBlock()
        if has_selection:
            pos = sel_end if not reversed_selection else sel_start
            cursor.setPosition(pos, QtGui.QTextCursor.MoveAnchor)
        else:
            cursor.movePosition(cursor.Down, cursor.MoveAnchor, 1)
        self.editor.setTextCursor(cursor)

    def __on_keyPressed(self, event):
        if(event.modifiers() & QtCore.Qt.ControlModifier and
           event.key() == QtCore.Qt.Key_Slash):
            event.accept()
            self.comment()