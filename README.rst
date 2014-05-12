Add python support to pyQode
============================

Status
------

Package:
++++++++


.. image:: http://img.shields.io/pypi/v/pyqode.python.png
    :target: https://pypi.python.org/pypi/pyqode.python/
    :alt: Latest PyPI version

.. image:: http://img.shields.io/pypi/dm/pyqode.python.png
    :target: https://pypi.python.org/pypi/pyqode.python/
    :alt: Number of PyPI downloads


Stable (`master`_):
+++++++++++++++++++

.. image:: https://travis-ci.org/pyQode/pyqode.python.svg?branch=master
    :target: https://travis-ci.org/pyQode/pyqode.python
    :alt: Travis-CI build status

.. image:: https://coveralls.io/repos/pyQode/pyqode.python/badge.png?branch=master
    :target: https://coveralls.io/r/pyQode/pyqode.python?branch=master
    :alt: Coverage Status

Unstable (`develop`_):
++++++++++++++++++++++

.. image:: https://travis-ci.org/pyQode/pyqode.python.svg?branch=develop
    :target: https://travis-ci.org/pyQode/pyqode.python
    :alt: Travis-CI build status

.. image:: https://coveralls.io/repos/pyQode/pyqode.python/badge.png?branch=develop
    :target: https://coveralls.io/r/pyQode/pyqode.python?branch=develop
    :alt: Coverage Status

About pyqode.python
-------------------

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


Snapshots
---------

Here are a few snapshots of the Qidle example application (snapshots
taken on a Gnome 3 desktop):

.. image:: doc/source/_static/qidle.png
    :alt: Preview of Qidle, the pyqode clone of idle (example app)


.. _Downloads: https://github.com/pyQode/pyqode.python/releases
.. _Source repository: https://github.com/pyQode/pyqode.python/
.. _Wiki: https://github.com/pyQode/pyqode.core/wiki
.. _official pyqode extension package: https://github.com/pyQode/pyqode.core/wiki/Extensions#official-packages
.. _pyQode: https://github.com/pyQode
.. _Jedi: https://github.com/davidhalter/jedi
.. _`Documentation`: http://pyqodepython.readthedocs.org/en/latest/
.. _master: https://github.com/pyQode/pyqode.python/tree/master
.. _develop: https://github.com/pyQode/pyqode.python/tree/develop
