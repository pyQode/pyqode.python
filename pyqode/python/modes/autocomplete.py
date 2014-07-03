# -*- coding: utf-8 -*-
""" Contains the python autocomplete mode """
import jedi
from pyqode.core.api import TextHelper
from pyqode.core.modes import AutoCompleteMode


class PyAutoCompleteMode(AutoCompleteMode):
    """
    Extends :class:`pyqode.core.modes.AutoCompleteMode` to add
    support for function docstring and method/function call.

    Docstring completion adds a `:param` sphinx tag foreach parameter in the
    above function.

    Function completion adds "):" to function definition.

    Method completion adds "self):" to method definition.
    """
    # pylint: disable=no-init, missing-docstring

    def _format_func_params(self, prev_line, indent):
        parameters = ""
        line_nbr = TextHelper(self.editor).current_line_nbr() - 1
        col = len(prev_line) - len(prev_line.strip()) + len("def ") + 1
        script = jedi.Script(self.editor.toPlainText(), line_nbr, col,
                             self.editor.file.path,
                             self.editor.file.encoding)
        definition = script.goto_definitions()[0]
        for defined_name in definition.defined_names():
            if defined_name.name != "self" and defined_name.type == 'param':
                parameters += "\n{1}:param {0}:".format(
                    defined_name.name, indent * " ")
        to_insert = '"\n{0}{1}\n{0}"""'.format(indent * " ", parameters)
        return to_insert

    def _insert_docstring(self, prev_line, below_fct):
        indent = TextHelper(self.editor).line_indent()
        if "class" in prev_line or not below_fct:
            to_insert = '"\n{0}\n{0}"""'.format(indent * " ")
        else:
            to_insert = self._format_func_params(prev_line, indent)
        cursor = self.editor.textCursor()
        pos = cursor.position()
        cursor.insertText(to_insert)
        cursor.setPosition(pos)  # we are there ""|"
        cursor.movePosition(cursor.Down)
        self.editor.setTextCursor(cursor)

    def _in_method_call(self):
        helper = TextHelper(self.editor)
        line_nbr = helper.current_line_nbr() - 1
        expected_indent = helper.line_indent() - 4
        while line_nbr >= 0:
            text = helper.line_text(line_nbr)
            indent = len(text) - len(text.lstrip())
            if indent == expected_indent and 'class' in text:
                return True
            line_nbr -= 1
        return False

    def _handle_fct_def(self):
        if self._in_method_call():
            txt = "self):"
        else:
            txt = "):"
        cursor = self.editor.textCursor()
        cursor.insertText(txt)
        cursor.movePosition(cursor.Left, cursor.MoveAnchor, 2)
        self.editor.setTextCursor(cursor)

    def _on_post_key_pressed(self, event):
        # if we are in disabled cc, use the parent implementation
        helper = TextHelper(self.editor)
        column = helper.current_column_nbr()
        usd = self.editor.textCursor().block().userData()
        if usd:
            for start, end in usd.cc_disabled_zones:
                if (start <= column < end - 1 and
                        not helper.current_line_text(
                            ).lstrip().startswith('"""')):
                    return
            prev_line = helper.line_text(helper.current_line_nbr() - 1)
            is_below_fct_or_class = "def" in prev_line or "class" in prev_line
            if (event.text() == '"' and
                    '""' == helper.current_line_text().strip() and
                    (is_below_fct_or_class or column == 2)):
                self._insert_docstring(prev_line, is_below_fct_or_class)
            elif (event.text() == "(" and
                    helper.current_line_text().lstrip().startswith("def ")):
                self._handle_fct_def()
            else:
                super(PyAutoCompleteMode, self)._on_post_key_pressed(event)
