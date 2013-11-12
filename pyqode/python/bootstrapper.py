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
import time
from multiprocessing.connection import Listener
from pyqode.core import CodeCompletionMode, logger
from pyqode.qt import QtCore


class PreloadWorker(object):
    def __init__(self, modules):
        self.modules = modules

    def __call__(self, conn, *args, **kwargs):
        logger.debug("Boostrapper.preload started: %r" % self.modules)
        for m in self.modules:
            logger.debug("Preloading module %s" % m)
            self.preload(m)
        logger.debug("Boostrapper.preload finished")
        return []

    def preload(self, m):
        import jedi
        try:
            s = "import %s as x; x." % m
            jedi.Script(s, 1, len(s), None).completions()
        except :
            logger.exception("Failed to preload %s" % m)


class Bootstrapper(QtCore.QObject):
    """
    Utility class to help you bootstrap the code completion (if you don't want
    to use lazy bootstrap).

    The bootstrap consists of launching the code completion server and running
    a worker that will pre-load a list of modules.
    """

    #: Signal emitted when the preload worker has finished.
    preLoadFinished = QtCore.Signal()

    def __init__(self, modules):
        """
        :param modules: List of modules (strings) to preload.
        """
        super(Bootstrapper, self).__init__()
        self.modules = modules

    def bootstrap(self, port=8080):
        """
        Bootstraps code completion.
        """
        try:
            l = Listener(("localhost", port))
        except Exception:
            already_running = True
        else:
            already_running = False
            l.close()

        if not already_running:
            server = CodeCompletionMode.startCompletionServer()
            if not server:
                logger.warning("Failed to start completion server")
                self.preLoadFinished.emit()
            else:
                server.signals.workCompleted.connect(self._onWorkFinished)
                server.requestWork(self, PreloadWorker(self.modules))
                self._start = time.time()
        else:
            QtCore.QTimer.singleShot(500, self.preLoadFinished.emit)

    def _onWorkFinished(self, caller_id, worker):
        if caller_id == id(self) and isinstance(worker, PreloadWorker):
            self.preLoadFinished.emit()
            logger.debug("Bootstrapped in %f [s]" % (time.time() - self._start))
