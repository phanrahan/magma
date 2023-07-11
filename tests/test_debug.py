import os
import pathlib
import pytest
import uinspect

import magma as m
from magma.debug import get_debug_info, debug_info, magma_helper_function
from magma.passes.when import run_when_passes
from magma.backend.coreir.insert_coreir_wires import insert_coreir_wires


def test_magma_debug_ext():
    filedir = os.path.realpath(os.path.dirname(__file__))
    assert get_debug_info(2) == debug_info(
        f"{filedir}/test_debug.py",
        14,
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
    filename, lineno = uinspect.get_location()
    assert inst.debug_info.filename == filename


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
    filename, lineno = uinspect.get_location()
    assert all(inst.debug_info.filename == filename for inst in instances)
    assert instances[0].debug_info.lineno == lineno - 5
    assert instances[1].debug_info.lineno == lineno - 4
    assert instances[2].debug_info.lineno == lineno - 13


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

    filename, lineno = uinspect.get_location()
    assert Top.instances[0].debug_info.filename == filename
    assert Top.instances[0].debug_info.lineno == lineno - 4
    assert Top.instances[0].debug_info == Top.b0.debug_info


def test_when():

    class Top(m.Circuit):
        io = m.IO(I=m.In(m.Bit), S=m.In(m.Bit), O=m.Out(m.Bit))
        x = m.Bit(name="x")
        x @= io.I
        with m.when(io.S):
            io.O @= x
        with m.otherwise():
            io.O @= 0

    run_when_passes(Top)
    insert_coreir_wires(Top)

    filename, lineno = uinspect.get_location()
    assert Top.instances[0].debug_info.filename == filename
    assert Top.instances[0].debug_info.lineno == lineno - 8
    assert Top.instances[1].debug_info.filename == filename
    assert Top.instances[1].debug_info.lineno == lineno - 8


def test_wire():

    class Top(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        x = m.Bit(name="x")
        x @= io.I
        io.O @= x

    insert_coreir_wires(Top)

    filename, lineno = uinspect.get_location()
    assert Top.instances[0].debug_info.filename == filename
    assert Top.instances[0].debug_info.lineno == lineno - 4


def test_generator_instance():

    class MyGen(m.Generator2):
        def __init__(self, w: int):
            self.io = io = m.IO(I=m.In(m.Bits[w]), O=m.Out(m.Bits[w]))
            io.O @= io.I

    MyGen4 = MyGen(4)
    MyGen8 = MyGen(8)

    class Top(m.Circuit):
        io = m.IO(I=m.In(m.Bits[12]), O=m.Out(m.Bits[12]))
        x = MyGen4()(io.I[:4])
        y = MyGen8()(io.I[4:])
        io.O @= m.concat(x, y)

    filename, lineno = uinspect.get_location()
    instances = Top.instances
    assert all(inst.debug_info.filename == filename for inst in instances)
    assert instances[0].debug_info.lineno == lineno - 4
    assert instances[1].debug_info.lineno == lineno - 3
