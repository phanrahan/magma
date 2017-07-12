from magma import *
from magma.backend import firrtl

def test_and():
    main = DefineCircuit('main', "a", In(Bit), "b", In(Bit), "c", Out(Bit))
    c = main.a & main.b
    wire(c, main.c)
    assert type(c) == Out(Bit)
    assert firrtl.compile(main) == """
circuit main :
  module And1 :
    input I0 : UInt<1>
    input I1 : UInt<1>
    output O : UInt<1>
    
    O <= and(I0, I1)
  module main :
    input a : UInt<1>
    input b : UInt<1>
    output c : UInt<1>
    
    wire inst0_O : UInt<1>
    inst inst0 of And1
    inst0.I0[0] <= inst0_I0[0]
    inst0.I1[0] <= inst0_I1[0]
    inst0.O[0] <= inst0_O[0]
    c <= inst0_O[0]
""".lstrip()
