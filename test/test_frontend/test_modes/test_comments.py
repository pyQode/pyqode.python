"""
Test the autocomplete mode
"""
import logging
from pyqode.qt import QtCore
from pyqode.qt.QtTest import QTest
from pyqode.core import frontend
from pyqode.python.frontend import modes as pymodes
from ...helpers import editor_open


def get_mode(editor):
    return frontend.get_mode(editor, pymodes.CommentsMode)


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
    assert frontend.current_line_nbr(editor) == 2


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
