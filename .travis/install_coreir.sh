#!/bin/bash

mkdir deps
cd deps;
if [[ "$TRAVIS_BRANCH" == "coreir-dev" ]]; then
  git clone --single-branch --branch dev https://github.com/rdaly525/coreir.git
  cd coreir/build
  cmake -DCMAKE_INSTALL_PREFIX:PATH=$TRAVIS_BUILD_DIR/deps ..
  make install;
  cd ..;  # build
  cd ..;  # coreir
else
  # based on https://gist.github.com/steinwaywhw/a4cd19cda655b8249d908261a62687f8
  curl -s -L https://github.com/rdaly525/coreir/releases/latest | grep "href.*coreir-${TRAVIS_OS_NAME}.tar.gz" | cut -d \" -f 2 | xargs -I {} wget https://github.com"{}"
  mkdir coreir_release;
  tar -xf coreir-${TRAVIS_OS_NAME}.tar.gz -C coreir_release --strip-components 1;
  mkdir bin;
  mkdir lib;
  mkdir include;
  cd coreir_release;

  make install prefix=$TRAVIS_BUILD_DIR/deps;
  cd ..; #coreir_release
fi

if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
  # avoid strange libjpeg error (see https://github.com/sgrif/pq-sys/issues/1
  # for some more info)
  export DYLD_LIBRARY_PATH=/System/Library/Frameworks/ImageIO.framework/Versions/A/Resources/:$DYLD_LIBRARY_PATH
  export DYLD_LIBRARY_PATH=$TRAVIS_BUILD_DIR/deps/lib:$DYLD_LIBRARY_PATH
else
  export LD_LIBRARY_PATH=$TRAVIS_BUILD_DIR/deps/lib:$LD_LIBRARY_PATH
fi

export PATH=$TRAVIS_BUILD_DIR/deps/bin:$PATH
cd ..;  # deps
