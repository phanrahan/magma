coreir = pytest.importorskip("coreir")
from magma import *


def test_coreir():
    class TestCircuit(Circuit):
        name = "test_coreir"
        IO = ["a", In(Bit), "b", In(Bit), "c", In(Bit), "d", Out(Bit)]
        @classmethod
        def definition(circuit):
            d = ~(circuit.a & circuit.b) | (circuit.b ^ circuit.c)
            wire(d, circuit.d)
    compile("build/test_coreir", TestCircuit, output="coreir")
    with open("build/test_coreir.json") as actual:
        with open("gold/test_coreir.json") as gold:
            assert actual.read() == gold.read()

if __name__ == "__main__":
    test_coreir()
