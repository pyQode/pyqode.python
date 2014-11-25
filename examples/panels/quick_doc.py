"""
Minimal example showing the use of the QuickDockPanel.
"""
import logging
logging.basicConfig(level=logging.DEBUG)
import sys

from pyqode.qt import QtWidgets
from pyqode.core.api import code_edit
from pyqode.core.api import CodeEdit
from pyqode.python.backend import server
from pyqode.python.panels import QuickDocPanel


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    editor = CodeEdit()
    editor.backend.start(server.__file__)
    editor.resize(800, 600)
    # we must add the document analyser prior to adding the symbol browser
    # panel
    editor.panels.append(QuickDocPanel(), QuickDocPanel.Position.BOTTOM)
    editor.show()
    editor.setPlainText('''# Press Alt+Q on a symbol to get its documentation
import os


class Foo:
    """
    A foo class
    """

    def spam(self, eggs):
        """ spams some eggs """
        return str(eggs).lower()

foo = Foo()
os.path.join(foo.spam())
''', '', '')
    app.exec_()
    editor.close()
    del editor
    del app
