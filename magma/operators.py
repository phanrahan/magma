from hwtypes import BitVector

from .digital import Digital
from .bit import Bit
from .bits import Bits
from .bitutils import clog2, seq2int
from .circuit import coreir_port_mapping
from .conversions import array, as_bits, from_bits
from .generator import Generator2
from .interface import IO
from .protocol_type import MagmaProtocol
from .t import Type, In, Out
from .tuple import Product
from .wire import wire
from magma.mux import Mux


def mux(I, S, **kwargs):
    if isinstance(S, Type) and S.const():
        S = seq2int(S.bits())
    if isinstance(S, int):
        return I[S]
    T = type(I[0])
    return Mux(len(I), T, **kwargs)()(*I, S)


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
