Changelog
=========

2.11.1
------

Try again to switch to pycodestyle.

2.11.0
------

Switch from pep8 to pycodestyle.

2.10.2
------

pyQode now works with jedi versions > 0.10; older versions are no longer supported.

2.10.1
------

Remove smart backspace and indenter mode from PyConsole so that the behaviour is closer to
what you'd have when running python in a terminal.

2.10.0
------

New features:

- add an interactive python console widget

2.9.0
-----

New features:

- use margin position in linter to define pep8.MAX_LINE_LENGTH

2.8.0
-----

Fixed bugs:

- fix IndexError in calltips if cursor at the beginning of the last (empty) line

2.7.0
-----

Fixed bugs:
    - PyInteractiveConsole: fix regex if path contains a '-' (e.g. "/usr/.../dist-packages/module.py")
    - PyInteractiveConsole: make sure to set QT_LOGGING_TO_CONSOLE otherwise
      the traceback does not show up with PyQt >= 5.5
    - PyCommentMode: fix preserve selection if multiple lines were selected
    - SH: Fix import builtins not working with python 2.7 on OSX
    - fix many potential memory leaks by breaking the circular dependencies
      correctly before removing a mode/panel
2.6.3
-----
New features:
    - add a freeze script that works with pyside to the pynotepad example

Fixed bugs:
    - ignore PEP8 warnings: 'W291', 'W292', 'W293', 'W391'.
      Those warnings are meaningless since pyqode will now clean trailing white spaces and ensure a single unique
      blank line at the end of the file when it saves content to disk.

2.6.2
-----

Improve linux icon theme integration (will use code-xxx icons for code
completion icons and outline widget)

Fix a few issues in the pynotepad example and add a freeze_setup that works
with python3 and PyQt5 (but not yet with python2 and PySide).

2.6.1
-----
New features/improvements:
    - improve syntax highlighter: ['and', 'or', 'not', 'in', 'is'] and ['from', 'import', 'as']
      the results are closer to what you can get with the pygments lexer

Fixed bugs:
    - fix another corner case with auto indent

2.6.0
-----

New features:
    - Switch from Frosted to PyFlakes
    - Wheel support

Fixed bugs:
    - Fix unimplemented code completion icon types (Jedi 0.9)
    - Improve calltips behaviour
    - Fix custom editor example
    - PyInteractiveConsole: fix traceback regex to work with dotted package
      names (e.g. pyqode.core directory name when installed in development
      mode)
    - Fix a couple of corner cases in autoindent mode
    - Fix quick doc panel colors on Ubuntu

2.5.0
-----

New features:
    - Unified API for document outline (see pyQode/pyQode#24)

Fixed bugs:
    - fix a bug with interpreter selection in the pynotepad example (see pyQode/pyQode#25)

2.4.2
-----

Fixed bugs:

- fix an issue with newest version of pep8.py

2.4.1
-----

New features:

- implement pyQode/pyQode#21
- add CaseConverterMode to PyCodeEdit

Fixed bugs:

- fix buffering issue with PyInteractiveConsole, now ``PYTHONBUFFERED`` is always set to 1.
- fix auto-indent bug: if a parentheses is closed but the cursor if after a "," and just before ")"
  indentation was not right. The solution is to check for ',' and ignore whitespaces before the
  previous character.


2.4.0
-----

New features:

- add outline tree view
- improvements to the syntax highlighter: make use of the new formats types
- add more examples

Fixed bugs:

- fix default encoding on windows
- fix lost of selection after unindent
- fix file path regex for exception traceback highlighting in the python
  interactive console
- fix some bugs with pyside
- fix some bugs with python 2
- fix some bugs with auto indent mode
- fix some bugs with auto completes of triple quotes (both single and double
  quotes)


2.3.0
-----

New features:
    - add support for python2. You may now use python2 for writing a pyqode
      app (backend AND frontend)!
    - make use of the new modes introduced in pyqode.core (occurrences
      highlighter, extended selection, global checker panel,...)
    - automatically fold docstring when opening a document
    - many improvements to the auto indent mode. It is more robust and should
      resists malformed code (e.g. unclosed parentheses,...)

Fixed bugs:
    - fix cursor position after unindent
    - fix a few bugs with autoindent
    - fix pyinteractive console colors on dark color schemes


2.2.0
-----

New features:
    - automatically fold import statements when opening document
    - improved GoToAssignment mode (now highlighting word only if a jump is
      possible)
    - SH: highlight cls pseudo keyword
    - SH: highlight builtin methods (__init__, __call__, __add__,...)
    - add support for auto completion of classmethods
    - improve defined_names worker to work recursively (now able to catch
      nested classes)

Fixed bugs:
    - fix confusing convention: now both line numbers and column numbers starts
      from 0
    - fix editor not having focus when clicking on an item in the symbol
      browser panel
    - fix regex in PyInteractiveConsole
    - fix performance issue with import region folding
    - fix performance issue with docstring folding
    - fix performance issue with auto indent
    - fix code completion tooltip: use description instead of full name
    - fix highlighting of commented docstrings

2.1.0
-----

New features:
  - code folding (with support for folding docstrings and imports)
  - new python syntax highlighter (based on the Spyder IDE PythonSH) with
    additional support for docstrings, decorators and self parameter.
    The new highlighter is a lot faster than the previous one and has a better
    docstring highlighting.
  - new PyInteractiveConsole for running python program. The new console has
    support for highlighting tracebakc and let you jump to the incriminated
    file with just one click.

Bug fixed:
  - many bugs have been fixed in the auto indent mode
  - many small bugs have been fixed in pynotepad
  - fix cursor position after comment/uncomment (Ctrl+/)

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

      - PyAutoCompleteMode
      - CommentsMode
      - DocumentAnalyserMode
      - GoToAssignmentsMode
    - add the following new panels:

      - QuickDocPanel
      - SymbolBrowserPanel
    - CodeCompletion: provides method to interact with the subprocess interpreter
    - CodeCompletion: preload hooks
    - Add `Boostrapper` class to help start the code completion with a list of modules to
      preload + example with a splash screen.

Fixed bugs:
    - Disable actions which depends on preload
    - Disable code completion in commente and strings
    - Fix highlighting in docstrings (highlighting was lost when there was an '=' in the docstring.

1.0.0
-----

Initial development.
