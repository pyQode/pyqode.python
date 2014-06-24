# -*- coding: utf-8 -*-
""" Contains smart indent modes """
import re
from pyqode.core.api import TextHelper
from pyqode.core.qt.QtGui import QTextCursor
from pyqode.core.modes.autoindent import AutoIndentMode
from pyqode.core.modes.matcher import SymbolMatcherMode


class PyAutoIndentMode(AutoIndentMode):
    """
    Customised :class:`pyqode.core.modes.AutoIndentMode` for python
    that tries its best to follow the pep8 indentation guidelines.
    """
    def __init__(self):
        super(PyAutoIndentMode, self).__init__()

    def on_install(self, editor):
        super().on_install(editor)
        self._helper = TextHelper(editor)

    def has_two_empty_line_before(self, tc):
        ln = tc.blockNumber()
        limit = ln - 1
        while ln > limit:
            if self._helper.line_text(ln).strip() != "":
                return False
            ln -= 1
        return True

    def has_unclosed_paren(self, tc):
        ln = tc.blockNumber()
        while ln >= 0:
            line = self._helper.line_text(ln)
            if line.count("(") > line.count(")"):
                return True
            ln -= 1
        return False

    def is_in_string_def(self, full_line, column):
        count = 0
        char = "'"
        for i in range(len(full_line)):
            if full_line[i] == "'" or full_line[i] == '"':
                count += 1
            if full_line[i] == '"' and i < column:
                char = '"'
        count_after_col = 0
        for i in range(column, len(full_line)):
            if full_line[i] == "'" or full_line[i] == '"':
                count_after_col += 1
        return count % 2 == 0 and count_after_col % 2 == 1, char

    def is_paren_open(self, paren):
        return (paren.character == "(" or paren.character == "["
                or paren.character == '{')

    def is_paren_closed(self, paren):
        return (paren.character == ")" or paren.character == "]"
                or paren.character == '}')

    def get_full_line(self, tc):
        tc2 = QTextCursor(tc)
        tc2.select(QTextCursor.LineUnderCursor)
        full_line = tc2.selectedText()
        return full_line

    def parens_count_for_block(self, col, block):
        data = block.userData()
        nb_open = 0
        nb_closed = 0
        lists = [data.parentheses, data.braces, data.square_brackets]
        for symbols in lists:
            for paren in symbols:
                if self.is_paren_open(paren):
                    if not col:
                        return -1, -1
                    nb_open += 1
                if paren.position >= col and self.is_paren_closed(paren):
                    nb_closed += 1
        return nb_closed, nb_open

    def between_paren(self, tc, col):
        nb_closed, nb_open = self.parens_count_for_block(col, tc.block())
        block = tc.block().next()
        while nb_open == nb_closed == 0 and block.isValid():
            nb_closed, nb_open = self.parens_count_for_block(nb_open, block)
            block = block.next()
        # if not, is there an non closed paren on the next lines.
        parens = {'(': 0, '{': 0, '[': 0}
        matching = {')': '(', '}': '{', ']': '['}
        rparens = {')': 0, '}': 0, ']': 0}
        rmatching = {'(': ')', '{': '}', '[': ']'}
        if nb_open != nb_closed:
            # look down
            if nb_open > nb_closed:
                operation = self._next_block
                down = True
            else:
                operation = self._prev_block
                down = False
            block = tc.block()
            # block = operation(tc.block())
            offset = col
            while block.isValid():
                data = block.userData()
                lists = [data.parentheses, data.braces, data.square_brackets]
                for symbols in lists:
                    for paren in symbols:
                        if paren.position < offset and down:
                            continue
                        if paren.position >= offset and not down:
                            continue
                        if self.is_paren_open(paren):
                            parens[paren.character] += 1
                            rparens[rmatching[paren.character]] -= 1
                            if (operation == self._prev_block and
                                    rparens[rmatching[paren.character]] < 0):
                                return True
                        if self.is_paren_closed(paren):
                            rparens[paren.character] += 1
                            parens[matching[paren.character]] -= 1
                            if (operation == self._next_block and
                                    parens[matching[paren.character]] < 0):
                                return True
                block = operation(block)
                offset = 0 if down else len(block.text())
        elif nb_open > 0:
            return True
        return False

    def _next_block(self, b):
        return b.next()

    def _prev_block(self, b):
        return b.previous()

    def is_in_comment(self, column, tc, full_line):
        use_parent_impl = False
        usd = tc.block().userData()
        for start, end in usd.cc_disabled_zones:
            if start < column < end:
                string = full_line[start:end]
                if not ((string.startswith("'") or string.startswith('"')) and
                        (string.endswith("'") or string.endswith('"'))):
                    use_parent_impl = True
                    break
        return use_parent_impl

    def get_last_word(self, tc):
        tc2 = QTextCursor(tc)
        tc2.movePosition(QTextCursor.Left, 1)
        tc2.movePosition(QTextCursor.WordLeft, tc.KeepAnchor)
        # tc2.movePosition(QTextCursor.Right, tc.KeepAnchor,
        #                  self.editor.cursorPosition[1])
        return tc2.selectedText().strip()

    def get_indent_of_opening_paren(self, tc, column):
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
            ol, oc = self.editor.modes.get(SymbolMatcherMode).symbol_pos(
                tc2, '(', 0)
            line = self._helper.line_text(ol)
            return len(line) - len(line.lstrip())
        return None

    def get_last_open_paren_pos(self, tc, column):
        pos = None
        char = None
        ln = tc.blockNumber() + 1
        tc_trav = QTextCursor(tc)
        while ln >= 1:
            tc_trav.movePosition(tc_trav.StartOfLine, tc_trav.MoveAnchor)
            data = tc_trav.block().userData()
            lists = [data.parentheses, data.braces, data.square_brackets]
            for symbols in lists:
                for paren in reversed(symbols):
                    if paren.position < column:
                        if self.is_paren_open(paren):
                            if paren.position > column:
                                continue
                            else:
                                pos = tc_trav.position() + paren.position
                                char = paren.character
                                # ensure it does not have a closing paren on
                                # the same line
                                tc3 = QTextCursor(tc)
                                tc3.setPosition(pos)
                                l, c = self.editor.modes.get(
                                    SymbolMatcherMode).symbol_pos(tc3, ')')
                                if l == ln and c < column:
                                    continue
                                return pos, char
            # check previous line
            tc_trav.movePosition(tc_trav.Up, tc_trav.MoveAnchor)
            ln = tc_trav.blockNumber() + 1
            column = len(self._helper.line_text(ln))
        return pos, char

    def get_parent_pos(self, tc, column):
        pos, char = self.get_last_open_paren_pos(tc, column)
        if char == '(':
            ptype = 0
            closingchar = ')'
        elif char == '[':
            ptype = 1
            closingchar = ']'
        elif char == '{':
            ptype = 2
            closingchar = '}'
        tc2 = QTextCursor(tc)
        tc2.setPosition(pos)
        ol, oc = self.editor.modes.get(SymbolMatcherMode).symbol_pos(
            tc2, char, ptype)
        cl, cc = self.editor.modes.get(SymbolMatcherMode).symbol_pos(
            tc2, closingchar, ptype)
        return (ol, oc), (cl, cc)

    def get_next_char(self, tc):
        tc2 = QTextCursor(tc)
        tc2.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor)
        char = tc2.selectedText()
        return char

    def handle_indent_after_paren(self, column, line, fullline, tc):
        """
        Handle indent between symbols such as parenthesis, braces,...
        """
        # elements might be separated by ',' 'or' 'and'
        next_char = self.get_next_char(tc)
        nextcharisclosingsymbol = next_char in [']', ')', '}']
        (oL, oC), (cL, cC) = self.get_parent_pos(tc, column)
        closingline = self._helper.line_text(cL)
        openingline = self._helper.line_text(oL)
        openingline = re.sub(r'".*"', "", openingline)
        openingline = re.sub(r"'.*'", "", openingline)
        openingindent = len(openingline) - len(openingline.lstrip())
        tokens = [t.strip() for t in re.split(', |and |or ',
                                              line[oC:column]) if t]

        # align with first token pos
        if len(closingline) > cC and closingline[cC] == ":":
            post = openingindent * " " + 8 * " "
        else:
            # press enter before a '}', ']', ')'
            # which close an affectation (tuple, list , dict)
            if nextcharisclosingsymbol and re.match('.*=[\s][\W].*',
                                                    openingline):
                post = openingindent * " "
            else:
                # align elems in list, tuple, dict
                if re.match('.*=[\s][\W].*', openingline) and oL - cL == 1:
                    post = openingindent * " " + 4 * " "
                # align elems in fct declaration (we align with first
                # token)
                else:
                    if len(tokens):
                        post = oC * " "
                    else:
                        post = openingindent * " " + 4 * " "
        pre = ""
        in_string_def, char = self.is_in_string_def(fullline, column)
        if in_string_def:
            pre = char
            post += char
        return pre, post

    def at_block_start(self, tc, line):
        """
        Improve QTextCursor.atBlockStart to ignore spaces
        """
        if tc.atBlockStart():
            return True
        column = tc.columnNumber()
        indentation = len(line) - len(line.lstrip())
        return column <= indentation

    def at_block_end(self, tc, fullline):
        if tc.atBlockEnd():
            return True
        column = tc.columnNumber()
        return column >= len(fullline.rstrip()) - 1

    def _get_indent(self, cursor):
        pos = cursor.position()
        ln, column = self._helper.cursor_position()
        fullline = self.get_full_line(cursor)
        line = fullline[:column]
        # no indent
        if pos == 0 or column == 0:
            return "", ""
        pre, post = AutoIndentMode._get_indent(self, cursor)
        if self.at_block_start(cursor, line):
            if self.has_two_empty_line_before(cursor):
                post = post[:-4]
            return pre, post
        # return pressed in comments
        if self.is_in_comment(column, cursor, fullline):
            if line.strip().startswith("#") and column != len(fullline):
                post += '# '
            return pre, post
        elif self.between_paren(cursor, column):
            try:
                pre, post = self.handle_indent_after_paren(
                    column, line, fullline, cursor)
            except TypeError:
                return pre, post
        else:
            lastword = self.get_last_word(cursor)
            inStringDef, char = self.is_in_string_def(fullline, column)
            if inStringDef:
                # the string might be between paren if multiline
                # check if there a at least a non closed paren on the previous
                # lines
                if self.has_unclosed_paren(cursor):
                    pre = char
                else:
                    pre = '" \\'
                    post += 4 * ' '
                if fullline.endswith(':'):
                    post += 4 * " "
                post += char
            elif fullline.rstrip().endswith(":") and \
                    lastword.rstrip().endswith(':') and \
                    self.at_block_end(cursor, fullline):
                try:
                    indent = (self.get_indent_of_opening_paren(cursor, column)
                              + 4)
                    if indent:
                        post = indent * " "
                except TypeError:
                    kw = ["if", "class", "def", "while", "for", "else", "elif",
                          "except", "finally", "try"]
                    l = fullline
                    ln = cursor.blockNumber()

                    def check_kw_in_line(kwds, lparam):
                        for kwd in kwds:
                            if kwd in lparam:
                                return True
                        return False

                    while not check_kw_in_line(kw, l) and ln:
                        ln -= 1
                        l = self._helper.line_text(ln)
                    indent = (len(l) - len(l.lstrip())) * " "
                    indent += 4 * " "
                    post = indent
            elif line.endswith("\\"):
                # increment indent
                post += 4 * " "
            elif fullline.endswith(")") and lastword.endswith(')'):
                # find line where the open braces can be found and align with
                # that line
                indent = self.get_indent_of_opening_paren(cursor, column)
                if indent:
                    post = indent * " "
            elif ("\\" not in fullline and "#" not in fullline and
                  fullline.strip() and not fullline.endswith(')') and
                  not self.at_block_end(cursor, fullline)):
                if lastword and lastword[-1] != " ":
                    pre += " \\"
                else:
                    pre += '\\'
                post += 4 * " "
                if fullline.endswith(':'):
                    post += 4 * " "
            elif (lastword == "return" or lastword == "pass"):
                post = post[:-4]

        return pre, post
