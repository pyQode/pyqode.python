#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#The MIT License (MIT)
#
#Copyright (c) <2013-2014> <Colin Duquesnoy and others, see AUTHORS.txt>
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.
#
"""
This package contains python specific modes, panels and editor.
"""
import re
import sys
import weakref
from PyQt4 import QtCore, QtGui

from pyqode.core.editor import QCodeEdit, Panel
from pyqode.core import modes
from pyqode.core import panels
from pyqode.core.api import constants


from pyqode.python.modes import PyAutoCompleteMode
from pyqode.python.modes import CalltipsMode
from pyqode.python.modes import CommentsMode
from pyqode.python.modes import PEP8CheckerMode
from pyqode.python.modes import PyAutoIndentMode
from pyqode.python.modes import PyFlakesCheckerMode
from pyqode.python.modes import PyHighlighterMode
from pyqode.python.modes import PyIndenterMode
from pyqode.python.modes import DEFAULT_DARK_STYLES
from pyqode.python.modes import DEFAULT_LIGHT_STYLES
from pyqode.python.modes import GoToAssignmentsMode
from pyqode.python.modes import DocumentAnalyserMode
from pyqode.python.panels import SymbolBrowserPanel
from pyqode.python.panels import QuickDocPanel

import pyqode.python.ui.pyqode_python_icons_rc


class QPythonCodeEdit(QCodeEdit):
    """
    Extends QCodeEdit with a hardcoded set of modes and panels specifics to
    a python code editor widget.

    **Panels:**
        * :class:`pyqode.core.FoldingPanel`
        * :class:`pyqode.core.LineNumberPanel`
        * :class:`pyqode.core.MarkerPanel`
        * :class:`pyqode.core.SearchAndReplacePanel`

    **Modes:**
        * :class:`pyqode.core.CaretLineHighlighterMode`
        * :class:`pyqode.core.RightMarginMode`
        * :class:`pyqode.core.CodeCompletionMode` + :class:`pyqode.python.JediCompletionProvider` and :class:`pyqode.core.DocumentWordCompletionProvider`
        * :class:`pyqode.core.ZoomMode`
        * :class:`pyqode.core.SymbolMatcherMode`
        * :class:`pyqode.python.PyAutoCompleteMode`
        * :class:`pyqode.python.PyHighlighterMode`
        * :class:`pyqode.python.PyAutoIndentMode`
        * :class:`pyqode.python.PyFlakesCheckerMode`
        * :class:`pyqode.python.PEP8CheckerMode`
        * :class:`pyqode.python.CalltipsMode`
        * :class:`pyqode.python.PyIndenterMode`

    It also implements utility methods to switch from a white style to a dark
    style and inversely.

    .. note:: This code editor widget use PEP 0263 to detect file encoding.
              If the opened file does not respects the PEP 0263,
              :py:func:`sys.getfilesystemencoding` is used as the default
              encoding.
    """
    DARK_STYLE = 0
    LIGHT_STYLE = 1

    def __init__(self, parent=None):
        super(QPythonCodeEdit, self).__init__(parent)
        self.setLineWrapMode(self.NoWrap)
        self.setWindowTitle("pyQode - Python Editor")

        # install those modes first as they are required by other modes/panels
        self.installMode(DocumentAnalyserMode())

        # panels
        self.installPanel(panels.LineNumberPanel())
        self.installPanel(panels.MarkerPanel())
        self.installPanel(panels.SearchAndReplacePanel(),
                          Panel.Position.BOTTOM)
        self.installPanel(SymbolBrowserPanel(), Panel.Position.TOP)

        # modes
        # generic
        self.installMode(modes.CaretLineHighlighterMode())
        self.installMode(modes.FileWatcherMode())
        self.installMode(modes.RightMarginMode())
        self.installMode(modes.ZoomMode())
        self.installMode(modes.SymbolMatcherMode())
        self.installMode(modes.WordClickMode())
        self.installMode(modes.CodeCompletionMode())
        # python specifics
        self.installMode(PyHighlighterMode(self.document()))
        self.installMode(PyAutoCompleteMode())
        self.installMode(PyAutoIndentMode())
        # self.installMode(PyFlakesCheckerMode())
        self.installMode(PEP8CheckerMode())
        self.installMode(CalltipsMode())
        self.installMode(PyIndenterMode())
        self.installMode(GoToAssignmentsMode())
        self.installPanel(QuickDocPanel(), Panel.Position.BOTTOM)
        self.installMode(CommentsMode())

    def start_server(self, script=None, interpreter=sys.executable, args=None):
        """
        Overrides QCodeEdit.start_server to allow script to be None. In this
        case QPythonCodeEdit will use its internal server.
        """
        if script is None:
            from pyqode.python import server
            script = server.__file__
        super().start_server(script, interpreter=interpreter, args=args)

    def setModulesToPreload(self, modules=None):
        """
        Sets the list of modules to preload. This must be called before opening
        the first file with pyqode. (you can also pass the list of modules to
        the constructor using the modulesToPreload argument).
        """
        self._cc_provider().modules = modules

    @QtCore.pyqtSlot()
    def useDarkStyle(self, use=True):
        """
        Changes the editor style to a dark color scheme similar to pycharm's
        darcula color scheme.
        """
        if not use:
            return
        setDarkColorScheme(self)

    @QtCore.pyqtSlot()
    def useLightStyle(self, use=True):
        """
        Changes the editor style to a dark color scheme similar to QtCreator's
        default color scheme.
        """
        if not use:
            return
        setLightColorScheme(self)

    def detectEncoding(self, data):
        """
        Detects encoding based on PEP 0263
        """
        encoding = self.getDefaultEncoding()
        if sys.version_info[0] == 3:
            data = str(data.decode("utf-8"))
        for l in data.splitlines():
            regexp = re.compile(r"#.*coding[:=]\s*([-\w.]+)")
            match = regexp.match(l)
            if match:
                encoding = match.groups()[0]
        return encoding


