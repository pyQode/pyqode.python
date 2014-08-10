# -*- coding: utf-8 -*-
"""
This packages contains the python specific panels:

    - QuickDocPanel: show docstring of functions/classes.
    - SymbolBrowserPanel: combo box that shows the symbols
      in the current document.

"""
from pyqode.python.panels.symbol_browser import SymbolBrowserPanel
from pyqode.python.panels.quick_doc import QuickDocPanel

__all__ = [
    'SymbolBrowserPanel',
    'QuickDocPanel',
]
