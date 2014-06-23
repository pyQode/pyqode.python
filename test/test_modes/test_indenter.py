from pyqode.python import modes


def get_mode(editor):
    return editor.modes.get(modes.PyIndenterMode)


def test_indent(editor):
    editor.clear()
    # empty doc
    mode = get_mode(editor)
    mode.indent()
    assert editor.toPlainText() == '    '
    editor.clear()
    editor.setPlainText('print("foo")')
    mode.indent()
    assert editor.toPlainText() == '    print("foo")'
    editor.use_spaces_instead_of_tabs = False
    editor.clear()
    mode.indent()
    assert editor.toPlainText() == '\t'
    editor.use_spaces_instead_of_tabs = True


def test_unindent(editor):
    editor.clear()
    # empty doc
    mode = get_mode(editor)
    mode.unindent()
    assert editor.toPlainText() == ''
    editor.clear()
    editor.setPlainText('    print("foo")')
    mode.unindent()
    assert editor.toPlainText() == 'print("foo")'
