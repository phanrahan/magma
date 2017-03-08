import sys
from magma import *
from magma.ir import compile

Buf = DeclareCircuit('Buf', "I", In(Bit), "O", Out(Bit))

main = DefineCircuit("main", "I", In(Bit), "O", Out(Bit))

buf = Buf()
wire(main.I, buf[0])
wire(buf[1], main.O)

print(compile(main))


