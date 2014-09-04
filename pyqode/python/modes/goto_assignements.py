# -*- coding: utf-8 -*-
"""
Contains the go to assignments mode.
"""
import logging
import os
from pyqode.qt import QtCore, QtGui, QtWidgets
from pyqode.core.api import Mode, TextHelper, DelayJobRunner
from pyqode.core.backend import NotConnected
from pyqode.core.modes import WordClickMode
from pyqode.python.backend import workers


def _logger():
    return logging.getLogger(__name__)


class Assignment(object):
    """
    Assignment definition.
    """
    def __init__(self, path, line, column, full_name):
        #: Module path
        if path:
            path = path.replace(".pyc", ".py")
        self.module_path = path
        #: Line number
        self.line = line
        #: Column number
        self.column = column
        #: Assignement full name
        self.full_name = full_name

    def __str__(self):
        if self.line and self.column:
            return "%s (%s, %s)" % (self.full_name, self.line + 1,
                                    self.column + 1)
        return self.full_name

    def __repr__(self):
        return "Definition(%r, %r, %r, %r)" % (self.module_path, self.line,
                                               self.column, self.full_name)


class GoToAssignmentsMode(WordClickMode):
    """
    Goes to the assignments (using jedi.Script.goto_assignments). If there are
    more than one assignments, an input dialog is used to ask the user to
    choose the desired assignment.

    This mode will emit
    :attr:`pyqode.python.modes.GoToAssignmentsMode.out_of_doc` if the
    definition can not be reached in the current document. IDE will typically
    open a new editor tab and go to the definition.

    """
    #: Signal emitted when the definition cannot be reached in the current
    #: document
    out_of_doc = QtCore.Signal(Assignment)

    #: Signal emitted when no results could be found.
    no_results_found = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self._definitions = []
        self._goto_requested = False
        self.action_goto = QtWidgets.QAction("Go to assignments", self)
        self.action_goto.setShortcut("F2")
        self.action_goto.triggered.connect(self.request_goto)
        self.word_clicked.connect(self._on_word_clicked)
        self._runner = DelayJobRunner(delay=1)

    def on_state_changed(self, state):
        super().on_state_changed(state)
        if state:
            self.editor.add_action(self.action_goto)
        else:
            self.editor.remove_action(self.action_goto)

    def request_goto(self):
        """
        Request a goto action for the word under the text cursor.
        """
        self._goto_requested = True
        self._check_word_cursor()

    def _check_word_cursor(self, tc=None):
        """
        Request a go to assignment.

        :param tc: Text cursor which contains the text that we must look for
                   its assignment. Can be None to go to the text that is under
                   the text cursor.
        :type tc: QtGui.QTextCursor
        """
        if not tc:
            tc = TextHelper(self.editor).word_under_cursor()

        request_data = {
            'code': self.editor.toPlainText(),
            'line': tc.blockNumber(),
            'column': tc.columnNumber(),
            'path': self.editor.file.path,
            'encoding': self.editor.file.encoding
        }
        try:
            self.editor.backend.send_request(
                workers.goto_assignments, request_data,
                on_receive=self._on_results_available)
        except NotConnected:
            pass

    def _goto(self, definition):
        print('goto', definition.module_path, definition.line,
              definition.column)
        fp = ''
        if self.editor.file.path:
            fp = os.path.normpath(self.editor.file.path.replace(".pyc", ".py"))
        if definition.module_path == fp:
            line = definition.line
            col = definition.column
            _logger().debug("Go to %s" % definition)
            self._runner.request_job(
                TextHelper(self.editor).goto_line,
                line, move=True, column=col)
        else:
            _logger().debug("Out of doc: %s" % definition)
            self.out_of_doc.emit(definition)

    def _unique(self, seq):
        """
        Not performant but works.
        """
        # order preserving
        checked = []
        for e in seq:
            present = False
            for c in checked:
                if str(c) == str(e):
                    present = True
                    break
            if not present:
                checked.append(e)
        return checked

    def _clear_selection(self):
        super()._clear_selection()
        self._definitions[:] = []

    def _validate_definitions(self, definitions):
        if definitions:
            if len(definitions) == 1:
                return definitions[0].line is not None and \
                       definitions[0].module_path
            return True
        return False

    def _on_results_available(self, status, definitions):
        _logger().debug("Got %r" % definitions)
        definitions = [Assignment(path, line, col, full_name)
                       for path, line, col, full_name in definitions]
        definitions = self._unique(definitions)
        self._definitions = definitions
        if self._validate_definitions(definitions):
            if self._goto_requested:
                self._perform_goto(definitions)
            else:
                self._select_word_cursor()
                self.editor.set_mouse_cursor(QtCore.Qt.PointingHandCursor)
        else:
            self._clear_selection()
            self.editor.set_mouse_cursor(QtCore.Qt.IBeamCursor)
        self._goto_requested = False

    def _perform_goto(self, definitions):
        if len(definitions) == 1:
            definition = definitions[0]
            if definition:
                self._goto(definition)
        elif len(definitions) > 1:
            _logger().debug(
                "More than 1 assignments in different modules, user "
                "need to make a choice: %s" % definitions)
            def_str, result = QtWidgets.QInputDialog.getItem(
                self.editor, "Choose a definition",
                "Choose the definition you want to go to:",
                [str(d) for d in definitions])
            if result:
                for definition in definitions:
                    if definition and str(definition) == def_str:
                        self._goto(definition)
                        break

    def _on_word_clicked(self):
        self._perform_goto(self._definitions)
