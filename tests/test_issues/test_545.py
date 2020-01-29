from magma.circuit import sequential
from magma import Bit

import sys
import os

TEST_SYNTAX_PATH = os.path.join(os.path.dirname(__file__), '../test_syntax')

sys.path.append(TEST_SYNTAX_PATH)

from test_sequential import DefineRegister, phi

def test_545():
    @sequential
    class PE:
        def __call__(self, in0: Bit, in1: Bit) -> Bit:
            return in0 & in1

