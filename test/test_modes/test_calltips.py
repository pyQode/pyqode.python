"""
Test the autocomplete mode
"""
from pyqode.core.api import TextHelper
from pyqode.qt.QtTest import QTest
from pyqode.python import modes as pymodes


def get_mode(editor):
    return editor.modes.get(pymodes.CalltipsMode)


def test_enabled(editor):
    mode = get_mode(editor)
    assert mode.enabled
    mode.enabled = False
    mode.enabled = True


def test_calltips(editor):
    editor.clear()
    mode = get_mode(editor)
    assert editor.backend.connected
    assert mode is not None
    editor.setPlainText("open(__file_")
    TextHelper(editor).goto_line(1, len('open(__file_'))
    QTest.keyPress(editor, ',')
    QTest.keyRelease(editor, ',')
    QTest.qWait(1000)


def test_calltips_with_closing_paren(editor):
    editor.clear()
    mode = get_mode(editor)
    assert editor.backend.connected
    assert mode is not None
    editor.setPlainText("open")
    TextHelper(editor).goto_line(1, len('open'))
    QTest.keyPress(editor, '(')
    QTest.keyRelease(editor, '(')
    QTest.qWait(1000)
    mode._display_tooltip(None, 0)
