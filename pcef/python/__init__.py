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
import pcef.core
from pcef.qt import QtCore, QtGui
from pcef.python.modes import PyHighlighterMode
from pcef.python.modes import PyAutoIndentMode


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
        self.installPanel(pcef.core.SearchAndReplacePanel(),
                          pcef.core.PanelPosition.BOTTOM)
        self.installMode(pcef.core.CaretLineHighlighterMode())
        self.installMode(pcef.core.RightMarginMode())
        self.installMode(PyHighlighterMode(self.document()))
        self.installMode(pcef.core.ZoomMode())
        self.installMode(PyAutoIndentMode())

    @QtCore.Slot()
    def useDarkStyle(self, use=True):
        if not use:
            return
        for k, v in pcef.core.constants.DEFAULT_DARK_STYLES.items():
            self.style.setValue(k, v, "Python")
        self.style.setValue("background", "#252525")
        self.style.setValue("foreground", "#A9B7C6")
        self.style.setValue("caretLineBackground", "#2d2d2d")
        self.style.setValue("selectionBackground",
                            '#78879b')
        self.style.setValue("selectionForeground",
                            "#FFFFFF")
        self.style.setValue("panelBackground",
                            '#302F2F')
        self.style.setValue("panelForeground",
                            '#808080')
        self.style.setValue("panelHighlight",
                            '#404040')
        self.style.setValue("whiteSpaceForeground",
                            '#404040')
        self.style.setValue("nativeFoldingIndicator", False)
        self.style.setValue("foldScopeBackground", QtGui.QColor("#808080"))
        self.pyHighlighter.rehighlight()

    @QtCore.Slot()
    def useLightStyle(self, use=True):
        if not use:
            return
        for k, v in pcef.core.constants.DEFAULT_STYLES.items():
            self.style.setValue(k, v, "Python")
        self.style.setValue("background", "#FFFFFF")
        self.style.setValue("foreground", "#000000")
        self.style.setValue("caretLineBackground", "#E4EDF8")
        self.style.setValue("selectionBackground",
                            pcef.core.constants.SELECTION_BACKGROUND)
        self.style.setValue("selectionForeground",
                            pcef.core.constants.SELECTION_FOREGROUND)
        self.style.setValue("panelBackground",
                            pcef.core.constants.PANEL_BACKGROUND)
        self.style.setValue("panelForeground",
                            pcef.core.constants.PANEL_FOREGROUND)
        self.style.setValue("whiteSpaceForeground",
                            pcef.core.constants.EDITOR_WS_FOREGROUND)
        self.style.setValue("panelHighlight",
                            pcef.core.constants.PANEL_HIGHLIGHT)
        self.style.setValue("nativeFoldingIndicator", True)
        self.foldingPanel.resetScopeColor()
        self.pyHighlighter.rehighlight()

    def detectEncoding(self, data):
        encoding = self.getDefaultEncoding()
        data = str(data.decode("utf-8"))
        for l in data.splitlines():
            regexp = re.compile(r"#.*coding[:=]\s*([-\w.]+)")
            match = regexp.match(l)
            if match:
                encoding = match.groups()[0]
        return encoding

__all__ = ['PyHighlighterMode', 'PyAutoIndentMode', "__version__",
           "QPythonCodeEdit"]
