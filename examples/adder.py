import sys
from full_adder import FullAdder

from magma import *

def DefineAdder(N):
    T = UInt(N)
    class Adder(Circuit):
        name = "Adder{}".format(N)
        IO = ["a", In(T), "b", In(T), "cin", In(Bit), "out", Out(T), "cout", Out(Bit)]
        @classmethod
        def definition(io):
            adders = [FullAdder() for _ in range(N)]
            circ = braid(adders, foldargs={"cin":"cout"})
            wire(io.a, circ.a)
            wire(io.b, circ.b)
            wire(io.cin, circ.cin)
            wire(io.cout, circ.cout)
            wire(io.out, circ.out)
    return Adder


if __name__ == "__main__":
    from magma.python_simulator import PythonSimulator
    from magma.scope import Scope
    from magma.bit_vector import BitVector

    Adder4 = DefineAdder(4)
    simulator = PythonSimulator(Adder4)
    scope = Scope()
    simulator.set_value(Adder4.a, scope, BitVector(2, num_bits=4).as_bool_list())
    simulator.set_value(Adder4.b, scope, BitVector(3, num_bits=4).as_bool_list())
    simulator.set_value(Adder4.cin, scope, True)
    simulator.evaluate()
    assert simulator.get_value(Adder4.out, scope) == int2seq(6, 4)
    assert simulator.get_value(Adder4.cout, scope) == False
    print("Success!")
