"""
A basic example that show you how to create a basic python code editor widget,
from scratch.

Editor features:
    - syntax highlighting
    - code completion (using jedi)
    - code folding
    - auto indentation
    - auto complete
    - comments mode (ctrl+/)
    - calltips mode
    - linters (pyflakes and pep8) modes + display panel
    - line number panel
    - builtin search and replace panel
"""
import logging
logging.basicConfig()
# optionally, set the qt api to use (in ['pyqt4', 'pyqt5', 'pyside'])
# import os; os.environ['QT_API'] = 'pyside'
import sys
from pyqode.qt import QtWidgets
from pyqode.python.backend import server
from pyqode.core import api, modes, panels
from pyqode.python import modes as pymodes, panels as pypanels, widgets


class MyPythonCodeEdit(widgets.PyCodeEditBase):
    def __init__(self):
        super(MyPythonCodeEdit, self).__init__()

        # starts the default pyqode.python server (which enable the jedi code
        # completion worker).
        self.backend.start(server.__file__)

        # some other modes/panels require the analyser mode, the best is to
        # install it first
        self.modes.append(pymodes.DocumentAnalyserMode())

        #--- core panels
        self.panels.append(panels.FoldingPanel())
        self.panels.append(panels.LineNumberPanel())
        self.panels.append(panels.CheckerPanel())
        self.panels.append(panels.SearchAndReplacePanel(),
                           panels.SearchAndReplacePanel.Position.BOTTOM)
        self.panels.append(panels.EncodingPanel(), api.Panel.Position.TOP)
        # add a context menu separator between editor's
        # builtin action and the python specific actions
        self.add_separator()

        #--- python specific panels
        self.panels.append(pypanels.QuickDocPanel(), api.Panel.Position.BOTTOM)

        #--- core modes
        self.modes.append(modes.CaretLineHighlighterMode())
        self.modes.append(modes.CodeCompletionMode())
        self.modes.append(modes.ExtendedSelectionMode())
        self.modes.append(modes.FileWatcherMode())
        self.modes.append(modes.OccurrencesHighlighterMode())
        self.modes.append(modes.RightMarginMode())
        self.modes.append(modes.SmartBackSpaceMode())
        self.modes.append(modes.SymbolMatcherMode())
        self.modes.append(modes.ZoomMode())

        #---  python specific modes
        self.modes.append(pymodes.CommentsMode())
        self.modes.append(pymodes.CalltipsMode())
        self.modes.append(pymodes.FrostedCheckerMode())
        self.modes.append(pymodes.PEP8CheckerMode())
        self.modes.append(pymodes.PyAutoCompleteMode())
        self.modes.append(pymodes.PyAutoIndentMode())
        self.modes.append(pymodes.PyIndenterMode())


app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
editor = MyPythonCodeEdit()
editor.file.open(__file__)
window.setCentralWidget(editor)
window.show()
app.exec_()
