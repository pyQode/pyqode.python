# -*- coding: utf-8 -*-
""" Contains smart indent modes """
import re
from PyQt4.QtGui import QTextCursor
from pyqode.core.modes.autoindent import AutoIndentMode
from pyqode.core.modes.matcher import SymbolMatcherMode


class PyAutoIndentMode(AutoIndentMode):
    """
    Customised :class:`pyqode.core.AutoIndentMode` for python, the indentation
    level is based on the previous line indent but is automatically incremented
    after a *:* and decremented after *pass* or *return*
    """
    def __init__(self):
        super(PyAutoIndentMode, self).__init__()

    def is_operator(self, word):
        operators = ['.', ',', '+', '-', '/', '*', 'or', 'and', "=", "%", "=="]
        return word in operators

    def has_two_empty_line_before(self, tc):
        ln = tc.blockNumber()
        limit = ln - 1
        while ln > limit:
            if self.editor.line_text(ln).strip() != "":
                return False
            ln -= 1
        return True

    def has_unclosed_paren(self, tc):
        ln = tc.blockNumber()
        while ln >= 0:
            line = self.editor.line_text(ln)
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

    def between_paren(self, tc, col):
        data = tc.block().userData()
        nb_open = 0
        nb_closed = 0
        lists = [data.parentheses, data.braces, data.square_brackets]
        for symbols in lists:
            for paren in symbols:
                if paren.position >= col:
                    break
                if self.is_paren_open(paren):
                    nb_open += 1
                if self.is_paren_closed(paren):
                    nb_closed += 1
        block = tc.block().next()
        # if not, is there an non closed paren on the next lines.
        parens = {'(': 0, '{': 0, '[': 0}
        matching = {')': '(', '}': '{', ']': '['}
        if not nb_open > nb_closed:
            while block.isValid():
                data = block.userData()
                lists = [data.parentheses, data.braces, data.square_brackets]
                for symbols in lists:
                    for paren in symbols:
                        if self.is_paren_open(paren):
                            parens[paren.character] += 1
                        if self.is_paren_closed(paren):
                            parens[matching[paren.character]] -= 1
                            if parens[matching[paren.character]] < 0:
                                return True
                block = block.next()
            return False
        else:
            return True

    def is_in_comment(self, column, tc, full_line):
        use_parent_impl = False
        usd = tc.block().userData()
        for start, end in usd.cc_disabled_zones:
            if start < column < end:
                string = full_line[start:end]
                if not ((string.startswith("'") or
                        string.startswith('"')) and
                        (string.endswith("'") or
                         string.endswith('"'))):
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
            ol, oc = self.editor.get_mode(SymbolMatcherMode).symbol_pos(
                tc2, '(', 0)
            line = self.editor.line_text(ol)
            return len(line) - len(line.lstrip())
        return None

    def get_last_open_paren_pos(self, tc, column):
        pos = None
        char = None
        ln = tc.blockNumber() + 1
        tc_trav = QTextCursor(tc)
        while ln > 1:
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
                                l, c = self.editor.get_mode(
                                    SymbolMatcherMode).symbol_pos(tc3, ')')
                                if l == ln and c < column:
                                    continue
                                return pos, char
            # check previous line
            tc_trav.movePosition(tc_trav.Up, tc_trav.MoveAnchor)
            ln = tc_trav.blockNumber() + 1
            column = len(self.editor.line_text(ln))
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
        ol, oc = self.editor.get_mode(SymbolMatcherMode).symbol_pos(
            tc2, char, ptype)
        cl, cc = self.editor.get_mode(SymbolMatcherMode).symbol_pos(
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
        closingline = self.editor.line_text(cL)
        openingline = self.editor.line_text(oL)
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
                if re.match('.*=[\s][\W].*', openingline):
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

    def _get_indent(self, tc):
        pos = tc.position()
        ln, column = self.editor.cursor_position
        fullline = self.get_full_line(tc)
        line = fullline[:column]
        # no indent
        if pos == 0 or column == 0:
            return "", ""
        pre, post = AutoIndentMode._get_indent(self, tc)
        if self.at_block_start(tc, line):
            return pre, post
        # return pressed in comments
        if self.is_in_comment(column, tc, fullline):
            if line.strip().startswith("#") and column != len(fullline):
                post = post + '#'
            return pre, post
        elif self.between_paren(tc, column):
            pre, post = self.handle_indent_after_paren(column, line, fullline,
                                                       tc)
        else:
            lastword = self.get_last_word(tc)
            inStringDef, char = self.is_in_string_def(fullline, column)
            if inStringDef:
                # the string might be between paren if multiline
                # check if there a at least a non closed paren on the previous
                # lines
                if self.has_unclosed_paren(tc):
                    pre = char
                else:
                    pre = '" \\'
                    post += 4 * ' '
                if fullline.endswith(':'):
                    post += 4 * " "
                post += char
            elif fullline.rstrip().endswith(":") and \
                    lastword.rstrip().endswith(':') and self.at_block_end(
                    tc, fullline):
                try:
                    indent = self.get_indent_of_opening_paren(tc, column) + 4
                    if indent:
                        post = indent * " "
                except TypeError:
                    kw = ["if", "class", "def", "while", "for", "else", "elif",
                          "except", "finally", "try"]
                    l = fullline
                    ln = tc.blockNumber()

                    def check_kw_in_line(kwds, lparam):
                        for kwd in kwds:
                            if kwd in lparam:
                                return True
                        return False

                    while not check_kw_in_line(kw, l) and ln:
                        ln -= 1
                        l = self.editor.line_text(ln)
                    indent = (len(l) - len(l.lstrip())) * " "
                    indent += 4 * " "
                    post = indent
            elif fullline.endswith("\\"):
                # increment indent
                post += 4 * " "
            elif fullline.endswith(")") and lastword.endswith(')'):
                # find line where the open braces can be found and align with
                # that line
                indent = self.get_indent_of_opening_paren(tc, column)
                if indent:
                    post = indent * " "
            elif ("\\" not in fullline and "#" not in fullline and
                    fullline.strip() and not fullline.endswith(')') and
                    not self.at_block_end(tc, fullline)):
                if lastword and lastword[-1] != " ":
                    pre += " \\"
                else:
                    pre += '\\'
                post += 4 * " "
                if fullline.endswith(':'):
                    post += 4 * " "
            elif (lastword == "return" or lastword == "pass" or
                    self.has_two_empty_line_before(tc)):
                post = post[:-4]

        return pre, post
