"""
Minimal example showing the use of the SymbolBrowserPanel.

This panel works in combination with the DocumentAnalyserMode.
"""
import logging
logging.basicConfig(level=logging.DEBUG)
import sys

from pyqode.qt import QtWidgets
from pyqode.core.api import code_edit
from pyqode.core.api import CodeEdit
from pyqode.python.backend import server
from pyqode.python.modes import DocumentAnalyserMode
from pyqode.python.panels import SymbolBrowserPanel


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    editor = CodeEdit()
    editor.backend.start(server.__file__)
    editor.resize(800, 600)
    # we must add the document analyser prior to adding the symbol browser
    # panel
    editor.modes.append(DocumentAnalyserMode(editor.document()))
    editor.panels.append(SymbolBrowserPanel(), SymbolBrowserPanel.Position.TOP)
    editor.show()
    editor.file.open(code_edit.__file__)
    app.exec_()
    editor.close()
    del editor
    del app
