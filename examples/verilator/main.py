from magma import *
from magma.verilator.verilator import compile as compileverilator
from mantle.verilog.gates import And, XOr

def f(a, b, c):
    return (a & b) ^ c

#main = DefineCircuit('main', "a", In(Bit), "b", In(Bit), "c", In(Bit), "d", Out(Bit), 'CLK', In(Bit))
main = DefineCircuit('main', "a", In(Bit), "b", In(Bit), "c", In(Bit), "d", Out(Bit))
t = And(2)(main.a,main.b)
d = XOr(2)(t,main.c)
wire(d,main.d)
EndCircuit()

compile("main", main)
compileverilator('sim_main.cpp', main, f)

#print(testvectors(main))

