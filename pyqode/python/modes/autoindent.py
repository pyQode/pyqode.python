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
        char = "'"
        for i in range(len(fullLine)):
            if fullLine[i] == "'" or fullLine[i] == '"':
                count += 1
            if fullLine[i] == '"' and i < column:
                char = '"'
        count_after_col = 0
        for i in range(column, len(fullLine)):
            if fullLine[i] == "'" or fullLine[i] == '"':
                count_after_col += 1
        return count % 2 == 0 and count_after_col % 2 == 1, char

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
        # does it have an opened paren on the same line?
        for symbols in lists:
            for paren in symbols:
                if paren.position >= col:
                    break
                if self.isOpenParen(paren):
                    nb_open += 1
                if self.isClosedParen(paren):
                    nb_closed += 1
        block = tc.block().next()
        # if not, is there an non closed paren on the next lines.
        parens = {'(': 0, '{': 0, '[': 0}
        matching = {')': '(', '}': '{', ']': '['}
        if not nb_open > nb_closed:
            while block.isValid():
                data = block.userData()
                lists = [data.parentheses, data.braces, data.squareBrackets]
                for symbols in lists:
                    for paren in symbols:
                        if self.isOpenParen(paren):
                            parens[paren.character] += 1
                        if self.isClosedParen(paren):
                            parens[matching[paren.character]] -= 1
                            if parens[matching[paren.character]] < 0:
                                return True
                block = block.next()
            return False
        else:
            return True

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
        tc2.movePosition(QTextCursor.Left, 1)
        tc2.movePosition(QTextCursor.WordLeft, tc.KeepAnchor)
        # tc2.movePosition(QTextCursor.Right, tc.KeepAnchor,
        #                  self.editor.cursorPosition[1])
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
        pos = None
        char = None
        ln = tc.blockNumber() + 1
        tc_trav = QTextCursor(tc)
        while ln > 1:
            tc_trav.movePosition(tc_trav.StartOfLine, tc_trav.MoveAnchor)
            data = tc_trav.block().userData()
            lists = [data.parentheses, data.braces, data.squareBrackets]
            for symbols in lists:
                for paren in reversed(symbols):
                    if paren.position < column:
                        if self.isOpenParen(paren):
                            if paren.position > column:
                                continue
                            else:
                                pos = tc_trav.position() + paren.position
                                char = paren.character
                                # ensure it does not have a closing paren on the
                                # same line
                                tc3 = QTextCursor(tc)
                                tc3.setPosition(pos)
                                l, c = self.editor.symbolMatcherMode.getSymbolPos(
                                    tc3, ')')
                                if l == ln and c < column:
                                    continue
                                return pos, char
            # check previous line
            tc_trav.movePosition(tc_trav.Up, tc_trav.MoveAnchor)
            ln = tc_trav.blockNumber() + 1
            column = len(self.editor.lineText(ln))
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

    def getNextChar(self, tc):
        tc2 = QTextCursor(tc)
        tc2.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor)
        char = tc2.selectedText()
        return char

    def handleIndentAfterParen(self, column, line, fullLine, tc):
        # elements might be separated by ',' 'or' 'and'
        nextChar = self.getNextChar(tc)
        nextCharIsClosingSymbol = nextChar in [']', ')', '}']
        (oL, oC), (cL, cC) = self.getParenPos(tc, column)
        closingLine = self.editor.lineText(cL)
        openingLine = self.editor.lineText(oL)
        openingIndent = len(openingLine) - len(openingLine.lstrip())
        tokens = [t.strip() for t in re.split(', |and |or ',
                                              line[oC:column]) if t]

        # align with first token pos
        if len(closingLine) > cC and closingLine[cC] == ":":
            post = openingIndent * " " + 8 * " "
        else:
            # press enter before a '}', ']', ')'
            # which close an affectation (tuple, list , dict)
            if nextCharIsClosingSymbol and re.match('.*=[\s][\W].*',
                                                    openingLine):
                post = openingIndent * " "
            else:
                # align elems in list, tuple, dict
                if re.match('.*=[\s][\W].*', openingLine):
                    post = openingIndent * " " + 4 * " "
                # align elems in fct declaration (we align with first
                # token)
                else:
                    if len(tokens):
                        post = oC * " "
                    else:
                        post = openingIndent * " " + 4 * " "
        pre = ""
        inStringDef, char = self.inStringDef(fullLine, column)
        if inStringDef:
            pre = char
            post += char
        return pre, post

    def atBlockStart(self, tc, line):
        """
        Improve QTextCursor.atBlockStart to ignore spaces
        """
        if tc.atBlockStart():
            return True
        column = tc.columnNumber()
        indentation = len(line) - len(line.lstrip())
        return column <= indentation

    def atBlockEnd(self, tc, fullLine):
        if tc.atBlockEnd():
            return True
        column = tc.columnNumber()
        return column >= len(fullLine.rstrip()) - 1

    def _getIndent(self, tc):
        pos = tc.position()
        ln, column = self.editor.cursorPosition
        fullLine = self.getfullLine(tc)
        line = fullLine[:column]
        # no indent
        if pos == 0 or column == 0:
            return "", ""
        pre, post = AutoIndentMode._getIndent(self, tc)
        if self.atBlockStart(tc, line):
            return pre, post
        # return pressed in comments
        if self.inComment(column, tc, fullLine):
            if line.strip().startswith("#") and column != len(fullLine):
                post = post + '#'
            return pre, post
        elif self.betweenParen(tc, column):
            pre, post = self.handleIndentAfterParen(column, line, fullLine, tc)
        else:
            lastWord = self.getLastWord(tc)
            inStringDef, char = self.inStringDef(fullLine, column)
            if inStringDef:
                # the string might be between paren if multiline
                # check if there a at least a non closed paren on the previous
                # lines
                if self.isStringBetweenParams(tc):
                    pre =  char
                else:
                    pre = '" \\'
                    post += 4 * ' '
                if fullLine.endswith(':'):
                    post += 4 * " "
                post += char
            elif fullLine.rstrip().endswith(":") and \
                    lastWord.rstrip().endswith(':') and self.atBlockEnd(
                    tc, fullLine):
                try:
                    indent = self.getIndentOfOpeningParen(tc, column) + 4
                    if indent:
                        post = indent * " "
                except TypeError:
                    kw = ["if", "class", "def", "while", "for", "else", "elif", "except", "finally", "try"]
                    l = fullLine
                    ln = tc.blockNumber()
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
                    post = indent
            elif fullLine.endswith("\\"):
                # increment indent
                post = post + 4 * " "
            elif fullLine.endswith(")") and lastWord.endswith(')'):
                # find line where the open braces can be found and align with
                # that line
                indent = self.getIndentOfOpeningParen(tc, column)
                if indent:
                    post = indent * " "
            elif (not "\\" in fullLine and not "#" in fullLine and
                      fullLine.strip() and not fullLine.endswith(')') and
                      not self.atBlockEnd(tc, fullLine)):
                if lastWord and lastWord[-1] != " ":
                    pre += " \\"
                else:
                    pre += '\\'
                post += 4 * " "
                if fullLine.endswith(':'):
                    post += 4 * " "
            elif (lastWord == "return" or lastWord == "pass" or
                    self.twoPrevEmptyLine(tc)):
                post = post[:-4]

        return pre, post
