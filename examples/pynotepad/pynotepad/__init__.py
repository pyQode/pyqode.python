"""
This package contains the code of the notepad application:

    - editor: contains our custom CodeEdit class definition. This is just
    a CodeEdit configured with a set of modes and panels.

    - main_window: This is the main window of the application

    - server.py: This is the server script for the pyqode backend.
"""
import sys
from pyqode.qt.QtWidgets import QApplication
from .main_window import MainWindow
from .settings import Settings


__version__ = '1.1.0'


def main():
    if hasattr(sys, 'frozen'):
        sys.stdout = open('pynotepad_stdout.txt', 'w')
        sys.stderr = open('pynotepad_stderr.txt', 'w')
    app = QApplication(sys.argv)
    if not Settings().interpreter:
        Settings().interpreter = sys.executable
    win = MainWindow()
    win.show()
    app.exec_()
