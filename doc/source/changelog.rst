Change Log
==========

.. note::

    These lists are not exhaustive.

2.0.0
-----

Too many things have change since 1.3.2 as the API has undergone some heavy
refactoring.

1.3.2
-----

New features:
    - add support for jedi 0.8 final which bring several minor enhancements

Fixed bugs:
    - fix a bug with boostrap.py

1.3.1
-----

New features:

    - the comments mode is now PEP8 compliant
    - the documentation panel now uses docutils to get an html representation
      of docstrings
    - QPythonCodeEdit now includes the file watcher mode
    - lots of improvements to the auto indent mode

Fixed bugs:

    - Add support for jedi 0.8 (which has not been released yet, compatibility
      with jedi 0.7 has been kept)
    - many bug fixes to the auto indent mode


1.3.0
-----

Fixed bugs:

    - more fixes to auto completion
    - fixes for auto indentation mode
    - fix type error in document layout parser.
    - Fix calltips when there is a closing parenthesis


1.2.0
-----

Fixed bugs:

    - Fix various bugs with auto complete
    - Fix bugs with code completion in comments and strings
    - Fix for designer plugin

1.1.0
-----

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

Fixed bugs:
    - Disable actions which depends on preload
    - Disable code completion in commente and strings
    - Fix highlighting in docstrings (highlighting was lost when there was an '=' in the docstring.

1.0.0
-----

Initial development.