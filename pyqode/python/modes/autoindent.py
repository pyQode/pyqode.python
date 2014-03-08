#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#The MIT License (MIT)
#
#Copyright (c) <2013-2014> <Colin Duquesnoy and others, see AUTHORS.txt>
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
import re
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
        operators = ['.', ',', '+', '-', '/', '*', 'or', 'and', "=", "%", "=="]
        return word in operators

    def twoPrevEmptyLine(self, tc):
        ln = tc.blockNumber()
        limit = ln - 1
        while ln > limit:
            if self.editor.lineText(ln).strip() != "":
                return False
            ln -= 1
        return True

    def isStringBetweenParams(self, tc):
        ln = tc.blockNumber()
        while ln >= 0:
            line = self.editor.lineText(ln)
            if line.count("(") > line.count(")"):
                return True
            ln -= 1
        return False

    def inStringDef(self, fullLine, column):
        count = 0
        for i in range(len(fullLine)):
            if fullLine[i] == "'" or fullLine[i] == '"':
                count += 1
        count_after_col = 0
        for i in range(column, len(fullLine)):
            if fullLine[i] == "'" or fullLine[i] == '"':
                count_after_col += 1
        return count % 2 == 0 and count_after_col == 1

    def isOpenParen(self, paren):
        return (paren.character == "(" or paren.character == "["
                or paren.character == '{')

    def isClosedParen(self, paren):
        return (paren.character == ")" or paren.character == "]"
                or paren.character == '}')

    def getfullLine(self, tc):
        tc2 = QTextCursor(tc)
        tc2.select(QTextCursor.LineUnderCursor)
        full_line = tc2.selectedText()
        return full_line

    def betweenParen(self, tc, col):
        data = tc.block().userData()
        nb_open = 0
        nb_closed = 0
        lists = [data.parentheses, data.braces, data.squareBrackets]
        for symbols in lists:
            for paren in symbols:
                if paren.position >= col:
                    break
                if self.isOpenParen(paren):
                    nb_open += 1
                if self.isClosedParen(paren):
                    nb_closed += 1
        return nb_open > nb_closed

    def inComment(self, column, tc, fullLine):
        useParentImpl = False
        usd = tc.block().userData()
        for start, end in usd.cc_disabled_zones:
            if start < column < end:
                string = fullLine[start:end]
                if not ((string.startswith("'") or
                        string.startswith('"')) and
                        (string.endswith("'") or
                         string.endswith('"'))):
                    useParentImpl = True
                    break
        return useParentImpl

    def getLastWord(self, tc):
        tc2 = QTextCursor(tc)
        tc2.movePosition(QTextCursor.WordLeft)
        tc2.select(QTextCursor.WordUnderCursor)
        return tc2.selectedText().strip()

    def getIndentOfOpeningParen(self, tc, column):
        # find last closed paren
        pos = None
        data = tc.block().userData()
        tc2 = QTextCursor(tc)
        tc2.movePosition(tc2.StartOfLine, tc2.MoveAnchor)
        for paren in reversed(data.parentheses):
            if paren.character == ')':
                column = paren.position
                pos = tc2.position() + column + 1
                break
        if pos:
            tc2 = QTextCursor(tc)
            tc2.setPosition(pos)
            oL, oC = self.editor.symbolMatcherMode.getSymbolPos(
                tc2, '(', 0)
            line = self.editor.lineText(oL)
            return len(line) - len(line.lstrip())
        return None

    def getLastOpenParenPos(self, tc, column):
        ln = tc.blockNumber() + 1
        tc2 = QTextCursor(tc)
        tc2.movePosition(tc2.StartOfLine, tc2.MoveAnchor)
        pos = None
        char = None
        data = tc.block().userData()
        lists = [data.parentheses, data.braces, data.squareBrackets]
        for symbols in lists:
            for paren in reversed(symbols):
                if paren.position < column:
                    if self.isOpenParen(paren):
                        column = paren.position
                        pos = tc2.position() + column
                        char = paren.character
                        # ensure it does not have a closing paren on the same
                        # line
                        tc3 = QTextCursor(tc)
                        tc3.setPosition(pos)
                        # ensure we don't have a closing paren on the same line
                        l, c = self.editor.symbolMatcherMode.getSymbolPos(tc3)
                        if l == ln:
                            continue
                        break
        return pos, char

    def getParenPos(self, tc, column):
        pos, char = self.getLastOpenParenPos(tc, column)
        if char == '(':
            pType = 0
            closingChar = ')'
        elif char == '[':
            pType = 1
            closingChar = ']'
        elif char == '{':
            pType = 2
            closingChar = '}'
        tc2 = QTextCursor(tc)
        tc2.setPosition(pos)
        oL, oC = self.editor.symbolMatcherMode.getSymbolPos(
            tc2, char, pType)
        cL, cC = self.editor.symbolMatcherMode.getSymbolPos(
            tc2, closingChar, pType)
        return (oL, oC), (cL, cC)

    def handleIndentAfterParen(self, column, line, fullLine, tc):
        # elements might be separated by ',' 'or' 'and'
        (oL, oC), (cL, cC) = self.getParenPos(tc, column)
        closingLine = self.editor.lineText(cL)
        openingLine = self.editor.lineText(oL)
        openingIndent = len(openingLine) - len(openingLine.lstrip())
        tokens = [t.strip() for t in re.split(', |and |or ',
                                              line[oC:column]) if t]
        if tokens:
            # align with first token pos
            if len(closingLine) > cC and closingLine[cC] == ":":
                post = openingIndent * " " + 8 * " "
            else:
                post = oC * " "
        else:
            if len(closingLine) > cC and closingLine[cC] == ":":
                post = openingIndent * " " + 8 * " "
            else:
                post = openingIndent * " " + 4 * " "
        pre = ""
        if self.inStringDef(fullLine, column):
            pre = '"'
            post += '"'
        return pre, post

    def _getIndent(self, tc):
        pos = tc.position()
        ln, column = self.editor.cursorPosition
        fullLine = self.getfullLine(tc)
        line = fullLine[:column]
        if pos == 0 or column == 0:
            return "", ""
        pre, post = AutoIndentMode._getIndent(self, tc)
        lastWord = self.getLastWord(tc)
        if self.inComment(column, tc, fullLine):
            if line.strip().startswith("#") and column != len(fullLine):
                post = post + '#'
            return pre, post
        elif self.betweenParen(tc, column):
            pre, post = self.handleIndentAfterParen(column, line, fullLine, tc)
        else:
            if self.inStringDef(fullLine, column):
                # the string might be between paren if multiline
                # check if there a at least a non closed paren on the previous
                # lines
                if self.isStringBetweenParams(tc):
                    pre = '"'
                    post += '"'
                else:
                    pre = '" \\'
                    post += 4 * ' ' + '"'
            elif fullLine.endswith(":"):
                indent = self.getIndentOfOpeningParen(tc, column) + 4
                if indent:
                    post = indent * " "
            elif fullLine.endswith("\\"):
                # increment indent
                post = post + 4 * " "
            elif fullLine.endswith(")"):
                # find line where the open braces can be found and align with
                # that line
                indent = self.getIndentOfOpeningParen(tc, column)
                if indent:
                    post = indent * " "
            elif (lastWord == "return" or lastWord == "pass" or
                    self.twoPrevEmptyLine(tc)):
                post = post[:-4]

        return pre, post

        #     if full_line.endswith(":"):
        #         kw = ["if", "def", "while", "for", "else", "elif", "except", "finally"]
        #         l = full_line
        #         ln = tc.blockNumber() + 1
        #
        #         def check_kw_in_line(kws, l):
        #             for kw in kws:
        #                 if kw in l:
        #                     return True
        #             return False
        #
        #         while not check_kw_in_line(kw, l) and ln:
        #             ln -= 1
        #             l = self.editor.lineText(ln)
        #         indent = (len(l) - len(l.lstrip())) * " "
        #         indent += 4 * " "
        #     # si dans un string
        #     if line.endswith("\\"):
        #         indent += 4 * " "
        #     elif last_word in ["return", "pass"]:
        #         indent = indent[4:]
        #     if line.startswith("#"):
        #         indent += "# "
        #     if line.endswith(")"):
        #         # find the indent of the line where the opening brace can be found.
        #         if hasattr(self.editor, "symbolMatcherMode"):
        #             ln, cn = self.editor.symbolMatcherMode.getOpeningSymbolPos(
        #                 self.editor.textCursor())
        #             if ln and cn:
        #                 l = self.editor.lineText(ln)
        #                 indent = (len(l) - len(l.lstrip())) * " "
        #     data = tc.block().userData()
        #     nb_open = 0
        #     nb_closed = 0
        #     lists = [data.parentheses, data.braces, data.squareBrackets]
        #     for symbols in lists:
        #         for paren in symbols:
        #             if paren.position >= col:
        #                 break
        #             if self.isOpenParen(paren):
        #                 nb_open += 1
        #             if self.isClosedParen(paren):
        #                 nb_closed += 1
        #     if nb_open > nb_closed:
        #         # align with first parameter
        #         if nb_open - nb_closed != 0 and ("," in line or "=" in line
        #                                          or last_word == "%"):
        #             paren_pos = self.getLastOpenParenPos(data, col)
        #             if ',' in line and paren_pos > line.rfind(","):
        #                 indent += 4 * " "
        #             else:
        #                 indent = (paren_pos + 1) * " "
        #         # no parameters declare, indent normally
        #         else:
        #             indent += 4 * " "
        #     elif ((nb_open == nb_closed or nb_closed == 0) and
        #           (len(full_line) - len(line) > 0)):
        #         if (not "\\" in full_line and not "#" in full_line and
        #                 self.isOperator(last_word)):
        #             pre += "\\"
        #             indent += 4 * " "
        #
        #     for symbols in lists:
        #         for paren in symbols:
        #             if self.isClosedParen(paren):
        #                 nb_closed += 1
        #     inString, lastChar = self.inStringDef(full_line, col)
        #     if inString:
        #         if nb_open == 0 and nb_closed == 0:
        #             pre += "\\"
        #             indent += 4 * " "
        #         pre = lastChar + pre
        #         indent = indent + lastChar
        #     tc.setPosition(pos)
        #     return pre, indent
        # return "", ""
