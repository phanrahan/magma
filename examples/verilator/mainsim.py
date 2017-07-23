import os
os.environ['MANTLE'] = 'lattice'

from magma import *
from mantle import And2, Xor2
from simulator import testvectors

main = DefineCircuit('main', "a", In(Bit), "b", In(Bit), "c", In(Bit), "d", Out(Bit), 'CLK', In(Bit))
t = And2()(main.a,main.b)
d = Xor2()(t,main.c)
wire(d,main.d)
EndCircuit()

print(testvectors(main))

