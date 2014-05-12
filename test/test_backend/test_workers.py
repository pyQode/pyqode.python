"""
Test all workers in pyqode.python.backend.workers.
"""
import sys
from pyqode.python import frontend as pyfrontend
from pyqode.python.backend import workers


def test_calltips():
    data = {
        'code': "open(",
        'line': 1,
        'column': len('open('),
        'path': None
    }
    status, results = workers.calltips(data)
    assert status is True
    assert len(results) == 6


def test_calltips_with_closing_paren():
    data = {
        'code': "open()",
        'line': 1,
        'column': len('open()'),
        'path': None
    }
    status, results = workers.calltips(data)
    assert status is False
    assert len(results) == 0


def test_goto_assignments():
    data = {
        'code': "foo = 10;print(foo)",
        'line': 1,
        'column': len('foo = 10;print(foo)') - 1,
        'path': None
    }
    status, results = workers.goto_assignments(data)
    assert status is True
    assert len(results) == 1
    definition = results[0]
    module, line, column, full_name = definition
    assert line == 1
    assert column == 0

    data = {
        'code': "foo = 10;print(foo)",
        'line': 1,
        'column': len('foo = 10;print(foo)'),
        'path': None
    }
    status, results = workers.goto_assignments(data)
    assert status is True
    assert len(results) == 0


def test_defined_names():
    from pyqode.python.frontend import code_edit
    code = ""
    filename = code_edit.__file__
    with open(filename, 'r') as file:
        code = file.read()
    status, results = workers.defined_names({'code': code, 'path': filename})
    assert status is True
    assert len(results) == 18
    print(code)
    print(results)
