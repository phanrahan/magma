import pytest
from typing import Optional

import magma as m
from magma.passes.passes import CircuitPass
import magma.testing


class _MyWrapperGen(m.Generator2):
    def __init__(self, width: Optional[int]):
        T = m.Bits[width] if width is not None else m.Bit
        self.io = io = m.IO(I=m.In(T), O=m.Out(T)) + m.ClockIO()
        m.inline_verilog2(
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
        self._repr_str += repr(ckt)

    @property
    def repr_str(self) -> str:
        return self._repr_str


def test_compilation_coreir():
    with pytest.raises(NotImplementedError) as e:
        m.compile("", _Top, output="coreir")


def test_compilation_mlir():
    basename = f"test_inline_verilog_expression_compilation_mlir"
    m.compile(f"build/{basename}", _Top, output="mlir")
    assert m.testing.check_files_equal(
        __file__, f"build/{basename}.mlir", f"gold/{basename}.mlir")
