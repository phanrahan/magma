import sys
from magma import *
from magma.ir import compile

And2 = DeclareCircuit('And2', "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))

main = DefineCircuit("main", "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))
and2 = And2()
main.O(and2(main.I0,main.I1))
EndCircuit()

print(compile(main))


