"""
This module contains a native python syntax highlighter, strongly inspired from
spyderlib.widgets.source_code.syntax_higlighter.PythonSH and slighltly modified
to highlight decorator, self attribute and sphinx doc tags.

It is approximately 3 time faster then :class:`pyqode.core.modes.PygmentsSH`.

"""
import builtins
import re
from pyqode.core.qt import QtGui
from pyqode.core.api import SyntaxHighlighter as BaseSH, TextHelper
from pyqode.core.api import TextBlockHelper
import sys


def any(name, alternates):
    """Return a named group pattern matching list of alternates."""
    return "(?P<%s>" % name + "|".join(alternates) + ")"

kwlist = [
    'self',
    'False',
    'None',
    'True',
    'and',
    'as',
    'assert',
    'break',
    'class',
    'continue',
    'def',
    'del',
    'elif',
    'else',
    'except',
    'finally',
    'for',
    'from',
    'global',
    'if',
    'import',
    'in',
    'is',
    'lambda',
    'nonlocal',
    'not',
    'or',
    'pass',
    'raise',
    'return',
    'try',
    'while',
    'with',
    'yield',
]


def make_python_patterns(additional_keywords=[], additional_builtins=[]):
    """Strongly inspired from idlelib.ColorDelegator.make_pat"""
    kw = r"\b" + any("keyword", kwlist+additional_keywords) + r"\b"
    builtinlist = [str(name) for name in dir(builtins)
                   if not name.startswith('_')]+additional_builtins
    builtin = r"([^.'\"\\#]\b|^)" + any("builtin", builtinlist) + r"\b"
    comment = any("comment", [r"#[^\n]*"])
    instance = any("instance", [r"\bself\b"])
    decorator = any('decorator', [r'@\w*', r'.setter'])
    number = any("number",
                 [r"\b[+-]?[0-9]+[lLjJ]?\b",
                  r"\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b",
                  r"\b[+-]?0[oO][0-7]+[lL]?\b",
                  r"\b[+-]?0[bB][01]+[lL]?\b",
                  r"\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?[jJ]?\b"])
    sqstring = r"(\b[rRuU])?'[^'\\\n]*(\\.[^'\\\n]*)*'?"
    dqstring = r'(\b[rRuU])?"[^"\\\n]*(\\.[^"\\\n]*)*"?'
    uf_sqstring = r"(\b[rRuU])?'[^'\\\n]*(\\.[^'\\\n]*)*(\\)$(?!')$"
    uf_dqstring = r'(\b[rRuU])?"[^"\\\n]*(\\.[^"\\\n]*)*(\\)$(?!")$'
    sq3string = r"(\b[rRuU])?'''[^'\\]*((\\.|'(?!''))[^'\\]*)*(''')?"
    dq3string = r'(\b[rRuU])?"""[^"\\]*((\\.|"(?!""))[^"\\]*)*(""")?'
    uf_sq3string = r"(\b[rRuU])?'''[^'\\]*((\\.|'(?!''))[^'\\]*)*(\\)?(?!''')$"
    uf_dq3string = r'(\b[rRuU])?"""[^"\\]*((\\.|"(?!""))[^"\\]*)*(\\)?(?!""")$'
    string = any("string", [sq3string, dq3string, sqstring, dqstring])
    ufstring1 = any("uf_sqstring", [uf_sqstring])
    ufstring2 = any("uf_dqstring", [uf_dqstring])
    ufstring3 = any("uf_sq3string", [uf_sq3string])
    ufstring4 = any("uf_dq3string", [uf_dq3string])
    return "|".join([instance, decorator, kw, builtin, comment, ufstring1,
                     ufstring2,
                     ufstring3, ufstring4, string, number,
                     any("SYNC", [r"\n"])])

CELL_SEPARATORS = ('#%%', '# %%', '# <codecell>', '# In[')


