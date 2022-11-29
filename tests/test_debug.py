import os

from magma.debug import get_debug_info, debug_info


def test_magma_debug_ext():
    filedir = os.path.realpath(os.path.dirname(__file__))
    assert get_debug_info(2) == debug_info(
        f"{filedir}/test_debug_ext.py",
        8,
        None
    )
