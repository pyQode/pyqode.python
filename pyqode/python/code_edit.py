# -*- coding: utf-8 -*-
"""
This package contains the python code editor widget
"""
from pyqode.core.qt import QtCore, QtGui
from pyqode.core import api
from pyqode.core import modes
from pyqode.core import panels
from pyqode.python import managers as pymanagers
from pyqode.python import modes as pymodes
from pyqode.python import panels as pypanels
# pylint: disable=unused-import
from pyqode.python.ui import pyqode_python_icons_rc


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

    def __init__(self, parent=None):
        super(PyCodeEdit, self).__init__(parent)
        self.file = pymanagers.PyFileManager(self)
        self.setLineWrapMode(self.NoWrap)
        self.setWindowTitle("pyQode - Python Editor")

        # install those modes first as they are required by other modes/panels
        self.modes.append(pymodes.DocumentAnalyserMode())

        # panels
        self.panels.append(panels.LineNumberPanel())
        self.panels.append(panels.MarkerPanel())
        self.panels.append(panels.SearchAndReplacePanel(),
                           panels.SearchAndReplacePanel.Position.BOTTOM)
        self.panels.append(pypanels.SymbolBrowserPanel(),
                           pypanels.SymbolBrowserPanel.Position.TOP)
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
        self.modes.append(pymodes.PyHighlighterMode(self.document()))
        self.modes.append(pymodes.PyAutoCompleteMode())
        self.modes.append(pymodes.PyAutoIndentMode())
        self.modes.append(pymodes.FrostedCheckerMode())
        self.modes.append(pymodes.PEP8CheckerMode())
        self.modes.append(pymodes.CalltipsMode())
        self.modes.append(pymodes.PyIndenterMode())
        self.modes.append(pymodes.GoToAssignmentsMode())
        self.modes.append(pymodes.CommentsMode())

    @QtCore.Slot()
    def use_dark_style(self, use=True):
        """
        Changes the editor style to a dark color scheme similar to pycharm's
        darcula color scheme.
        """
        if not use:
            return
        set_dark_color_scheme(self)

    @QtCore.Slot()
    def use_white_style(self, use=True):
        """
        Changes the editor style to a dark color scheme similar to QtCreator's
        default color scheme.
        """
        if not use:
            return
        set_white_color_scheme(self)

    def setPlainText(self, txt, mimetype='text/x-python', encoding='utf-8'):
        """
        Extends QCodeEdit.setPlainText to allow user to setPlainText without
        mimetype (since the python syntax highlighter does not use it).
        """
        # pylint: disable=invalid-name, no-self-use
        super().setPlainText(txt, mimetype, encoding)


def set_dark_color_scheme(code_edit):
    """
    Set a dark scheme on a :class:`pyqode.core.api.CodeEdit`.

    The color scheme is similar to pycharm's darcula color scheme.

    .. note:: This function will work only if a
        :class:`pyqode.python.modes.PyHighlighterMode` has been
        installed on the CodeEdit instance

    :param code_edit: CodeEdit instance
    :type code_edit: pyqode.core.api.CodeEdit
    """
    highlighter = code_edit.modes.get(pymodes.PyHighlighterMode)
    highlighter.styles = highlighter.DEFAULT_DARK_STYLES
    code_edit.background = QtGui.QColor("#252525")
    code_edit.foreground = QtGui.QColor("#A9B7C6")
    code_edit.whitespaces_foreground = QtGui.QColor('#404040')
    line_highlighter = code_edit.modes.get(modes.CaretLineHighlighterMode)
    line_highlighter.refresh()
    symbol_matcher = code_edit.modes.get(modes.SymbolMatcherMode)
    assert isinstance(symbol_matcher, modes.SymbolMatcherMode)
    symbol_matcher.match_background = QtGui.QColor("transparent")
    symbol_matcher.match_foreground = QtGui.QColor("#FF8647")


def set_white_color_scheme(code_edit):
    """
    Set a light scheme on a :class:`pyqode.core.api.CodeEdit`.

    The color scheme is similar to the qt creator's default color scheme.

    .. note:: This function will work only if a
        :class:`pyqode.python.modes.PyHighlighterMode` has been
        installed on the ```code_edit``` instance.

    :param code_edit: CodeEdit instance
    :type code_edit: pyqode.core.api.CodeEdit
    """
    highlighter = code_edit.modes.get(pymodes.PyHighlighterMode)
    highlighter.styles = highlighter.DEFAULT_LIGHT_STYLES
    code_edit.background = QtGui.QColor("#FFFFFF")
    code_edit.foreground = QtGui.QColor("#000000")
    code_edit.whitespaces_foreground = QtGui.QColor('#404040')
    line_highlighter = code_edit.modes.get(modes.CaretLineHighlighterMode)
    line_highlighter.refresh()
    symbol_matcher = code_edit.modes.get(modes.SymbolMatcherMode)
    assert isinstance(symbol_matcher, modes.SymbolMatcherMode)
    symbol_matcher.match_background = QtGui.QBrush(QtGui.QColor('#B4EEB4'))
    symbol_matcher.match_foreground = QtGui.QColor('red')
