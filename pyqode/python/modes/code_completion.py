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


def iconFromType(name, type):
    """
    Returns the retVal that corresponds to the suggestion.
    """
    retVal = None
    type = type.upper()
    if type == "FORFLOW" or type == "STATEMENT":
        type = "PARAM"
    if type == "PARAM" or type == "FUNCTION":
        if name.startswith("__"):
            type += "-PRIV"
        elif name.startswith("_"):
            type += "-PROT"
    if type in ICONS:
        retVal = ICONS[type]
    elif type:
        logger.warning("Unimplemented completion type: %s" %
                       type)
    return retVal


class AddSysPathWorker(object):
    def __init__(self, path):
        self.path = path

    def __call__(self, *args, **kwargs):
        import sys
        if isinstance(self.path, list):
            for p in self.path:
                sys.path.insert(0, p)
        else:
            sys.path.insert(0, self.path)


class RemoveSysPathWorker(object):
    def __init__(self, path):
        self.path = path

    def __call__(self, *args, **kwargs):
        import sys
        if isinstance(self.path, list):
            for p in self.path:
                sys.path.remove(p)
        else:
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
    def printSrvSysPath(cls):
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

    def __init__(self, addToPath=True, modules=None):
        CompletionProvider.__init__(self)
        #: True to add the parent directory of the python module to sys.path.
        #: Default is True.
        self.addToPath = addToPath
        #: Modules to preload.
        self.modules = modules

    def preload(self, code, filePath, fileEncoding):
        """
        Preload the opened file (jedi.api.preload_module) and possibly add the
        parent directory to :py:attr:`sys.path` (if addToPath is True)
        """
        try:
            import jedi
        except ImportError:
            logger.error("Failed to import jedi. Check your jedi "
                         "installation")
        else:
            if self.addToPath:
                dir = os.path.dirname(filePath)
                sys.path.append(dir)
            # preloads the current file (the one open in the editor)
            fn = os.path.splitext(os.path.basename(filePath))[0]
            jedi.api.preload_module(fn)
            # preloads user defined list of modules
            if self.modules and not "preloaded" in self.processDict:
                logger.debug("Preloading modules %r" % self.modules)
                jedi.api.preload_module(*self.modules)
                self.processDict["preloaded"] = True
        logger.debug("Preload finished")
        return []

    def complete(self, code, line, column, completionPrefix,
            filePath, fileEncoding):
        """
        Completes python code using `jedi`_.
        """
        retVal = []
        try:
            import jedi
        except ImportError:
            logger.error("Failed to import jedi. Check your jedi "
                         "installation")
        else:
            try:
                script = jedi.Script(code, line, column, filePath, fileEncoding)
                completions = script.completions()
            except jedi.NotFoundError:
                completions = []
            for completion in completions:
                name = completion.name
                desc = completion.description
                # deduce type from description
                type = desc.split(':')[0]
                desc = desc.split(':')[1]
                icon = iconFromType(name, type)
                retVal.append(Completion(name, icon=icon, tooltip=desc))
        return retVal
