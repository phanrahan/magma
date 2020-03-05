import sys
from magma import *
from magma.ir import compile

class And2(Circuit):
    name = "And2"
    io = IO(I0=In(Bit), I1=In(Bit), O=Out(Bit))

main = DefineCircuit("main", "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))
and2 = And2()
main.O(and2(main.I0,main.I1))
EndCircuit()

print(compile(main))


