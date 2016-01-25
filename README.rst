.. image:: https://raw.githubusercontent.com/pyQode/pyQode/master/media/pyqode-banner.png

|

.. image:: https://img.shields.io/pypi/v/pyqode.python.svg
   :target: https://pypi.python.org/pypi/pyqode.python/
   :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/pyqode.python.svg
   :target: https://pypi.python.org/pypi/pyqode.python/
   :alt: Number of PyPI downloads

.. image:: https://img.shields.io/pypi/l/pyqode.python.svg

.. image:: https://travis-ci.org/pyQode/pyqode.python.svg?branch=master
   :target: https://travis-ci.org/pyQode/pyqode.python
   :alt: Travis-CI build status


.. image:: https://coveralls.io/repos/pyQode/pyqode.python/badge.svg?branch=master
   :target: https://coveralls.io/r/pyQode/pyqode.python?branch=master
   :alt: Coverage Status


About
-----

*pyqode.python* adds **python** support to `pyQode`_ (code completion,
calltips, ...).

- `Issue tracker`_
- `Wiki`_
- `API reference`_
- `Contributing`_
- `Changelog`_
- `Screenshots`_


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

pyQode is licensed under the **MIT license**.

Requirements
------------

pyqode.python depends on the following libraries:

- python 2.7 or python 3 (>= 3.2)
- pyqode.core
- jedi
- pep8
- frosted
- docutils

Installation
------------

::

    $ pip install pyqode.python --upgrade


Testing
-------

pyqode.core has a test suite and measure its coverage.

To run the tests, just run ``python setup.py test``

To measure coverage, run::

    python setup.py test -a "--cov pyqode"

To check for PEP8 warnings, install pytest-pep8 and run::

    python setup.py test -a "--pep8 -m pep8"


To run a single test, use ``-a "-- test_file_path.py::test_function"``, e.g.::

    python setup.py test -a "-- test/test_api/test_code_edit.py::test_set_plain_text"


Testing Matrix
++++++++++++++

We test the following combinations on Travis-CI:

+--------------------------+---------+---------+
|                          | PyQt4   | PyQt5   |
+==========================+=========+=========+
| GNU/Linux - Python 2.7   | yes     | no      |
+--------------------------+---------+---------+
| GNU/Linux - Python 3.4   | yes     | yes     |
+--------------------------+---------+---------+

.. _Screenshots: https://github.com/pyQode/pyQode/wiki/Screenshots-and-videos#pyqodepython-screenshots
.. _Issue tracker: https://github.com/pyQode/pyQode/issues
.. _Wiki: https://github.com/pyQode/pyQode/wiki
.. _API reference: https://pythonhosted.org/pyqode.python/
.. _pyQode: https://github.com/pyQode/pyQode
.. _Jedi: https://github.com/davidhalter/jedi
.. _Changelog: https://github.com/pyQode/pyqode.python/blob/master/CHANGELOG.rst
.. _Contributing: https://github.com/pyQode/pyqode.python/blob/master/CONTRIBUTING.rst
