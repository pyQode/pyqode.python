#!/usr/bin/env python
#
# Copyright (c) <2013-2016> Colin Duquesnoy
#
# This file is part of OpenCobolIDE.
#
# OpenCobolIDE is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# OpenCobolIDE is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# OpenCobolIDE. If not, see http://www.gnu.org/licenses/.
#
"""
Setup script for pynotepad

You will need to install PyQt4 on your own.
"""
import os
import sys
from setuptools import setup, find_packages


#
# add ``build_ui command`` (optional, for development only)
# this command requires the following packages:
#   - pyqt_distutils
#   - pyqode-uic
#
try:
    from pyqt_distutils.build_ui import build_ui
    cmdclass = {'build_ui': build_ui}
except ImportError:
    cmdclass = {}


def read_version():
    """
    Reads the version without self importing
    """
    with open("pynotepad/__init__.py") as f:
        lines = f.read().splitlines()
        for l in lines:
            if "__version__" in l:
                return l.split("=")[1].strip().replace('"', "")


def is_run_as_root():
    return os.getuid() == 0


# get long description
with open('readme.rst', 'r') as readme:
    long_desc = readme.read()


# install requirements
requirements = ['pygments>=1.6', 'pyqode.core', 'chardet']

data_files = []
if sys.platform == "linux" and is_run_as_root():
    data_files.append(('/usr/share/applications', ['share/pynotepad.desktop']))
    data_files.append(('/usr/share/pixmaps', ['share/pynotepad.png']))
    data_files.append(('/usr/share/pynotepad', ['libraries.zip']))


setup(
    name='pynotepad',
    version=read_version(),
    packages=find_packages(),
    keywords=["pynotepad editor text source code"],
    data_files=data_files,
    url='https://github.com/pyQode/pyqode.core/examples/pynotepad',
    license='MIT',
    author='Colin Duquesnoy',
    author_email='colin.duquesnoy@gmail.com',
    description='A simple pynotepad based on pyQode',
    long_description=long_desc,
    zip_safe=False,
    install_requires=requirements,
    cmdclass=cmdclass,
    entry_points={'gui_scripts': ['pynotepad = pynotepad:main']},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: X11 Applications :: Qt',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Developers',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Text Editors :: Integrated Development Environments (IDE)']
)
