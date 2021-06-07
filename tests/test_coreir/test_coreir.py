from magma.frontend.coreir_ import GetCoreIRModule
from magma.backend.coreir.coreir_utils import check_magma_interface
from magma.backend.coreir.coreir_backend import CoreIRBackend
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
        io = IO(I=In(Bit), O=Out(Bit))
        wire(io.I, io.O)
    backend = magma.backend.coreir.coreir_backend.CoreIRBackend()
    check_magma_interface(TestCircuit0.interface)


def test_check_interface_array():
    """
    This should work with valid types
    """
    class TestCircuit1(Circuit):
        name = "TestCircuit1"
        io = IO(I=In(Array[8, Bit]), O=Out(Array[8, Bit]))
        wire(io.I, io.O)
    backend = magma.backend.coreir.coreir_backend.CoreIRBackend()
    check_magma_interface(TestCircuit1.interface)


def test_check_interface_tuple():
    """
    This should work with valid types
    """

    class T(Product):
        a = Bit
        b = Array[7, Bit]

    class TestCircuit2(Circuit):
        name = "TestCircuit2"
        io = IO(I=In(T), O=Out(T))
        wire(io.I, io.O)
    backend = magma.backend.coreir.coreir_backend.CoreIRBackend()
    check_magma_interface(TestCircuit2.interface)


def test_nested_clocks():
    c = coreir.Context()
    cirb = CoreIRBackend(c)
    args = ['clocks', In(Array[2, Clock])]

    class inner_test_circuit(Circuit):
        name = "inner_test_nested_clocks"
        io = IO(**dict(zip(args[::2], args[1::2])))

    class test_circuit(Circuit):
        name = "test_nested_clocks"
        io = IO(**dict(zip(args[::2], args[1::2])))
        inner_test_circuit()(io.clocks)
    GetCoreIRModule(cirb, test_circuit)
