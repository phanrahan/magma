from magma.config import config
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
cell_0 = _Cell()
cell_1 = _Cell()
cell_2 = _Cell()
cell_3 = _Cell()
cell_4 = _Cell()
wire(_Top.I, cell_0.I)
wire(cell_0.O, cell_1.I)
wire(cell_1.O, cell_2.I)
wire(cell_2.O, cell_3.I)
wire(cell_3.O, cell_4.I)
wire(cell_4.O, _Top.O)
EndCircuit()

"""
    assert pass_.code == expected
