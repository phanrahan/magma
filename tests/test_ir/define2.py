import sys
from magma import *
from magma.ir import compile

And2 = DeclareCircuit('And2', "I0", In(Bit), "I1", In(Bit), "O", Out(Bit)) 

AndN2 = DefineCircuit("And2", "I", In(Array2), "O", Out(Bit) )
and2 = And2()
wire( AndN2.I[0], and2.I0 )
wire( AndN2.I[1], and2.I1 )
wire( and2.O, AndN2.O )
EndCircuit()

main = DefineCircuit("main", "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))
and2 = AndN2()
main.O( and2(array(main.I0, main.I1)) )
EndCircuit()

print(compile(main))
