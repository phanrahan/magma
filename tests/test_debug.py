import os
import pathlib
import pytest

import magma as m
from magma.debug import get_debug_info, debug_info


def test_magma_debug_ext():
    filedir = os.path.realpath(os.path.dirname(__file__))
    assert get_debug_info(2) == debug_info(
        f"{filedir}/test_debug.py",
        11,
        None
    )


@pytest.mark.parametrize('T,name', ((m.Bit, "bit"), (m.Bits[8], "bits")))
def test_primitive_debug_info(T, name):

    class Foo(m.Circuit):
        ~(T())  # just to instance some primitive

    inst = Foo.instances[0]
    filename = pathlib.Path(inst.debug_info.filename)
    filename = pathlib.Path("/".join(filename.parts[-2:]))
    assert str(filename) == f"magma/{name}.py"
