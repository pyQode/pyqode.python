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
#th pyQode. If not, see http://www.gnu.org/licenses/.
#
""" This module contains the python specific syntax highlighter
"""
import sys
from pyqode.core import TextStyle, SyntaxHighlighter
from pyqode.core.system import memoized
from pyqode.qt import QtGui, QtCore
from pyqode.core import Mode, IndentBasedFoldDetector


#: Default (white) color scheme for :class:`pyqode.python.PyHighlighterMode`
#: Those values are added to :attr:`pyqode.core.QCodeEdit.style` properties in
#: the *Python* section
DEFAULT_LIGHT_STYLES = {
    'keyword': TextStyle('#808000 nbold nitalic nunderlined'),
    'builtins': TextStyle('#808000 nbold nitalic nunderlined'),
    'operator': TextStyle('darkGray nbold nitalic nunderlined'),
    'punctuation': TextStyle('darkGray nbold nitalic nunderlined'),
    'decorator': TextStyle('#808000 nbold nitalic nunderlined'),
    'brace': TextStyle('#404040 nbold nitalic nunderlined'),
    'class': TextStyle('#800080 nbold nitalic nunderlined'),
    'function': TextStyle('#800080 nbold nitalic nunderlined'),
    'string': TextStyle('#008000 nbold nitalic nunderlined'),
    'docstring': TextStyle('#0000AA nbold nitalic nunderlined'),
    'comment': TextStyle('#008000 nbold italic nunderlined'),
    'self': TextStyle('#8F2828 nbold italic nunderlined'),
    'numbers': TextStyle('#000080 nbold nitalic nunderlined'),
    'predefined': TextStyle('#B200B2 nbold nitalic nunderlined'),
    'docstringTag': TextStyle('#0000FF nbold nitalic underlined'),
}

#: Alternative dark color scheme for :class:`pyqode.python.PyHighlighterMode`
#: Those values are added to :attr:`pyqode.core.QCodeEdit.style` properties in
#: the *Python* section
DEFAULT_DARK_STYLES = {
    'keyword': TextStyle('#CC7832 bold nitalic nunderlined'),
    'builtins': TextStyle('#CC7832 nbold nitalic nunderlined'),
    'operator': TextStyle('#A9B7C6 nbold nitalic nunderlined'),
    'punctuation': TextStyle('#A9B7C6 nbold nitalic nunderlined'),
    'decorator': TextStyle('#BBB529 nbold nitalic nunderlined'),
    'brace': TextStyle('#AAAAAA nbold nitalic nunderlined'),
    'class': TextStyle('#A9B7C6 bold nitalic nunderlined'),
    'function': TextStyle('#A9B7C6 bold nitalic nunderlined'),
    'string': TextStyle('#A5C261 nbold nitalic nunderlined'),
    'docstring': TextStyle('#629755 nbold nitalic nunderlined'),
    'comment': TextStyle('#808080 nbold italic nunderlined'),
    'self': TextStyle('#94558D nbold italic nunderlined'),
    'numbers': TextStyle('#6897B3 nbold nitalic nunderlined'),
    'predefined': TextStyle('#B200B2 nbold nitalic nunderlined'),
    'docstringTag': TextStyle('#427735 bold nitalic underlined')
}


