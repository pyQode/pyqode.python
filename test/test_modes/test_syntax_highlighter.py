from pyqode.python import modes
from ..helpers import editor_open


def get_mode(editor):
    return editor.modes.get(modes.PyHighlighterMode)


triple_quoted_string = '''
qdzqzdqzd
"""
"""
'''

def fake():
    """
    Pass
    """
    pass


def fake2():
    '''
    pass
    '''
    pass


val = ''' val '''
val2 = """ val """

# val = ''' val '''
# val2 = """ val """

val3 = 15
"""
def fake2():
    '''
    pass
    '''
    pass
"""

val4 = 15
'''
def fake2():
    """
    pass
    """
    pass
'''


@editor_open(__file__)
def test_enabled(editor):
    mode = get_mode(editor)
    assert mode.enabled
    mode.enabled = False
    mode.enabled = True
