#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# PCEF - Python/Qt Code Editing Framework
# Copyright 2013, Colin Duquesnoy <colin.duquesnoy@gmail.com>
#
# This software is released under the LGPLv3 license.
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""
This setup script packages pcef-python
"""
from setuptools import setup, find_packages
import sys

def read_version():
    with open("pcef/python/__init__.py") as f:
        lines = f.read().splitlines()
        for l in lines:
            if "__version__" in l:
                return l.split("=")[1].strip()


def readme():
    return str(open('README.rst').read())

# get requirements
requirements = ['pcef-core', 'jedi', 'pep8', 'pyflakes']
# todo check pylint with python3 on ubuntu, this does not works on win32
# if sys.platform != "win32":
#     requirements += ["pylint"]

setup(
    name='pcef-python',
    namespace_packages=['pcef'],
    version=read_version(),
    packages=find_packages(),
    keywords=["QCodeEditor", "PySide", "PyQt", "code editor", "python"],
    # package_data={'pcef.ui': ['rc/*']},
    package_dir={'pcef': 'pcef'},
    url='https://github.com/ColinDuquesnoy/PCEF',
    license='GNU LGPL v3',
    author='Colin Duquesnoy',
    author_email='colin.duquesnoy@gmail.com',
    description='PCEF python specific modes and panels',
    long_description=readme(),
    install_requires=requirements,
    entry_points={'pcef_plugins':
                 ['pcef_python = pcef.python.plugins.pcef_python_plugin']},
    zip_safe=False
)
