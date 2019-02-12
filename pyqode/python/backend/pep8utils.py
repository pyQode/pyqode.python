# -*- coding: utf-8 -*-
"""
This module contains utility classes for interacting with the pycodestyle
module using strings instread of files. This allow live checking on code
without the need to save.
"""
import pycodestyle


class CustomReport(pycodestyle.StandardReport):
    """
    Custom report used to get the pycodestyle results as a list of string. This
    is easier to handler then retrieving the stdout and parsing.
    """

    def get_file_results(self):
        self._deferred_print.sort()
        return self._deferred_print


class CustomChecker(pycodestyle.Checker):
    """
    Custom Checker with our Custom report.
    """

    def __init__(self, *args, **kwargs):
        super(CustomChecker, self).__init__(
            *args, report=CustomReport(kwargs.pop("options")), **kwargs)
