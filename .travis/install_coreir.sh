#!/bin/bash

set -e

if [ "$TRAVIS_BRANCH" == "coreir-dev" ]; then
    mkdir deps;
    mkdir deps/bin;
    mkdir deps/lib;
    mkdir deps/include;
    cd deps;
    git clone -b dev https://github.com/rdaly525/coreir.git;
    cd coreir;
    export CXX="g++-4.9";
    cd build
    cmake -DCMAKE_INSTALL_PREFIX:PATH=$TRAVIS_BUILD_DIR/deps ..
    make install;
    cd ..;  # build
    cd ..;  # coreir
    cd ..;  # deps
    export PATH=$TRAVIS_BUILD_DIR/deps/bin:$PATH;
    export LD_LIBRARY_PATH=$TRAVIS_BUILD_DIR/deps/lib:$LD_LIBRARY_PATH;
    pip install --upgrade git+git://github.com/leonardt/pycoreir.git@dev;
else
    # based on https://gist.github.com/steinwaywhw/a4cd19cda655b8249d908261a62687f8
    curl -s -L https://github.com/rdaly525/coreir/releases/latest | grep "href.*coreir-linux.tar.gz" | cut -d \" -f 2 | xargs -I {} wget https://github.com"{}"
    mkdir coreir_release;
    tar -xf coreir-linux.tar.gz -C coreir_release --strip-components 1;
    export PATH=$TRAVIS_BUILD_DIR/coreir_release/bin:$PATH;
    export LD_LIBRARY_PATH=$TRAVIS_BUILD_DIR/coreir_release/lib:$LD_LIBRARY_PATH;
fi
