# -*- coding: utf-8 -*-
""" Contains the python autocomplete mode """
from pyqode.core.api import TextHelper
from pyqode.core.modes import AutoCompleteMode


class PyAutoCompleteMode(AutoCompleteMode):
    """
    Extends :class:`pyqode.core.modes.AutoCompleteMode` to add
    support for method/function call:

        - function completion adds "):" to the function definition.
        - method completion adds "self):" to the method definition.
    """
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
        if (event.text() == "(" and
                helper.current_line_text().lstrip().startswith("def ")):
            self._handle_fct_def()
        else:
            line = TextHelper(self.editor).current_line_text().strip()
            if line != '"""':
                super(PyAutoCompleteMode, self)._on_post_key_pressed(event)


# Auto complete has been removed because there no way to know if there is
# already a docstring after the user has typed """ (all the below code is now
# a docstring).
# In a future version of pyqode, there will be a code assistant widget
# that allow to execute a contextual action where the user has a choice
# to make (e.g. insert sphinx or epydoc params,...)
# I keep the below code as a reference the day we implement that feature in the
# code assistant.

    # def _format_func_params(self, indent):
    #     parameters = []
    #     th = TextHelper(self.editor)
    #     current_line_nbr = th.current_line_nbr()
    #     line_nbr = current_line_nbr - 2
    #     def_line_nbr = None
    #     l = line_nbr
    #     while def_line_nbr is None:
    #         if 'def ' in th.line_text(l):
    #             def_line_nbr = l
    #             break
    #         l -= 1
    #     for i in range(def_line_nbr, line_nbr + 1):
    #         txt = th.line_text(i)
    #         if i == def_line_nbr:
    #             # remove `def fct_name(`
    #             txt = txt[txt.find('(') + 1:]
    #         if i == line_nbr:
    #             # remove `):`
    #             txt = txt[:txt.rfind('):')]
    #         params = txt.strip().split(',')
    #         parameters += params
    #     param_str = ""
    #     for param in parameters:
    #         if param and param != '"""':
    #             param_str += "\n{1}:param {0}:".format(param.strip(),
    #                                                    indent * " ")
    #     return '{1}\n{0}"""'.format(indent * " ", param_str)
    #
    # def _insert_docstring(self, def_line, below_fct):
    #     indent = TextHelper(self.editor).line_indent()
    #     if "class" in def_line or not below_fct:
    #         to_insert = '\n{0}"""'.format(indent * " ")
    #     else:
    #         to_insert = self._format_func_params(indent)
    #     cursor = self.editor.textCursor()
    #     pos = cursor.position()
    #     cursor.beginEditBlock()
    #     cursor.insertText(to_insert)
    #     cursor.setPosition(pos)
    #     cursor.endEditBlock()
    #     self.editor.setTextCursor(cursor)
