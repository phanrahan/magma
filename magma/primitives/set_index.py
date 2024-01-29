from magma.array import Array
from collections.abc import Sequence
from typing import Union, Sequence as Sequnce_T

from magma.bits import UInt
from magma.bitutils import clog2
from magma.primitives import mux


def set_index(target: Array, value, idx: Union[UInt, Sequnce_T[UInt]]):
    """
    Returns a new value where index `idx` of `target` is set to `value`
    * `target` - a value of type `Array[N, T]` or `Array[(N, M, L, ...), T]`
    * `value` - a value of type `T`
    * `idx` - a value of type `UInt[clog2(N)]` or `(UInt[clog2(L)],
              UInt[clog2(M), UInt[clog2(N)], ...)`
    NOTE(rkshthrmsh): Ordering of indices in `idx` is reverse of ordering in
                      N-D Array definition.
    For more details see: https://github.com/phanrahan/magma/issues/1310.
    """
    if not isinstance(target, Array):
        raise TypeError("Expected target to be an array")

    if isinstance(idx, UInt):
        target_T = type(target)
        if not isinstance(value, target_T.T):
            raise TypeError(
                f"Expected `value` ({type(value)}) to be the same type as"
                f"`target`'s contents ({target_T.T})"
            )
        if len(idx) != clog2(len(target_T)):
            raise TypeError(
                f"Expected number of `idx` ({len(idx)}) bits to map to the "
                f"length of `target` ({clog2(len(target_T))})")
        return target_T([
            mux([elem, value], idx == i) for i, elem in enumerate(target)
        ])
    if isinstance(idx, Sequence):
        if len(idx) == 1:
            return set_index(target, value, idx[0])
        return set_index(target, set_index(target[idx[0]], value, idx[1:]),
                         idx[0])
    raise TypeError(
        f"Expected `idx` ({type(idx)}) to be UInt or List[UInt, ...] "
    )
