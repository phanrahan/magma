import pytest

import magma as m
from magma.passes.black_box import BlackBoxPass
from magma.testing import check_files_equal


# NOTE(rsetaluri): We need this fixture per function, since each function may
# run a pass to modify the circuits. However, the setup is identical for each so
# we reuse this fixture across all the test.
@pytest.fixture(scope="function")
def ckts():

    class _Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        io.O @= io.I


    class _Bar(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        io.O @= io.I


    class _Top(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        io.O @= _Foo()(io.I)

    return (_Foo, _Bar, _Top)


def test_noop(ckts):
    _Foo, _Bar, _Top = ckts
    m.compile("build/test_passes_black_box_noop", _Top, output="coreir")
    assert check_files_equal(__file__,
                             f"build/test_passes_black_box_noop.json",
                             f"gold/test_passes_black_box_noop.json")


def test_basic(ckts):
    _Foo, _Bar, _Top = ckts
    BlackBoxPass(_Top, (_Foo,)).run()
    m.compile("build/test_passes_black_box_basic", _Top, output="coreir")
    assert check_files_equal(__file__,
                             f"build/test_passes_black_box_basic.json",
                             f"gold/test_passes_black_box_basic.json")


def test_unused(ckts):
    _Foo, _Bar, _Top = ckts
    BlackBoxPass(_Top, (_Bar,)).run()
    m.compile("build/test_passes_black_box_unused", _Top, output="coreir")
    assert check_files_equal(__file__,
                             f"build/test_passes_black_box_unused.json",
                             f"gold/test_passes_black_box_noop.json")


def test_compiler_args(ckts):
    _Foo, _Bar, _Top = ckts
    m.compile("build/test_passes_black_box_compiler_args", _Top,
              output="coreir", black_boxes=(_Foo,))
    assert check_files_equal(__file__,
                             f"build/test_passes_black_box_compiler_args.json",
                             f"gold/test_passes_black_box_basic.json")
