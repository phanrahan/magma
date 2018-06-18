from full_adder import FullAdder

import magma as m
from magma.bitutils import int2seq

def DefineAdder(N):
    T = m.UInt(N)
    class Adder(m.Circuit):
        name = "Adder{}".format(N)
        IO = ["a", m.In(T), "b", m.In(T), "cin", m.In(m.Bit),
              "out", m.Out(T), "cout", m.Out(m.Bit)]
        @classmethod
        def definition(io):
            adders = [FullAdder() for _ in range(N)]
            circ = m.braid(adders, foldargs={"cin":"cout"})
            m.wire(io.a, circ.a)
            m.wire(io.b, circ.b)
            m.wire(io.cin, circ.cin)
            m.wire(io.cout, circ.cout)
            m.wire(io.out, circ.out)
    return Adder


if __name__ == "__main__":
    from magma.simulator.python_simulator import PythonSimulator
    from magma.bit_vector import BitVector

    Adder4 = DefineAdder(4)
    simulator = PythonSimulator(Adder4)
    simulator.set_value(Adder4.a, BitVector(2, num_bits=4))
    simulator.set_value(Adder4.b, BitVector(3, num_bits=4))
    simulator.set_value(Adder4.cin, True)
    simulator.evaluate()
    #assert simulator.get_value(Adder4.out) == int2seq(6, 4)
    assert simulator.get_value(Adder4.out) == BitVector(6, num_bits=4)
    assert simulator.get_value(Adder4.cout) == False
    print("Success!")
