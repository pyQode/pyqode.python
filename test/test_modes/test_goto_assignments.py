"""
Test the autocomplete mode
"""
from pyqode.core.api import TextHelper
from pyqode.qt import QtCore, QtWidgets
from pyqode.qt.QtTest import QTest
from pyqode.python import modes as pymodes


def get_mode(editor):
    return editor.modes.get(pymodes.GoToAssignmentsMode)


def test_enabled(editor):
    mode = get_mode(editor)
    assert mode.enabled
    mode.enabled = False
    mode.enabled = True


def test_goto_variable(editor):
    editor.clear()
    code = "a = 15\nprint(a)"
    editor.setPlainText(code)
    mode = get_mode(editor)
    TextHelper(editor).goto_line(2, len('print(a)') - 2)
    mode.request_goto()
    QTest.qWait(1000)


out = False


def _on_out_of_doc(*args):
    global out
    out = True


def test_goto_out_of_doc(editor):
    global out
    out = False
    editor.clear()
    code = "a = 15\nprint(a)"
    editor.setPlainText(code)
    mode = get_mode(editor)
    TextHelper(editor).goto_line(2, len('print(a)') - 4)
    mode.out_of_doc.connect(_on_out_of_doc)
    assert out is False
    mode.request_goto()
    QTest.qWait(1000)
    assert out is True


def accept_dlg():
    widgets = QtWidgets.QApplication.instance().topLevelWidgets()
    for w in widgets:
        if isinstance(w, QtWidgets.QDialog):
            QTest.keyPress(w, QtCore.Qt.Key_Tab)
            QTest.keyPress(w, QtCore.Qt.Key_Tab)
            QTest.keyPress(w, QtCore.Qt.Key_Return)


def test_multiple_results(editor):
    editor.clear()
    code = "import os\nos.path.abspath('..')"
    editor.setPlainText(code)
    mode = get_mode(editor)
    TextHelper(editor).goto_line(2, 4)
    mode.request_goto()
    QtCore.QTimer.singleShot(1000, accept_dlg)
    QTest.qWait(1000)


no_results = False


def _on_no_results(*args):
    global no_results
    no_results = True


def test_no_results(editor):
    global no_results
    no_results = False
    editor.clear()
    code = "import foo"
    editor.setPlainText(code)
    mode = get_mode(editor)
    mode.no_results_found.connect(_on_no_results)
    TextHelper(editor).goto_line(1, len('import foo') -2)
    assert no_results is False
    mode.request_goto()
    QTest.qWait(1000)
    assert no_results is True


def test_make_unique(editor):
    seq = ['a', 'b', 'c', 'a']
    mode = get_mode(editor)
    new_seq = mode._unique(seq)
    assert len(new_seq) == len(seq) - 1
