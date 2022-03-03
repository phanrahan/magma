import math

from magma.common import deprecated


@deprecated(msg="Use bitutils.clog2 instead")
def log2_ceil(x: int) -> int:
    return math.ceil(math.log(x, 2))
