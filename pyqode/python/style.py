"""
This module contains the style options specific to pyqode.python.

Syntax highlighter options
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autodata:: py_keyword
.. autodata:: py_builtins
.. autodata:: py_operator
.. autodata:: py_punctuation
.. autodata:: py_brace
.. autodata:: py_class
.. autodata:: py_function
.. autodata:: py_docstring
.. autodata:: py_comment
.. autodata:: py_self
.. autodata:: py_numbers
.. autodata:: py_predefined
.. autodata:: py_docstringTag

"""
from pyqode.core.frontend.utils import TextStyle
# pylint: disable=C0103
# ----------------
# PySyntaxHighlighter
# ----------------
#: TextStyle for python keywords
keyword = TextStyle('#808000 nbold nitalic nunderlined')
#: TextStyle for python builtins (open,...)
builtins = TextStyle('#808000 nbold nitalic nunderlined')
#: TextStyle for python operators (+,-,...)
operator = TextStyle('darkGray nbold nitalic nunderlined')
#: TextStyle for python punctuation ( . )
punctuation = TextStyle('darkGray nbold nitalic nunderlined')
#: TextStyle for python decorators
decorator = TextStyle('#808000 nbold nitalic nunderlined')
#: TextStyle for python braces ({}[]())
brace = TextStyle('#404040 nbold nitalic nunderlined')
#: TextStyle for python classes (definition)
klass = TextStyle('#800080 nbold nitalic nunderlined')
#: TextStyle for python functions (definition)
function = TextStyle('#800080 nbold nitalic nunderlined')
#: TextStyle for python strings ("xxx", 'xxx', '''xxx''')
string = TextStyle('#008000 nbold nitalic nunderlined')
#: TextStyle for python strings (\"\"\"xxx\"\"\")
docstring = TextStyle('#0000AA nbold nitalic nunderlined')
#: TextStyle for python comments (# xxx)
comment = TextStyle('#008000 nbold italic nunderlined')
#: TextStyle for python self attribute (in method definition and body)
self = TextStyle('#8F2828 nbold italic nunderlined')
#: TextStyle for python numbers
numbers = TextStyle('#000080 nbold nitalic nunderlined')
predefined = TextStyle('#B200B2 nbold nitalic nunderlined')
#: TextStyle for sphinx docstrings tags.
docstring_tag = TextStyle('#0000FF nbold nitalic underlined')
