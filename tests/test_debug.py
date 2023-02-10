import os
import pathlib
import pytest

import magma as m
from magma.debug import get_debug_info, debug_info, magma_helper_function
from magma.passes.finalize_whens import finalize_whens
from magma.backend.coreir.insert_coreir_wires import insert_coreir_wires


def test_magma_debug_ext():
    filedir = os.path.realpath(os.path.dirname(__file__))
    assert get_debug_info(2) == debug_info(
        f"{filedir}/test_debug.py",
        13,
        None
    )


@pytest.mark.parametrize(
    'op',
    (
        lambda: ~m.Bit(),
        lambda: m.Bit() | m.Bit(),
        lambda: m.Bit() == m.Bit(),
        lambda: ~m.Bits[8](),
        lambda: m.Bits[8]() | m.Bits[8](),
        lambda: m.Bits[8]() == m.Bits[8](),
        lambda: m.mux([m.Bit(), m.Bit()], m.Bit()),
        lambda: m.register(m.Bit()),
    )
)
def test_primitive_debug_info(op):

    class Foo(m.Circuit):
        op()  # just to instance some primitive

    inst = Foo.instances[0]
    assert inst.debug_info.filename == __file__


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


def test_circuit_builder():

    class Builder(m.CircuitBuilder):
        def __init__(self, name):
            super().__init__(name)
            self._add_port("I", m.In(m.Bit))
            self._add_port("O", m.Out(m.Bit))
            m.wire(self._port("I"), self._port("O"))

    class Top(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        b0 = Builder(name="b0")
        b0.I @= io.I
        io.O @= b0.O

    assert Top.instances[0].debug_info.filename == __file__
    assert Top.instances[0].debug_info == Top.b0.debug_info


def test_when():

    class Top(m.Circuit):
        io = m.IO(I=m.In(m.Bit), S=m.In(m.Bit), O=m.Out(m.Bit))
        with m.when(io.S):
            io.O @= io.I
        with m.otherwise():
            io.O @= 0

    finalize_whens(Top)

    assert Top.instances[0].debug_info.filename == __file__


def test_wire():

    class Top(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        x = m.Bit(name="x")
        x @= io.I
        io.O @= x

    insert_coreir_wires(Top)

    assert Top.instances[0].debug_info.filename == __file__