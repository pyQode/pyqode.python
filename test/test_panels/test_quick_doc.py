from pyqode.core.api import TextHelper
from pyqode.qt import QtCore
from pyqode.qt.QtTest import QTest
from pyqode.python import panels


def get_panel(editor):
    return editor.panels.get(panels.QuickDocPanel)


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
    TextHelper(editor).goto_line(1, 1)
    panel._on_action_quick_doc_triggered()
    QTest.qWait(2000)
    assert panel.isVisible()
    assert 'open' in panel.text_edit.toPlainText()
    editor.clear()
    panel._on_action_quick_doc_triggered()
    QTest.qWait(1000)
    assert panel.isVisible()
    assert panel.text_edit.toPlainText() == 'Documentation not found'
