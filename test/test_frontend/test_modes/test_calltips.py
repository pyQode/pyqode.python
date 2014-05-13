"""
Test the autocomplete mode
"""
import logging
from PyQt4 import QtCore
from PyQt4.QtTest import QTest
from pyqode.core import frontend
from pyqode.python.frontend import modes as pymodes
from ...helpers import editor_open


def get_mode(editor):
    return frontend.get_mode(editor, pymodes.CalltipsMode)


def test_enabled(editor):
    mode = get_mode(editor)
    assert mode.enabled
    mode.enabled = False
    mode.enabled = True


def test_calltips(editor):
    editor.clear()
    mode = get_mode(editor)
    assert frontend.connected_to_server(editor)
    assert mode is not None
    editor.setPlainText("open(__file_", 'text/x-python', 'utf-8')
    frontend.goto_line(editor, 1, len('open(__file_'))
    QTest.keyPress(editor, ',')
    QTest.keyRelease(editor, ',')
    QTest.qWait(1000)


def test_calltips_with_closing_paren(editor):
    editor.clear()
    mode = get_mode(editor)
    assert frontend.connected_to_server(editor)
    assert mode is not None
    editor.setPlainText("open", 'text/x-python', 'utf-8')
    frontend.goto_line(editor, 1, len('open'))
    QTest.keyPress(editor, '(')
    QTest.keyRelease(editor, '(')
    QTest.qWait(1000)
    mode._display_tooltip(None, 0)
