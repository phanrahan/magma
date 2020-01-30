import magma as m

import sys
import os

TEST_SYNTAX_PATH = os.path.join(os.path.dirname(__file__), '../test_syntax')

sys.path.append(TEST_SYNTAX_PATH)

from test_sequential import DefineRegister, phi


def test_555():
    @m.circuit.sequential
    class A:
        def __call__(self, i: m.Bit) -> m.Bit:
            return i


    @m.circuit.sequential
    class B:
        def __init__(self):
            self.a0: A = A()
            self.a1: A = A()

        def __call__(self, i : m.Bit) -> m.Bit:
            if i:
                return self.a0(i)
            else:
                return self.a1(~i)
