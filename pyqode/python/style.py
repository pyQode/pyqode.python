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
from pyqode.core.api.system import TextStyle

# ----------------
# PySyntaxHighlighter
# ----------------
py_keyword = TextStyle('#808000 nbold nitalic nunderlined')
"""
TextStyle for python keywords
"""

py_builtins = TextStyle('#808000 nbold nitalic nunderlined')
"""
TextStyle for python builtins (open,...)
"""

py_operator = TextStyle('darkGray nbold nitalic nunderlined')
"""
TextStyle for python operators (+,-,...)
"""

py_punctuation = TextStyle('darkGray nbold nitalic nunderlined')
"""
TextStyle for python punctuation ( . )
"""

py_decorator = TextStyle('#808000 nbold nitalic nunderlined')
"""
TextStyle for python decorators
"""

py_brace = TextStyle('#404040 nbold nitalic nunderlined')
"""
TextStyle for python braces ({}[]())
"""

py_class = TextStyle('#800080 nbold nitalic nunderlined')
"""
TextStyle for python classes (definition)
"""

py_function = TextStyle('#800080 nbold nitalic nunderlined')
"""
TextStyle for python functions (definition)
"""

py_string = TextStyle('#008000 nbold nitalic nunderlined')
"""
TextStyle for python strings ("xxx", 'xxx', '''xxx''')
"""

py_docstring = TextStyle('#0000AA nbold nitalic nunderlined')
"""
TextStyle for python strings (\"\"\"xxx\"\"\")
"""

py_comment = TextStyle('#008000 nbold italic nunderlined')
"""
TextStyle for python comments (# xxx)
"""

py_self = TextStyle('#8F2828 nbold italic nunderlined')
"""
TextStyle for python self attribute (in method definition and body)
"""

py_numbers = TextStyle('#000080 nbold nitalic nunderlined')
"""
TextStyle for python numbers
"""

py_predefined = TextStyle('#B200B2 nbold nitalic nunderlined')
"""
..todo:: ???
"""

py_docstring_tag = TextStyle('#0000FF nbold nitalic underlined')
"""
TextStyle for sphinx docstrings tages.
"""
