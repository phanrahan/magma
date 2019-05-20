#!/usr/bin/env bash

export PATH=$TRAVIS_BUILD_DIR/miniconda/bin:$PATH
source activate test-env

echo [distutils]                                  > ~/.pypirc
echo index-servers =                             >> ~/.pypirc
echo "  pypi"                                    >> ~/.pypirc
echo                                             >> ~/.pypirc
echo [pypi]                                      >> ~/.pypirc
echo repository=https://upload.pypi.org/legacy/  >> ~/.pypirc
echo username=leonardt                           >> ~/.pypirc
echo password=$PYPI_PASSWORD                     >> ~/.pypirc

pip install twine
python setup.py sdist build

twine upload dist/*
