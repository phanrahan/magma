import magma as m
import fault as f


def test_register():
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bits[4]), O=m.Out(m.Bits[4]))
        io += m.ClockIO(has_reset=True)
        io.O @= m.Register(
            m.Bits[4], reset_type=m.Reset
        )()(io.I)

    tester = f.PythonTester(Foo, Foo.CLK)
    tester.circuit.I = 3
    tester.step(2)
    tester.circuit.O.expect(3)
