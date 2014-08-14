# -*- coding: utf-8 -*-
"""
Tests for PyCodeEdit
"""
from pyqode.qt import QtWidgets
from pyqode.qt.QtTest import QTest
from pyqode.core.api import CodeEdit, ColorScheme
from pyqode.python.widgets.code_edit import PyCodeEdit
from pyqode.python.modes import PythonSH
from ..helpers import editor_open


@editor_open(__file__)
def test_py_code_edit(editor):
    assert isinstance(editor, QtWidgets.QPlainTextEdit)
    assert isinstance(editor, CodeEdit)
    assert isinstance(editor, PyCodeEdit)
    QTest.qWait(1000)
    editor.modes.get(PythonSH).color_scheme = ColorScheme('darcula')
    QTest.qWait(1000)
    editor.modes.get(PythonSH).color_scheme = ColorScheme('qt')
    QTest.qWait(1000)
