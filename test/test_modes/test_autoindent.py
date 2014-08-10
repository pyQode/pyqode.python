"""
To test auto indentation, we simply need to setup the context (code + cursor
position), execute a key press event and compare the resulting plainText with
the expected results (code + cursor position).

As it would be a little tedious to do it entirely with code, we made this
test data driven. It will look in the **auto_indent_cases** directory
for context files (``.ctx``).

Context files are python files with a specific syntax to mark the cursor
position (represented by ``|``) and make the distinction between the input
context and the expected results (``->``)

E.g.::

    class Foo:|
    ->
    class Foo:
        |
"""
import glob
from pyqode.core.api import TextHelper
from pyqode.qt import QtCore, QtWidgets
from pyqode.qt.QtTest import QTest
import pytest
from test.helpers import cwd_at


class Context:
    """
    A context is loaded from a .in or .out file. It basically consist of a
    code fragment and the text cursor position.

    """
    def __init__(self, file_path):
        self.input_code = ''
        self.expected_code = ''
        self.input_line = 0
        self.expected_line = 0
        self.input_column = 1
        self.expected_column = 1
        self._load(file_path)

    def _get_cursor_pos(self, code):
        for i, line in enumerate(code.splitlines()):
            if '|' in line:
                line_nbr = i + 1
                column_nbr = line.find('|')
                return line_nbr, column_nbr
        return 1, 0

    def _load(self, file_path):
        with open(file_path) as file:
            code = file.read()
        input_context, output_context = code.split('\n->\n')
        self.input_line, self.input_column = self._get_cursor_pos(input_context)
        self.expected_line, self.expected_column = self._get_cursor_pos(output_context)
        self.input_code = input_context.replace('|', '')
        self.expected_code = output_context.replace('|', '')


class Case:
    """
    Auto indent test case.

    The test consists of 3 steps:
        - setup input context (.in file)
        - execute a key pressed event with Key_Return
        - compare the results with the output context (.out file)

    """

    def __init__(self, file_path):
        self.name = file_path
        self.context = Context(file_path)

    def run(self, editor):
        editor.setPlainText(self.context.input_code)
        TextHelper(editor).goto_line(self.context.input_line,
                                     self.context.input_column)
        wait = 1
        QTest.qWait(wait)
        QTest.keyPress(editor, QtCore.Qt.Key_Return)
        QTest.qWait(wait)
        assert editor.toPlainText() == self.context.expected_code
        assert TextHelper(editor).current_line_nbr() == self.context.expected_line
        assert TextHelper(editor).current_column_nbr() == self.context.expected_column


@cwd_at('test/test_modes')
def collect_cases():
    cases = []
    for file_path in sorted(glob.glob('auto_indent_cases/*.ctx')):
        # if '44' in file_path:
        cases.append(Case(file_path))
    return cases


@pytest.mark.parametrize('test_case', collect_cases())
def test_auto_indent(editor, test_case):
    QtWidgets.QApplication.setActiveWindow(editor)
    editor.setFocus(True)
    test_case.run(editor)

