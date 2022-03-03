import math

from magma.common import deprecated


@deprecated(msg="Use bitutils.clog2 instead")
def log2_ceil(x: int) -> int:
    return math.ceil(math.log(x, 2))


@deprecated(msg="Use bitutils.flog2 instead")
def log2_floor(x: int) -> int:
    return math.floor(math.log(x, 2))


@deprecated(msg="Use bitutils.is_pow2 instead")
def is_pow2(x: int) -> bool:
    return log2_ceil(x) == log2_floor(x)
