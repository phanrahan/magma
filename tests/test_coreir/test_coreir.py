from magma.frontend.coreir_ import GetCoreIRModule
from magma.backend.coreir_utils import check_magma_interface
from magma.backend.coreir_ import CoreIRBackend
from magma.t import Type, Kind
from magma import *
import magma
import pytest
coreir = pytest.importorskip("coreir")


def test_check_interface_bit():
    """
    This should work with valid types
    """
    class TestCircuit0(Circuit):
        name = "TestCircuit0"
        io = m.IO(I=In(Bit), O=Out(Bit))
        @classmethod
        def definition(cls):
            wire(cls.I, cls.O)
    backend = magma.backend.coreir_.CoreIRBackend()
    check_magma_interface(TestCircuit0.interface)


def test_check_interface_array():
    """
    This should work with valid types
    """
    class TestCircuit1(Circuit):
        name = "TestCircuit1"
        io = m.IO(I=In(Array[8, Bit]), O=Out(Array[8, Bit]))
        @classmethod
        def definition(cls):
            wire(cls.I, cls.O)
    backend = magma.backend.coreir_.CoreIRBackend()
    check_magma_interface(TestCircuit1.interface)


def test_check_interface_tuple():
    """
    This should work with valid types
    """

    class T(m.Product):
        a = Bit
        b = Array[7, Bit]

    class TestCircuit2(Circuit):
        name = "TestCircuit2"
        io = m.IO(I=In(T), O=Out(T))
        @classmethod
        def definition(cls):
            wire(cls.I, cls.O)
    backend = magma.backend.coreir_.CoreIRBackend()
    check_magma_interface(TestCircuit2.interface)


def test_nested_clocks():
    c = coreir.Context()
    cirb = CoreIRBackend(c)
    args = ['clocks', In(Array[2, Clock])]

    inner_test_circuit = DefineCircuit('inner_test_nested_clocks', *args)
    EndCircuit()

    test_circuit = DefineCircuit('test_nested_clocks', *args)
    inner_test_circuit()
    EndCircuit()
    GetCoreIRModule(cirb, test_circuit)
