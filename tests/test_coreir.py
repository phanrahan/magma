import pytest
coreir = pytest.importorskip("coreir")
from magma import *


def test_coreir_bit():
    class TestCircuit(Circuit):
        name = "test_coreir_bit"
        IO = ["a", In(Bit), "b", In(Bit), "c", In(Bit), "d", Out(Bit)]
        @classmethod
        def definition(circuit):
            d = ~(circuit.a & circuit.b) | (circuit.b ^ circuit.c)
            wire(d, circuit.d)
    compile("build/test_coreir_bit", TestCircuit, output="coreir")
    with open("build/test_coreir_bit.json") as actual:
        with open("gold/test_coreir_bit.json") as gold:
            assert actual.read() == gold.read()


def test_coreir_bits():
    class TestCircuit(Circuit):
        name = "test_coreir_bits"
        IO = ["a", In(Bits(4)), "b", In(Bits(4)), "c", In(Bits(4)), "d", Out(Bits(4))]
        @classmethod
        def definition(circuit):
            d = ~(circuit.a & circuit.b) | (circuit.b ^ circuit.c)
            wire(d, circuit.d)
    compile("build/test_coreir_bits", TestCircuit, output="coreir")
    with open("build/test_coreir_bits.json") as actual:
        with open("gold/test_coreir_bits.json") as gold:
            assert actual.read() == gold.read()

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
    with open("build/test_coreir_uint.json") as actual:
        with open("gold/test_coreir_uint.json") as gold:
            assert actual.read() == gold.read()

if __name__ == "__main__":
    test_coreir()
