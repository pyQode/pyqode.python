# syntax.py
from pcef.core import TextStyle
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
    'docstring': TextStyle('#000080 nbold nitalic nunderlined'),
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


class PyHighlighterMode(QSyntaxHighlighter, Mode):
    """Syntax highlighter for the Python language.
    """
    IDENTIFIER = "pyHighlighter"
    _DESCRIPTION = "Custom QSyntaxHighlighter to highlight python syntax"

    # Python keywords
    keywords = [
        'and', 'assert', 'break', 'class', 'continue', 'def',
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
        QSyntaxHighlighter.__init__(self, document)
        Mode.__init__(self)
        # Multi-line strings (expression, flag, style)
        # FIXME: The triple-quotes in these two lines will mess up the
        # syntax highlighting from this point onward
        self.tri_single = (QRegExp("'''"), 1, 'docstring')
        self.tri_double = (QRegExp('"""'), 2, 'docstring')

        rules = []

        # Keyword, operator, and brace rules
        rules += [(r'\b%s\b' % w, 0, 'keyword')
            for w in PyHighlighterMode.keywords]
        rules += [(r'\b%s\b' % w, 0, 'builtins')
            for w in PyHighlighterMode.builtins]
        rules += [(r'%s\b' % w, 0, 'docstringTag')
            for w in PyHighlighterMode.docstringTags]
        rules += [(r'%s' % b, 0, 'brace')
            for b in PyHighlighterMode.braces]
        rules += [(r'%s' % b, 0, 'punctuation')
            for b in PyHighlighterMode.punctuations]

        # All other rules
        rules += [
            # 'def' followed by an identifier
            (r'\bdef\b\s*(\w+)', 1, 'function'),
            # 'class' followed by an identifier
            (r'\bclass\b\s*(\w+)', 1, 'class'),
            # predefined items (__xxx__)
            (r'__.*__', 0, 'predefined'),
            # Double-quoted string, possibly containing escape sequences
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, 'string'),

            (r'@.*', 0, 'decorator'),

            # Numeric literals
            (r'\b[+-]?[0-9]+[lL]?\b', 0, 'numbers'),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, 'numbers'),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, 'numbers'),

            (r'\bself\b', 0, 'self'),
        ]
        rules += [(r'%s' % o, 0, 'operator')
            for o in PyHighlighterMode.operators]

        rules += [(r'#[^\n]*', 0, 'comment')]

        # Single-quoted string, possibly containing escape sequences
        rules += [(r"'[^'\\]*(\\.[^'\\]*)*'", 0, 'string')]

        # Build a QRegExp for each pattern
        self.rules = [(QRegExp(pat), index, fmt)
            for (pat, index, fmt) in rules]

    def format(self, style_key):
        """Return a QTextCharFormat with the given attributes.
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

    def _onStateChanged(self, state):
        if state:
            self.setDocument(self.editor.document())
        else:
            self.setDocument(None)

    def _onStyleChanged(self, section, key):
        if not key:
            self.rehighlight()

    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text.
        """
        original_txt = text
        # Do other syntax formatting
        for expression, nth, fm in self.rules:
            index = expression.indexIn(text, 0)

            while index >= 0:
                # We actually want the index of the nth match
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, self.format(fm))
                index = expression.indexIn(text, index + length)

        # Do string highlighting
        for expression, nth, fm in self.rules:
            index = expression.indexIn(text, 0)
            while index >= 0:
                if fm == "string":
                    # We actually want the index of the nth match
                    index = expression.pos(nth)
                    length = len(expression.cap(nth))
                    self.setFormat(index, length, self.format(fm))
                index = expression.indexIn(text, index + length)

        # Do docstring highlighting
        for expression, nth, fm in self.rules:
            index = expression.indexIn(text, 0)
            while index >= 0:
                if fm == "docstring":
                    # We actually want the index of the nth match
                    index = expression.pos(nth)
                    length = len(expression.cap(nth))
                    self.setFormat(index, length, self.format(fm))
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        # Do multi-line strings
        in_multiline = self.match_multiline(text, *self.tri_single)
        if not in_multiline:
            in_multiline = self.match_multiline(text, *self.tri_double)

        # Do docstring tag highlighting
        for expression, nth, fm in self.rules:
            index = expression.indexIn(text, 0)
            while index >= 0:
                if fm == "docstringTag":
                    # We actually want the index of the nth match
                    index = expression.pos(nth)
                    length = len(expression.cap(nth))
                    self.setFormat(index, length, self.format(fm))
                index = expression.indexIn(text, index + length)

        #Spaces
        expression = QRegExp('\s+')
        index = expression.indexIn(original_txt, 0)
        while index >= 0:
            index = expression.pos(0)
            length = len(expression.cap(0))
            self.setFormat(index, length, self.format(
                self.editor.style.value("whiteSpaceForeground")))
            index = expression.indexIn(original_txt, index + length)

    def match_multiline(self, text, delimiter, in_state, style):
        """Do highlighting of multi-line strings. ``delimiter`` should be a
        ``QRegExp`` for triple-single-quotes or triple-double-quotes, and
        ``in_state`` should be a unique integer to represent the corresponding
        state changes when inside those strings. Returns True if we're still
        inside a multi-line string when this function is finished.
        """
        # If inside triple-single quotes, start at 0
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        # Otherwise, look for the delimiter on this line
        else:
            start = delimiter.indexIn(text)
            # Move past this match
            add = delimiter.matchedLength()

        # As long as there's a delimiter match on this line...
        while start >= 0:
            # Look for the ending delimiter
            end = delimiter.indexIn(text, start + add)
            # Ending delimiter on this line?
            if end >= add:
                length = end - start + add + delimiter.matchedLength()
                self.setCurrentBlockState(0)
            # No; multi-line string
            else:
                self.setCurrentBlockState(in_state)
                length = len(text) - start + add
            # Apply formatting
            self.setFormat(start, length, self.format(style))
            # Look for the next match
            start = delimiter.indexIn(text, start + length)

        # Return True if still inside a multi-line string, False otherwise
        if self.currentBlockState() == in_state:
            return True
        else:
            return False
