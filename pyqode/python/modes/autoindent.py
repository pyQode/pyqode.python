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

    def isOperator(self, word):
        operators = ['.', ',', '+', '-', '/', '*', 'or', 'and', "=", "%",
                     "=="]
        return word in operators

    def inStringDef(self, full_line, column):
        count = 0
        last = ""
        for i in range(column):
            if full_line[i] == "'" or full_line[i] == '"':
                count += 1
                last = full_line[i]
        count_after_col = 0
        for i in range(column, len(full_line)):
            if full_line[i] == "'" or full_line[i] == '"':
                count_after_col += 1
        return count % 2 != 0 and count_after_col == 1, last

    def _getIndent(self, tc):
        # if we are in disabled cc, use the parent implementation
        column = self.editor.cursorPosition[1]
        usd = self.editor.textCursor().block().userData()
        for start, end in usd.cc_disabled_zones:
            if start <= column < end:
                return super(PyAutoIndentMode, self)._getIndent(tc)
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
            line = line.lstrip()
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
            # si dans un string
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
                if paren.position >= col and nb_open:
                    break
                if paren.character == "(":
                    nb_open += 1
                if paren.character == ")":
                    nb_closed += 1
            if nb_open > nb_closed:
                # align with first parameter
                if nb_open - nb_closed != 0 and ("," in line or last_word == "%"):
                    indent = (data.parentheses[0].position + 1) * " "
                # no parameters declare, indent normally
                else:
                    indent += 4 * " "
            elif ((nb_open == nb_closed or nb_closed == 0) and
                  (len(full_line) - len(line) > 0)):
                if (not "\\" in full_line and not "#" in full_line and
                        self.isOperator(last_word)):
                    pre += "\\"
                    indent += 4 * " "

            inString, lastChar = self.inStringDef(full_line, col)
            if inString:
                if ((nb_open == nb_closed)
                    and (len(full_line) - len(line) > 0)):
                    pre += "\\"
                    indent += 4 * " "
                pre = lastChar + pre
                indent = indent + lastChar
            tc.setPosition(pos)
            return pre, indent
        return "", ""
