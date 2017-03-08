import sys
from magma import *
from magma.ir import compile


Tuple2 = Tuple(x=Bit, y=Bit)

And2 = DeclareCircuit('And2', "I0", In(Bit), "I1", In(Bit), "O", Out(Bit)) 

AndN2 = DefineCircuit("And2", "I", In(Tuple2), "O", Out(Bit) )
and2 = And2()
wire( AndN2.I.x, and2.I0 )
wire( AndN2.I.y, and2.I1 )
wire( and2.O, AndN2.O )
EndCircuit()

main = DefineCircuit("main", "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))
and2 = AndN2()
main.O( and2(tuple_(x=main.I0, y=main.I1)) )
EndCircuit()

print(compile(main))
