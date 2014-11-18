"""
Test the autocomplete mode
"""
from pyqode.qt.QtTest import QTest
from pyqode.core.api import TextHelper
from pyqode.python import modes as pymodes

from ..helpers import editor_open


def get_mode(editor):
    return editor.modes.get(pymodes.CommentsMode)


@editor_open(__file__)
def test_enabled(editor):
    mode = get_mode(editor)
    assert mode.enabled
    mode.enabled = False
    mode.enabled = True


@editor_open(__file__)
def test_comment_single(editor):
    editor.setPlainText('import os')
    QTest.qWait(100)
    TextHelper(editor).goto_line(0, 0)
    QTest.qWait(100)
    mode = get_mode(editor)
    mode.comment()
    QTest.qWait(100)
    assert editor.toPlainText() == '# import os'
    assert TextHelper(editor).current_line_nbr() == 0


@editor_open(__file__)
def test_uncomment_single(editor):
    editor.clear()
    editor.setPlainText('# import os\n')
    QTest.qWait(100)
    mode = get_mode(editor)
    QTest.qWait(100)
    mode.comment()
    QTest.qWait(100)
    assert editor.toPlainText() == 'import os\n'
    editor.clear()
    editor.setPlainText('#import os\n')
    QTest.qWait(100)
    mode = get_mode(editor)
    mode.comment()
    QTest.qWait(100)
    assert editor.toPlainText() == '# #import os\n'


@editor_open(__file__)
def test_comment_selection(editor):
    editor.clear()
    editor.setPlainText('import os;\n  \ndef foo():\n    print("bar")')
    QTest.qWait(100)
    mode = get_mode(editor)
    editor.selectAll()
    mode.comment()
    QTest.qWait(100)
    assert editor.toPlainText() == '# import os;\n  \n# def foo():\n#     print("bar")'
