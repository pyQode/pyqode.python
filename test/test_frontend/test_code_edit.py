# -*- coding: utf-8 -*-
"""
Tests for PyCodeEdit
"""
from PyQt4 import QtGui
from PyQt4.QtTest import QTest
from pyqode.core.frontend import CodeEdit
from pyqode.python.frontend import PyCodeEdit
from ..helpers import editor_open


@editor_open(__file__)
def test_py_code_edit(editor):
    assert isinstance(editor, QtGui.QPlainTextEdit)
    assert isinstance(editor, CodeEdit)
    assert isinstance(editor, PyCodeEdit)
    QTest.qWait(1000)
    editor.use_dark_style()
    QTest.qWait(100)
    editor.use_white_style()

    # for coverage
    editor.use_dark_style(use=False)
    editor.use_white_style(use=False)
