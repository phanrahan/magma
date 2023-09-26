from magma.array import Array
from magma.bits import UInt
from magma.bitutils import clog2
from magma.primitives import mux
from typing import Union, List

def set_index(target: Array, value, idx: Union[UInt, List[UInt]]):
    """
    Returns a new value where index `idx` of `target` is set to `value`
    * `target` - a value of type `Array[N, T]` or `Array[(N, M, ..), T]`
    * `value` - a value of type `T`
    * `idx` - a value of type `UInt[clog2(N)]` or `[UInt[clog2(M)], UInt[clog2(N)], ..]`
    NOTE: Ordering of indices in `idx` is reverse of ordering in N-D Array definition.
    More details: https://github.com/phanrahan/magma/issues/1310
    """
    if not isinstance(target, Array):
        raise TypeError("Expected target to be an array")

    if isinstance(idx, list):
        if len(idx) > 1:
            return set_index(target,
                             set_index(target[idx[0]], value, idx[1:]),
                             idx[0])
        else: # len(idx) == 1
            return set_index(target, value, idx[0])
    elif isinstance(idx, UInt):
        target_T = type(target)
        if not isinstance(value, target_T.T):
            raise TypeError(
                (f"Expected `value` ({type(value)}) to be the same type as"
                f"`target`'s contents ({target_T.T})"))
        if not isinstance(idx, UInt):
            raise TypeError("Expected `idx` ({type(idx)}) to be a UInt")
        if len(idx) != clog2(len(target_T)):
            raise TypeError(
                (f"Expected number of `idx` ({len(idx)}) bits to map to the length of"
                f"`target` ({clog2(len(target_T))})"))

        return target_T([
            mux([elem, value], idx == i) for i, elem in enumerate(target)
        ])
    else:
        raise TypeError(f"Expected `idx` ({type(idx)}) to be UInt or List[UInt, ...] ")
