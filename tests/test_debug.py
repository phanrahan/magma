import os
import pathlib
import pytest

import magma as m
from magma.debug import get_debug_info, debug_info, magma_helper_function


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


def test_helper_function():

    class Foo(m.Circuit):
        io = m.IO()

    def _make_foo():  # no helper fn annotation
        return Foo()

    @magma_helper_function
    def _make_foo_annotated():
        return Foo()

    class Bar(m.Circuit):
        io = m.IO()
        Foo()
        _make_foo_annotated()
        _make_foo()

    instances = Bar.instances
    assert instances[1].debug_info.lineno == instances[0].debug_info.lineno + 1
    assert instances[2].debug_info.lineno == instances[0].debug_info.lineno - 8
