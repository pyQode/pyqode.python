"""
Test all workers in pyqode.python.backend.workers.
"""
import sys
from pyqode.python.backend import workers
from pyqode.python.widgets import code_edit


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
    code = ""
    filename = code_edit.__file__
    with open(filename, 'r') as file:
        code = file.read()
    status, results = workers.defined_names({'code': code, 'path': filename})
    assert status is True
    assert len(results)
    definitions = []
    for i, definition in enumerate(results):
        d = workers.Definition()
        d.from_dict(definition)
        definitions.append(d)
        if i:
            assert d != definitions[i-1]


    # no changes should be detected, returning an empty list with a status
    # set to False
    status, results = workers.defined_names({'code': code, 'path': filename})
    assert status is False
    assert results is None

    # now that the code changed, defined_names should return
    # (True, [xxx, yyy, ...])
    code += "\ndef foo():\n    print('bar')"
    status, results = workers.defined_names({'code': code, 'path': filename})
    assert status is True
    assert len(results)


def test_quick_doc():
    data = {
        'code': "open",
        'line': 1,
        'column': 1,
        'path': None
    }
    status, results = workers.quick_doc(data)
    assert status is True
    assert len(results) == 1
    assert isinstance(results[0], str)


def test_run_pep8():
    status, messages = workers.run_pep8(
        {'code': 'print("foo")\n', 'path': None})
    assert status is True
    assert len(messages) == 0

    status, messages = workers.run_pep8(
        {'code': 'print("foo"); print("bar")\n', 'path': None})
    assert status is True
    assert len(messages) == 1


def test_run_frosted():
    status, messages = workers.run_frosted(
        {'code': None, 'path': __file__, 'encoding': 'utf-8'})
    assert status is False
    assert len(messages) == 0

    # OK
    status, messages = workers.run_frosted(
        {'code': 'print("foo")\n', 'path': __file__, 'encoding': 'utf-8'})
    assert status is True
    assert len(messages) == 0

    # Syntax error
    status, messages = workers.run_frosted(
        {'code': 'print("foo\n', 'path': __file__,
         'encoding': 'utf-8'})
    assert status is True
    assert len(messages) == 1

    # unused import
    status, messages = workers.run_frosted(
        {'code': 'import sys; print("foo");\n', 'path': __file__,
         'encoding': 'utf-8'})
    assert status is True
    assert len(messages) == 1
    msg, status, line = messages[0]
    assert 'sys imported but unused' in msg.lower()


def test_completions():
    provider = workers.JediCompletionProvider()
    completions = provider.complete('import ', 1, len('import '), None,
                                    'utf-8', '')
    assert len(completions) > 10


def test_make_icon():
    class Name:
        @property
        def string(self):
            return 'Foo'
    assert workers.icon_from_typename(Name(), 'PARAM') is not None
    assert workers.icon_from_typename(Name(), 'FOO') is None
    assert workers.icon_from_typename('_protected', 'PARAM') is not None
    assert workers.icon_from_typename('__private', 'PARAM') is not None
