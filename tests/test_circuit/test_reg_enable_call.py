import magma as m
from magma.generator import ParamDict


def test_reg_enable_call():
    class test_reg_enable_call(m.Circuit):
        io = m.IO(I=m.In(m.Bits[5]), O=m.Out(m.Bits[5]), nen=m.In(m.Bit))
        io += m.ClockIO()
        reg = m.Register(m.Bits[5], has_enable=True,
                         name_map=ParamDict(CE="en"))()
        io.O @= reg(io.I, ~io.nen)

    assert repr(test_reg_enable_call) == """\
test_reg_enable_call = DefineCircuit("test_reg_enable_call", "I", In(Bits[5]), \
"O", Out(Bits[5]), "nen", In(Bit), "CLK", In(Clock))
magma_Bit_not_inst0 = magma_Bit_not()
reg = Register()
wire(test_reg_enable_call.nen, magma_Bit_not_inst0.in)
wire(test_reg_enable_call.I, reg.I)
wire(magma_Bit_not_inst0.out, reg.en)
wire(reg.O, test_reg_enable_call.O)
EndCircuit()\
"""
    m.compile("build/test_reg_enable_call", test_reg_enable_call)
