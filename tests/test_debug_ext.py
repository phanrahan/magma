import os

import magma_debug


def test_magma_debug_ext():
    filedir = os.path.realpath(os.path.dirname(__file__))
    assert magma_debug.get_fn_ln(0) == (
        f"{filedir}/test_debug_ext.py",
        8
    )