class PyHighlighterMode(SyntaxHighlighter, Mode):
    """
    Syntax highlighter specifically crafted for the Python programming language.

    Contrarily to :class:`pyqode.core.PygmentsSyntaxHighlighter` this syntax
    highlighter highlights multi-line comments and docstrings properly.
    Its color scheme is entirely configurable (the properties are available in
    the Python section of :attr:`pyqode.core.QCodeEdit.style`).

    .. note:: To detect and remember multi-line strings/docstrings we use
              :attr:`QtGui.QTextBlock.userState` which is a bitmask combination
              that store two information:

                  * the 7 first **bits** are used to store the following states:

                      - 0: not a multi-line string/docstring
                      - 1: start of multi-line string/docstring
                      - 2: multi-line string/docstring

                  * the 8th **bit** is used to make the difference between a
                    docstring and a string which are highlighted with a different
                    color.
    """
    _DESCRIPTION = "Custom QtGui.QSyntaxHighlighter to highlight python syntax"

    #: List of python keywords
    keywords = [
        'and', 'assert', 'break', 'continue', 'def', 'class',
        'del', 'elif', 'else', 'except', 'exec', 'finally',
        'for', 'from', 'global', 'if', 'import', 'in',
        'is', 'lambda', 'not', 'or', 'pass', 'print',
        'raise', 'return', 'try', 'while', 'yield',
        'None', 'True', 'False', "with"
    ]

    #: List of builtins
    builtins = [
        "__import__", "abs", "all", "any", "apply", "basestring", "bin",
        "bool", "buffer", "bytearray", "bytes", "callable", "chr",
        "classmethod", "cmp", "coerce", "compile", "complex", "delattr",
        "dict", "dir", "divmod", "enumerate", "eval", "execfile", "exit",
        "file", "filter", "float", "frozenset", "getattr", "globals",
        "hasattr", "hash", "hex", "id", "as",
        "input", "int", "intern", "isinstance", "issubclass", "iter", "len",
        "list", "locals", "long", "map", "max", "min", "next", "object", "oct",
        "open", "ord", "pow", "property", "range", "raw_input", "reduce",
        "reload", "repr", "reversed", "round", "set", "setattr", "slice",
        "sorted", "staticmethod", "str", "sum", "super", "tuple", "type",
        "unichr", "unicode", "vars", "xrange", "zip", "None", "Ellipsis",
        "NotImplemented", "False", "True", "ArithmeticError", "AssertionError",
        "AttributeError", "BaseException", "DeprecationWarning", "EOFError",
        "EnvironmentError", "Exception", "FloatingPointError", "FutureWarning",
        "GeneratorExit", "IOError", "ImportError", "ImportWarning",
        "IndentationError", "IndexError", "KeyError", "KeyboardInterrupt",
        "LookupError", "MemoryError", "NameError", "NotImplemented",
        "NotImplementedError", "OSError", "OverflowError", "OverflowWarning",
        "PendingDeprecationWarning", "ReferenceError", "RuntimeError",
        "RuntimeWarning", "StandardError", "StopIteration", "SyntaxError",
        "SyntaxWarning", "SystemError", "SystemExit", "TabError", "TypeError",
        "UnboundLocalError", "UnicodeDecodeError", "UnicodeEncodeError",
        "UnicodeError", "UnicodeTranslateError", "UnicodeWarning",
        "UserWarning", "ValueError", "VMSError", "Warning", "WindowsError",
        "ZeroDivisionError"]

    #: List of python operators
    operators = [
        '=',
        # Comparison
        '==', '!=', '<', '<=', '>', '>=',
        # Arithmetic
        '\+', '-', '\*', '/', '//', '\%', '\*\*',
        # In-place
        '\+=', '-=', '\*=', '/=', '\%=',
        # Bitwise
        '\^', '\|', '\&', '\~', '>>', '<<',
    ]

    #: List of docstring tags (only Sphinx atm)
    docstringTags = [
        ":param", ":type", ":return", ":rtype", ":raise", ":except",
        "@param", "@type", "@return", "@rtype", "@raise", "@except",
        ".. note", ".. warning"
    ]

    #: List of special punctuation
    braces = [
        '\{', '\}', '\(', '\)', '\[', '\]',
    ]

    #: List of highlighted punctuations
    punctuations = ["\:", "\,", "\."]

    def __init__(self, document=None):
        SyntaxHighlighter.__init__(self, document,
                                   foldDetector=IndentBasedFoldDetector())
        self.__doc = document
        Mode.__init__(self)
        self.tri_single = (QtCore.QRegExp("'''"), 1, 'docstring')
        self.tri_double = (QtCore.QRegExp('"""'), 2, 'docstring')

        self.cnt = 0

        rules = []

        self.spacesPattern = QtCore.QRegExp(r'\s+')
        self.wordsPattern = QtCore.QRegExp(r'\s+')
        self.docstringPattern = QtCore.QRegExp(r"(:|@)\w+")

        # All other rules
        rules += [
            # 'def' followed by an identifier
            (r'\bdef\b\s*(\w+)', 'function'),
            # 'class' followed by an identifier
            (r'\bclass\b\s*(\w+)', 'class'),
            # words (keywords, builtin, ...
            (r'\b\w+\b', 'word'),
            # predefined items (__xxx__)
            (r'\b__.*__\b', 'predefined'),

            (r'@.*', 'decorator'),

            # Numeric literals
            (r'\b[+-]?[0-9]+[lL]?\b', 'numbers'),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 'numbers'),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 'numbers'),
        ]
        # Double-quoted string, possibly containing escape sequences
        rules += [(r'%s' % o, 'operator')
                  for o in PyHighlighterMode.operators]

        rules += [(r'#[^\n]*', 'comment')]

        # Single-quoted string, possibly containing escape sequences
        rules += [(r'"[^"\\]*(\\.[^"\\]*)*"', 'string')]
        rules += [(r"'[^'\\]*(\\.[^'\\]*)*'", 'string')]

        # Build a QtCore.QRegExp for each pattern
        self.rules = [(QtCore.QRegExp(pat), fmt) for (pat, fmt) in rules]

    @memoized
    def format(self, style_key, current_style_bck):
        if isinstance(style_key, QtGui.QColor):
            value = style_key
        else:
            value = self.editor.style.value(style_key, "Python")
        if isinstance(value, QtGui.QColor):
            _color = value
            _format = QtGui.QTextCharFormat()
            _format.setForeground(_color)
            return _format
        else:
            _format = QtGui.QTextCharFormat()
            _format.setForeground(value.color)
            if value.bold:
                _format.setFontWeight(QtGui.QFont.Bold)
            if value.italic:
                _format.setFontItalic(True)
            if value.underlined:
                _format.setFontUnderline(True)
        return _format

    def _onInstall(self, editor):
        Mode._onInstall(self, editor)
        for k, v in DEFAULT_LIGHT_STYLES.items():
            self.editor.style.addProperty(k, v, "Python")
        self.__foreground = self.editor.style.value(
            "whiteSpaceForeground")
        self.__bck = self.editor.style.value("background").name()

    def _onStateChanged(self, state):
        if state:
            self.setDocument(self.editor.document())
        else:
            self.setDocument(None)

    def _onStyleChanged(self, section, key):
        if not key:
            self.__foreground = self.editor.style.value(
                "whiteSpaceForeground")
            self.__bck = self.editor.style.value("background").name()
            self.rehighlight()
        if key == "whiteSpaceForeground":
            self.__foreground = self.editor.style.value(
                "whiteSpaceForeground")
            self.rehighlight()
        elif key == "background":
            self.__bck = self.editor.style.value("background").name()
            self.rehighlight()

    def rehighlight(self, *args, **kwargs):
        self.__cancelMemoizeCache()
        SyntaxHighlighter.rehighlight(self)

    @memoized
    def formatFromWord(self, word):
        if word in self.keywords:
            return "keyword"
        if word in self.builtins:
            return "builtins"
        if word in self.braces:
            return "braces"
        if word in self.punctuations:
            return "punctuation"
        if word == "self":
            return word
        return None

    def highlightSpaces(self, text):
        expression = self.spacesPattern
        index = expression.indexIn(text, 0)
        while index >= 0:
            index = expression.pos(0)
            length = len(expression.cap(0))
            self.setFormat(index, length, self.format(self.__foreground,
                                                      self.__bck))
            index = expression.indexIn(text, index + length)

    def highlightDocstringTags(self, text):
        index = self.docstringPattern.indexIn(text, 0)
        while index >= 0:
            length = self.docstringPattern.matchedLength()
            self.setFormat(index, length, self.format("docstringTag",
                                                      self.__bck))
            index = self.docstringPattern.indexIn(text, index + length)

    def doHighlightBlock(self, text):
        if self.match_multiline(text):
            self.highlightSpaces(text)
            self.highlightDocstringTags(text)
            return
        for expression, fmt in self.rules:
            index = expression.indexIn(text)
            # used = False
            toApply = fmt
            while index >= 0:
                l = expression.matchedLength()
                if fmt == "word":
                    word = text[index:index + l]
                    toApply = self.formatFromWord(word)
                if toApply:
                    self.setFormat(index, l, self.format(toApply, self.__bck))
                index = expression.indexIn(text, index + l)
                if fmt == "string" or fmt == "comment":
                    self.setCurrentBlockState(4)
        #Spaces
        self.highlightSpaces(text)

    def match_multiline(self, text):
        #
        # checks if the text is a multi-line comment, makes the difference
        # between single quote and double quote, makes the difference between
        # a multi line string and multi line docstring.
        #
        multi = False
        state = 0
        original_text = text
        text = text.strip()
        if text.startswith("#"):
            return False

        # retrieve value from state, is the previous line a multi-line
        # string or docstring?
        # state is the stored in the two first bits
        # 0: not a multi-line comment or the last line
        # 1: start of multi-line comment
        # 2: multi-line comment (not start nor end)
        prevState = self.previousBlockState() & 0x2
        # docstring or string is stored in bit 8
        # 0: string
        # 1: docstring
        wasDocstring = self.previousBlockState() & 0x80
        if self.previousBlockState() == -1:
            prevState = 0
            wasDocstring = 0

        # check for mutli-line string that is not a docstring (a var)
        docstring = 0x80
        if prevState == 0 and "=" in text:
            text = text.split("=")[1].strip()
            docstring = 0

        # single quoted
        if text.startswith("'''") or text.endswith("'''"):
            if prevState == 1:
                # end of comment
                multi = True
                state = 0
                docstring = wasDocstring
            elif prevState == 0 or prevState == -1:
                state = 1
                # start of single quoted comment
                if text.startswith("'''") and text.endswith("'''") and len(text) > 6:
                    state = 0
                multi = True
            else:
                # in single quoted docstring/string
                multi = True
                state = 2
                docstring = wasDocstring
        elif text.startswith('"""') or text.endswith('"""'):
            if prevState == 2:
                # end of comment
                multi = True
                state = 0
                docstring = wasDocstring
            elif prevState == 0 or prevState == -1:
                # start of comment
                multi = True
                state = 2
                # start of single quoted string/docstring
                if text.startswith('"""') and text.endswith('"""') and len(text) > 6:
                    state = 0
            else:
                multi = True
                state = 1
                docstring = wasDocstring
        else:
            if prevState > 0:
                multi = True
                state = prevState
                docstring = wasDocstring
        if multi:
            fmt = "docstring"
            if not docstring:
                fmt = "string"
            self.setFormat(len(original_text) - len(text),
                           len(text), self.format(fmt, self.__bck))
        # takes multi-line type into account
        state |= docstring
        self.setCurrentBlockState(state)
        # print("State:", state)
        return multi

    def __cancelMemoizeCache(self):
        def nextInt():
            for i in range(sys.maxsize):
                yield i

        self.__bck = nextInt()
