from pyqode.qt import QtCore
from pyqode.qt.QtTest import QTest
from pyqode.core import frontend
from pyqode.python.frontend import panels


def get_panel(editor):
    return frontend.get_panel(editor, panels.QuickDocPanel)


def test_enabled(editor):
    panel = get_panel(editor)
    assert panel.enabled
    panel.enabled = False
    panel.enabled = True
    panel.enabled = False


def test_get_doc(editor):
    panel = get_panel(editor)
    assert not panel.isVisible()
    editor.setPlainText('open')
    frontend.goto_line(editor, 1, 1)
    QTest.keyPress(panel, QtCore.Qt.Key_Q, QtCore.Qt.AltModifier)
    QTest.qWait(1000)
    assert panel.isVisible()
    assert 'open' in panel.text_edit.toPlainText()
    editor.clear()
    QTest.keyPress(panel, QtCore.Qt.Key_Q, QtCore.Qt.AltModifier)
    QTest.qWait(1000)
    assert panel.isVisible()
    assert panel.text_edit.toPlainText() == 'Documentation not found'
