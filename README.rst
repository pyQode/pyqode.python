.. image:: https://raw.githubusercontent.com/pyQode/pyqode.core/master/doc/source/_static/pyqode-banner.png


About
-----
.. image:: http://img.shields.io/pypi/v/pyqode.python.png
    :target: https://pypi.python.org/pypi/pyqode.python/
    :alt: Latest PyPI version

.. image:: http://img.shields.io/pypi/dm/pyqode.python.png
    :target: https://pypi.python.org/pypi/pyqode.python/
    :alt: Number of PyPI downloads

.. image:: https://travis-ci.org/pyQode/pyqode.python.svg?branch=master
    :target: https://travis-ci.org/pyQode/pyqode.python
    :alt: Travis-CI build status

.. image:: https://coveralls.io/repos/pyQode/pyqode.python/badge.png?branch=master
    :target: https://coveralls.io/r/pyQode/pyqode.python?branch=master
    :alt: Coverage Status

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

    $ pip install pyqode.python


Testing
-------

pyqode.python has a test suite and measure its coverage.

To run the tests, you must first install tox and pytest::

    $ pip install tox pytest

You might also want to install pytest-cov and pytest-pep8.

Then you can run the tests by running the following command::

    $ tox

To run the tests for a specifc environment, use the -e option. E.g. to run
tests with python 2.7 and pyqt4, you would run::

    $ tox -e py27-pyqt4

Here is the list of available test environments:

- py27-pyqt4
- py27-pyqt5
- py32-pyqt4
- py32-pyqt5
- py33-pyqt4
- py33-pyqt5
- py34-pyqt4
- py34-pyqt5
- cov
- pep8

.. _Screenshots: https://github.com/pyQode/pyQode/wiki/Screenshots-and-videos#pyqodepython-screenshots
.. _Issue tracker: https://github.com/pyQode/pyQode/issues
.. _Wiki: https://github.com/pyQode/pyQode/wiki
.. _API reference: https://pythonhosted.org/pyqode.python/
.. _pyQode: https://github.com/pyQode/pyQode
.. _Jedi: https://github.com/davidhalter/jedi
.. _Changelog: https://github.com/pyQode/pyqode.python/blob/master/CHANGELOG.rst
.. _Contributing: https://github.com/pyQode/pyqode.python/blob/master/CONTRIBUTING.rst