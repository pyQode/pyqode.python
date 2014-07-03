# -*- coding: utf-8 -*-
"""
This module contains the python specific syntax highlighter
"""
from pyqode.core.qt import QtGui, QtCore
from pyqode.core.api import SyntaxHighlighter
from pyqode.core.api import Mode
from pyqode.core.api.utils import TextStyle
from pyqode.core.api.utils import memoized


class PyHighlighterMode(SyntaxHighlighter):
    """
    Syntax highlighter specifically crafted for the Python programming
    language.

    Contrarily to :class:`pyqode.core.modes.PygmentsSyntaxHighlighter`
    this syntax highlighter highlights multi-line comments and docstrings
    properly.

    Its color scheme is entirely configurable through the properties exposed in
    :mod:`pyqode.python.style`

    .. note:: To detect and remember multi-line strings/docstrings we use
              :attr:`QtGui.QTextBlock.userState` which is a bitmask combination
              that store two information:

                  * the 7 first **bits** are used to store the following
                    states:

                      - 0: not a multi-line string/docstring
                      - 1: start of multi-line string/docstring
                      - 2: multi-line string/docstring

                  * the 8th **bit** is used to make the difference between a
                    docstring and a string which are highlighted with a
                    different color.
    """
    _DESCRIPTION = "Custom QtGui.QSyntaxHighlighter to highlight python syntax"

    #: Default (white) color scheme for
    #: :class:`pyqode.python.modes.PyHighlighterMode`
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

    #: Alternative dark color scheme for
    #: :class:`pyqode.python.modes.PyHighlighterMode`
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
        r'\{', r'\}', r'\(', r'\)', r'\[', r'\]',
    ]

    #: List of highlighted punctuations
    punctuations = ["\:", "\,", "\."]

    def __init__(self, document=None):
        super().__init__(document)
        self.__doc = document
        self.tri_single = (QtCore.QRegExp("'''"), 1, 'docstring')
        self.tri_double = (QtCore.QRegExp('"""'), 2, 'docstring')

        self._cache_version = -1

        rules = []

        self.space_ptrn = QtCore.QRegExp(r'\s+')
        self.words_ptrn = QtCore.QRegExp(r'\s+')
        self.docstring_ptrn = QtCore.QRegExp(r"(:|@)\w+")

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

        self._init_style()

    def _init_style(self):
        self.styles = self.DEFAULT_LIGHT_STYLES

    def refresh_style(self):
        self.styles.clear()
        del self.styles
        self._init_style()
        self._purge_mem_cache()
        if self.editor:
            self.rehighlight()

    @memoized
    def format(self, style_key, cache_version):
        """
        Returns a QTextCharFormat from a style key.

        :param style_key: QColor or style key name.
        """
        if isinstance(style_key, QtGui.QColor):
            value = style_key
        else:
            value = self.styles[style_key]
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

    def on_install(self, editor):
        Mode.on_install(self, editor)

    def on_state_changed(self, state):
        if state:
            self.setDocument(self.editor.document())
        else:
            self.setDocument(None)

    def rehighlight(self, *args, **kwargs):
        self._purge_mem_cache()
        super().rehighlight()

    @memoized
    def format_from_word(self, word):
        if word in self.keywords:
            return "keyword"
        if word in self.builtins:
            return "builtins"
        # if word in self.braces:
        #     return "braces"
        # if word in self.punctuations:
        #     return "punctuation"
        if word == "self":
            return word
        return None

    def highlight_spaces(self, text):
        expression = self.space_ptrn
        index = expression.indexIn(text, 0)
        while index >= 0:
            index = expression.pos(0)
            length = len(expression.cap(0))
            self.setFormat(index, length, self.format(
                self.editor.whitespaces_foreground, self._cache_version))
            index = expression.indexIn(text, index + length)

    def highlight_sphinx_tags(self, text):
        index = self.docstring_ptrn.indexIn(text, 0)
        while index >= 0:
            length = self.docstring_ptrn.matchedLength()
            self.setFormat(index, length, self.format("docstringTag",
                                                      self._cache_version))
            index = self.docstring_ptrn.indexIn(text, index + length)

    def highlight_block(self, text):
        usd = self.currentBlock().userData()
        if hasattr(usd, "cc_disabled_zones"):
            usd.cc_disabled_zones[:] = []
        if self.match_multiline(text):
            self.highlight_spaces(text)
            self.highlight_sphinx_tags(text)
            return
        for expression, fmt in self.rules:
            index = expression.indexIn(text)
            # used = False
            to_apply = fmt
            while index >= 0:
                l = expression.matchedLength()
                if fmt == "word":
                    word = text[index:index + l]
                    to_apply = self.format_from_word(word)
                if to_apply:
                    self.setFormat(index, l, self.format(to_apply,
                                                         self._cache_version))
                if fmt == "string":
                    usd.cc_disabled_zones.append((index, index + l))
                elif fmt == "comment":
                    usd.cc_disabled_zones.append((index, pow(2, 32)))
                index = expression.indexIn(text, index + l)
        # spaces
        self.highlight_spaces(text)

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
        prev_state = self.previousBlockState() & 0x2
        # docstring or string is stored in bit 8
        # 0: string
        # 1: docstring
        was_docstring = self.previousBlockState() & 0x80
        if self.previousBlockState() == -1:
            prev_state = 0
            was_docstring = 0

        # check for mutli-line string that is not a docstring (a var)
        docstring = 0x80
        if prev_state == 0 and "=" in text:
            text = text.split("=")[1].strip()
            docstring = 0

        # single quoted
        if text.startswith("'''") or text.endswith("'''"):
            if prev_state == 0 or prev_state == -1:
                state = 1
                # start of single quoted comment
                if (text.startswith("'''") and text.endswith("'''") and
                        len(text) > 6):
                    state = 0
                multi = True
            else:
                # in single quoted docstring/string
                multi = True
                state = 2
                docstring = was_docstring
        elif text.startswith('"""') or text.endswith('"""'):
            if prev_state == 2:
                # end of comment
                multi = True
                state = 0
                docstring = was_docstring
            else:
                # start of comment
                multi = True
                state = 2
                # start of single quoted string/docstring
                if (text.startswith('"""') and text.endswith('"""') and
                        len(text) > 6):
                    state = 0
        else:
            if prev_state > 0:
                multi = True
                state = prev_state
                docstring = was_docstring
        if multi:
            fmt = "docstring"
            if not docstring:
                fmt = "string"
            self.setFormat(len(original_text) - len(text),
                           len(text), self.format(fmt, self._cache_version))
            usd = self.currentBlock().userData()
            end = pow(2, 32)
            if not state:
                end = len(text)
            usd.cc_disabled_zones.append((len(original_text) - len(text),
                                          end))
        # takes multi-line type into account
        state |= docstring
        self.setCurrentBlockState(state)
        # print("State:", state)
        return multi

    def _purge_mem_cache(self):
        self._cache_version += 1
