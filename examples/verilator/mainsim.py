import os
os.environ['MANTLE'] = 'lattice'

from magma import *
from mantle import And, XOr
from simulator import testvectors

main = DefineCircuit('main', "a", In(Bit), "b", In(Bit), "c", In(Bit), "d", Out(Bit), 'CLK', In(Bit))
t = And(2)(main.a,main.b)
d = XOr(2)(t,main.c)
wire(d,main.d)
EndCircuit()

print(testvectors(main))

