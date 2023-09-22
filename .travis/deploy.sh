#!/usr/bin/env bash

export PATH=$TRAVIS_BUILD_DIR/miniconda/bin:$PATH

pip install twine
python setup.py sdist

twine upload dist/*.tar.gz -u leonardt -p $PYPI_PASSWORD