#
# Pygments Syntax highlighter
#
class PythonSH(BaseSH):
    """Python Syntax Highlighter"""
    mimetype = 'text/x-python'

    # Syntax highlighting rules:
    PROG = re.compile(make_python_patterns(), re.S)
    IDPROG = re.compile(r"\s+(\w+)", re.S)
    ASPROG = re.compile(r".*?\b(as)\b")
    # Syntax highlighting states (from one text block to another):
    (NORMAL, INSIDE_SQ3STRING, INSIDE_DQ3STRING,
     INSIDE_SQSTRING, INSIDE_DQSTRING) = list(range(5))

    # Comments suitable for Outline Explorer
    OECOMMENT = re.compile('^(# ?--[-]+|##[#]+ )[ -]*[^- ]+')

    def __init__(self, parent, color_scheme=None):
        super().__init__(parent, color_scheme)
        self.import_statements = []
        self.global_import_statements = []
        self.found_cell_separators = False

    def highlight_block(self, text, block):
        prev_block = block.previous()
        prev_state = TextBlockHelper.get_state(prev_block)
        if prev_state == self.INSIDE_DQ3STRING:
            offset = -4
            text = r'""" '+text
        elif prev_state == self.INSIDE_SQ3STRING:
            offset = -4
            text = r"''' "+text
        elif prev_state == self.INSIDE_DQSTRING:
            offset = -2
            text = r'" '+text
        elif prev_state == self.INSIDE_SQSTRING:
            offset = -2
            text = r"' "+text
        else:
            offset = 0
            prev_state = self.NORMAL

        import_stmt = None

        block.docstring = False

        self.setFormat(0, len(text), self.formats["normal"])

        state = self.NORMAL
        match = self.PROG.search(text)
        block.docstring_start = False
        while match:
            for key, value in list(match.groupdict().items()):
                if value:
                    start, end = match.span(key)
                    start = max([0, start+offset])
                    end = max([0, end+offset])
                    if key == "uf_sq3string":
                        self.setFormat(start, end-start,
                                       self.formats["string"])
                        state = self.INSIDE_SQ3STRING
                    elif key == "uf_dq3string":
                        self.setFormat(start, end-start,
                                       self.formats["docstring"])
                        block.docstring = True
                        state = self.INSIDE_DQ3STRING
                    elif key == "uf_sqstring":
                        self.setFormat(start, end-start,
                                       self.formats["string"])
                        state = self.INSIDE_SQSTRING
                    elif key == "uf_dqstring":
                        self.setFormat(start, end-start,
                                       self.formats["string"])
                        state = self.INSIDE_DQSTRING
                    else:
                        if '"""' in value:
                            block.docstring = True
                            self.setFormat(start, end-start,
                                           self.formats["docstring"])
                        elif key == 'decorator':
                            self.setFormat(start, end-start,
                                           self.formats["decorator"])
                        elif value == 'self':
                            self.setFormat(start, end-start,
                                           self.formats["self"])
                        else:
                            self.setFormat(start, end-start, self.formats[key])
                        if key == "keyword":
                            if value in ("def", "class"):
                                match1 = self.IDPROG.match(text, end)
                                if match1:
                                    start1, end1 = match1.span(1)
                                    fmt = self.formats["definition"]
                                    if value == "class":
                                        fmt.setFontWeight(QtGui.QFont.Bold)
                                    self.setFormat(start1, end1-start1, fmt)
                            elif value == "import":
                                import_stmt = text.strip()
                                # color all the "as" words on same line, except
                                # if in a comment; cheap approximation to the
                                # truth
                                if '#' in text:
                                    endpos = text.index('#')
                                else:
                                    endpos = len(text)
                                while True:
                                    match1 = self.ASPROG.match(text, end,
                                                               endpos)
                                    if not match1:
                                        break
                                    start, end = match1.span(1)
                                    self.setFormat(start, end-start,
                                                   self.formats["keyword"])

            match = self.PROG.search(text, match.end())

        TextBlockHelper.set_state(block, state)

        # update import zone
        if import_stmt is not None:
            if not block in self.import_statements:
                block.import_stmt = import_stmt
                self.import_statements.append(block)
                txt = block.text()
                if len(txt) - len(txt.strip()) == 0:
                    self.global_import_statements.append(block)

        # update import statements
        if ((not self.editor.file.opening or
                block == self.document().lastBlock()) and
                len(self.global_import_statements) > 1):
            end = 0
            start = sys.maxsize
            for block in self.global_import_statements:
                n = block.blockNumber()
                if n > end:
                    end = n
                if n < start:
                    start = n
            block = self.document().findBlockByNumber(start)
            TextBlockHelper.set_fold_lvl(block, 1)
            TextBlockHelper.set_fold_trigger(block, True)
            for line in range(start + 1, end + 1):
                block = self.document().findBlockByNumber(line)
                TextBlockHelper.set_fold_lvl(block, 1)
                TextBlockHelper.set_fold_trigger(block, False)
            if block.next().isValid():
                TextBlockHelper.set_fold_lvl(block.next(), 0)

    def get_import_statements(self):
        return list(self.import_statements.values())

    def rehighlight(self):
        self.import_statements = {}
        self.global_import_statements = {}
        self.found_cell_separators = False
        super().rehighlight()

    def detect_fold_level(self, prev_block, block):
        # Python is an indent based language so use indentation for folding
        # makes sense but we restrict new regions to indentation after a ':',
        # that way only the real logical blocks are displayed.
        lvl = super().detect_fold_level(prev_block, block)
        prev_lvl = TextBlockHelper.get_fold_lvl(prev_block)
        # cancel false indentation, indentation can only happen if there is
        # ':' on the previous line
        if(prev_block and
                lvl > prev_lvl and
                not prev_block.text().strip().endswith(':')):
            lvl = prev_lvl
        th = TextHelper(self.editor)
        fmts = ['docstring']
        wasdocstring = th.is_comment_or_string(prev_block, formats=fmts)
        if block.docstring:
            if wasdocstring:
                # find block that starts the docstring
                p = prev_block.previous()
                wasdocstring = th.is_comment_or_string(p, formats=fmts)
                while wasdocstring or p.text().strip() == '':
                    p = p.previous()
                    wasdocstring = th.is_comment_or_string(p, formats=fmts)
                lvl = TextBlockHelper.get_fold_lvl(p.next()) + 1
        return lvl
