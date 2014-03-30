# -*- coding: utf-8 -*-
""" Contains the python autocomplete mode """
import jedi
from PyQt4 import QtGui
from pyqode.core.modes import AutoCompleteMode


class PyAutoCompleteMode(AutoCompleteMode):
    """
    Extends :class:`pyqode.core.AutoCompleteMode` to add support for function
    docstring and method/function call.

    Docstring completion adds a `:param` sphinx tag foreach parameter in the
    above function.

    Function completion adds "):" to function definition.

    Method completion adds "self):" to method definition.
    """

    def _format_func_params(self, indent):
        parameters = ""
        l = self.editor.cursor_position[0] - 1
        c = indent + len("def ") + 1
        script = jedi.Script(self.editor.toPlainText(), l, c,
                             self.editor.file_path,
                             self.editor.file_encoding)
        definition = script.goto_definitions()[0]
        for defined_name in definition.defined_names():
            if defined_name.name != "self" and defined_name.type == 'param':
                parameters += "\n{1}:param {0}:".format(
                    defined_name.name, indent * " ")
        to_insert = '"\n{0}{1}\n{0}"""'.format(indent * " ", parameters)
        return to_insert

    def _insert_docstring(self, prev_line, below_fct):
        indent = self.editor.line_indent()
        if "class" in prev_line or not below_fct:
            to_insert = '"\n{0}\n{0}"""'.format(indent * " ")
        else:
            to_insert = self._format_func_params(indent)
        tc = self.editor.textCursor()
        p = tc.position()
        tc.insertText(to_insert)
        tc.setPosition(p)  # we are there ""|"
        tc.movePosition(tc.Down)
        self.editor.setTextCursor(tc)

    def _in_method_call(self):
        l = self.editor.cursor_position[0] - 1
        expected_indent = self.editor.line_indent() - 4
        while l >= 0:
            text = self.editor.line_text(l)
            indent = len(text) - len(text.lstrip())
            if indent == expected_indent and 'class' in text:
                return True
            l -= 1
        return False

    def _handle_fct_def(self):
        if self._in_method_call():
            txt = "self):"
        else:
            txt = "):"
        tc = self.editor.textCursor()
        tc.insertText(txt)
        tc.movePosition(tc.Left, tc.MoveAnchor, 2)
        self.editor.setTextCursor(tc)

    def _on_post_key_pressed(self, e):
        # if we are in disabled cc, use the parent implementation
        column = self.editor.cursor_position[1]
        usd = self.editor.textCursor().block().userData()
        for start, end in usd.cc_disabled_zones:
            if (start <= column < end - 1 and
                    not self.editor.current_line_text.lstrip().startswith(
                    '"""')):
                return
        prev_line = self.editor.line_text(self.editor.cursor_position[0] - 1)
        is_below_fct_or_class = "def" in prev_line or "class" in prev_line
        if (e.text() == '"' and '""' == self.editor.current_line_text.strip()
                and (is_below_fct_or_class or column == 2)):
            self._insert_docstring(prev_line, is_below_fct_or_class)
        elif (e.text() == "(" and
                self.editor.current_line_text.lstrip().startswith("def ")):
            self._handle_fct_def()
        else:
            super(PyAutoCompleteMode, self)._on_post_key_pressed(e)
