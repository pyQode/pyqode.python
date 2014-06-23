"""
Test the autocomplete mode
"""
from pyqode.core.api import TextHelper
from pyqode.python import modes as pymodes


def get_mode(editor):
    return editor.modes.get(pymodes.CommentsMode)


def test_enabled(editor):
    mode = get_mode(editor)
    assert mode.enabled
    mode.enabled = False
    mode.enabled = True


def test_comment_single(editor):
    editor.clear()
    editor.setPlainText('import os\n')
    mode = get_mode(editor)
    mode.comment()
    assert editor.toPlainText() == '# import os\n'
    assert TextHelper(editor).current_line_nbr() == 2


def test_uncomment_single(editor):
    editor.clear()
    editor.setPlainText('# import os\n')
    mode = get_mode(editor)
    mode.comment()
    assert editor.toPlainText() == 'import os\n'
    editor.clear()
    editor.setPlainText('#import os\n')
    mode = get_mode(editor)
    mode.comment()
    assert editor.toPlainText() == '# #import os\n'


def test_comment_selection(editor):
    editor.clear()
    editor.setPlainText('import os;\n  \ndef foo():\n    print("bar")')
    mode = get_mode(editor)
    editor.selectAll()
    mode.comment()
    assert editor.toPlainText() == '# import os;\n  \n# def foo():\n#     print("bar")'
