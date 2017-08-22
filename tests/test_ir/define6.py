import sys
from magma import *
from magma.ir import compile

Tuple2 = Tuple('x', Bit, 'y', Bit)

And = DeclareCircuit('And', "I", In(Array(2,Tuple2)), "O", Out(Bit)) 

And4 = DefineCircuit("And4", "I", In(Array4), "O", Out(Bit) )
and_ = And()
wire( And4.I[0], and_.I[0].x )
wire( And4.I[1], and_.I[0].y )
wire( And4.I[2], and_.I[1].x )
wire( And4.I[3], and_.I[1].y )
wire( and_.O, And4.O )
EndCircuit()

main = DefineCircuit("main", 
    "I0", In(Bit), "I1", In(Bit), "I2", In(Bit), "I3", In(Bit),
    "O", Out(Bit))
and4 = And4()
I = array([main.I0, main.I1, main.I2, main.I3])
main.O( and4(I) )
EndCircuit()

print(compile(main))
