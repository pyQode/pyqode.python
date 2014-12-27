#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This setup script packages pyqode.python
"""
from setuptools import setup, find_packages
from pyqode.python import __version__

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


def readme():
    return str(open('README.rst').read())


# get requirements
requirements = [
    'pyqode.qt',
    'pyqode.core',
    'jedi',
    'pep8',
    'frosted',
    'docutils'
]

setup(
    name='pyqode.python',
    namespace_packages=['pyqode'],
    version=__version__,
    packages=[p for p in find_packages() if 'test' not in p],
    keywords=["CodeEdit PySide PyQt code editor widget python"],
    package_dir={'pyqode': 'pyqode'},
    url='https://github.com/pyQode/pyqode.python',
    license='MIT',
    author='Colin Duquesnoy',
    author_email='colin.duquesnoy@gmail.com',
    description='Add python support to pyqode',
    long_description=readme(),
    install_requires=requirements,
    entry_points={'pyqode_plugins':
                  ['pyqode_python = '
                   'pyqode.python.designer_plugin']},
    zip_safe=False,
    cmdclass=cmdclass,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: X11 Applications :: Qt',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Widget Sets',
        'Topic :: Text Editors :: Integrated Development Environments (IDE)'
    ]
)
