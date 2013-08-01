"""
This panel shows preload informations
"""
import logging
import jedi
import time
from pcef.core import Panel, indexByName
from pcef.core import DelayJobRunner
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
        self.__jobRunner = DelayJobRunner(self, nbThreadsMax=1, delay=500)
        self.visibilityChangeRequested.connect(self.setVisible)
        self.progressUpdateRequested.connect(self.updateProgressInfos)
        self.label = QtGui.QLabel("")
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

    def _onStateChanged(self, state):
        Panel._onStateChanged(self, state)
        if state:
            self.editor.newTextSet.connect(self.requestPreload)
        else:
            self.editor.newTextSet.disconnect(self.requestPreload)

    def sizeHint(self, *args, **kwargs):
        return QtCore.QSize(self.maximumWidth(), 40)

    def requestPreload(self):
        self.label.setText("Preloading module %s" % self.editor.fileName)
        self.show()
        self.__jobRunner.requestJob(
            self.preload, True, self.editor.toPlainText(),
            self.editor.fileEncoding, self.editor.filePath)

    def preload(self, code, fileEncoding, filePath):
        l = logging.getLogger("pcef")
        self.visibilityChangeRequested.emit(True)
        self.progressUpdateRequested.emit("Parsing module...")
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
        toPreLoad = []
        for definition in names:
            script = ""
            if definition.type == "import":
                script = "{0};{1}.".format(definition.description, definition.name)
            elif definition.type == "class":
                script = "{0}.".format(definition.name)
            if script:
                toPreLoad.append((definition, script))
        nb = len(toPreLoad)
        for i, elem in enumerate(toPreLoad):
            definition = elem[0]
            script = elem[1]
            msg = "Parsing {2} ({0}/{1})".format(i+1, nb, definition.name)
            l.info(msg)
            self.progressUpdateRequested.emit(msg)
            try:
                jedi.Script(script, 1, len(script), "").completions()
            except Exception as e:
                logging.error("Failed to parse %s - %s" % (definition.name, e))
        self.progressUpdateRequested.emit("Finished")
        l.info("Pre-loading finished")
        self.visibilityChangeRequested.emit(False)

    def updateProgressInfos(self, text):
        self.label.setText(text)
        self.editor.refreshPanels()
        self.repaint()

    def paintEvent(self, event):
        # print("Paint event")
        painter = QtGui.QPainter(self)
        painter.fillRect(event.rect(), self.palette().brush(
            QtGui.QPalette.ToolTipBase))
        painter.setPen(QtGui.QPen(self.palette().window().color()))
        painter.drawLine(event.rect().bottomLeft(), event.rect().bottomRight())
        # QtGui.QWidget.paintEvent(self, event)
