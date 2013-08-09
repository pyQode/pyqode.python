#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# pyQode - Python/Qt Code Editor widget
# Copyright 2013, Colin Duquesnoy <colin.duquesnoy@gmail.com>
#
# This software is released under the LGPLv3 license.
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""
This setup script packages pyqode-python
"""
from setuptools import setup, find_packages


def read_version():
    with open("pyqode/python/__init__.py") as f:
        lines = f.read().splitlines()
        for l in lines:
            if "__version__" in l:
                return l.split("=")[1].strip()


def readme():
    return str(open('README.rst').read())


# get requirements
requirements = ['pyqode-core', 'jedi', 'pep8', 'pyflakes']


setup(
    name='pyqode-python',
    namespace_packages=['pyqode'],
    version=read_version(),
    packages=find_packages(),
    keywords=["QCodeEditor", "PySide", "PyQt", "code editor", "python"],
    package_data={'pyqode.python.ui': ['*.ui', 'rc/*']},
    package_dir={'pyqode': 'pyqode'},
    url='https://github.com/ColinDuquesnoy/pyqode-python',
    license='GNU LGPL v3',
    author='Colin Duquesnoy',
    author_email='colin.duquesnoy@gmail.com',
    description='Python/Qt Code Editor widget',
    long_description=readme(),
    install_requires=requirements,
    entry_points={'pyqode_plugins':
                 ['pyqode_python = pyqode.python.plugins.pyqode_python_plugin']},
    zip_safe=False
)
