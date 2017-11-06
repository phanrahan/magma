#!/bin/bash

set -e

if [ "$TRAVIS_BRANCH" == "coreir-dev" ]; then
    sudo add-apt-repository -y ppa:ubuntu-toolchain-r/test
    sudo apt-get update
    sudo apt-get install g++-4.9
    mkdir deps;
    mkdir deps/bin;
    mkdir deps/lib;
    mkdir deps/include;
    cd deps;
    git clone -b dev https://github.com/rdaly525/coreir.git;
    cd coreir;
    export COREIRCONFIG="g++-4.9";
    export COREIR=$PWD;
    make install prefix=$TRAVIS_BUILD_DIR/deps;
    cd ..;
    cd ..;
    export PATH=$TRAVIS_BUILD_DIR/deps/bin:$PATH;
    export LD_LIBRARY_PATH=$TRAVIS_BUILD_DIR/deps/lib:$LD_LIBRARY_PATH;
    pip install git+git://github.com/leonardt/pycoreir.git@dev;
else
    wget https://github.com/rdaly525/coreir/releases/download/v0.0.2/coreir.tar.gz;
    mkdir coreir_release;
    tar -xf coreir.tar.gz -C coreir_release --strip-components 1;
    export PATH=$TRAVIS_BUILD_DIR/coreir_release/bin:$PATH;
    export LD_LIBRARY_PATH=$TRAVIS_BUILD_DIR/coreir_release/lib:$LD_LIBRARY_PATH;
    pip install coreir;
fi
