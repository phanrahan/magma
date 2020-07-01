from magma.bits import Bits, UInt
from magma.bitutils import clog2
from magma.t import Direction
from magma.conversions import array, zext, uint


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


def set_slice(target: Bits, value: Bits, start: UInt, width: int):
    """
    target: the output with a dynamic slice range replaced by value
    value: the output driving a slice of target
    start: dynamic start index of the slice
    width: constant slice width
    default_value: the value to use to wire to target if it is not in the slice
                   range (driven by value)
    """
    output = type(target).qualify(Direction.Undirected)()
    start = zext(start, clog2(len(target)) - len(start))
    for i in range(len(target)):
        # Can't write start <= i < (start + width) because that implicitly
        # calls __bool__?
        in_slice_range = (start <= i) & (i < (start + width))
        output[i] @= in_slice_range.ite(value[uint(i, clog2(len(target))) -
                                              start], target[i])
    return output
