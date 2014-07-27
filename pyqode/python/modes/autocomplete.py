# -*- coding: utf-8 -*-
""" Contains the python autocomplete mode """
import jedi
from pyqode.core.api import TextHelper
from pyqode.core.modes import AutoCompleteMode
from pyqode.core.qt import QtCore


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

    def _format_func_params(self, indent):
        parameters = []
        th = TextHelper(self.editor)
        current_line_nbr = th.current_line_nbr()
        line_nbr = current_line_nbr - 2
        def_line_nbr = None
        l = line_nbr
        while def_line_nbr is None:
            if 'def ' in th.line_text(l):
                def_line_nbr = l
                break
            l -= 1
        for i in range(def_line_nbr, line_nbr + 1):
            txt = th.line_text(i)
            if i == def_line_nbr:
                # remove `def fct_name(`
                txt = txt[txt.find('(') + 1:]
            if i == line_nbr:
                # remove `):`
                txt = txt[:txt.rfind('):')]
            params = txt.strip().split(',')
            parameters += params
        param_str = ""
        for param in parameters:
            if param and param != '"""':
                param_str += "\n{1}:param {0}:".format(param.strip(),
                                                       indent * " ")
        return '{1}\n{0}"""'.format(indent * " ", param_str)

    def _insert_docstring(self, def_line, below_fct):
        indent = TextHelper(self.editor).line_indent()
        if "class" in def_line or not below_fct:
            to_insert = '\n{0}"""'.format(indent * " ")
        else:
            to_insert = self._format_func_params(indent)
        cursor = self.editor.textCursor()
        pos = cursor.position()
        cursor.beginEditBlock()
        cursor.insertText(to_insert)
        cursor.setPosition(pos)
        cursor.endEditBlock()
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
        cursor = self.editor.textCursor()
        if event.key() == QtCore.Qt.Key_Return:
            cursor = helper.select_lines(helper.current_line_nbr() - 1,
                                         helper.current_line_nbr() - 1,
                                         apply_selection=False)
            cursor.movePosition(cursor.EndOfLine)
            # add a fake space that will determine if we are in a docstring
            cursor.insertText(' ')
        in_docstring = helper.is_comment_or_string(cursor)
        if event.key() == QtCore.Qt.Key_Return:
            # remove fake space
            cursor.movePosition(cursor.Left, cursor.KeepAnchor)
            cursor.removeSelectedText()
        l = helper.current_line_nbr() - 2
        def_line_nbr = None
        while def_line_nbr is None and l > 0:
            ltext = TextHelper(self.editor).line_text(l)
            if 'def ' in ltext:
                def_line_nbr = l
                break
            l -= 1
        prev_line = helper.previous_line_text()
        def_line = ''
        if def_line_nbr:
            # function
            is_below_fct_or_class = True
        else:
            # class
            def_line = helper.line_text(helper.current_line_nbr() - 2)
            is_below_fct_or_class = "class" in def_line
        if (event.key() == QtCore.Qt.Key_Return and in_docstring and
                '"""' == prev_line.strip()):
            self._insert_docstring(def_line, is_below_fct_or_class)
        elif (event.text() == "(" and
                helper.current_line_text().lstrip().startswith("def ")):
            self._handle_fct_def()
        else:
            line = TextHelper(self.editor).current_line_text().strip()
            if line != '"""':
                super(PyAutoCompleteMode, self)._on_post_key_pressed(event)
