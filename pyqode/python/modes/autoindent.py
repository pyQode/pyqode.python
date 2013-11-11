#!/usr/bin/env python
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
""" Contains smart indent modes """
from pyqode.qt.QtGui import QTextCursor
from pyqode.core.modes.autoindent import AutoIndentMode


class PyAutoIndentMode(AutoIndentMode):
    """
    Customised :class:`pyqode.core.AutoIndentMode` for python, the indentation
    level is based on the previous line indent but is automatically incremented
    after a *:* and decremented after *pass* or *return*
    """
    #: Mode identifier
    IDENTIFIER = "pyAutoIndentMode"
    #: Mode description
    _DESCRIPTION = """ This mode provides python specific auto indentation. """

    def __init__(self):
        super(PyAutoIndentMode, self).__init__()

    def _getIndent(self, tc):
        col = self.editor.cursorPosition[1]
        pos = tc.position()
        if pos != 0 and col != 0:
            pre, indent = AutoIndentMode._getIndent(self, tc)
            tc.movePosition(QTextCursor.WordLeft)
            tc.select(QTextCursor.WordUnderCursor)
            last_word = tc.selectedText().strip()
            tc.select(QTextCursor.LineUnderCursor)
            full_line = tc.selectedText()
            line = full_line[:col]
            full_line.lstrip()
            line.lstrip()
            tc.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, 1)
            if full_line.endswith(":"):
                kw = ["if", "def", "while", "for", "else", "elif", "except", "finally"]
                l = full_line
                ln = tc.blockNumber() + 1
                def check_kw_in_line(kws, l):
                    for kw in kws:
                        if kw in l:
                            return True
                    return False
                while not check_kw_in_line(kw, l) and ln:
                    ln -= 1
                    l = self.editor.lineText(ln)
                indent = (len(l) - len(l.lstrip())) * " "
                indent += 4 * " "
            if line.endswith("\\"):
                indent += 4 * " "
            elif last_word in ["return", "pass"]:
                indent = indent[4:]
            if line.startswith("#"):
                indent += "# "
            if line.endswith(")"):
                # find the indent of the line where the opening brace can be found.
                if hasattr(self.editor, "symbolMatcherMode"):
                    ln, cn = self.editor.symbolMatcherMode.getOpeningSymbolPos(
                        self.editor.textCursor())
                    if ln and cn:
                        l = self.editor.lineText(ln)
                        indent = (len(l) - len(l.lstrip())) * " "
            data = tc.block().userData()
            nb_open = 0
            nb_closed = 0
            for paren in data.parentheses:
                if paren.position > col - 1:
                    break
                if paren.character == "(":
                    nb_open += 1
                if paren.character == ")":
                    nb_closed += 1
            if nb_open > nb_closed:
                if nb_open - nb_closed <= 1 and ("," in line or last_word == "%"):
                    indent = (data.parentheses[0].position + 1) * " "
                else:
                    indent += 4 * " "
            elif ((nb_open == nb_closed or nb_open == 0) and
                  (len(full_line) - len(line) > 0)):
                if not "\\" in full_line:
                    pre = "\\"
            tc.setPosition(pos)
            return pre, indent
        return "", ""
