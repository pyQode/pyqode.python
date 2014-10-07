"""
This module provides an easy access to the application settings
"""
import json
import os
from pyqode.qt.QtCore import QSettings
import sys


class Settings:
    def __init__(self):
        self.settings = QSettings('pyqode', 'pynotepad')

    @property
    def interpreter(self):
        return self.settings.value('interpreter', '')

    @interpreter.setter
    def interpreter(self, value):
        assert os.path.exists(value)
        self.settings.setValue('interpreter', value)

    @property
    def run_configs(self):
        """
        Returns the dictionary of run configurations. A run configuration is
        just a list of arguments to append to the run command.

        This is internally stored as a json object

        """
        string = self.settings.value('run_configs', '{}')
        return json.loads(string)

    @run_configs.setter
    def run_configs(self, value):
        self.settings.setValue('run_configs', json.dumps(value))

    def get_run_config_for_file(self, filename):
        try:
            dic = self.run_configs
            config = dic[filename]
        except KeyError:
            config = []
            self.set_run_config_for_file(filename, config)
        return config

    def set_run_config_for_file(self, filename, config):
        dic = self.run_configs
        dic[filename] = config
        self.run_configs = dic
