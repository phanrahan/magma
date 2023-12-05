import pytest
from typing import Optional

import magma as m
from magma.passes.passes import CircuitPass
import magma.testing


class _MyWrapperGen(m.Generator):
    def __init__(self, width: Optional[int]):
        T = m.Bits[width] if width is not None else m.Bit
        self.io = io = m.IO(I=m.In(T), O=m.Out(T)) + m.ClockIO()
        m.inline_verilog(
            f"reg [{width - 1}:0] R;\nasssign R <= {{I}};\n",
            I=io.I
        )
        io.O @= m.InlineVerilogExpression("R | I", T)()()

        self.name = f"MyWrapperGen_{width}"


class _Top(m.Circuit):
    name = "Top"
    T = m.Bits[2]
    io = m.IO(I=m.In(T), O=m.Out(T)) + m.ClockIO()
    tmp = _MyWrapperGen(1)()(m.bits([io.I[0]]))
    tmp = m.bits([tmp[0]] * len(T))
    io.O @= _MyWrapperGen(2)()(tmp)


class _BuildRepr(CircuitPass):
    def __init__(self, main):
        super().__init__(main)
        self._repr_str = ""

    def __call__(self, ckt):
        self._repr_str += repr(ckt) + "\n\n"

    @property
    def repr_str(self) -> str:
        return self._repr_str


def test_basic():
    expected = \
"""InlineVerilog_1c808aa902d1c7bf = DeclareCircuit("InlineVerilog_1c808aa902d1c7bf", "I0", In(Bits[1]))

InlineVerilogExpression_Bits1_a489b4461c0192fc = DeclareCircuit("InlineVerilogExpression_Bits1_a489b4461c0192fc", "O", Out(Bits[1]))

MyWrapperGen_1 = DefineCircuit("MyWrapperGen_1", "I", In(Bits[1]), "O", Out(Bits[1]), "CLK", In(Clock))
InlineVerilog_1c808aa902d1c7bf_inst0 = InlineVerilog_1c808aa902d1c7bf()
InlineVerilogExpression_Bits1_a489b4461c0192fc_inst0 = InlineVerilogExpression_Bits1_a489b4461c0192fc()
wire(MyWrapperGen_1.I, InlineVerilog_1c808aa902d1c7bf_inst0.I0)
wire(InlineVerilogExpression_Bits1_a489b4461c0192fc_inst0.O, MyWrapperGen_1.O)
EndCircuit()

InlineVerilog_4e1d0f2526d96566 = DeclareCircuit("InlineVerilog_4e1d0f2526d96566", "I0", In(Bits[2]))

InlineVerilogExpression_Bits2_a489b4461c0192fc = DeclareCircuit("InlineVerilogExpression_Bits2_a489b4461c0192fc", "O", Out(Bits[2]))

MyWrapperGen_2 = DefineCircuit("MyWrapperGen_2", "I", In(Bits[2]), "O", Out(Bits[2]), "CLK", In(Clock))
InlineVerilog_4e1d0f2526d96566_inst0 = InlineVerilog_4e1d0f2526d96566()
InlineVerilogExpression_Bits2_a489b4461c0192fc_inst0 = InlineVerilogExpression_Bits2_a489b4461c0192fc()
wire(MyWrapperGen_2.I, InlineVerilog_4e1d0f2526d96566_inst0.I0)
wire(InlineVerilogExpression_Bits2_a489b4461c0192fc_inst0.O, MyWrapperGen_2.O)
EndCircuit()

Top = DefineCircuit("Top", "I", In(Bits[2]), "O", Out(Bits[2]), "CLK", In(Clock))
MyWrapperGen_1_inst0 = MyWrapperGen_1()
MyWrapperGen_2_inst0 = MyWrapperGen_2()
wire(Top.I[0], MyWrapperGen_1_inst0.I[0])
wire(MyWrapperGen_1_inst0.O[0], MyWrapperGen_2_inst0.I[0])
wire(MyWrapperGen_1_inst0.O[0], MyWrapperGen_2_inst0.I[1])
wire(MyWrapperGen_2_inst0.O, Top.O)
EndCircuit()

"""
    p = _BuildRepr(_Top)
    p.run()
    assert p.repr_str == expected


def test_compilation_coreir():
    with pytest.raises(NotImplementedError) as e:
        m.compile("", _Top, output="coreir")


def test_compilation_mlir():
    basename = f"test_inline_verilog_expression_compilation_mlir"
    m.compile(f"build/{basename}", _Top, output="mlir")
    assert m.testing.check_files_equal(
        __file__, f"build/{basename}.mlir", f"gold/{basename}.mlir")
