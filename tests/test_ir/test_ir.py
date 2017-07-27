from magma import DeclareCircuit, DefineCircuit, EndCircuit, In, Out, Bit, \
    wire, Array, array
from mantle.lattice.mantle40 import And
from magma.ir import compile


def test_print_ir():

    And2 = DeclareCircuit('And2', "I0", In(Bit), "I1", In(Bit), "O", Out(Bit)) 

    AndN2 = DefineCircuit("And2", "I", In(Array(2, Bit)), "O", Out(Bit) ) 
    and2 = And2() 
    wire( AndN2.I[0], and2.I0 ) 
    wire( AndN2.I[1], and2.I1 ) 
    wire( and2.O, AndN2.O ) 
    EndCircuit() 

    main = DefineCircuit("main", "I0", In(Bit), "I1", In(Bit), "O", Out(Bit)) 
    and2 = AndN2() 
    main.O( and2(array(main.I0, main.I1)) ) 
    EndCircuit() 

    result = compile(main)
    assert result == """\
And2 = DefineCircuit("And2", "I", Array(2,In(Bit)), "O", Out(Bit))  # {filename} 11
inst0 = And2()  # {filename} 12
wire(And2.I[0], inst0.I0)  # {filename} 13
wire(And2.I[1], inst0.I1)  # {filename} 14
wire(inst0.O, And2.O)  # {filename} 15
EndCircuit()  # {filename} 16

main = DefineCircuit("main", "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))  # {filename} 18
inst0 = And2()  # {filename} 19
wire(main.I0, inst0.I[0])  # {filename} 20
wire(main.I1, inst0.I[1])  # {filename} 20
wire(inst0.O, main.O)  # {filename} 20
EndCircuit()  # {filename} 21

""".format(filename=__file__)
