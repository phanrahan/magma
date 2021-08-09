#!/bin/bash
CIRCT_HOME=/Users/rajsekhar/private/magma-mlir-experiments/circt
OPT=$CIRCT_HOME/build/bin/circt-opt
TRANSLATE=$CIRCT_HOME/build/bin/circt-translate
OPT_ARGS="--lower-seq-to-sv --canonicalize --hw-cleanup --prettify-verilog"
TRANSLATE_ARGS="--export-verilog"
cat $1 | $OPT $OPT_ARGS | $TRANSLATE $TRANSLATE_ARGS
