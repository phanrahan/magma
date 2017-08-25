import pytest
coreir = pytest.importorskip("coreir")
from magma import *
from magma.tests import magma_check_files_equal


def test_coreir_bit():
    class TestCircuit(Circuit):
        name = "test_coreir_bit"
        IO = ["a", In(Bit), "b", In(Bit), "c", In(Bit), "d", Out(Bit)]
        @classmethod
        def definition(circuit):
            d = ~(circuit.a & circuit.b) | (circuit.b ^ circuit.c)
            wire(d, circuit.d)
    compile("build/test_coreir_bit", TestCircuit, output="coreir")
    assert magma_check_files_equal(__file__, 
            "build/test_coreir_bit.json", "gold/test_coreir_bit.json")


def test_coreir_bits():
    class TestCircuit(Circuit):
        name = "test_coreir_bits"
        IO = ["a", In(Bits(4)), "b", In(Bits(4)), "c", In(Bits(4)), "d", Out(Bits(4))]
        @classmethod
        def definition(circuit):
            d = ~(circuit.a & circuit.b) | (circuit.b ^ circuit.c)
            wire(d, circuit.d)
    compile("build/test_coreir_bits", TestCircuit, output="coreir")
    assert magma_check_files_equal(__file__, 
            "build/test_coreir_bits.json", "gold/test_coreir_bits.json")


def test_coreir_uint():
    class TestCircuit(Circuit):
        name = "test_coreir_uint"
        IO = ["a", In(UInt(4)), "b", In(UInt(4)), "c", Out(UInt(4))]
        @classmethod
        def definition(circuit):
            tmp1 = circuit.a + circuit.b
            tmp2 = circuit.a - circuit.b
            tmp3 = tmp1 * tmp2
            tmp4 = tmp3 / circuit.a
            wire(tmp4, circuit.c)
    compile("build/test_coreir_uint", TestCircuit, output="coreir")
    assert magma_check_files_equal(__file__, 
            "build/test_coreir_uint.json", "gold/test_coreir_uint.json")

if __name__ == "__main__":
    test_coreir()
