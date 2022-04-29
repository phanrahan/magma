import pytest

import magma as m
from magma.compile_exception import UnsupportedOpException


def test_basic():

    class _(m.Circuit):
        with m.compile_guard2("X"):
            with m.compile_guard2("Y", "undefined"):
                inst = m.Register(m.Bit)()

        assert inst.compile_guard2s[0].cond == "X"
        assert inst.compile_guard2s[0].cond_type.name == "defined"
        assert inst.compile_guard2s[1].cond == "Y"
        assert inst.compile_guard2s[1].cond_type.name == "undefined"


def test_nested_circuit_definition():
    # This test checks that when we nest circuit definitions (usually in the
    # case of calling generators inside of definitions), we isolate their
    # compile guard stacks.

    class _Gen(m.Generator2):
        def __init__(self, n):
            T = m.Bits[n]
            self.io = m.IO(I=m.In(T), O=m.Out(T))
            with m.compile_guard2("Y"):
                self.io.O @= ~self.io.I

    class _(m.Circuit):
        with m.compile_guard2("X"):
            inst = _Gen(8)()

            # Check that the compile_guard2 invokations in this circuit and _Gen
            # stay isolated.
            assert len(inst.compile_guard2s) == 1
            assert inst.compile_guard2s[0].cond == "X"
            assert len(type(inst).instances[0].compile_guard2s) == 1
            assert type(inst).instances[0].compile_guard2s[0].cond == "Y"


def test_coreir_backend_exception():

    class _Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bit))
        with m.compile_guard2("X"):
            m.register(io.I)

    with pytest.raises(UnsupportedOpException):
        m.compile("", _Foo, output="coreir")
