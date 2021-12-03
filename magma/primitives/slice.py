from magma.bit import Bit
from magma.bits import Bits, UInt
from magma.bitutils import clog2
from magma.common import deprecated
from magma.t import Direction
from magma.conversions import array, zext, uint
from magma.protocol_type import magma_type


def get_slice(value: Bits, start: Bits, width: int):
    """
    Dynamic slice based off the value of `start` with constant `width`.

    Example:
    ```
    class TestSlice(m.Circuit):
        # Slice a 6 bit window of I using x as the start index
        IO = m.IO(
            I=m.In(m.Bits[10]),
            x=m.In(m.Bits[2]),
            O=m.Out(m.Bits[6])
        )

        io.O @= m.get_slice(io.I, start=io.x, width=6)
    ```

    Notes:
      * For now we only support slicing bits with bits index
      * We could add support for slicing Arrays
      * We could restrict index to be a UInt
    """
    # Construct an array where the index `i` is the slice of bits from `i` to
    # `i+width`, index into this array using `start`.
    return array([value[i:i + width] for i in range(len(value) - width)])[start]


@deprecated(msg="m.slice will not be supported in future versions, use "
            "m.get_slice instead")
def slice(*args, **kwargs):
    return get_slice(*args, **kwargs)


def set_slice(target: Bits, value: Bits, start: UInt, width: int):
    """
    target: the output with a dynamic slice range replaced by value
    value: the output driving a slice of target
    start: dynamic start index of the slice
    width: constant slice width
    """
    if not isinstance(start, UInt):
        raise TypeError("start should be a UInt")
    T = magma_type(type(target))
    output = T.qualify(Direction.Undirected)()
    orig_start_len = len(start)
    if len(start) < clog2(len(target)):
        start = zext(start, clog2(len(target)) - len(start))
    for i in range(len(target)):
        in_slice_range = Bit(True)
        # guards to avoid constant compare verilator error
        if i < (1 << orig_start_len) - 1:
            in_slice_range &= start <= i
        if i > 0:
            in_slice_range &= i <= (start + width - 1)
        value_idx = (uint(i, clog2(len(target))) - start)[:clog2(len(value))]
        if len(value_idx) == 1:
            value_idx = value_idx[0]
        output[i] @= in_slice_range.ite(value[value_idx], target[i])
    return output
