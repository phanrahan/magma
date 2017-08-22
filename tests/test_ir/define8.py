import sys
from magma import *
from magma.ir import compile

Array22 = Array(2, Array2)

And = DeclareCircuit('And', "I", In(Array22), "O", Out(Bit)) 

And4 = DefineCircuit("And4", "I0", In(Array2), "I1", In(Array2), "O", Out(Bit) )
and_ = And()
wire( And4.I0, and_.I[0] )
wire( And4.I1, and_.I[1] )
wire( and_.O, And4.O )
EndCircuit()

main = DefineCircuit("main", 
    "I0", In(Bit), "I1", In(Bit),
    "I2", In(Bit), "I3", In(Bit),
    "O", Out(Bit))
and4 = And4()
I0 = array([main.I0, main.I1]),
I1 = array([main.I2, main.I3])
O = and4(I0, I1)
main.O( O )
EndCircuit()

print(compile(main))
