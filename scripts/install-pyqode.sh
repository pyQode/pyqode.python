#! /bin/bash
for package in 'pyqode.qt' 'pyqode.core'
do
    git clone https://github.com/pyQode/${package}
    pushd ${package}
    pip install -e .
    popd
done
