# -*- coding: utf-8 -*-
from pyqode.core import frontend
from PyQt4 import QtGui, QtCore


class CommentsMode(frontend.Mode):
    """
    Mode that allow to comment/uncomment a set of lines using Ctrl+/.
    """
    def __init__(self):
        super(CommentsMode, self).__init__()
        self.action = QtGui.QAction("Comment/Uncomment", self.editor)
        self.action.setShortcut("Ctrl+/")

    def _on_state_changed(self, state):
        """
        Called when the mode is activated/deactivated
        """
        if state:
            self.action.triggered.connect(self.comment)
            self.separator = self.editor.add_separator()
            self.editor.add_action(self.action)
        else:
            self.editor.remove_action(self.action)
            self.editor.remove_action(self.separator)
            self.action.triggered.disconnect(self.comment)

    def comment(self):
        """
        Comments/Uncomments the selected lines or the current lines if there
        is no selection.
        """
        cursor = self.editor.textCursor()
        # make comment/uncomment a single operation for the undo stack
        cursor.beginEditBlock()
        # did the user do a reversed selection (from bottom to top)?
        sel_start = cursor.selectionStart()
        sel_end = cursor.selectionEnd()
        reversed_selection = cursor.position() == sel_start
        # were there any selected lines? If not select the current line
        has_selection = True
        if not cursor.hasSelection():
            cursor.select(QtGui.QTextCursor.LineUnderCursor)
            has_selection = False

        # get selected lines
        lines = cursor.selection().toPlainText().splitlines()
        nb_lines = len(lines)

        # move to first line
        cursor.setPosition(sel_start)

        # we uncomment if all lines were commented, otherwise we comment all
        # lines in selection
        comment = False
        for i in range(nb_lines):
            cursor.movePosition(QtGui.QTextCursor.StartOfLine)
            cursor.movePosition(QtGui.QTextCursor.EndOfLine, cursor.KeepAnchor)
            line = cursor.selectedText().lstrip()
            if not line.strip():
                # skips empty lines
                continue
            indent = len(cursor.selectedText()) - len(line)
            if not line.startswith("# "):
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
                    cursor.movePosition(cursor.Right, cursor.KeepAnchor, 2)
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
                    cursor.insertText("# ")
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

    def _on_key_pressed(self, event):
        if(event.modifiers() & QtCore.Qt.ControlModifier and
           event.key() == QtCore.Qt.Key_Slash):
            event.accept()
            self.comment()
