from magma.array import Array
from magma.bits import UInt
from magma.bitutils import clog2
from magma.primitives import mux


def set_index(target: Array, value, idx: UInt):
    """
    Returns a new value where index `idx` of value `target` is set to `value`
    * `target` - a value of type `Array[N, T]`
    * `value` - a value of type `T`
    * `idx` - a value of type `UInt[clog2(N)]`
    """
    if not isinstance(target, Array):
        raise TypeError("Expected target to be an array")
    target_T = type(target)
    if not isinstance(value, target_T.T):
        raise TypeError(
            "Expected value to be the same type as `target`'s contents")
    if not isinstance(idx, UInt):
        raise TypeError("Expected `idx` to be a UInt")
    if len(idx) != clog2(len(target_T)):
        raise TypeError(
            "Expected number of `idx` bits to map to the length of `target`")

    return target_T([
        mux([elem, value], idx == i) for i, elem in enumerate(target)
    ])
