from magma.passes import IRPass
from magma import Bit, Circuit, IO, In, Out, wire


class _Cell(Circuit):
    io = IO(I=In(Bit), O=Out(Bit))

    io.O <= io.I


class _Top(Circuit):
    io = IO(I=In(Bit), O=Out(Bit))

    in_ = io.I
    for _ in range(5):
        cell = _Cell()
        cell.I <= in_
        in_ = cell.O
    io.O <= in_


def test_basic():
    pass_ = IRPass(_Top)
    pass_.run()
    expected = """_Cell = DefineCircuit("_Cell", "I", In(Bit), "O", Out(Bit))
wire(_Cell.I, _Cell.O)
EndCircuit()

_Top = DefineCircuit("_Top", "I", In(Bit), "O", Out(Bit))
_Cell_inst0 = _Cell()
_Cell_inst1 = _Cell()
_Cell_inst2 = _Cell()
_Cell_inst3 = _Cell()
_Cell_inst4 = _Cell()
wire(_Top.I, _Cell_inst0.I)
wire(_Cell_inst0.O, _Cell_inst1.I)
wire(_Cell_inst1.O, _Cell_inst2.I)
wire(_Cell_inst2.O, _Cell_inst3.I)
wire(_Cell_inst3.O, _Cell_inst4.I)
wire(_Cell_inst4.O, _Top.O)
EndCircuit()

"""
    assert pass_.code == expected
