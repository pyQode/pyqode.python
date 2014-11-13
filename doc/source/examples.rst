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

PyNotepad
---------

This example is a complete but minimal python code editor application.
It is too large to be included here but you should really have a look at it as
this example combines nearly all the concepts exposed by pyqode.python.
