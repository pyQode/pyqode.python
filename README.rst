Python extensions for PCEF
========================================

*version 1.0.0-beta.1*

.. image:: https://travis-ci.org/ColinDuquesnoy/pcef-python.png?branch=master
    :target: https://travis-ci.org/ColinDuquesnoy/pcef-python
    :alt: Travis-CI build status

What is pcef-python?
-----------------------

*pcef-python* is an `official pcef extension package`_ that adds **python** support to `PCEF`_.

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

PCEF is licensed under the LGPL v3.

Requirements
------------

pcef-python depends on the following libraries:

 - pcef-core
 - jedi
 - pep8
 - pyflakes

Installation
------------

::

    $ pip install pcef-python

Usage
-----

The *public API* is exposed by the *pcef.python* package.

Here is a simple example using PyQt4:

.. code:: python

    # simple example using PyQt4
    import sys
    import PyQt4  # just to tell pcef we want to use PyQt4.
    import pcef.python
    from PyQt4.QtGui import QApplication


    def main():
        app = QApplication(sys.argv)
        editor = pcef.python.QPythonCodeEdit()
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

.. _Downloads: https://github.com/ColinDuquesnoy/pcef-python/releases
.. _Source repository: https://github.com/ColinDuquesnoy/pcef-python/
.. _Wiki: https://github.com/ColinDuquesnoy/pcef-core/wiki


.. _official pcef extension package: https://github.com/ColinDuquesnoy/pcef-core/wiki/Extensions#official-packages
.. _PCEF: https://github.com/ColinDuquesnoy/pcef-core
.. _Jedi: https://github.com/davidhalter/jedi


Screenshots
-------------

Here are a few screenshots to illustrate the python specific features *(all the screenshots were taken on Linux Mint 15 Cinnamon)*:

* Code completion:

.. image:: https://raw.github.com/ColinDuquesnoy/pcef-python/master/screenshots/code_completion.png
    :alt: Code completion
    
* Code folding:

.. image:: https://raw.github.com/ColinDuquesnoy/pcef-python/master/screenshots/code_folding.png
    :alt: Code Folding
    
* On the fly code checking (PyFlakes):

.. image:: https://raw.github.com/ColinDuquesnoy/pcef-python/master/screenshots/error_indicators.png
    :alt: Error indicators
    
* On the fly PEP8 style checking

.. image:: https://raw.github.com/ColinDuquesnoy/pcef-python/master/screenshots/pep8_warnings.png
    :alt: PEP8 warnings
