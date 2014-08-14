"""
This module contains the Interactive python console, for running python
programs.
"""
from pyqode.qt import QtCore, QtGui, QtWidgets
from pyqode.core.widgets import InteractiveConsole


class PyInteractiveConsole(InteractiveConsole):
    """
    Extends the InteractiveConcole to highlight python traceback. If the user
    press on a filename in a traceback, the signal open_file_requested is
    emitted with the file path to open and the line where the user want to go.

    """
    #: Signal emitted when the user pressed on a traceback file location.
    #: Client code should open the requested file in the editor.
    open_file_requested = QtCore.Signal(str, int)

    class UserData(QtGui.QTextBlockUserData):
        def __init__(self, filename, line, start, end):
            super().__init__()
            self.filename = filename
            self.line = line
            self.start_pos_in_block = start
            self.end_pos_in_block = end
            self.PROG = QtCore.QRegExp(
                r'\s*File "[a-zA-Z\/_]*((.\.[a-z]*")|(")), line [0-9]*.*')
            self.FILENAME_PROG = QtCore.QRegExp(r'"[a-zA-Z\/_\.]*"')
            self.LINE_PROG = QtCore.QRegExp(r'line [0-9]*')

    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_writer(self._write)
        self.setMouseTracking(True)

    def _write(self, text_edit, text, color):
        def write(text_edit, text, color):
            text_edit.moveCursor(QtGui.QTextCursor.End)
            fmt = QtGui.QTextCharFormat()
            fmt.setUnderlineStyle(QtGui.QTextCharFormat.NoUnderline)
            fmt.setForeground(QtGui.QBrush(color))
            text_edit.setCurrentCharFormat(fmt)
            text_edit.insertPlainText(text)
            text_edit.moveCursor(QtGui.QTextCursor.End)

        def write_with_underline(text_edit, text, color, line, start, end):
            text_edit.moveCursor(QtGui.QTextCursor.End)
            text_edit.setTextColor(color)
            fmt = QtGui.QTextCharFormat()
            fmt.setUnderlineColor(color)
            fmt.setUnderlineStyle(QtGui.QTextCharFormat.SingleUnderline)
            fmt.setForeground(QtGui.QBrush(color))
            text_edit.setCurrentCharFormat(fmt)
            text_edit.insertPlainText(text)
            text_edit.moveCursor(QtGui.QTextCursor.End)
            block = self.document().lastBlock()
            data = self.UserData(text, line, start, end)
            block.setUserData(data)

        for line in text.splitlines():
            if color == self.stderr_color:
                # check if File and highlight it in blue, also store it
                if self.PROG.indexIn(line) != -1:
                    # get line number
                    self.LINE_PROG.indexIn(line)
                    start = self.LINE_PROG.pos(0)
                    end = start + len(self.LINE_PROG.cap(0))
                    l = int(line[start:end].replace('line ', ''))

                    self.FILENAME_PROG.indexIn(line)
                    start = self.FILENAME_PROG.pos(0)
                    end = start + len(self.FILENAME_PROG.cap(0))
                    write(self, line[:start + 1], color)
                    write_with_underline(self, line[start + 1:end - 1],
                                         QtGui.QColor('blue'), l,
                                         start, end)
                    write(self, line[end - 1:] + '\n', color)
                    continue
            write(text_edit, line + '\n', color)

    def mouseMoveEvent(self, e):
        """
        Extends mouseMoveEvent to display a pointing hand cursor when the
        mouse cursor is over a file location
        """
        super().mouseMoveEvent(e)
        cursor = self.cursorForPosition(e.pos())
        assert isinstance(cursor, QtGui.QTextCursor)
        p = cursor.positionInBlock()
        usd = cursor.block().userData()
        if usd and usd.start_pos_in_block <= p <= usd.end_pos_in_block:
            if QtWidgets.QApplication.overrideCursor() is None:
                QtWidgets.QApplication.setOverrideCursor(
                    QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        else:
            if QtWidgets.QApplication.overrideCursor() is not None:
                QtWidgets.QApplication.restoreOverrideCursor()

    def mousePressEvent(self, e):
        """
        Emits open_file_requested if the press event occured  over
        a file location string.
        """
        super().mousePressEvent(e)
        cursor = self.cursorForPosition(e.pos())
        p = cursor.positionInBlock()
        usd = cursor.block().userData()
        if usd and usd.start_pos_in_block <= p <= usd.end_pos_in_block:
            if e.button() == QtCore.Qt.LeftButton:
                self.open_file_requested.emit(usd.filename, usd.line)

    def leaveEvent(self, e):
        super().leaveEvent(e)
        if QtWidgets.QApplication.overrideCursor() is not None:
            QtWidgets.QApplication.restoreOverrideCursor()
