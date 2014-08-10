# This foo class is here so that the document analyser got nodes with children
# DO NOT REMOVE IT
from pyqode.qt.QtTest import QTest
from pyqode.python import modes as pymodes
from ..helpers import editor_open


class Foo:
    def y(self):
        pass


def get_mode(editor):
    return editor.modes.get(pymodes.DocumentAnalyserMode)


def test_enabled(editor):
    mode = get_mode(editor)
    assert mode.enabled
    mode.enabled = False
    mode.enabled = True


@editor_open(__file__)
def test_with_children(editor):
    # wait for the defined_names worker to complete
    QTest.qWait(1000)


def test_empty_doc(editor):
    editor.clear()
    get_mode(editor)._run_analysis()
