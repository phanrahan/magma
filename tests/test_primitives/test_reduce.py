import os
import operator

import pytest

import magma as m
from magma.testing import check_files_equal
from magma.simulator import PythonSimulator

import fault


@pytest.mark.parametrize('op', [operator.and_, operator.or_, operator.xor])
def test_reduce(op):
    class test_reduce(m.Circuit):
        name = f"test_reduce_{op.__name__}"
        io = m.IO(I=m.In(m.Bits[5]), O=m.Out(m.Bit))

        io.O @= m.reduce(op, io.I)

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
        tester.circuit.O.expect(0)
        assert sim.get_value(test_reduce.O) == 0
    else:
        tester.circuit.O.expect(1)
        assert sim.get_value(test_reduce.O) == 1

    tester.circuit.I = (1 << 5) - 1
    sim.set_value(test_reduce.I, (1 << 5) - 1)

    tester.eval()
    sim.evaluate()

    tester.circuit.O.expect(1)
    assert sim.get_value(test_reduce.O) == 1

    tester.circuit.I = 0
    sim.set_value(test_reduce.I, 0)

    tester.eval()
    sim.evaluate()

    tester.circuit.O.expect(0)
    assert sim.get_value(test_reduce.O) == 0

    tester.compile_and_run("verilator", skip_compile=True,
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))
