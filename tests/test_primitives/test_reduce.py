import operator
import os
import pytest

import fault

import magma as m
from magma.testing import check_files_equal


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

    tester = fault.Tester(test_reduce)

    tester.circuit.I = 2

    tester.eval()

    if op == operator.and_:
        tester.circuit.O0.expect(0)
        tester.circuit.O1.expect(0)
    else:
        tester.circuit.O0.expect(1)
        tester.circuit.O1.expect(1)

    tester.circuit.I = (1 << 5) - 1

    tester.eval()

    tester.circuit.O0.expect(1)
    tester.circuit.O1.expect(1)

    tester.circuit.I = 0

    tester.eval()

    tester.circuit.O0.expect(0)
    tester.circuit.O1.expect(0)

    tester.compile_and_run("verilator", skip_compile=True,
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))
