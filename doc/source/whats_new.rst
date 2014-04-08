What's New?
===========
This page lists the most prominent milestones achieved by the pyQode
developers. For more specific details about what is planned and what has been 
accomplished, please visit the `issues page on github`_ and the
:doc:`changelog </changelog>`, respectively.


Milestones
----------

1.3.1
+++++

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
+++++

Bug fixes release:
    - more fixes to auto completion
    - fixes for auto indentation mode
    - fix type error in document layout parser.
    - fix call-tips when there is a closing parenthesis


1.2.0
+++++

Bug fixes release:

    - Fix a few bugs with auto complete
    - Fix bugs with code completion in comments and strings
    - Fix for designer plugin


1.1.0
+++++

    Add many new modes and panels and improve the user experience by adding more utility
    methods and class.

1.0.0
+++++

    Initial development of pyqode.python, based on the python features of
    pcef (the old pyqode library).


.. _`jedi`: https://github.com/davidhalter/jedi
.. _`issues page on github`: https://github.com/pyQode/pyqode.python