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
from pyqode.python.modes import FrostedCheckerMode
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
        * :class:`pyqode.core.CodeCompletionMode`
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
        self.install_mode(DocumentAnalyserMode())

        # panels
        self.install_panel(panels.LineNumberPanel())
        self.install_panel(panels.MarkerPanel())
        self.install_panel(panels.SearchAndReplacePanel(),
                           Panel.Position.BOTTOM)
        self.install_panel(SymbolBrowserPanel(), Panel.Position.TOP)

        # modes
        # generic
        self.install_mode(modes.CaretLineHighlighterMode())
        self.install_mode(modes.FileWatcherMode())
        self.install_mode(modes.RightMarginMode())
        self.install_mode(modes.ZoomMode())
        self.install_mode(modes.SymbolMatcherMode())
        self.install_mode(modes.WordClickMode())
        self.install_mode(modes.CodeCompletionMode())
        # python specifics
        self.install_mode(PyHighlighterMode(self.document()))
        self.install_mode(PyAutoCompleteMode())
        self.install_mode(PyAutoIndentMode())
        self.install_mode(FrostedCheckerMode())
        self.install_mode(PEP8CheckerMode())
        self.install_mode(CalltipsMode())
        self.install_mode(PyIndenterMode())
        self.install_mode(GoToAssignmentsMode())
        self.install_panel(QuickDocPanel(), Panel.Position.BOTTOM)
        self.install_mode(CommentsMode())

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

    def detect_encoding(self, data):
        """
        Detects encoding based on PEP 0263
        """
        encoding = self.default_encoding()
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
        QCodeEdit instance

    :param codeEdit: QCodeEdit instance
    :type codeEdit: pyqode.core.QCodeEdit
    """
    style = codeEdit.style.clone()
    for k, v in DEFAULT_DARK_STYLES.items():
        style.set_value(k, v, "Python")
    style.set_value("background", QtGui.QColor("#252525"))
    style.set_value("foreground", QtGui.QColor("#A9B7C6"))
    style.set_value("caretLineBackground", QtGui.QColor("#2d2d2d"))
    style.set_value("whiteSpaceForeground", QtGui.QColor('#404040'))
    style.set_value("matchedBraceBackground", None)
    style.set_value("matchedBraceForeground", QtGui.QColor("#FF8647"))
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
        style.set_value(k, v, "Python")
    style.set_value("background", QtGui.QColor("#FFFFFF"))
    style.set_value("foreground", QtGui.QColor("#000000"))
    style.set_value("caretLineBackground", QtGui.QColor("#E4EDF8"))
    style.set_value("whiteSpaceForeground",
                    constants.EDITOR_WS_FOREGROUND)
    style.set_value("matchedBraceBackground", QtGui.QColor("#B4EEB4"))
    style.set_value("matchedBraceForeground", QtGui.QColor("#FF0000"))
    codeEdit.style = style
