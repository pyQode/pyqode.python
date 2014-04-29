Add python support to pyQode
============================

.. image:: https://travis-ci.org/pyQode/pyqode.python.svg?branch=master
    :target: https://travis-ci.org/pyQode/pyqode.python
    :alt: Travis-CI build status

.. image:: http://img.shields.io/pypi/dm/pyqode.python.svg
    :target: https://pypi.python.org/pypi/pyqode.python/
    :alt: Number of PyPI downloads

.. image:: http://img.shields.io/pypi/v/pyqode.python.svg
    :target: https://pypi.python.org/pypi/pyqode.python/
    :alt: Latest PyPI version

What is pyqode.python?
----------------------

*pyqode.python* is an `official pyqode extension package`_ that adds **python**
support to `pyQode`_.

Features:
---------

  * calltips mode (using `Jedi`_)
  * code completion provider (using `Jedi`_)
  * code folding mode
  * auto indent mode
  * on the fly code checkers (frosted (fork of PyFlakes), PEP8)
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
 - frosted
 - docutils

Installation
------------

::

    $ pip3 install pyqode.python


Resources
---------

-  `Downloads`_
-  `Source repository`_
-  `Wiki`_
-  `Documentation`_

.. _Downloads: https://github.com/pyQode/pyqode.python/releases
.. _Source repository: https://github.com/pyQode/pyqode.python/
.. _Wiki: https://github.com/pyQode/pyqode.core/wiki


.. _official pyqode extension package: https://github.com/pyQode/pyqode.core/wiki/Extensions#official-packages
.. _pyQode: https://github.com/pyQode
.. _Jedi: https://github.com/davidhalter/jedi
.. _`Documentation`: http://pyqodepython.readthedocs.org/en/latest/
