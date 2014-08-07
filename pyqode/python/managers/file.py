"""
Contains the python specific FileManager.
"""
import ast
import re
from pyqode.core.managers import FileManager


class PyFileManager(FileManager):
    """
    Extends file manager to override detect_encoding. With python, we can
    detect encoding by reading the two first lines of a file and extracting its
    encoding tag.

    """

    def detect_encoding(self, path):
        """
        For the implementation of encoding definitions in Python, look at:
        - http://www.python.org/dev/peps/pep-0263/

        .. note:: code taken and adapted from
            ```jedi.common.source_to_unicode.detect_encoding```
        """
        with open(path, 'rb') as file:
            source = file.read()
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

    def open(self, path, encoding=None, use_cached_encoding=True):
        if encoding is None:
            encoding = self.detect_encoding(path)
        super().open(path, encoding=encoding,
                     use_cached_encoding=use_cached_encoding)
