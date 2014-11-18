from pyqode.core.api import TextHelper
from pyqode.qt.QtTest import QTest
from pyqode.python import panels

from ..helpers import editor_open


def get_panel(editor):
    return editor.panels.get(panels.SymbolBrowserPanel)


def test_empty_editor(editor):
    editor.panels.clear()
    editor.modes.clear()
    p = panels.SymbolBrowserPanel()
    editor.panels.append(p, p.Position.TOP)
    panel = get_panel(editor)
    assert panel.enabled
    panel.enabled = False
    panel.enabled = True
    panel.enabled = False


@editor_open(__file__)
def test_goto_definition(editor):
    editor.show()
    QTest.qWait(1000)
    panel = get_panel(editor)
    line = TextHelper(editor).current_line_nbr()
    panel._on_definition_activated(len(panel._definitions) - 2)
    assert TextHelper(editor).current_line_nbr() != line
