# -*- coding: utf-8 -*-
""" Contains smart indent modes """
import re
from pyqode.core.api import TextHelper, get_block_symbol_data
from pyqode.qt.QtGui import QTextCursor
from pyqode.core.modes.autoindent import AutoIndentMode
from pyqode.core.modes.matcher import SymbolMatcherMode


class PyAutoIndentMode(AutoIndentMode):
    """
    Customised :class:`pyqode.core.modes.AutoIndentMode` for python
    that tries its best to follow the pep8 indentation guidelines.

    """
    def __init__(self):
        super(PyAutoIndentMode, self).__init__()
        self._helper = None

    def on_install(self, editor):
        super().on_install(editor)
        self._helper = TextHelper(editor)

    def _get_indent(self, cursor):
        ln, column = self._helper.cursor_position()
        fullline = self._get_full_line(cursor)
        line = fullline[:column]
        pre, post = AutoIndentMode._get_indent(self, cursor)
        if self._at_block_start(cursor, line):
            return pre, post
        # return pressed in comments
        if (self._helper.is_comment_or_string(
                cursor, formats=['comment', 'docstring']) or
                fullline.endswith('"""')):
            if line.strip().startswith("#") and column != len(fullline):
                post += '# '
            return pre, post
        # between parens
        elif self._between_paren(cursor, column):
            try:
                pre, post = self._handle_indent_between_paren(
                    column, line, fullline, cursor)
            except TypeError:
                return pre, post
        else:
            lastword = self._get_last_word(cursor)
            lastwordu = self._get_last_word_unstripped(cursor)
            in_string_def, char = self._is_in_string_def(fullline, column)
            if in_string_def:
                post, pre = self._handle_indent_inside_string(
                    char, cursor, fullline, post)
            elif (fullline.rstrip().endswith(":") and
                    lastword.rstrip().endswith(':') and
                    self._at_block_end(cursor, fullline)):
                post = self._handle_new_scope_indentation(
                    cursor, fullline)
            elif line.endswith("\\"):
                # if user typed \ and press enter -> indent is always
                # one level higher
                post += self.editor.tab_length * " "
            elif (fullline.endswith((')', '}', ']')) and
                    lastword.endswith((')', '}', ']'))):
                post = self._handle_indent_after_paren(cursor, post)
            elif ("\\" not in fullline and "#" not in fullline and
                  not self._at_block_end(cursor, fullline)):
                post, pre = self._handle_indent_in_statement(
                    fullline, lastwordu, post, pre)
            elif lastword == "return" or lastword == "pass":
                post = post[:-self.editor.tab_length]
        return pre, post

    @staticmethod
    def _is_in_string_def(full_line, column):
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

    @staticmethod
    def _is_paren_open(paren):
        return (paren.character == "(" or paren.character == "["
                or paren.character == '{')

    @staticmethod
    def _is_paren_closed(paren):
        return (paren.character == ")" or paren.character == "]"
                or paren.character == '}')

    @staticmethod
    def _get_full_line(tc):
        tc2 = QTextCursor(tc)
        tc2.select(QTextCursor.LineUnderCursor)
        full_line = tc2.selectedText()
        return full_line

    def _parens_count_for_block(self, col, block):
        open_p = []
        closed_p = []
        lists = get_block_symbol_data(self.editor, block)
        for symbols in lists:
            for paren in symbols:
                if paren.position >= col:
                    continue
                if self._is_paren_open(paren):
                    if not col:
                        return -1, -1, [], []
                    open_p.append(paren)
                if self._is_paren_closed(paren):
                    closed_p.append(paren)
        return len(open_p), len(closed_p), open_p, closed_p

    def _between_paren(self, tc, col):
        block = tc.block()
        nb_open = nb_closed = 0
        while block.isValid():  # and nb_open >= nb_closed:
            o, c, _, _ = self._parens_count_for_block(col, block)
            nb_open += o
            nb_closed += c
            block = block.previous()
            col = len(block.text())
        return nb_open > nb_closed

    @staticmethod
    def _get_last_word(tc):
        tc2 = QTextCursor(tc)
        tc2.movePosition(QTextCursor.Left, 1)
        tc2.movePosition(QTextCursor.WordLeft, tc.KeepAnchor)
        return tc2.selectedText().strip()

    @staticmethod
    def _get_last_word_unstripped(tc):
        tc2 = QTextCursor(tc)
        tc2.movePosition(QTextCursor.Left, 1)
        tc2.movePosition(QTextCursor.WordLeft, tc.KeepAnchor)
        return tc2.selectedText()

    def _get_indent_of_opening_paren(self, tc):
        tc.movePosition(tc.Left, tc.KeepAnchor)
        char = tc.selectedText()
        tc.movePosition(tc.Right, tc.MoveAnchor)
        mapping = {')': ('(', 0), '}': ('{', 1), ']': ('[', 2)}
        try:
            character, char_type = mapping[char]
        except KeyError:
            return None
        else:
            ol, oc = self.editor.modes.get(SymbolMatcherMode).symbol_pos(
                tc, character, char_type)
            line = self._helper.line_text(ol)
            return len(line) - len(line.lstrip())

    def _get_first_open_paren(self, tc, column):
        pos = None
        char = None
        ln = tc.blockNumber() + 1
        tc_trav = QTextCursor(tc)
        mapping = {'(': (')', 0), '[': (']', 1), '{': ('}', 2)}
        while ln >= 1:
            tc_trav.movePosition(tc_trav.StartOfLine, tc_trav.MoveAnchor)
            lists = get_block_symbol_data(self.editor, tc_trav.block())
            all_symbols = []
            for symbols in lists:
                all_symbols += [s for s in symbols]
            symbols = sorted(all_symbols, key=lambda x: x.position)
            for paren in reversed(symbols):
                if paren.position < column:
                    if self._is_paren_open(paren):
                        if paren.position > column:
                            continue
                        else:
                            pos = tc_trav.position() + paren.position
                            char = paren.character
                            # ensure it does not have a closing paren on
                            # the same line
                            tc3 = QTextCursor(tc)
                            tc3.setPosition(pos)
                            try:
                                ch, ch_type = mapping[paren.character]
                                l, c = self.editor.modes.get(
                                    SymbolMatcherMode).symbol_pos(
                                    tc3, ch, ch_type)
                            except KeyError:
                                continue
                            if l == ln and c < column:
                                continue
                            return pos, char
            # check previous line
            tc_trav.movePosition(tc_trav.Up, tc_trav.MoveAnchor)
            ln = tc_trav.blockNumber() + 1
            column = len(self._helper.line_text(ln))
        return pos, char

    def _get_paren_pos(self, tc, column):
        pos, char = self._get_first_open_paren(tc, column)
        if char == '(':
            ptype = 0
            closingchar = ')'
        elif char == '[':
            ptype = 1
            closingchar = ']'
        else:
            ptype = 2
            closingchar = '}'
        tc2 = QTextCursor(tc)
        tc2.setPosition(pos)
        ol, oc = self.editor.modes.get(SymbolMatcherMode).symbol_pos(
            tc2, char, ptype)
        cl, cc = self.editor.modes.get(SymbolMatcherMode).symbol_pos(
            tc2, closingchar, ptype)
        return (ol, oc), (cl, cc)

    @staticmethod
    def _get_next_char(tc):
        tc2 = QTextCursor(tc)
        tc2.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor)
        char = tc2.selectedText()
        return char

    def _handle_indent_between_paren(self, column, line, fullline, tc):
        """
        Handle indent between symbols such as parenthesis, braces,...
        """
        # elements might be separated by ',' 'or' 'and'
        next_char = self._get_next_char(tc)
        nextcharisclosingsymbol = next_char in [']', ')', '}']
        (ol, oc), (cl, cc) = self._get_paren_pos(tc, column)
        closingline = self._helper.line_text(cl)
        openingline = self._helper.line_text(ol)
        openingline = re.sub(r'".*"', "", openingline)
        openingline = re.sub(r"'.*'", "", openingline)
        openingindent = len(openingline) - len(openingline.lstrip())
        tokens = [t.strip() for t in re.split(', |and |or ',
                                              line[oc:column]) if t]
        # align with first token pos
        if len(closingline) > cc and closingline[cc] == ":":
            if ('def ' in openingline or
                    'class ' in openingline) and oc != tc.positionInBlock():
                post = oc * ' '
            else:
                post = openingindent * " " + 8 * " "
        else:
            # press enter before a '}', ']', ')'
            # which close an affectation (tuple, list , dict)
            if nextcharisclosingsymbol and re.match('.*=[\s][\W].*',
                                                    openingline):
                post = openingindent * " "
            else:
                # align elems in list, tuple, dict
                if re.match('.*=[\s][\W].*', openingline) and ol - cl == 1:
                    post = openingindent * " " + self.editor.tab_length * " "
                # align elems in fct declaration (we align with first
                # token)
                else:
                    if len(tokens):
                        otext = TextHelper(self.editor).line_text(ol)
                        if (ol == TextHelper(self.editor).current_line_nbr() or
                                otext[-1] not in ['(', '{', '[']):
                            # align with last opened paren
                            post = oc * " "
                        else:
                            # align with first open paren
                            indent = TextHelper(self.editor).line_indent()
                            post = indent * ' '
                    else:
                        indent = (len(openingindent * " " +
                                      self.editor.tab_length * " ") //
                                  self.editor.tab_length *
                                  self.editor.tab_length)
                        post = indent * ' '
        pre = ""
        in_string_def, char = self._is_in_string_def(fullline, column)
        if in_string_def:
            pre = char
            post += char
        return pre, post

    @staticmethod
    def _at_block_start(tc, line):
        """
        Improve QTextCursor.atBlockStart to ignore spaces
        """
        if tc.atBlockStart():
            return True
        column = tc.columnNumber()
        indentation = len(line) - len(line.lstrip())
        return column <= indentation

    @staticmethod
    def _at_block_end(tc, fullline):
        if tc.atBlockEnd():
            return True
        column = tc.columnNumber()
        return column >= len(fullline.rstrip()) - 1

    def _handle_indent_inside_string(self, char, cursor, fullline, post):
        # break string with a '\' at the end of the original line, always
        # breaking strings enclosed by parens is done in the
        # _handle_between_paren method
        n = self.editor.tab_length
        pre = '" \\'
        post += n * ' '
        if fullline.endswith(':'):
            post += n * " "
        post += char
        return post, pre

    def _handle_new_scope_indentation(self, cursor, fullline):
        try:
            indent = (self._get_indent_of_opening_paren(cursor) +
                      self.editor.tab_length)
            post = indent * " "
        except TypeError:
            # e.g indent is None (meaning the line does not ends with ):, ]:
            # or }:
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
            indent += self.editor.tab_length * " "
            post = indent
        return post

    def _handle_indent_after_paren(self, cursor, post):
        indent = self._get_indent_of_opening_paren(cursor)
        if indent is not None:
            post = indent * " "
        return post

    def _handle_indent_in_statement(self, fullline, lastword, post, pre):
        if lastword and lastword[-1] != " ":
            pre += " \\"
        else:
            pre += '\\'
        post += self.editor.tab_length * " "
        if fullline.endswith(':'):
            post += self.editor.tab_length * " "
        return post, pre
