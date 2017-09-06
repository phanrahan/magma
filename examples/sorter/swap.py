from magma import Circuit, Bits, In, Out, wire, fork, join, flat, uncurry, map_
from magma.primitives import And, Or

__all__  = ['Swap',  'swap']
__all__ += ['DefineSwap', 'Swaps', 'swaps']

#
# Binary swap circuit
#
class Swap(Circuit):
    IO = ['I', In(Bits(2)), "O", Out(Bits(2))]
    @classmethod
    def definition(io):
        swap = uncurry( fork( And(2), Or(2) ) , prefix="in")
        wire( swap( io.I ), io.O )

def swap(I):
    return Swap()(I)

def DefineSwaps(n):
    class Swaps(Circuit):
        name = 'Swap{}'.format(n)
        IO = ['I', In(Bits(n)), "O", Out(Bits(n))]
        @classmethod
        def definition(io):
            s = flat( join( map_(Swap, n//2) ), flatargs = ['I', 'O'] )
            wire(s(io.I), io.O)
    return Swaps

def Swaps(n):
    return DefineSwaps(n)()

def swaps(I):
    n = len(I)
    return Swaps(n)(I)
