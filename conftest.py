# -*- coding: utf-8 -*-
"""
This scripts configures the test suite. We do two things:

    - setup the logging module
    - create ONE SINGLE INSTANCE of QApplication:
      this implies that you must use **QApplication.instance** in your
      test scripts (or the app fixture).
"""
import logging
import sys
import pytest
from pyqode.qt.QtWidgets import QApplication


try:
    import faulthandler
    faulthandler.enable()
except ImportError:
    pass


# -------------------
# Setup logging
# -------------------
logging.basicConfig(level=logging.DEBUG,
                    filename='pytest.log',
                    filemode='w')

# -------------------
# Setup QApplication
# -------------------
# 2. create qt application
_app = QApplication(sys.argv)
_widget = None


# -------------------
# Session fixtures
# -------------------
@pytest.fixture(scope="session")
def app(request):
    global _app
    return app


@pytest.fixture()
def editor(request):
    global _app, _widget
    from pyqode.core import modes, cache
    from pyqode.python.widgets.code_edit import PyCodeEdit
    from pyqode.python.panels import SymbolBrowserPanel
    from pyqode.qt.QtTest import QTest

    cache.Cache().clear()

    _widget = PyCodeEdit()
    _widget.panels.append(SymbolBrowserPanel(),
                          SymbolBrowserPanel.Position.TOP)
    _widget.resize(800, 600)

    while not _widget.backend.connected:
        QTest.qWait(100)

    _widget.modes.get(modes.FileWatcherMode).file_watcher_auto_reload = True
    _widget.save_on_focus_out = False

    def fin():
        global _widget
        _widget.close()
        del _widget

    request.addfinalizer(fin)
    return _widget
