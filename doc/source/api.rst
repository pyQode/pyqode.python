API Reference
======================

The API reference documentation is auto extracted from the source code and only
cover the public API exposed by the **pyqode.python** package.

.. contents:: :local:

QPythonCodeEdit
--------------------

.. autoclass:: pyqode.python.QPythonCodeEdit
    :members:

    .. automethod:: pyqode.python.QPythonCodeEdit.useDarkStyle

        Changes the editor style to a dark color scheme similar to pycharm's
        darcula color scheme.

    .. automethod:: pyqode.python.QPythonCodeEdit.useLightStyle

        Changes the editor style to a dark color scheme similar to QtCreator's
        default color scheme.

Bootstrapper
-------------------

.. autoclass:: pyqode.python.Bootstrapper
    :members:

Modes
-----------

AutoCompleteMode
+++++++++++++++++++

.. autoclass:: pyqode.python.PyAutoCompleteMode
    :members:

CalltipsMode
++++++++++++++++

.. autoclass:: pyqode.python.CalltipsMode
    :members:

CommentsMode
++++++++++++++++

.. autoclass:: pyqode.python.CommentsMode
    :members:

DocumentAnalyser
+++++++++++++++++++++++++

Definition
**************

.. autoclass:: pyqode.python.modes.document_analyser.Definition
    :members:

DocumentAnalyserMode
************************
.. autoclass:: pyqode.python.DocumentAnalyserMode
    :members:

GoToAssignmentsMode
+++++++++++++++++++

Assignment
**************
.. autoclass:: pyqode.python.modes.goto_assignements.Assignment
    :members:

GoToAssignmentsMode
*********************
.. autoclass:: pyqode.python.GoToAssignmentsMode
    :members:

JediCompletionProvider
+++++++++++++++++++++++++

.. autoclass:: pyqode.python.JediCompletionProvider
    :members:

PEP8CheckerMode
++++++++++++++++++

.. autoclass:: pyqode.python.PEP8CheckerMode
    :members:

PyAutoIndentMode
+++++++++++++++++

.. autoclass:: pyqode.python.PyAutoIndentMode
    :members:

PyFlakesCheckerMode
+++++++++++++++++++++

.. autoclass:: pyqode.python.PyFlakesCheckerMode
    :members:

PyHighlighterMode
++++++++++++++++++++++

.. autoclass:: pyqode.python.PyHighlighterMode
    :members:

.. autoattribute:: pyqode.python.DEFAULT_LIGHT_STYLES

    Default (white) color scheme for :class:`pyqode.python.PyHighlighterMode`
    Those values are added to :attr:`pyqode.core.QCodeEdit.style` properties in
    the *Python* section:

    .. code-block:: python

         {'keyword': TextStyle('#808000 nbold nitalic nunderlined'),
         'builtins': TextStyle('#808000 nbold nitalic nunderlined'),
         'operator': TextStyle('darkGray nbold nitalic nunderlined'),
         'punctuation': TextStyle('darkGray nbold nitalic nunderlined'),
         'decorator': TextStyle('#808000 nbold nitalic nunderlined'),
         'brace': TextStyle('#404040 nbold nitalic nunderlined'),
         'class': TextStyle('#800080 nbold nitalic nunderlined'),
         'function': TextStyle('#800080 nbold nitalic nunderlined'),
         'string': TextStyle('#008000 nbold nitalic nunderlined'),
         'docstring': TextStyle('#0000AA nbold nitalic nunderlined'),
         'comment': TextStyle('#008000 nbold italic nunderlined'),
         'self': TextStyle('#8F2828 nbold italic nunderlined'),
         'numbers': TextStyle('#000080 nbold nitalic nunderlined'),
         'predefined': TextStyle('#B200B2 nbold nitalic nunderlined'),
         'docstringTag': TextStyle('#0000FF nbold nitalic underlined'),}


.. autoattribute:: pyqode.python.DEFAULT_DARK_STYLES


    Alternative dark color scheme for :class:`pyqode.python.PyHighlighterMode`
    Those values are added to :attr:`pyqode.core.QCodeEdit.style` properties in
    the *Python* section:

    .. code-block:: python

        {'keyword': TextStyle('#CC7832 bold nitalic nunderlined'),
        'builtins': TextStyle('#CC7832 nbold nitalic nunderlined'),
        'operator': TextStyle('#A9B7C6 nbold nitalic nunderlined'),
        'punctuation': TextStyle('#A9B7C6 nbold nitalic nunderlined'),
        'decorator': TextStyle('#BBB529 nbold nitalic nunderlined'),
        'brace': TextStyle('#AAAAAA nbold nitalic nunderlined'),
        'class': TextStyle('#A9B7C6 bold nitalic nunderlined'),
        'function': TextStyle('#A9B7C6 bold nitalic nunderlined'),
        'string': TextStyle('#A5C261 nbold nitalic nunderlined'),
        'docstring': TextStyle('#629755 nbold nitalic nunderlined'),
        'comment': TextStyle('#808080 nbold italic nunderlined'),
        'self': TextStyle('#94558D nbold italic nunderlined'),
        'numbers': TextStyle('#6897B3 nbold nitalic nunderlined'),
        'predefined': TextStyle('#B200B2 nbold nitalic nunderlined'),
        'docstringTag': TextStyle('#427735 bold nitalic underlined'),}


PyIndenterMode
++++++++++++++++++++++

.. autoclass:: pyqode.python.PyIndenterMode
    :members:

Panels
--------------

PreLoadPanel
+++++++++++++
.. autoclass:: pyqode.python.PreLoadPanel
    :members:

SymbolBrowserPanel
+++++++++++++++++++++++

.. autoclass:: pyqode.python.SymbolBrowserPanel
    :members:

QuickDocPanel
+++++++++++++++
.. autoclass:: pyqode.python.QuickDocPanel
    :members:

Utilities
--------------

.. autofunction:: pyqode.python.setDarkColorScheme
.. autofunction:: pyqode.python.setLightColorScheme
