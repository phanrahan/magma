import sys
from magma import *

def test():
    class And2(Circuit):
        name = "And2"
        io = IO(I0=In(Bit), I1=In(Bit), O=Out(Bit))
    print(repr(And2))

    and2 = And2()
    and2.name = 'and2'
    print(repr(and2))
    print(repr(and2.I0))

    and2anon1 = AnonymousCircuit("I", and2.I0, "O", and2.O)
    and2anon1.name = 'and2anon1'
    print(repr(and2anon1))
    print(repr(and2anon1.I))

    and2anon = AnonymousCircuit("I", array([and2.I0, and2.I1]), "O", and2.O)
    and2anon.name = 'and2anon'
    print(repr(and2anon))
    print(repr(and2anon.I))
    print(repr(and2anon.I[0]))
    print(repr(and2anon.O))

test()
