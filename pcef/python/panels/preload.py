"""
This panel shows preload informations
"""
from pcef.core import Panel
from pcef.qt import QtGui, QtCore


class PreLoadPanel(Panel):
    """
    Preload the new file and show the current action + a progress bar
    """
    IDENTIFIER = "preLoadPanel"
    DESCRIPTION = "Pre-load the module definitions in a background thread"

    visibilityChangeRequested = QtCore.Signal(bool)
    progressUpdateRequested = QtCore.Signal(str)

    def __init__(self):
        Panel.__init__(self)
        self.label = QtGui.QLabel("Preloading module definitions. This can take "
                                  "a few seconds. Please wait...")
        self.movieLabel = QtGui.QLabel()
        self.layout = QtGui.QHBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.setStretchFactor(self.label, 100)
        self.movie = QtGui.QMovie(":/pcef_python_icons/rc/spinner.gif")
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
