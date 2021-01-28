from magma import sequential2
from magma import Bit


def test_545():
    @sequential2()
    class PE:
        def __call__(self, in0: Bit, in1: Bit) -> Bit:
            return in0 & in1
