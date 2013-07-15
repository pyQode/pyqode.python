#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# PCEF - Python/Qt Code Editing Framework
# Copyright 2013, Colin Duquesnoy <colin.duquesnoy@gmail.com>
#
# This software is released under the LGPLv3 license.
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
""" Contains the code folding mode use to control the foldingPanel """
from pcef.core import Mode, FoldingIndicator
from pcef.python import layout


class PyFolderMode(Mode):
    """
    Mode that manage the fold panel using the layout module
    """
    IDENTIFIER = "pyFolderMode"
    DESCRIPTION = "Manage the fold panel for a python source code"

    def __init__(self):
        Mode.__init__(self)
        self.__nbLines = 0

    def onStateChanged(self, state):
        """
        Called when the mode is activated/deactivated
        """
        if state:
            self.editor.blockCountChanged.connect(self.__onTextChanged)
            self.editor.newTextSet.connect(self.__onTextChanged)
        else:
            self.editor.blockCountChanged.disconnect(self.__onTextChanged)
            self.editor.newTextSet.disconnect(self.__onTextChanged)

    def __onTextChanged(self):
        """
        Update the fold panel markers if the number of lines changed using
        the PyDocAnalyser
        :return:
        """
        try:
            foldPanel = self.editor.foldingPanel
        except AttributeError:
            return
        root_node = layout.analyseLayout(self.editor.toPlainText())
        indicators = self.__getIndicators(root_node)
        oldIndicators = foldPanel.indicators
        if len(indicators) == len(oldIndicators):
            for new, old in zip(indicators, oldIndicators):
                if old.state == old.FOLDED:
                    new.state = new.FOLDED
        foldPanel.clearIndicators()
        for indic in indicators:
            foldPanel.addIndicator(indic)
            if indic.state == indic.FOLDED:
                foldPanel.fold(indic)

    def __getIndicators(self, root_node):
        markers = []
        for c in root_node.children:
            if (c.type == layout.DocumentLayoutNode.Type.GLOBAL_VAR or
                    c.type == layout.DocumentLayoutNode.Type.ENTRY_POINT):
                continue
            markers.append(FoldingIndicator(c.start, c.end))
            markers += self.__getIndicators(c)
        return markers
