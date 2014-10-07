This directory contains a complete application based on pyqode.python and
pyqode.core.

It uses *most of the pyqode.python features* and comes with packaging scripts
to show you how to setup a pyqode.python application and how to distribute it (
especially on Windows with cx_Freeze)

This application provides basic functionality such as writing and running a
script.

To **run** the example, just run::

    python pynotepad.py


To **install** the package *on linux*, just run::

    sudo python setup.py install

To **freeze the application on Windows**, you first need to install cx_Freeze.
Then you can run::

    python freeze_setup.py build

The resulting binary can be found in the **bin/** folder.

Additionally you can install innosetup and run setup.iss to build an installer
out of the frozen app (the resulting installer can be found in the **dist**
folder)
