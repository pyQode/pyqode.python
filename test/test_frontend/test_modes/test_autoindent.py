from PyQt4 import QtCore
from PyQt4.QtTest import QTest
import pytest
from pyqode.core import frontend
from pyqode.python.frontend import modes


def get_mode(editor):
    return frontend.get_mode(editor, modes.PyAutoIndentMode)


class AutoIndentCase:
    def __init__(self, code, result, line, column):
        self.code = code
        self.result = result
        self.line = line
        self.column = column

    def exec_test(self, editor):
        editor.clear()
        editor.setPlainText(self.code)
        frontend.goto_line(editor, self.line, self.column)
        QTest.keyPress(editor, QtCore.Qt.Key_Return)
        QTest.qWait(1000)
        assert editor.toPlainText() == self.result


CASES = [
    (AutoIndentCase("", '\n', 1, 0), ),
    (AutoIndentCase("    import os", '    \n    import os', 1, 4), ),
    (AutoIndentCase("import os", 'import os\n', 1, len('import os')), ),
    (AutoIndentCase("class Foo:", 'class Foo:\n    ', 1, len("class Foo:")), ),
    (AutoIndentCase("# print(foo)", '# print(foo)\n', 1, len("# print(foo)")), ),
    (AutoIndentCase("# print(foo)", '# print(foo\n# )', 1, len("# print(foo)") - 1), ),
    (AutoIndentCase("# print(foo)", '# print(foo\n# )', 1, len("# print(foo)") - 1), ),
    (AutoIndentCase("print(foo)", 'print(\n    foo)', 1, len("print(")), ),
    (AutoIndentCase("print(foo, (1, 2))", 'print(\n    foo, (1, 2))', 1, len("print(")), ),
    (AutoIndentCase("print(foo, (1, 2))", 'print(foo,\n      (1, 2))', 1, len("print(foo,")), )
]


@pytest.mark.parametrize(('case',), CASES)
def test_auto_indent(editor, case):
    case.exec_test(editor)
