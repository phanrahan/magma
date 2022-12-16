from magma import Circuit, IO, In, Out, Bit, wire, Array, array
from magma.ir import compile


def test_print_ir():

    class _And2(Circuit):
        name = "And2"
        io = IO(I0=In(Bit), I1=In(Bit), O=Out(Bit))

    class _AndN2(Circuit):
        name = "AndN2"
        io = IO(I=In(Array[2, Bit]), O=Out(Bit))
        and2 = _And2()
        wire( io.I[0], and2.I0 )
        wire( io.I[1], and2.I1 )
        wire( and2.O, io.O )

    class main(Circuit):
        name = "main"
        io = IO(I0=In(Bit), I1=In(Bit), O=Out(Bit))
        and2 = _AndN2()
        io.O( and2(array([io.I0, io.I1])) )

    result = compile(main)
    #print(result)
    assert result == """\
AndN2 = DefineCircuit("AndN2", "I", Array[(2, In(Bit))], "O", Out(Bit))
And2_inst0 = And2()
wire(AndN2.I[0], And2_inst0.I0)
wire(AndN2.I[1], And2_inst0.I1)
wire(And2_inst0.O, AndN2.O)
EndCircuit()
main = DefineCircuit("main", "I0", In(Bit), "I1", In(Bit), "O", Out(Bit))
AndN2_inst0 = AndN2()
wire(main.I0, AndN2_inst0.I[0])
wire(main.I1, AndN2_inst0.I[1])
wire(AndN2_inst0.O, main.O)
EndCircuit()
"""
