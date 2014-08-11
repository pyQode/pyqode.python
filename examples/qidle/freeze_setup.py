#!/usr/bin/env python
# coding: latin-1
#
# GTermEditor
#
# Copyright 2013-2014, Sirmo Games S.A.
#
"""
This setup script build a frozen distribution of the application (with the
python interpreter and 3rd party libraries embedded) for Windows.

Run the following command to freeze the app (the frozen executable can be
found in the bin folder::

    python freeze_setup.py build

"""
import sys
from cx_Freeze import setup, Executable
from pyqode.core.modes import PYGMENTS_STYLES


def read_version():
    """
    Reads the version without self importing
    """
    with open("qidle/__init__.py") as f:
        lines = f.read().splitlines()
        for l in lines:
            if "__version__" in l:
                return l.split("=")[1].strip().replace('"', "").replace("'", '')


# automatically build when run without arguments
if len(sys.argv) == 1:
    sys.argv.append("build")

# Build options
# get pygments styles (and remove our own styles since them have already
# been packaged).
pygments_styles = PYGMENTS_STYLES
pygments_styles.remove('darcula')
pygments_styles.remove('qt')
options = {"namespace_packages": ["pyqode.core", 'pyqode.python'],
           "include_msvcr": True,
           "build_exe": "bin",
           'include_files': ['libraries.zip'],
           "includes": ["pkg_resources"] +
                       ["pygments.styles.%s" % style for style in pygments_styles]}

# Run the cxFreeze setup
setup(name="Qidle",
      version=read_version(),
      options={"build_exe": options},
      executables=[
          Executable("qidle.py", targetName="Qidle.exe",
                     icon='share/qidle.ico',
                     base="Win32GUI")])

# we need to copy the pyqode.python server script to the binary
# dir since this script must be out of a zip file to be run.
from pyqode.python.backend import server
with open(server.__file__, 'rb') as f:
    with open('bin/server.py', 'wb') as script:
        script.write(f.read())

