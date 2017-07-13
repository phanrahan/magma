from magma import *
from magma.backend import firrtl

def test_1_bit_logic():
    main = DefineCircuit('main', "a", In(Bit), "b", In(Bit), "c", Out(Bit))
    c = (main.a & main.b) ^ (main.a | main.b)
    wire(c, main.c)
    assert type(c) == Out(Bit)
    assert firrtl.compile(main) == """
circuit main :
  module And1 :
    input I0 : UInt<1>
    input I1 : UInt<1>
    output O : UInt<1>
    
    O <= and(I0, I1)
  module Or1 :
    input I0 : UInt<1>
    input I1 : UInt<1>
    output O : UInt<1>
    
    O <= or(I0, I1)
  module Xor1 :
    input I0 : UInt<1>
    input I1 : UInt<1>
    output O : UInt<1>
    
    O <= xor(I0, I1)
  module main :
    input a : UInt<1>
    input b : UInt<1>
    output c : UInt<1>
    
    wire inst0_O : UInt<1>
    wire inst1_O : UInt<1>
    wire inst2_O : UInt<1>
    inst inst0 of And1
    inst0.I0 <= a
    inst0.I1 <= b
    inst0.O <= inst0_O
    inst inst1 of Or1
    inst1.I0 <= a
    inst1.I1 <= b
    inst1.O <= inst1_O
    inst inst2 of Xor1
    inst2.I0 <= inst0_O
    inst2.I1 <= inst1_O
    inst2.O <= inst2_O
    c <= inst2_O
""".lstrip()

def test_bit_array_logic():
    main = DefineCircuit('main', "a", In(Array(8, Bit)), "b", In(Array(8, Bit)), "c", Out(Array(8, Bit)))
    c = (main.a & main.b) ^ (main.a | main.b)
    wire(c, main.c)
    assert type(c) == Out(Array(8, Bit))
    assert firrtl.compile(main) == """
circuit main :
  module And8 :
    input I0 : UInt<8>
    input I1 : UInt<8>
    output O : UInt<8>
    
    O <= and(I0, I1)
  module Or8 :
    input I0 : UInt<8>
    input I1 : UInt<8>
    output O : UInt<8>
    
    O <= or(I0, I1)
  module Xor8 :
    input I0 : UInt<8>
    input I1 : UInt<8>
    output O : UInt<8>
    
    O <= xor(I0, I1)
  module main :
    input a : UInt<8>
    input b : UInt<8>
    output c : UInt<8>
    
    wire inst0_O : UInt<8>
    wire inst1_O : UInt<8>
    wire inst2_O : UInt<8>
    inst inst0 of And8
    inst0.I0 <= a
    inst0.I1 <= b
    inst0.O <= inst0_O
    inst inst1 of Or8
    inst1.I0 <= a
    inst1.I1 <= b
    inst1.O <= inst1_O
    inst inst2 of Xor8
    inst2.I0 <= inst0_O
    inst2.I1 <= inst1_O
    inst2.O <= inst2_O
    c <= inst2_O
""".lstrip()
