import functools
import math
from typing import List, Optional, Sequence, Tuple

import hwtypes


__all__  = ['seq2int', 'int2seq']
__all__ += ['clog2', 'clog2safe']


# TODO(rsetaluri): We should deprecate this function and invoke the hwtypes
# versions directly at the call sites.
def seq2int(l: Sequence) -> int:
    return int(hwtypes.BitVector[len(l)](l))


# TODO(rsetaluri): We should deprecate this function and invoke the hwtypes
# versions directly at the call sites.
def int2seq(i: int, n: Optional[int] = None) -> List[int]:
    bit_length = i.bit_length()
    if n is None:
        n = bit_length
    elif n < bit_length:
        raise ValueError("Insufficient number of bits")
    return hwtypes.BitVector[n](i).bits()


def clog2(x: int) -> int:
    return math.ceil(math.log(x, 2))


def clog2safe(x: int) -> int:
    if x == 1:
        return 1
    return clog2(x)
