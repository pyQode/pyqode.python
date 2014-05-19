# -*- coding: utf-8 -*-
"""
This package contains python specific modes, panels and editor.
"""
from pyqode.qt import QtCore, QtGui

from pyqode.core.frontend import CodeEdit
from pyqode.core import frontend
from pyqode.core.frontend import modes
from pyqode.core.frontend import panels
from pyqode.core import style as core_style
from pyqode.python import style
from pyqode.python.frontend import modes as pymodes
from pyqode.python.frontend.modes.syntax_highlighter import DEFAULT_DARK_STYLES
from pyqode.python.frontend.modes.syntax_highlighter import \
    DEFAULT_LIGHT_STYLES
from pyqode.python.frontend import panels as pypanels
# pylint: disable=unused-import
from pyqode.python.frontend.ui import pyqode_python_icons_rc


class PyCodeEdit(CodeEdit):
    """
    Extends CodeEdit with a hardcoded set of modes and panels specifics to
    a python code editor widget.

    **Panels:**
        * :class:`pyqode.core.frontend.panels.LineNumberPanel`
        * :class:`pyqode.core.frontend.panels.MarkerPanel`
        * :class:`pyqode.core.frontend.panels.SearchAndReplacePanel`
        * :class:`pyqode.python.frontend.panels.QuickDocPanel`
        * :class:`pyqode.python.frontend.panels.SymbolBrowserPanel`

    **Modes:**
        * :class:`pyqode.core.frontend.modes.CaretLineHighlighterMode`
        * :class:`pyqode.core.frontend.modes.RightMarginMode`
        * :class:`pyqode.core.frontend.modes.CodeCompletionMode`
        * :class:`pyqode.core.frontend.modes.ZoomMode`
        * :class:`pyqode.core.frontend.modes.SymbolMatcherMode`
        * :class:`pyqode.python.frontend.modes.PyAutoCompleteMode`
        * :class:`pyqode.python.frontend.modes.PyHighlighterMode`
        * :class:`pyqode.python.frontend.modes.PyAutoIndentMode`
        * :class:`pyqode.python.frontend.modes.PyFlakesCheckerMode`
        * :class:`pyqode.python.frontend.modes.PEP8CheckerMode`
        * :class:`pyqode.python.frontend.modes.CalltipsMode`
        * :class:`pyqode.python.frontend.modes.PyIndenterMode`

    It also implements utility methods to switch from a white style to a dark
    style and inversely.

    .. note:: This code editor widget use PEP 0263 to detect file encoding.
              If the opened file does not respects the PEP 0263,
              :py:func:`sys.getfilesystemencoding` is used as the default
              encoding.
    """
    DARK_STYLE = 0
    LIGHT_STYLE = 1

    def __init__(self, parent=None):
        super(PyCodeEdit, self).__init__(parent)
        self.setLineWrapMode(self.NoWrap)
        self.setWindowTitle("pyQode - Python Editor")

        # install those modes first as they are required by other modes/panels
        frontend.install_mode(self, pymodes.DocumentAnalyserMode())

        # panels
        frontend.install_panel(self, panels.LineNumberPanel())
        frontend.install_panel(self, panels.MarkerPanel())
        frontend.install_panel(self, panels.SearchAndReplacePanel(),
                               panels.SearchAndReplacePanel.Position.BOTTOM)
        frontend.install_panel(self, pypanels.SymbolBrowserPanel(),
                               pypanels.SymbolBrowserPanel.Position.TOP)

        # modes
        # generic
        frontend.install_mode(self, modes.CaretLineHighlighterMode())
        frontend.install_mode(self, modes.FileWatcherMode())
        frontend.install_mode(self, modes.RightMarginMode())
        frontend.install_mode(self, modes.ZoomMode())
        frontend.install_mode(self, modes.SymbolMatcherMode())
        frontend.install_mode(self, modes.WordClickMode())
        frontend.install_mode(self, modes.CodeCompletionMode())
        # python specifics
        frontend.install_mode(self, pymodes.PyHighlighterMode(self.document()))
        frontend.install_mode(self, pymodes.PyAutoCompleteMode())
        frontend.install_mode(self, pymodes.PyAutoIndentMode())
        frontend.install_mode(self, pymodes.FrostedCheckerMode())
        frontend.install_mode(self, pymodes.PEP8CheckerMode())
        frontend.install_mode(self, pymodes.CalltipsMode())
        frontend.install_mode(self, pymodes.PyIndenterMode())
        frontend.install_mode(self, pymodes.GoToAssignmentsMode())
        frontend.install_panel(self, pypanels.QuickDocPanel(),
                               frontend.Panel.Position.BOTTOM)
        frontend.install_mode(self, pymodes.CommentsMode())

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
    Set a dark scheme on a :class:`pyqode.core.frontend.CodeEdit`.

    The color scheme is similar to pycharm's darcula color scheme.

    .. note:: This function will work only if a
        :class:`pyqode.python.frontend.modes.PyHighlighterMode` has been
        installed on the CodeEdit instance

    :param code_edit: CodeEdit instance
    :type code_edit: pyqode.core.frontend.CodeEdit
    """
    for key, val in DEFAULT_DARK_STYLES.items():
        style.__dict__[key] = val
    core_style.background = QtGui.QColor("#252525")
    core_style.foreground = QtGui.QColor("#A9B7C6")
    core_style.caretLineBackground = QtGui.QColor("#2d2d2d")
    core_style.whiteSpaceForeground = QtGui.QColor('#404040')
    core_style.matchedBraceBackground = None
    core_style.matchedBraceForeground = QtGui.QColor("#FF8647")
    code_edit.refresh_style()


def set_white_color_scheme(code_edit):
    """
    Set a light scheme on a :class:`pyqode.core.frontend.CodeEdit`.

    The color scheme is similar to the qt creator's default color scheme.

    .. note:: This function will work only if a
        :class:`pyqode.python.frontend.modes.PyHighlighterMode` has been
        installed on the ```code_edit``` instance.

    :param code_edit: CodeEdit instance
    :type code_edit: pyqode.core.frontend.CodeEdit
    """
    for key, value in DEFAULT_LIGHT_STYLES.items():
        style.__dict__[key] = value
    core_style.background = QtGui.QColor("#FFFFFF")
    core_style.foreground = QtGui.QColor("#000000")
    core_style.caretLineBackground = QtGui.QColor("#E4EDF8")
    core_style.whiteSpaceForeground = QtGui.QColor("#dddddd")
    core_style.matchedBraceBackground = QtGui.QColor("#B4EEB4")
    core_style.matchedBraceForeground = QtGui.QColor("#FF0000")
    code_edit.refresh_style()
