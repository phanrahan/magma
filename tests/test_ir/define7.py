import sys
from magma import *
from magma.ir import compile

Array22 = Array(2, Array2)

And = DeclareCircuit('And', "I", In(Array22), "O", Out(Bit)) 

And4 = DefineCircuit("And4", "I", In(Array22), "O", Out(Bit) )
and_ = And()
wire( And4.I, and_.I )
wire( and_.O, And4.O )
EndCircuit()

main = DefineCircuit("main", 
    "I0", In(Bit), "I1", In(Bit), "I2", In(Bit), "I3", In(Bit),
    "O", Out(Bit))
and4 = And4()
I = array(array(main.I0, main.I1), array(main.I2, main.I3))
O = and4(I)
main.O( O )
EndCircuit()

print(compile(main))
