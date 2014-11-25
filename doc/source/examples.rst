Examples
========
If you downloaded a source archive or cloned pyQode from github, you will find a
series of examples in the ``examples`` directory, at the root of the archive.

All examples requires ``pyqode.qt``, ``pyqode.core`` and
``pyqode.python`` to be installed.

.. note:: All examples are bindings independent so that every user can run them
          without being required to install an unwanted qt binding.

.. highlight:: python
   :linenothreshold: 5

Pre-configured
--------------

Basic example that show you how to use the pre-configured python code editor
widget.

.. literalinclude:: /../../examples/preconfigured.py
   :linenos:

Custom
------

Basic example that show you how to build a custom python code editor widget

.. literalinclude:: /../../examples/custom.py
   :linenos:

Modes
-----

Auto complete
+++++++++++++

.. literalinclude:: /../../examples/modes/autocomplete.py
   :linenos:

Auto indent
+++++++++++

.. literalinclude:: /../../examples/modes/autoindent.py
   :linenos:

Call tips
+++++++++

.. literalinclude:: /../../examples/modes/calltips.py
   :linenos:

Comment/Uncomment
+++++++++++++++++

.. literalinclude:: /../../examples/modes/comments.py
   :linenos:

Go to assignment
++++++++++++++++

.. literalinclude:: /../../examples/modes/goto.py
   :linenos:

PEP8 linter
+++++++++++

.. literalinclude:: /../../examples/modes/pep8.py
   :linenos:

PyFlakes linter
+++++++++++++++

.. literalinclude:: /../../examples/modes/pyflakes.py
   :linenos:

Syntax highlighter
++++++++++++++++++

.. literalinclude:: /../../examples/modes/syntax_highlighter.py
   :linenos:


Panels
------

Documentation
+++++++++++++

.. literalinclude:: /../../examples/panels/quick_doc.py
   :linenos:

Symbol browser
++++++++++++++

.. literalinclude:: /../../examples/panels/symbol_browser.py
   :linenos:

Widgets
-------

Interactive console
+++++++++++++++++++

.. literalinclude:: /../../examples/widgets/interactive_console.py
   :linenos:

.. literalinclude:: /../../examples/widgets/interactive_process.py
   :linenos:

Outline
+++++++

.. literalinclude:: /../../examples/widgets/outline.py
   :linenos:

PyNotepad
---------

This example is a complete but minimal python code editor application.
It is too large to be included here but you should really have a look at it as
this example combines nearly all the concepts exposed by pyqode.python.
