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
"""
Contains the JediCompletionProvider class implementation.
"""
import jedi
import logging
import time

from pcef.core import CompletionProvider
from pcef.core import Completion
from pcef.core import indexByName
from pcef.core import DelayJobRunner
from pcef.qt import QtCore, QtGui


ICONS = {'CLASS': ':/pcef_python_icons/rc/class.png',
         'IMPORT': ':/pcef_python_icons/rc/namespace.png',
         'STATEMENT': ':/pcef_python_icons/rc/var.png',
         'FORFLOW': ':/pcef_python_icons/rc/var.png',
         'MODULE': ':/pcef_python_icons/rc/keyword.png',
         'PARAM': ':/pcef_python_icons/rc/var.png',
         'PARAM-PRIV': ':/pcef_python_icons/rc/var.png',
         'PARAM-PROT': ':/pcef_python_icons/rc/var.png',
         'FUNCTION': ':/pcef_python_icons/rc/func.png',
         'FUNCTION-PRIV': ':/pcef_python_icons/rc/func_priv.png',
         'FUNCTION-PROT': ':/pcef_python_icons/rc/func_prot.png'}


class JediCompletionProvider(CompletionProvider, QtCore.QObject):

    def __init__(self, editor):
        QtCore.QObject.__init__(self)
        CompletionProvider.__init__(self, editor, priority=1)

    def run(self, code, line, column, completionPrefix,
            filePath, fileEncoding):
        try:
            retVal = []
            script = jedi.Script(code, line, column,
                                 "", fileEncoding)
            # print("Jedi run", line, column)
            completions = script.completions()
            # print(len(completions))
            for completion in completions:
                    # get type from description
                    desc = completion.description
                    suggestionType = desc.split(':')[0].upper()
                    # get the associated icon if any
                    icon = None
                    if (suggestionType == "FORFLOW" or
                            suggestionType == "STATEMENT"):
                        suggestionType = "PARAM"
                    if suggestionType == "PARAM" or suggestionType == "FUNCTION":
                        if completion.name.startswith("__"):
                            suggestionType += "-PRIV"
                        elif completion.name.startswith("_"):
                            suggestionType += "-PROT"
                    if suggestionType in ICONS:
                        icon = ICONS[suggestionType]
                    else:
                        logging.getLogger("pcef").warning(
                            "Unimplemented completion type: %s" %
                            suggestionType)
                    retVal.append(Completion(completion.name, icon=icon,
                                             tooltip=desc.split(':')[1]))
        except Exception:
            pass
        # print("Finished")
        return retVal
