# -*- coding: utf-8 -*-
"""
A helper module for testing, introducing some helper functions. Inspired by
the jedi helper module for their testing package
"""
import os
import functools
import platform
import sys
from os.path import abspath
from os.path import dirname

from pyqode.qt.QtTest import QTest

from pyqode.core import actions
from pyqode.core import frontend
from pyqode.core import style
from pyqode.core import settings
from pyqode.core import frontend
from pyqode.core.frontend import modes
from pyqode.core.frontend import panels
from pyqode.python.frontend import open_file


test_dir = dirname(abspath(__file__))


# -------------------
# Decorators
# -------------------
def cwd_at(path):
    """
    Decorator to run function at `path`.

    :type path: str
    :arg path: relative path from repository root (e.g., 'pyqode' or 'test').
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwds):
            try:
                oldcwd = os.getcwd()
                repo_root = os.path.dirname(test_dir)
                os.chdir(os.path.join(repo_root, path))
                return func(*args, **kwds)
            finally:
                os.chdir(oldcwd)
        return wrapper
    return decorator


def editor_open(path):
    if not os.path.exists(path):
        try:
            with open(path, 'w') as dst:
                with open(__file__, 'r') as src:
                    dst.write(src.read())
        except OSError:
            pass

    def decorator(func):
        @functools.wraps(func)
        def wrapper(editor, *args, **kwds):
            open_file(editor, path)
            return func(editor, *args, **kwds)
        return wrapper
    return decorator


def preserve_settings(func):
    @functools.wraps(func)
    def wrapper(editor, *args, **kwds):
        dic = dict(settings.__dict__)
        try:
            ret = func(editor, *args, **kwds)
        finally:
            for k, v in dic.items():
                if k.startswith('_'):
                    continue
                setattr(settings, k, v)
            editor.refresh_settings()
        return ret
    return wrapper


def preserve_style(func):
    @functools.wraps(func)
    def wrapper(editor, *args, **kwds):
        dic = dict(style.__dict__)
        ret = None
        try:
            ret = func(editor, *args, **kwds)
        finally:
            print('Restoring default style')
            for k, v in dic.items():
                if k.startswith('_'):
                    continue
                print('STYLE', k, v)
                setattr(style, k, v)
                print('STYLE VAL:', k, getattr(style, k))
            editor.refresh_style()
            QTest.qWait(100)
        return ret
    return wrapper


def preserve_actions(func):
    @functools.wraps(func)
    def wrapper(editor, *args, **kwds):
        dic = dict(actions.__dict__)
        ret = None
        try:
            ret = func(editor, *args, **kwds)
        finally:
            for k, v in dic.items():
                if k.startswith('_'):
                    continue
                setattr(actions, k, v)
            editor.refresh_actions()
        return ret
    return wrapper


def preserve_editor_config(func):
    @functools.wraps(func)
    def wrapper(editor, *args, **kwds):
        ret = None
        try:
            ret = func(editor, *args, **kwds)
        finally:
            frontend.uninstall_all(editor)
            setup_editor(editor)
            if not frontend.connected_to_server(editor):
                frontend.start_server(editor, server_path())
                wait_for_connected(editor)
        return ret
    return wrapper


def preserve_visiblity(func):
    # todo: decorator to preserve editor visibility
    pass


def require_python2():
    """
    Skips the test if there is no python2 interpreter.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwds):
            if os.path.exists(python2_path()):
                return func(*args, **kwds)
        return wrapper
    return decorator


def log_test_name(func):
    @functools.wraps(func)
    def wrapper(*args, **kwds):
        import logging
        logging.info('---------------- %s ----------------' % func.__name__)
        return func(*args, **kwds)
    return wrapper



# -------------------
# Helper functions
# -------------------
def wait_for_connected(editor):
    while not frontend.connected_to_server(editor):
        QTest.qWait(100)


def python2_path():
    """
    Returns the path to the python2 interpreter.

    The expected python2 path is '/usr/bin/python' on Linux and
    'c:\Python27\python.exe' on Windows.
    """
    return '/usr/bin/python' if platform.system() == 'Linux' else \
        'c:\\Python27\\python.exe'


def server_path():
    return os.path.join(os.path.dirname(__file__), 'server.py')


def setup_editor(code_edit):
    from pyqode.python.frontend import modes as pymodes
    from pyqode.python.frontend import panels as pypanels

    # add panels
    frontend.install_mode(code_edit, pymodes.DocumentAnalyserMode())

    # panels
    frontend.install_panel(code_edit, panels.LineNumberPanel())
    frontend.install_panel(code_edit, panels.MarkerPanel())
    frontend.install_panel(code_edit, panels.SearchAndReplacePanel(),
                           panels.SearchAndReplacePanel.Position.BOTTOM)
    frontend.install_panel(code_edit, pypanels.SymbolBrowserPanel(),
                           pypanels.SymbolBrowserPanel.Position.TOP)

    # modes
    # generic
    frontend.install_mode(code_edit, modes.CaretLineHighlighterMode())
    frontend.install_mode(code_edit, modes.FileWatcherMode())
    frontend.install_mode(code_edit, modes.RightMarginMode())
    frontend.install_mode(code_edit, modes.ZoomMode())
    frontend.install_mode(code_edit, modes.SymbolMatcherMode())
    frontend.install_mode(code_edit, modes.WordClickMode())
    frontend.install_mode(code_edit, modes.CodeCompletionMode())
    # python specifics
    frontend.install_mode(code_edit, pymodes.PyHighlighterMode(code_edit.document()))
    frontend.install_mode(code_edit, pymodes.PyAutoCompleteMode())
    frontend.install_mode(code_edit, pymodes.PyAutoIndentMode())
    frontend.install_mode(code_edit, pymodes.FrostedCheckerMode())
    frontend.install_mode(code_edit, pymodes.PEP8CheckerMode())
    frontend.install_mode(code_edit, pymodes.CalltipsMode())
    frontend.install_mode(code_edit, pymodes.PyIndenterMode())
    frontend.install_mode(code_edit, pymodes.GoToAssignmentsMode())
    frontend.install_panel(code_edit, pypanels.QuickDocPanel(),
                           frontend.Panel.Position.BOTTOM)
    frontend.install_mode(code_edit, pymodes.CommentsMode())
