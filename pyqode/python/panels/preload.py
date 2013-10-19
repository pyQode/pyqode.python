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
This panel shows pre-load information.
"""
from pyqode.core import Panel
from pyqode.qt import QtGui, QtCore


class PreLoadPanel(Panel):
    """
    You can subclass the jedi completion provider to preload heavy modules which
    might take a while and need to be notify in a way or another to the user.
    This panel can be used for that purpose. It connects to the
    :attr:`pyqode.core.CodeCompletionMode.preLoadStarted` and
    :attr:`pyqode.core.CodeCompletionMode.preLoadCompleted`
    to automatically show/hide a little notification area with a
    QLabel and QMovieAnimation.
    """
    IDENTIFIER = "preLoadPanel"
    DESCRIPTION = "Pre-load the module definitions in a background thread"

    def __init__(self):
        Panel.__init__(self)
        self.label = QtGui.QLabel("Preloading module definitions. This can take "
                                  "a few seconds. Please wait...")
        self.movieLabel = QtGui.QLabel()
        self.layout = QtGui.QHBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.setStretchFactor(self.label, 100)
        self.movie = QtGui.QMovie(":/pyqode_python_icons/rc/spinner.gif")
        self.movieLabel.setMovie(self.movie)
        c = QtGui.QColor(0)
        c.setAlpha(0)
        self.movie.setBackgroundColor(c)
        self.movie.start()
        self.layout.addWidget(self.movieLabel)
        self.setLayout(self.layout)

    def _onInstall(self, editor):
        Panel._onInstall(self, editor)
        if hasattr(editor, "codeCompletionMode"):
            self.editor.codeCompletionMode.preLoadStarted.connect(
                self.show)
            self.editor.codeCompletionMode.preLoadCompleted.connect(
                self.hide)

    def sizeHint(self, *args, **kwargs):
        return QtCore.QSize(self.maximumWidth(), 40)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.fillRect(event.rect(), self.palette().brush(
            QtGui.QPalette.ToolTipBase))
        painter.setPen(QtGui.QPen(self.palette().window().color()))
        painter.drawLine(event.rect().bottomLeft(), event.rect().bottomRight())
