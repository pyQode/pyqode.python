# -*- coding: utf-8 -*-
"""
This package contains the python code editor widget
"""
from pyqode.qt import QtCore, QtGui
from pyqode.core import api
from pyqode.core import modes
from pyqode.core import panels
from pyqode.python import managers as pymanagers
from pyqode.python import modes as pymodes
from pyqode.python import panels as pypanels
from pyqode.python.folding import PythonFoldDetector
# load pyqode.python resources (code completion icons)
# DO NOT REMOVE
from pyqode.python._forms import pyqode_python_icons_rc


class PyCodeEdit(api.CodeEdit):
    """
    Extends CodeEdit with a hardcoded set of modes and panels specifics to
    a python code editor widget.

    It also implements utility methods to switch from a white style to a dark
    style and inversely.

    .. note:: This code editor widget use PEP 0263 to detect file encoding.
              If the opened file does not respects the PEP 0263,
              :py:func:`locale.getpreferredencoding` is used as the default
              encoding.
    """
    DARK_STYLE = 0
    LIGHT_STYLE = 1

    mimetypes = ['text/x-python']

    def __init__(self, parent=None):
        super(PyCodeEdit, self).__init__(parent)
        self.file = pymanagers.PyFileManager(self)
        self.setLineWrapMode(self.NoWrap)
        self.setWindowTitle("pyQode - Python Editor")

        # install those modes first as they are required by other modes/panels
        self.modes.append(pymodes.DocumentAnalyserMode())

        # panels
        self.panels.append(panels.FoldingPanel())
        self.panels.append(panels.LineNumberPanel())
        self.panels.append(panels.CheckerPanel())
        self.panels.append(panels.SearchAndReplacePanel(),
                           panels.SearchAndReplacePanel.Position.BOTTOM)
        self.panels.append(pypanels.SymbolBrowserPanel(),
                           pypanels.SymbolBrowserPanel.Position.TOP)
        self.panels.append(panels.EncodingPanel(), api.Panel.Position.TOP)
        self.add_separator()
        self.panels.append(pypanels.QuickDocPanel(), api.Panel.Position.BOTTOM)

        # modes
        # generic
        self.modes.append(modes.CaretLineHighlighterMode())
        self.modes.append(modes.FileWatcherMode())
        self.modes.append(modes.RightMarginMode())
        self.modes.append(modes.ZoomMode())
        self.modes.append(modes.SymbolMatcherMode())
        self.modes.append(modes.WordClickMode())
        self.modes.append(modes.CodeCompletionMode())
        # python specifics
        self.modes.append(pymodes.PythonSH(self.document()))
        self.modes.append(pymodes.PyAutoIndentMode())
        self.modes.append(pymodes.PyAutoCompleteMode())
        self.modes.append(pymodes.FrostedCheckerMode())
        self.modes.append(pymodes.PEP8CheckerMode())
        self.modes.append(pymodes.CalltipsMode())
        self.modes.append(pymodes.PyIndenterMode())
        self.modes.append(pymodes.GoToAssignmentsMode())
        self.modes.append(pymodes.CommentsMode())

        self.syntax_highlighter.fold_detector = PythonFoldDetector()

    def setPlainText(self, txt, mimetype='text/x-python', encoding='utf-8'):
        """
        Extends QCodeEdit.setPlainText to allow user to setPlainText without
        mimetype (since the python syntax highlighter does not use it).
        """
        super().setPlainText(txt, mimetype, encoding)
