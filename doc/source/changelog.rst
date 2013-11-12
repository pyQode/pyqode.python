Change Log
===========

.. note::

    These lists are not exhaustive.

1.1
-----------

New features:
    - add the following new modes:
        - :class:`pyqode.python.PyAutoCompleteMode`
        - :class:`pyqode.python.CommentsMode`
        - :class:`pyqode.python.DocumentAnalyserMode`
        - :class:`pyqode.python.GoToAssignmentsMode`
    - add the following new panels:
        - :class:`pyqode.python.QuickDocPanel`
        - :class:`pyqode.python.SymbolBrowserPanel`
    - CodeCompletion: provides method to interact with the subprocess interpreter
    - CodeCompletion: preload hooks
    - Add :class:`pyqode.python.Boostrapper` class to help start the code completion with a list of modules to
      preload + example with a splash screen.

Bug fixed:
    - Disable actions which depends on preload
    - Disable code completion in commente and strings
    - Fix highlighting in docstrings (highlighting was lost when there was an '=' in the docstring.

1.0
----------

Initial development.