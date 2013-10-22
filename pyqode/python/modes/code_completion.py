#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#The MIT License (MIT)
#
#Copyright (c) <2013> <Colin Duquesnoy and others, see AUTHORS.txt>
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
Contains the JediCompletionProvider class implementation.
"""
import os
import sys

from pyqode.core import CompletionProvider, logger
from pyqode.core import Completion, CodeCompletionMode


#: Default icons
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


class AddSysPathWorker(object):
    def __init__(self, path):
        self.path = path

    def __call__(self, *args, **kwargs):
        import sys
        sys.path.insert(0, self.path)

class RemoveSysPathWorker(object):
    def __init__(self, path):
        self.path = path

    def __call__(self, *args, **kwargs):
        import sys
        sys.path.remove(self.path)


class PrintSysPathWorker(object):
    def __call__(self, *args, **kwargs):
        import sys
        print(sys.path)


class PyCodeCompletionMode(CodeCompletionMode):
    """
    Extends CodeCompletionMode to add a few utility methods to easily
    interoperates with the code completion subprocess.
    """
    @classmethod
    def appendToSrvSysPath(cls, path):
        """
        Inserts a path in sys.modules on the server subprocess.
        """
        w = AddSysPathWorker(path)
        cls.SERVER.requestWork(w, w)

    @classmethod
    def removeFromSrvSysPath(cls, path):
        """
        Removes the path from sys.path on the server subprocess.
        """
        w = RemoveSysPathWorker(path)
        cls.SERVER.requestWork(w, w)

    @classmethod
    def printSrvSysPath(cls, path):
        """
        Prints the subprocess sys.path
        """
        w = PrintSysPathWorker()
        cls.SERVER.requestWork(w, w)


class JediCompletionProvider(CompletionProvider):
    """
    Completion provider using the awesome `jedi`_  library

    .. _`jedi`: https://github.com/davidhalter/jedi
    """
    #: Jedi provider's priority is higher than the priority of the default
    #: DocumentWordsCompletionProvider, this makes the jedi completions appear
    # before the document words completions.
    PRIORITY = 1

    def __init__(self, addToPath=True):
        CompletionProvider.__init__(self)
        #: True to add the parent directory of the python module to sys.path.
        #: Default is True.
        self.addToPath = addToPath

    def preload(self, code, filePath, fileEncoding):
        """
        Preload the opened file (jedi.api.preload_module) and possibly add the
        parent directory to :py:attr:`sys.path` (if addToPath is True)
        """
        try:
            import jedi
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
        """
        Completes python code using `jedi`_.
        """
        retVal = []
        try:
            import jedi
            retVal = []
            script = jedi.Script(code, line, column,
                                 "", fileEncoding)
            logger.debug("Running Jedi")
            completions = script.completions()
            logger.debug("Jedi finished")
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
        except ImportError:
            logger.error("Failed to import jedi. Check your jedi installation")
        except Exception as e:
            logger.error("Jedi failed to provide completions. Error: %s" % e)
        return retVal
