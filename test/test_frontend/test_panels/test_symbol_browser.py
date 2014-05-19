from pyqode.qt import QtCore
from pyqode.qt.QtTest import QTest
from pyqode.core import frontend, settings
from pyqode.python.frontend import panels

from ...helpers import editor_open
from ...helpers import preserve_editor_config


def get_panel(editor):
    return frontend.get_panel(editor, panels.SymbolBrowserPanel)


@preserve_editor_config
def test_empty_editor(editor):
    frontend.uninstall_all(editor)
    p = panels.SymbolBrowserPanel()
    frontend.install_panel(editor, p, p.Position.TOP)
    panel = get_panel(editor)
    assert panel.enabled
    panel.enabled = False
    panel.enabled = True
    panel.enabled = False


@editor_open(__file__)
def test_goto_definition(editor):
    QTest.qWait(1000)
    panel = get_panel(editor)
    line = frontend.current_line_nbr(editor)
    panel._on_definition_activated(len(panel._definitions) - 2)
    assert frontend.current_line_nbr(editor) != line
