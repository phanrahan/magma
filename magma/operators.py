from .circuit import Circuit, DeclareCoreirCircuit
from .array import Array
from .bits import Bits
from .conversions import array
from .t import Type, In, Out
from .tuple import Product
from .bitutils import clog2
from .generator import Generator
from .frontend.coreir_ import DefineCircuitFromGeneratorWrapper, GetCoreIRBackend
from .wire import wire


class CoreIRCommonLibMuxN(Generator):
    @staticmethod
    def generate(N: int, width: int):
        return DeclareCoreirCircuit(f"coreir_commonlib_mux{N}x{width}",
            *["I", In(Product.from_fields("anon",
                                          dict(data=Array[N, Bits[width]],
                                               sel=Bits[clog2(N)]))),
              "O", Out(Bits[width])],
            coreir_name="muxn",
            coreir_lib="commonlib",
            coreir_genargs={"width": width, "N": N}
        )

class Mux(Generator):
    @staticmethod
    def generate(height: int, T: Type):
        # TODO: Type must be hashable so we can cache
        N = T.flat_length()
        class Mux(Circuit):
            IO = []
            for i in range(height):
                IO += [f"I{i}", In(T)]
            IO += ["S", In(Bits[clog2(height)])]
            IO += ["O", Out(T)]
            @classmethod
            def definition(io):
                mux = CoreIRCommonLibMuxN(height, N)
                wire(mux.I.data, array(
                    [Bits[N](getattr(io, f"I{i}").flatten()) 
                     for i in range(height)]
                ))
                wire(mux.I.sel, io.S)
                wire(mux.O, io.O)
        return Mux


def slice(value: Bits, start: Bits, width: int):
    """
    Dynamic slice based off the value of `start` with constant `width`

    Example:
    ```
    class TestSlice(m.Circuit):
        # Slice a 6 bit window of I using x as the start index
        IO = [
            "I", m.In(m.Bits[10]), 
            "x", m.In(m.Bits[2]), 
            "O", m.Out(m.Bits[6])
        ]

        @classmethod
        def definition(io):
            io.O @= m.slice(io.I, start=io.x, width=6)
    ```

    Notes:
    * For now we only support slicing bits with bits index
    * We could add support for slicing Arrays
    * We could restrict index to be a UInt
    """
    # Construct an array where the index `i` is the slice of bits from `i` to
    # `i+width`, index into this array using `start`
    return array([value[i:i+width] for i in range(len(value) - width)])[start]