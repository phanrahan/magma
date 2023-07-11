import pytest
try:
    import coreir
except ImportError:
    pytest.skip("Missing coreir", allow_module_level=True)
import magma as m
from magma.passes.elaborate_circuit import elaborate_all_pass
import fault as f


def test_register():
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bits[4]), O=m.Out(m.Bits[4]))
        io += m.ClockIO(has_reset=True)
        io.O @= m.Register(
            m.Bits[4], reset_type=m.Reset
        )()(io.I)

    elaborate_all_pass(Foo, generators=(m.Mux,))

    tester = f.PythonTester(Foo, Foo.CLK)
    tester.circuit.I = 3
    tester.step(2)
    tester.circuit.O.expect(3)
