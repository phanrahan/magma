from magma.bit import Bit
from magma.conversions import bits
from magma.bits import Bits, UInt
from magma.primitives import mux


def set_bit(target: Bits, value: Bit, idx: UInt):
    """
    Returns a new value where index `idx` of value `target` is set to `value`
    """
    return bits([
        mux([bit, value], idx == i) for i, bit in enumerate(target)
    ])
