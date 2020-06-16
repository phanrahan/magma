from magma.bits import Bits
from magma.conversions import array


def slice(value: Bits, start: Bits, width: int):
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

        io.O @= m.slice(io.I, start=io.x, width=6)
    ```

    Notes:
      * For now we only support slicing bits with bits index
      * We could add support for slicing Arrays
      * We could restrict index to be a UInt
    """
    # Construct an array where the index `i` is the slice of bits from `i` to
    # `i+width`, index into this array using `start`.
    return array([value[i:i + width] for i in range(len(value) - width)])[start]
