import functools
import math
from typing import List, Optional, Sequence, Tuple


__all__  = ['seq2int', 'int2seq']
__all__ += ['clog2', 'clog2safe']


def _seq2int_reducer(i: int, it: Tuple[int, int]):
    idx, li = it
    return i if not li else i | 1 << idx


def seq2int(l: Sequence) -> int:
    return functools.reduce(_seq2int_reducer, enumerate(l), 0)


def int2seq(i: int, n: Optional[int] = None) -> List[int]:
    bit_length = i.bit_length()
    if n is None:
        n = bit_length
    elif n < bit_length:
        raise ValueError("Insufficient number of bits")
    return [1 if i & (1 << j) else 0 for j in range(n)]


def clog2(x: int) -> int:
    return math.ceil(math.log(x, 2))


def clog2safe(x: int) -> int:
    if x == 1:
        return 1
    return clog2(x)
