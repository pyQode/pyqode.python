#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# PCEF
# Copyright 2013, Colin Duquesnoy <colin.duquesnoy@gmail.com>
#
# This software is released under the LGPLv3 license.
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""
This package contains python specific modes, panels and editors.
"""
# from pcef.python import panels
import re
import sys
import pcef.core
from pcef.qt import QtCore, QtGui
from pcef.python.modes import PyAutoIndentMode
from pcef.python.modes import PyFlakesCheckerMode
from pcef.python.modes import PyFolderMode
from pcef.python.modes import PyHighlighterMode



#: pcef-python version
__version__ = "1.0.0-dev"


class QPythonCodeEdit(pcef.core.QCodeEdit):
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

    def __init__(self, parent=None):
        pcef.core.QCodeEdit.__init__(self, parent)
        self.setLineWrapMode(self.NoWrap)
        self.setWindowTitle("PCEF - Generic Editor")
        self.installPanel(pcef.core.FoldingPanel())
        self.installPanel(pcef.core.LineNumberPanel(),
                          pcef.core.PanelPosition.LEFT)
        self.installPanel(pcef.core.MarkerPanel())
        self.installPanel(pcef.core.SearchAndReplacePanel(),
                          pcef.core.PanelPosition.BOTTOM)
        self.installMode(pcef.core.CaretLineHighlighterMode())
        self.installMode(pcef.core.RightMarginMode())
        self.installMode(PyHighlighterMode(self.document()))
        self.installMode(pcef.core.ZoomMode())
        self.installMode(pcef.core.FileWatcherMode())
        self.installMode(PyAutoIndentMode())
        self.installMode(PyFolderMode())
        self.installMode(PyFlakesCheckerMode())


    @QtCore.Slot()
    def useDarkStyle(self, use=True):
        if not use:
            return
        style = self.style.clone()
        for k, v in pcef.core.constants.DEFAULT_DARK_STYLES.items():
            style.setValue(k, v, "Python")
        style.setValue("background", "#252525")
        style.setValue("foreground", "#A9B7C6")
        style.setValue("caretLineBackground", "#2d2d2d")
        style.setValue("whiteSpaceForeground", '#404040')
        self.style = style

    @QtCore.Slot()
    def useLightStyle(self, use=True):
        if not use:
            return
        style = self.style.clone()
        for k, v in pcef.core.constants.DEFAULT_STYLES.items():
            style.setValue(k, v, "Python")
        style.setValue("background", "#FFFFFF")
        style.setValue("foreground", "#000000")
        style.setValue("caretLineBackground", "#E4EDF8")
        style.setValue("whiteSpaceForeground",
                       pcef.core.constants.EDITOR_WS_FOREGROUND)
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

__all__ = ['PyHighlighterMode', 'PyAutoIndentMode', "__version__",
           "QPythonCodeEdit"]
