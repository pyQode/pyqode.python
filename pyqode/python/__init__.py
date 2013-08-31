#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2013 Colin Duquesnoy
#
# This file is part of pyQode.
#
# pyQode is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# pyQode is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with pyQode. If not, see http://www.gnu.org/licenses/.
#
"""
This package contains python specific modes, panels and editors.
"""
# from pyqode.python import panels
from glob import glob
import os
import re
import sys
import pyqode.core
from pyqode.qt import QtCore
from pyqode.python.modes import CalltipsMode
from pyqode.python.modes import JediCompletionProvider
from pyqode.python.modes import PEP8CheckerMode
from pyqode.python.modes import PyAutoIndentMode
from pyqode.python.modes import PyFlakesCheckerMode
from pyqode.python.modes import PyIndenterMode
from pyqode.python.modes import PyHighlighterMode
from pyqode.python.modes import DEFAULT_DARK_STYLES
from pyqode.python.modes import DEFAULT_LIGHT_STYLES
from pyqode.python.panels import PreLoadPanel
from pyqode.qt import QtGui


#: pyqode-python version
__version__ = "1.0b2"


import pyqode.python.ui.pyqode_python_icons_rc


class QPythonCodeEdit(pyqode.core.QCodeEdit):
    """
    Extends QCodeEdit with a hardcoded set of modes and panels specifics to
    a python code editor widget

    **Panels:**
        * line number panel
        * search and replace panel

    **Modes:**
        * document word completion
        * generic syntax highlighter (pygments)
    """
    DARK_STYLE = 0
    LIGHT_STYLE = 1

    def __init__(self, parent=None, addToPath=True):
        """
        :param addToPath: True to add the open file's parent directory to
                          sys.path so that jedi can complete sibling modules.
        """
        super(QPythonCodeEdit, self).__init__(parent)
        self.setLineWrapMode(self.NoWrap)
        self.setWindowTitle("pyQode - Python Editor")
        self.installPanel(pyqode.core.FoldingPanel())
        self.installPanel(pyqode.core.LineNumberPanel(),
                          pyqode.core.PanelPosition.LEFT)
        self.installPanel(pyqode.core.MarkerPanel())
        self.installPanel(pyqode.core.SearchAndReplacePanel(),
                          pyqode.core.PanelPosition.BOTTOM)
        self.installMode(pyqode.core.CaretLineHighlighterMode())
        self.installMode(pyqode.core.RightMarginMode())
        self.installMode(pyqode.core.CodeCompletionMode())
        self.codeCompletionMode.addCompletionProvider(
            JediCompletionProvider(addToPath=addToPath))
        self.codeCompletionMode.addCompletionProvider(
            pyqode.core.DocumentWordCompletionProvider())
        self.installMode(pyqode.core.ZoomMode())
        self.installMode(pyqode.core.FileWatcherMode())
        self.installMode(pyqode.core.SymbolMatcherMode())
        self.installMode(PyHighlighterMode(self.document()))
        self.installMode(PyAutoIndentMode())
        self.installMode(PyFlakesCheckerMode())
        self.installMode(PEP8CheckerMode())
        self.installMode(CalltipsMode())
        self.installMode(PyIndenterMode())
        self.installPanel(PreLoadPanel(), pyqode.core.PanelPosition.TOP)
        self.preLoadPanel.setVisible(False)

    @QtCore.Slot()
    def useDarkStyle(self, use=True):
        if not use:
            return
        style = self.style.clone()
        for k, v in DEFAULT_DARK_STYLES.items():
            style.setValue(k, v, "Python")
        style.setValue("background", QtGui.QColor("#252525"))
        style.setValue("foreground", QtGui.QColor("#A9B7C6"))
        style.setValue("caretLineBackground", QtGui.QColor("#2d2d2d"))
        style.setValue("whiteSpaceForeground", QtGui.QColor('#404040'))
        style.setValue("matchedBraceBackground", None)
        style.setValue("matchedBraceForeground", QtGui.QColor("#FF8647"))
        self.style = style

    @QtCore.Slot()
    def useLightStyle(self, use=True):
        if not use:
            return
        style = self.style.clone()
        for k, v in DEFAULT_LIGHT_STYLES.items():
            style.setValue(k, v, "Python")
        style.setValue("background", QtGui.QColor("#FFFFFF"))
        style.setValue("foreground", QtGui.QColor("#000000"))
        style.setValue("caretLineBackground", QtGui.QColor("#E4EDF8"))
        style.setValue("whiteSpaceForeground",
                       pyqode.core.constants.EDITOR_WS_FOREGROUND)
        style.setValue("matchedBraceBackground", QtGui.QColor("#B4EEB4"))
        style.setValue("matchedBraceForeground", QtGui.QColor("#FF0000"))
        self.style = style

    def detectEncoding(self, data):
        encoding = self.getDefaultEncoding()
        if sys.version_info[0] == 3:
            data = str(data.decode("utf-8"))
        for l in data.splitlines():
            regexp = re.compile(r"#.*coding[:=]\s*([-\w.]+)")
            match = regexp.match(l)
            if match:
                encoding = match.groups()[0]
        return encoding

__all__ = ["PEP8CheckerMode", 'PyHighlighterMode', 'PyAutoIndentMode',
           "__version__", "QPythonCodeEdit"]

if sys.platform == "win32":
    __all__ += ["cxFreeze_getDataFiles"]
