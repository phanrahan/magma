from .array import Array
from .bits import Bits
from .bitutils import clog2
from .circuit import coreir_port_mapping
from .conversions import array
from .generator import Generator2
from .interface import IO
from .t import Type, In, Out
from .tuple import Product
from .wire import wire


class CoreIRCommonLibMuxN(Generator2):
    def __init__(self, N: int, width: int):
        self.name = f"coreir_commonlib_mux{N}x{width}"
        MuxInT = Product.from_fields("anon", dict(data=Array[N, Bits[width]],
                                                  sel=Bits[clog2(N)]))
        self.io = IO(I=In(MuxInT), O=Out(Bits[width]))
        self.renamed_ports = coreir_port_mapping
        self.coreir_name = "muxn"
        self.coreir_lib = "commonlib"
        self.coreir_genargs = {"width": width, "N": N}


class Mux(Generator2):
    def __init__(self, height: int, T: Type):
        # TODO: Type must be hashable so we can cache.
        N = T.flat_length()

        io_dict = {}
        for i in range(height):
            io_dict[f"I{i}"] = In(T)
        io_dict["S"] = In(Bits[clog2(height)])
        io_dict["O"] = Out(T)

        self.name = "Mux"
        self.io = IO(**io_dict)
        mux = CoreIRCommonLibMuxN(height, N)()
        data = [Bits[N](getattr(self.io, f"I{i}").flatten())
                for i in range(height)]
        wire(mux.I.data, array(data))
        wire(mux.I.sel, self.io.S)
        wire(mux.O, self.io.O)


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
