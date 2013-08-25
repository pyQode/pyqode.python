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
Contains the JediCompletionProvider class implementation.
"""
import os
import jedi
import sys

from pyqode.core import CompletionProvider, logger
from pyqode.core import Completion


ICONS = {'CLASS': ':/pyqode_python_icons/rc/class.png',
         'IMPORT': ':/pyqode_python_icons/rc/namespace.png',
         'STATEMENT': ':/pyqode_python_icons/rc/var.png',
         'FORFLOW': ':/pyqode_python_icons/rc/var.png',
         'MODULE': ':/pyqode_python_icons/rc/keyword.png',
         'KEYWORD': ':/pyqode_python_icons/rc/keyword.png',
         'PARAM': ':/pyqode_python_icons/rc/var.png',
         'PARAM-PRIV': ':/pyqode_python_icons/rc/var.png',
         'PARAM-PROT': ':/pyqode_python_icons/rc/var.png',
         'FUNCTION': ':/pyqode_python_icons/rc/func.png',
         'FUNCTION-PRIV': ':/pyqode_python_icons/rc/func_priv.png',
         'FUNCTION-PROT': ':/pyqode_python_icons/rc/func_prot.png'}


class JediCompletionProvider(CompletionProvider):
    PRIORITY = 1

    def __init__(self, addToPath=True):
        CompletionProvider.__init__(self)
        self.addToPath = addToPath

    def preload(self, code, filePath, fileEncoding):
        try:
            if self.addToPath:
                dir = os.path.dirname(filePath)
                sys.path.append(dir)
            fn = os.path.splitext(os.path.basename(filePath))[0]
            jedi.api.preload_module(fn)
        except Exception as e:
            logger.error("JediCompletionProvider failed to preload: %s" % e)
        return None

    def complete(self, code, line, column, completionPrefix,
            filePath, fileEncoding):
        try:
            retVal = []
            script = jedi.Script(code, line, column,
                                 "", fileEncoding)
            completions = script.completions()
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
                # print(completion, desc)
                if suggestionType in ICONS:
                    icon = ICONS[suggestionType]
                else:
                    logger.warning("Unimplemented completion type: %s" %
                                   suggestionType)
                retVal.append(Completion(completion.name, icon=icon,
                                         tooltip=desc.split(':')[1]))
        except Exception as e:
            logger.error("Jedi failed to provide completions. Error: %s" % e)
        return retVal
