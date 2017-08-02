from magma import *

class FullAdder(Circuit):
    name = "FullAdder"
    IO = ["a", In(Bit), "b", In(Bit), "cin", In(Bit), "out", Out(Bit), "cout", Out(Bit)]
    @classmethod
    def definition(io):
        # Generate the sum
        a_xor_b = io.a ^ io.b
        wire(a_xor_b ^ io.cin, io.out)
        # Generate the carry
        a_and_b = io.a & io.b
        b_and_cin = io.b & io.cin
        a_and_cin = io.a & io.cin
        wire(a_and_b | b_and_cin | a_and_cin, io.cout)


if __name__ == "__main__":
    from magma.python_simulator import PythonSimulator
    from magma.scope import Scope

    simulator = PythonSimulator(FullAdder)
    scope = Scope()
    test_vectors = [
        [0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [1, 0, 0, 1, 0],
        [1, 1, 0, 0, 1],
        [0, 1, 1, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 1, 0, 0, 1],
        [1, 1, 1, 1, 1]
    ]

    for a, b, cin, out, cout in test_vectors:
        simulator.set_value(FullAdder.a, scope, bool(a))
        simulator.set_value(FullAdder.b, scope, bool(b))
        simulator.set_value(FullAdder.cin, scope, bool(cin))
        simulator.evaluate()
        assert simulator.get_value(FullAdder.out, scope) == bool(out)
        assert simulator.get_value(FullAdder.cout, scope) == bool(cout)

    print("Success!")
