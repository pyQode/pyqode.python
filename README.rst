Add python support to pyQode
========================================

.. image:: https://travis-ci.org/ColinDuquesnoy/pyqode.python.png?branch=master
    :target: https://travis-ci.org/ColinDuquesnoy/pyqode.python
    :alt: Travis-CI build status

.. image:: https://pypip.in/d/pyqode.python/badge.png
    :target: https://crate.io/packages/pyqode.python/
    :alt: Number of PyPI downloads

.. image:: https://pypip.in/v/pyqode.python/badge.png
    :target: https://crate.io/packages/pyqode.python/
    :alt: Latest PyPI version

What is pyqode.python?
-----------------------

*pyqode.python* is an `official pyqode extension package`_ that adds **python** support to `pyQode`_.

Features:
------------

  * calltips mode (using `Jedi`_)
  * code completion provider (using `Jedi`_)
  * code folding mode
  * auto indent mode
  * on the fly code checkers (PyFlakes, PEP8)
  * a customisable python specific syntax highlighter
  * a pre-configured QPythonCodeEdit (with the corresponding Qt Designer plugin)

License
-------

pyQode is licensed under the MIT license.

Requirements
------------

pyqode.python depends on the following libraries:

 - pyqode.core
 - jedi
 - pep8
 - pyflakes

Installation
------------

::

    $ pip install pyqode.python

Usage
-----

The *public API* is exposed by the *pyqode.python* package.

Here is a simple example using PyQt4:

.. code:: python

    # simple example using PyQt4
    import sys
    import PyQt4  # just to tell pyqode we want to use PyQt4.
    import pyqode.python
    from PyQt4.QtGui import QApplication


    def main():
        app = QApplication(sys.argv)
        editor = pyqode.python.QPythonCodeEdit()
        editor.openFile(__file__)
        editor.resize(800, 600)
        editor.show()
        return app.exec_()


    if __name__ == "__main__":
        sys.exit(main())


Resources
---------

-  `Downloads`_
-  `Source repository`_
-  `Wiki`_
-  `Documentation`_

.. _Downloads: https://github.com/ColinDuquesnoy/pyqode.python/releases
.. _Source repository: https://github.com/ColinDuquesnoy/pyqode.python/
.. _Wiki: https://github.com/ColinDuquesnoy/pyqode.core/wiki


.. _official pyqode extension package: https://github.com/ColinDuquesnoy/pyqode.core/wiki/Extensions#official-packages
.. _pyQode: https://github.com/ColinDuquesnoy/pyqode.python
.. _Jedi: https://github.com/davidhalter/jedi
.. _`Documentation`: http://pyqodepython.readthedocs.org/en/latest/


Changelog
--------------

1.1:
***********

    * **New**: add the following new modes:
    
        - pyqode.python.PyAutoCompleteMode
        
        - pyqode.python.CommentsMode
        
        - pyqode.python.DocumentAnalyserModeµ

        - pyqode.python.GoToAssignmentsMode

    * **New**: add the following new panels:
    
        - pyqode.python.QuickDocPanel
        
        - pyqode.python.SymbolBrowserPanel

    * **New**: CodeCompletion: provides method to interact with the subprocess interpreter

    * **New**: Add CodeCompletion preload hooks

    * **New**: Add pyqode.python.Boostrapper class to help start the code completion with a list of modules to preload + example with a splash screen.

    * **Fix**: Disable actions which depends on preload

    * **Fix**: Disable code completion in commente and strings

    * **Fix**: Better highlighting in docstrings (highlighting was lost when there was an ‘=’ in the docstring.

1.0:
***********

    Final 1.0 release, add documentation

1.0b3:
**********

    * fix syntax highlighting bugs with triple quoted string inside comment or
      string literals

    * fix bugs with designer plugins

    * update code completion provider to use jedi 0.7

    * many other bug fixes

1.0b2:
************

    * fix code completion icons path

1.0b:
************

    First beta version


Screenshots
-------------

Here are a few screenshots to illustrate the python specific features *(all the screenshots were taken on Linux Mint 15 Cinnamon)*:

* Code completion:

.. image:: https://raw.github.com/ColinDuquesnoy/pyqode.python/master/screenshots/code_completion.png
    :alt: Code completion
    
* Code folding:

.. image:: https://raw.github.com/ColinDuquesnoy/pyqode.python/master/screenshots/code_folding.png
    :alt: Code Folding
    
* On the fly code checking (PyFlakes):

.. image:: https://raw.github.com/ColinDuquesnoy/pyqode.python/master/screenshots/error_indicators.png
    :alt: Error indicators
    
* On the fly PEP8 style checking

.. image:: https://raw.github.com/ColinDuquesnoy/pyqode.python/master/screenshots/pep8_warnings.png
    :alt: PEP8 warnings

* Dark color scheme

.. image:: https://raw.github.com/ColinDuquesnoy/pyqode.python/master/screenshots/dark_style.png
    :alt: Dark style


.. image:: https://d2weczhvl823v0.cloudfront.net/ColinDuquesnoy/pyqode.python/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free

