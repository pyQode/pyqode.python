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

    #: Signal emitted when the pre load progressed. Params: labelText, value
    preLoadProgressUpdate = QtCore.Signal(str, int)
    preLoadFinished = QtCore.Signal()
    preLoadDialogExecRequired = QtCore.Signal()

    # PRELOADED_NAMES = []

    def __init__(self, editor, showProgressDialog=True):
        QtCore.QObject.__init__(self)
        CompletionProvider.__init__(self, editor, priority=1)
        self.editor.newTextSet.connect(self.__onNewTextSet)
        self.editor.focusedIn.connect(self.hideProgressDialog)
        self.__jobRunner = DelayJobRunner(self, nbThreadsMax=1, delay=500)
        self.__dlg = QtGui.QProgressDialog(editor)
        self.__dlg.setCancelButton(None)
        self.__dlg.hide()
        self.__showDlg = showProgressDialog
        if showProgressDialog:
            self.preLoadFinished.connect(self.hideProgressDialog)
            self.preLoadProgressUpdate.connect(self.updateProgressDialog)
            self.preLoadDialogExecRequired.connect(self.__execDlg)

    def hideProgressDialog(self):
        print("Hide")
        self.__dlg.hide()

    def updateProgressDialog(self, labelText, value):
        if value == -1:
            self.__dlg.setValue(0)
            self.__dlg.setMinimum(0)
            self.__dlg.setMaximum(0)
        else:
            self.__dlg.setMinimum(0)
            self.__dlg.setMaximum(100)
            self.__dlg.setValue(value)
        self.__dlg.setLabelText(labelText)

    def __execDlg(self):
        if self.__showDlg:
            self.__dlg.show()

    def __onNewTextSet(self):
        self.__dlg.setWindowTitle(
            "Preloading")
        self.__jobRunner.requestJob(
            self.__preLoadDocument, True, self.editor.toPlainText(),
            self.editor.filePath, self.editor.fileEncoding)

    def __preLoadDocument(self, code, fileEncoding, filePath):
        l = logging.getLogger("pcef")
        self.preLoadDialogExecRequired.emit()
        self.preLoadProgressUpdate.emit("Parsing module...", -1)
        names = jedi.api.defined_names(code, filePath, fileEncoding)
        # put up heavy modules first to avoid segfault with python 3
        index = indexByName(names, "QtCore")
        if index != -1:
            names.insert(0, names.pop(index))
        index = indexByName(names, "QtGui")
        if index != -1:
            names.insert(0, names.pop(index))
        index = indexByName(names, "numpy")
        if index != -1:
            names.insert(0, names.pop(index))
        toPreload = []
        for definition in names:
            script = ""
            if definition.type == "import":
                script = "{0};{1}.".format(definition.description, definition.name)
            elif definition.type == "class":
                script = "{0}.".format(definition.name)
            if script:
                toPreload.append((definition, script))
        nb = len(toPreload)
        for i, elem in enumerate(toPreload):
            definition = elem[0]
            script = elem[1]
            msg = "Parsing {2} ({0}/{1})".format(i+1, nb,
                                                          definition.name)
            l.info(msg)
            self.preLoadProgressUpdate.emit(msg, -1)
            jedi.Script(script, 1, len(script), None).completions()
        self.preLoadProgressUpdate.emit(msg, 100)
        time.sleep(0.2)
        l.info("Preloading finished")
        self.preLoadFinished.emit()

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
