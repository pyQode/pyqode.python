"""
Test all workers in pyqode.python.backend.workers.
"""
import sys

import jedi
from pyqode.core.modes import CheckerMessages
from pyqode.core.share import Definition

try:
    from future.builtins import str, open
except:
    pass
from pyqode.python.backend import workers
from pyqode.python.widgets import code_edit


def test_calltips():
    data = {
        'code': "open(",
        'line': 0,
        'column': len('open('),
        'path': None
    }
    results = workers.calltips(data)
    assert len(results) == 6


def test_calltips_with_closing_paren():
    data = {
        'code': "open()",
        'line': 0,
        'column': len('open()'),
        'path': None
    }
    results = workers.calltips(data)
    assert len(results) == 0


def test_goto_assignments():
    data = {
        'code': "foo = 10;print(foo)",
        'line': 0,
        'column': len('foo = 10;print(foo)') - 1,
        'path': None
    }
    results = workers.goto_assignments(data)
    # todo: restore assertion once jedi#571 is resolved
    # assert len(results) == 1
    # definition = results[0]
    # module, line, column, full_name = definition
    # assert line == 0
    # assert column == 0

    data = {
        'code': "foo = 10;print(foo)",
        'line': 0,
        'column': len('foo = 10;print(foo)'),
        'path': None
    }
    results = workers.goto_assignments(data)
    assert len(results) == 0


def test_extract_def():
    code = """
    import pyqode.python.widgets
    import PyQt5.QtWidgets as QtWidgets
    app = QtWidgets.QApplication([])
    editor = pyqode.python.widgets.PyCyodeEdit()
    editor.file.open(__file__)
    editor.show()
    app.exec()
    """
    for definition in jedi.names(code):
        result = workers._extract_def(definition, "")
        assert result

def test_defined_names():
    filename = __file__
    with open(filename, 'r', encoding='utf-8') as file:
        code = file.read()
    results = workers.defined_names({'code': code, 'path': filename})
    assert len(results)
    definitions = []
    for i, definition in enumerate(results):
        d = Definition.from_dict(definition)
        definitions.append(d)
        if i:
            assert d != definitions[i-1]

    # now that the code changed, defined_names should return
    # (True, [xxx, yyy, ...])
    code += "\ndef foo():\n    print('bar')"
    results = workers.defined_names({'code': code, 'path': filename})
    assert len(results)


def test_quick_doc():
    data = {
        'code': "open",
        'line': 0,
        'column': 1,
        'path': None
    }
    results = workers.quick_doc(data)
    assert len(results) == 1
    assert isinstance(results[0], str)


def test_run_pep8():
    messages = workers.run_pep8(
        {'code': 'print("foo")\n', 'path': None,
         'max_line_length': 79, 'ignore_rules': []})
    assert len(messages) == 0

    messages = workers.run_pep8(
        {'code': 'print("foo"); print("bar")\n', 'path': None,
         'max_line_length': 79, 'ignore_rules': []})
    assert len(messages) == 1
    assert messages[0][2] == 0


def test_run_pyflakes():
    messages = workers.run_pyflakes(
        {'code': None, 'path': __file__, 'encoding': 'utf-8',
         'max_line_length': 79, 'ignore_rules': []})
    assert len(messages) == 0

    # OK
    messages = workers.run_pyflakes(
        {'code': 'print("foo")\n', 'path': __file__, 'encoding': 'utf-8'})
    assert len(messages) == 0

    # Syntax error
    messages = workers.run_pyflakes(
        {'code': 'print("foo\n', 'path': __file__,
         'encoding': 'utf-8'})
    assert len(messages) == 1
    assert messages[0][2] == 0
    assert messages[0][1] == CheckerMessages.ERROR

    # unused import
    messages = workers.run_pyflakes(
        {'code': 'import sys; print("foo");\n', 'path': __file__,
         'encoding': 'utf-8'})
    assert len(messages) == 1
    msg, status, line = messages[0]
    assert "'sys' imported but unused" in msg
    assert line == 0


def test_completions():
    provider = workers.JediCompletionProvider()
    completions = provider.complete('import ', 0, len('import '), None,
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
