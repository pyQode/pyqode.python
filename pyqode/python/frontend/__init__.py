# -*- coding: utf-8 -*-
"""
The frontend packages contains classes and functions related to
tge gui side application. This is where you will find the python
specific modes and panels and an already configured CodeEdit made
for python programming.

"""
import re
import sys
from pyqode.core.frontend import open_file as _open_file
from pyqode.python.frontend.code_edit import PyCodeEdit
from pyqode.python.frontend import modes
from pyqode.python.frontend import panels


def open_file(editor, path, replace_tabs_by_spaces=True):
    """
    Extends pyqode.core.frontend.open_file to detect encoding from the script
    coding tag (we can do that only for python scripts).

    """
    def detect_encoding(path, default):
        """
        For the implementation of encoding definitions in Python, look at:
        - http://www.python.org/dev/peps/pep-0263/

        .. note:: code taken and adapted from
            ```jedi.common.source_to_unicode.detect_encoding```
        """
        import ast

        with open(path, 'rb') as f:
            source = f.read()
            # take care of line encodings (not in jedi)
            source = source.replace(b'\r', b'')
            source_str = str(source).replace('\\n', '\n')

        byte_mark = ast.literal_eval(r"b'\xef\xbb\xbf'")
        if source.startswith(byte_mark):
            # UTF-8 byte-order mark
            return 'utf-8'

        first_two_lines = re.match(r'(?:[^\n]*\n){0,2}', source_str).group(0)
        possible_encoding = re.search(r"coding[=:]\s*([-\w.]+)",
                                      first_two_lines)
        if possible_encoding:
            return possible_encoding.group(1)
        else:
            return default

    _open_file(editor, path, replace_tabs_by_spaces=replace_tabs_by_spaces,
               detect_encoding_func=detect_encoding,
               default_encoding='iso-8859-1')
