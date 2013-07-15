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
        foldPanel.clearIndicators()
        root_node = layout.analyseLayout(self.editor.toPlainText())
        for start, end in self.__getMarkers(root_node):
            foldPanel.addIndicator(FoldingIndicator(start, end))

    def __getMarkers(self, root_node):
        markers = []
        for c in root_node.children:
            markers.append((c.start, c.end))
            markers += self.__getMarkers(c)
        return markers
