import magma as m
import mantle

class FullAdder(m.Circuit):
    IO = ["a", m.In(m.Bit), "b", m.In(m.Bit), "cin", m.In(m.Bit),
          "out", m.Out(m.Bit), "cout", m.Out(m.Bit)]
    @classmethod
    def definition(io):
        # Generate the sum
        a_xor_b = io.a ^ io.b
        m.wire(a_xor_b ^ io.cin, io.out)
        # Generate the carry
        a_and_b = io.a & io.b
        b_and_cin = io.b & io.cin
        a_and_cin = io.a & io.cin
        m.wire(a_and_b | b_and_cin | a_and_cin, io.cout)


if __name__ == "__main__":
    from magma.simulator.python_simulator import PythonSimulator

    simulator = PythonSimulator(FullAdder)
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
        simulator.set_value(FullAdder.a, bool(a))
        simulator.set_value(FullAdder.b, bool(b))
        simulator.set_value(FullAdder.cin, bool(cin))
        simulator.evaluate()
        assert simulator.get_value(FullAdder.out) == bool(out)
        assert simulator.get_value(FullAdder.cout) == bool(cout)

    print("Success!")
