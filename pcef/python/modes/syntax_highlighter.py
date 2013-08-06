#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# PCEF - Python/Qt Code Editing Framework
# Copyright 2013, Colin Duquesnoy <colin.duquesnoy@gmail.com>
#
# This software is released under the LGPLv3 license.
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
""" This module contains the python specific syntax highlighter
"""
from pcef.core import TextStyle, memoized, SyntaxHighlighter
from pcef.qt.QtCore import QRegExp
from pcef.qt.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter
from pcef.core.mode import Mode


# Default highlighter styles values, mostly for the python highlighter but they
# may be shared between different highlighter/languages
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
    """ Syntax highlighter for the Python language.
    """
    IDENTIFIER = "pyHighlighterMode"
    _DESCRIPTION = "Custom QSyntaxHighlighter to highlight python syntax"

    # Python keywords
    keywords = [
        'and', 'assert', 'break', 'continue', 'def', 'class',
        'del', 'elif', 'else', 'except', 'exec', 'finally',
        'for', 'from', 'global', 'if', 'import', 'in',
        'is', 'lambda', 'not', 'or', 'pass', 'print',
        'raise', 'return', 'try', 'while', 'yield',
        'None', 'True', 'False', "with"
    ]

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

    # Python operators
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

    docstringTags = [
        ":param", ":type", ":return", ":rtype", ":raise", ":except",
        "@param", "@type", "@return", "@rtype", "@raise", "@except",
        ".. note", ".. warning"
    ]

    # Python braces
    braces = [
        '\{', '\}', '\(', '\)', '\[', '\]',
    ]
    punctuations = ["\:", "\,", "\."]

    def __init__(self, document=None):
        SyntaxHighlighter.__init__(self, document)
        self.__doc = document
        Mode.__init__(self)
        self.tri_single = (QRegExp("'''"), 1, 'docstring')
        self.tri_double = (QRegExp('"""'), 2, 'docstring')

        self.cnt = 0

        rules = []

        self.spacesPattern = QRegExp(r'\s+')
        self.wordsPattern = QRegExp(r'\s+')

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

        # Build a QRegExp for each pattern
        self.rules = [(QRegExp(pat), fmt) for (pat, fmt) in rules]
        print(self.rules)

    @memoized
    def format(self, style_key, current_style_bck):
        """
        Return a QTextCharFormat with the given attributes.

        :param current_style_bck: Used to clear cache
        """
        if isinstance(style_key, QColor):
            value = style_key
        else:
            value = self.editor.style.value(style_key, "Python")
        if isinstance(value, QColor):
            _color = value
            _format = QTextCharFormat()
            _format.setForeground(_color)
            return _format
        else:
            _format = QTextCharFormat()
            _format.setForeground(value.color)
            if value.bold:
                _format.setFontWeight(QFont.Bold)
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
        elif key == "background":
            self.__bck = self.editor.style.value("background").name()

    @memoized
    def formatFromWord(self, word):
        if word in self.keywords:
            return "keyword"
        if word in self.builtins:
            return "builtins"
        # if word in self.docstringTags:
        #     return "docstringTag"
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
        index = self.wordsPattern.indexIn(text)
        while index >= 0:
            l = self.wordsPattern.matchedLength()
            word = text[index:index + l]
            fmt = self.formatFromWord(word)
            if fmt:
                self.setFormat(index, l, self.format(fmt, self.__bck))
            index = self.wordsPattern.indexIn(text, index + l)

    def highlightBlock(self, text):
        """
        Apply syntax highlighting to the given block of text.
        """
        SyntaxHighlighter.highlightBlock(self, text)
        if self.match_multiline(text):
            self.highlightDocstringTags(text)
            self.highlightSpaces(text)
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

        #Spaces
        self.highlightSpaces(text)

    def match_multiline(self, text):
        """
        Highlight multilines
        """
        multi = False
        state = 0
        original_text = text
        text = text.strip()
        # single quoted
        if text.startswith("'''") or text.endswith("'''"):
            # begin of comment
            if self.previousBlockState() == 1:
                # end of comment
                multi = True
                state = 0
            elif (self.previousBlockState() == 0 or
                    self.previousBlockState() == -1):
                # start of single quoted comment
                multi = True
                state = 1
            else:
                # in double quoted doctring
                multi = True
                state = 2
        elif text.startswith('"""') or text.endswith('"""'):
            if self.previousBlockState() == 2:
                # end of comment
                multi = True
                state = 0
            elif (self.previousBlockState() == 0 or
                    self.previousBlockState() == -1):
                # start of comment
                multi = True
                state = 2
            else:
                multi = True
                state = 1
        else:
            if self.previousBlockState() > 0:
                multi = True
                state = self.previousBlockState()
        if multi:
            self.setFormat(0, len(original_text), self.format("docstring",
                                                              self.__bck))
        self.setCurrentBlockState(state)
        return multi
