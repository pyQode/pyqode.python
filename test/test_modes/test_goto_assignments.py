"""
Test the autocomplete mode
"""
from pyqode.core.api import TextHelper
from pyqode.qt import QtCore, QtWidgets
from pyqode.qt.QtTest import QTest
from pyqode.python import modes as pymodes
from test.helpers import editor_open


def get_mode(editor):
    return editor.modes.get(pymodes.GoToAssignmentsMode)


@editor_open(__file__)
def test_enabled(editor):
    mode = get_mode(editor)
    assert mode.enabled
    mode.enabled = False
    mode.enabled = True


@editor_open(__file__)
def test_goto_variable(editor):
    editor.clear()
    code = "a = 15\nprint(a)"
    editor.setPlainText(code)
    mode = get_mode(editor)
    TextHelper(editor).goto_line(2, len('print(a)') - 2)
    mode.request_goto()
    QTest.qWait(5000)
    assert TextHelper(editor).current_line_nbr() == 0


out = False


def _on_out_of_doc(*args):
    global out
    out = True


@editor_open(__file__)
def test_goto_out_of_doc(editor):
    global out
    out = False
    editor.clear()
    code = "import logging\nlogging.basicConfig()"
    editor.setPlainText(code)
    mode = get_mode(editor)
    TextHelper(editor).goto_line(1, len('logging.basicConfig()') - 4)
    mode.out_of_doc.connect(_on_out_of_doc)
    assert out is False
    mode.request_goto()
    QTest.qWait(5000)
    assert out is True


flg_multi = False


def accept_dlg():
    global flg_multi
    flg_multi = True
    widgets = QtWidgets.QApplication.instance().topLevelWidgets()
    for w in widgets:
        if isinstance(w, QtWidgets.QDialog):
            QTest.keyPress(w, QtCore.Qt.Key_Tab)
            QTest.keyPress(w, QtCore.Qt.Key_Tab)
            QTest.keyPress(w, QtCore.Qt.Key_Return)

@editor_open(__file__)
def test_multiple_results(editor):
    global flg_multi
    editor.clear()
    code = "import os\nos.path.abspath('..')"
    editor.setPlainText(code)
    mode = get_mode(editor)
    TextHelper(editor).goto_line(1, 4)
    QTest.qWait(5000)
    mode.request_goto()
    assert flg_multi is False
    QtCore.QTimer.singleShot(1000, accept_dlg)
    QTest.qWait(5000)
    assert flg_multi is True


@editor_open(__file__)
def test_make_unique(editor):
    seq = ['a', 'b', 'c', 'a']
    mode = get_mode(editor)
    new_seq = mode._unique(seq)
    assert len(new_seq) == len(seq) - 1
