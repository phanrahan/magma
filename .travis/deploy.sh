#!/usr/bin/env bash

export PATH=$TRAVIS_BUILD_DIR/miniconda/bin:$PATH
source activate test-env

pip install twine
python setup.py sdist build

twine upload dist/* -u leonardt -p $PYPI_PASSWORD
