import pytest
coreir = pytest.importorskip("coreir")
import magma
from magma import *
from magma.t import Type, Kind


def test_check_interface_bit():
    """
    This should work with valid types
    """
    class TestCircuit0(Circuit):
        name = "TestCircuit0"
        IO = ["I", In(Bit), "O", Out(Bit)]
        @classmethod
        def definition(cls):
            wire(cls.I, cls.O)
    backend = magma.backend.coreir_.CoreIRBackend()
    backend.check_interface(TestCircuit0)


def test_check_interface_array():
    """
    This should work with valid types
    """
    class TestCircuit1(Circuit):
        name = "TestCircuit1"
        IO = ["I", In(Array(8, Bit)), "O", Out(Array(8, Bit))]
        @classmethod
        def definition(cls):
            wire(cls.I, cls.O)
    backend = magma.backend.coreir_.CoreIRBackend()
    backend.check_interface(TestCircuit1)


def test_check_interface_tuple():
    """
    This should work with valid types
    """
    class TestCircuit2(Circuit):
        name = "TestCircuit2"
        IO = ["I", In(Tuple(a=Bit, b=Array(7, Bit))), "O", Out(Tuple(a=Bit, b=Array(7, Bit)))]
        @classmethod
        def definition(cls):
            wire(cls.I, cls.O)
    backend = magma.backend.coreir_.CoreIRBackend()
    backend.check_interface(TestCircuit2)
