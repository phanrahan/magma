import pytest
coreir = pytest.importorskip("coreir")
import magma
from magma import *
from magma.t import Type, Kind
from magma.backend.coreir_ import CoreIRBackend
from magma.frontend.coreir_ import GetCoreIRModule



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
        IO = ["I", In(Array[8, Bit]), "O", Out(Array[8, Bit])]
        @classmethod
        def definition(cls):
            wire(cls.I, cls.O)
    backend = magma.backend.coreir_.CoreIRBackend()
    backend.check_interface(TestCircuit1)


def test_check_interface_tuple():
    """
    This should work with valid types
    """

    class T(m.Product):
        a = Bit
        b = Array[7, Bit]

    class TestCircuit2(Circuit):
        name = "TestCircuit2"
        IO = ["I", In(T), "O", Out(T)]
        @classmethod
        def definition(cls):
            wire(cls.I, cls.O)
    backend = magma.backend.coreir_.CoreIRBackend()
    backend.check_interface(TestCircuit2)

def test_nested_clocks():
    c = coreir.Context()
    cirb = CoreIRBackend(c, check_context_is_default=False)
    args = ['clocks', In(Array[2, Clock])]

    inner_test_circuit = DefineCircuit('inner_test_nested_clocks', *args)
    EndCircuit()

    test_circuit = DefineCircuit('test_nested_clocks', *args)
    inner_test_circuit()
    EndCircuit()
    GetCoreIRModule(cirb, test_circuit)
