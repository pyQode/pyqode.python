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
""" Contains the python autocomplete mode """
import jedi
from pyqode.qt import QtGui
from pyqode.core import AutoCompleteMode


class PyAutoCompleteMode(AutoCompleteMode):
    """
    Extends :class:`pyqode.core.AutoCompleteMode` to add support for function docstring and
    method/function call.

    Docstring completion adds a `:param` sphinx tag foreach parameter in the
    above function.

    Function completion adds "):" to function definition.

    Method completion adds "self):" to method definition.
    """

    def _formatFuncParams(self, indent):
        parameters = ""
        l = self.editor.cursorPosition[0] - 1
        c = indent + len("def ") + 1
        script = jedi.Script(self.editor.toPlainText(), l, c,
                             self.editor.filePath,
                             self.editor.fileEncoding)
        definition = script.goto_definitions()[0]
        for defined_name in definition.defined_names():
            if defined_name.name != "self":
                parameters += "\n{1}:param {0}:".format(
                    defined_name.name, indent * " ")
        toInsert = '"\n{0}{1}\n{0}""'.format(indent * " ", parameters)
        return toInsert

    def _insertDocstring(self, prevLine):
        indent = self.editor.getLineIndent()
        if "class" in prevLine:
            toInsert = '"\n{0}\n{0}""'.format(indent * " ")
        else:
            toInsert = self._formatFuncParams(indent)
        tc = self.editor.textCursor()
        p = tc.position()
        tc.insertText(toInsert)
        tc.setPosition(p)  # we are there ""|"
        tc.movePosition(tc.Down)
        self.editor.setTextCursor(tc)

    def _inMethodCall(self):
        l = self.editor.cursorPosition[0] - 1
        expected_indent = self.editor.getLineIndent() - 4
        while l >= 0:
            text = self.editor.lineText(l)
            indent = len(text) - len(text.lstrip())
            if indent == expected_indent and 'class' in text:
                return True
            l -= 1
        return False

    def _handleFctDef(self):
        if self._inMethodCall():
            txt = "self):"
        else:
            txt = "):"
        tc = self.editor.textCursor()
        tc.insertText(txt)
        tc.movePosition(tc.Left, tc.MoveAnchor, 2)
        self.editor.setTextCursor(tc)

    def _onPostKeyPressed(self, e):
        prevLine = self.editor.lineText(self.editor.cursorPosition[0] - 1)
        isBelowFuncOrClassDef = "def" in prevLine or "class" in prevLine
        if (e.text() == '"' and '"""' == self.editor.currentLineText.strip()
                and isBelowFuncOrClassDef):
            self._insertDocstring(prevLine)
        elif e.text() == "(" and "def" in self.editor.currentLineText:
            self._handleFctDef()
        else:
            super(PyAutoCompleteMode, self)._onPostKeyPressed(e)
