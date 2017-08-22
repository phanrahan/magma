import sys
from magma import *

def test():
    And2 = DeclareCircuit('And2', "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))
    #print(And2)
    #print(And2.__name__)
    print(repr(And2))

    main = DefineCircuit("main", "I", In(Bits(2)), "O", Out(Bit) )

    and2 = And2()

    wire( main.I[0], and2.I0 )
    wire( main.I[1], and2.I1 )
    wire( and2.O, main.O )

    EndCircuit()

    print(main)
    print(main.__name__)
    print(repr(main))
    print(main.I)
    print(repr(main.I))
    print(and2.I0)
    print(repr(and2.I0))

test()