def setDarkColorScheme(codeEdit):
    """
    Set a dark scheme on a :class:`pyqode.core.QCodeEdit`.

    The color scheme is similar to pycharm's darcula color scheme.

    .. note:: This function will work only if a
              :class:`pyqode.python.PyHighlighterMode` has been installed on the
              codeEdit instance

    :param codeEdit: QCodeEdit instance
    :type codeEdit: pyqode.core.QCodeEdit
    """
    style = codeEdit.style.clone()
    for k, v in DEFAULT_DARK_STYLES.items():
        style.setValue(k, v, "Python")
    style.setValue("background", QtGui.QColor("#252525"))
    style.setValue("foreground", QtGui.QColor("#A9B7C6"))
    style.setValue("caretLineBackground", QtGui.QColor("#2d2d2d"))
    style.setValue("whiteSpaceForeground", QtGui.QColor('#404040'))
    style.setValue("matchedBraceBackground", None)
    style.setValue("matchedBraceForeground", QtGui.QColor("#FF8647"))
    codeEdit.style = style


def setLightColorScheme(codeEdit):
    """
    Set a light scheme on a :class:`pyqode.core.QCodeEdit`.

    The color scheme is similar to the qt creator's default color scheme.

    .. note:: This function will work only if a
              :class:`pyqode.python.PyHighlighterMode` has been installed on the
              codeEdit instance

    :param codeEdit: QCodeEdit instance
    :type codeEdit: pyqode.core.QCodeEdit
    """
    style = codeEdit.style.clone()
    for k, v in DEFAULT_LIGHT_STYLES.items():
        style.setValue(k, v, "Python")
    style.setValue("background", QtGui.QColor("#FFFFFF"))
    style.setValue("foreground", QtGui.QColor("#000000"))
    style.setValue("caretLineBackground", QtGui.QColor("#E4EDF8"))
    style.setValue("whiteSpaceForeground",
                   constants.EDITOR_WS_FOREGROUND)
    style.setValue("matchedBraceBackground", QtGui.QColor("#B4EEB4"))
    style.setValue("matchedBraceForeground", QtGui.QColor("#FF0000"))
    codeEdit.style = style
