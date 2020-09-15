import os
import operator

import pytest

import magma as m
from magma.testing import check_files_equal
from magma.simulator import PythonSimulator

import fault


@pytest.mark.parametrize('op, method', [
    (operator.and_, "reduce_and"),
    (operator.or_, "reduce_or"),
    (operator.xor, "reduce_xor")
])
def test_reduce(op, method):
    class test_reduce(m.Circuit):
        name = f"test_reduce_{op.__name__}"
        io = m.IO(I=m.In(m.Bits[5]), O0=m.Out(m.Bit), O1=m.Out(m.Bit))

        io.O0 @= m.reduce(op, io.I)
        io.O1 @= getattr(io.I, method)()

    m.compile(f'build/test_reduce_{op.__name__}', test_reduce, inline=True)

    assert check_files_equal(__file__, f"build/test_reduce_{op.__name__}.v",
                             f"gold/test_reduce_{op.__name__}.v")

    sim = PythonSimulator(test_reduce)
    tester = fault.Tester(test_reduce)

    tester.circuit.I = 2
    sim.set_value(test_reduce.I, 2)

    tester.eval()
    sim.evaluate()

    if op == operator.and_:
        tester.circuit.O0.expect(0)
        tester.circuit.O1.expect(0)
        assert sim.get_value(test_reduce.O0) == 0
        assert sim.get_value(test_reduce.O1) == 0
    else:
        tester.circuit.O0.expect(1)
        tester.circuit.O1.expect(1)
        assert sim.get_value(test_reduce.O0) == 1
        assert sim.get_value(test_reduce.O1) == 1

    tester.circuit.I = (1 << 5) - 1
    sim.set_value(test_reduce.I, (1 << 5) - 1)

    tester.eval()
    sim.evaluate()

    tester.circuit.O0.expect(1)
    tester.circuit.O1.expect(1)
    assert sim.get_value(test_reduce.O0) == 1
    assert sim.get_value(test_reduce.O1) == 1

    tester.circuit.I = 0
    sim.set_value(test_reduce.I, 0)

    tester.eval()
    sim.evaluate()

    tester.circuit.O0.expect(0)
    tester.circuit.O1.expect(0)
    assert sim.get_value(test_reduce.O0) == 0
    assert sim.get_value(test_reduce.O1) == 0

    tester.compile_and_run("verilator", skip_compile=True,
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))
