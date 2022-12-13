import magma as m
from magma.passes.elaborate_circuit import elaborate_circuit, elaborate_all_pass


def test_circuit():

    class Ckt(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        primitive = True

        @classmethod
        def elaborate(cls):
            cls.io.O @= ~cls.io.I

    assert repr(Ckt) == 'Ckt = DeclareCircuit("Ckt", "I", In(Bit), "O", Out(Bit))'
    assert not m.isdefinition(Ckt)
    assert m.isprimitive(Ckt)

    elaborate_circuit(Ckt)
    assert repr(Ckt) == ("""\
Ckt = DefineCircuit("Ckt", "I", In(Bit), "O", Out(Bit))
magma_Bit_not_inst0 = magma_Bit_not()
wire(Ckt.I, magma_Bit_not_inst0.in)
wire(magma_Bit_not_inst0.out, Ckt.O)
EndCircuit()"""
    )
    assert m.isdefinition(Ckt)
    assert not m.isprimitive(Ckt)


def test_generator():

    class Gen(m.Generator2):
        def __init__(self):
            self.io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
            self.primitive = True
            self.name = "Ckt"

        def elaborate(self):
            self.io.O @= ~self.io.I

    Ckt = Gen()

    assert repr(Ckt) == 'Ckt = DeclareCircuit("Ckt", "I", In(Bit), "O", Out(Bit))'
    assert not m.isdefinition(Ckt)
    assert m.isprimitive(Ckt)

    elaborate_circuit(Ckt)
    assert repr(Ckt) == ("""\
Ckt = DefineCircuit("Ckt", "I", In(Bit), "O", Out(Bit))
magma_Bit_not_inst0 = magma_Bit_not()
wire(Ckt.I, magma_Bit_not_inst0.in)
wire(magma_Bit_not_inst0.out, Ckt.O)
EndCircuit()"""
    )
    assert m.isdefinition(Ckt)
    assert not m.isprimitive(Ckt)


def test_pass():

    class Ckt(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        primitive = True

        @classmethod
        def elaborate(cls):
            cls.io.O @= ~cls.io.I

    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))
        io.O @= io.I

    class Top(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))

        @classmethod
        def elaborate(cls):
            cls.io.O @= Foo()(Ckt()(cls.io.I))

    assert repr(Ckt) == 'Ckt = DeclareCircuit("Ckt", "I", In(Bit), "O", Out(Bit))'
    assert repr(Top) == 'Top = DeclareCircuit("Top", "I", In(Bit), "O", Out(Bit))'

    elaborate_all_pass(Top, circuits=(Top,))

    assert repr(Ckt) == 'Ckt = DeclareCircuit("Ckt", "I", In(Bit), "O", Out(Bit))'
    assert repr(Top) == ("""\
Top = DefineCircuit("Top", "I", In(Bit), "O", Out(Bit))
Ckt_inst0 = Ckt()
Foo_inst0 = Foo()
wire(Top.I, Ckt_inst0.I)
wire(Ckt_inst0.O, Foo_inst0.I)
wire(Foo_inst0.O, Top.O)
EndCircuit()"""
    )

    elaborate_all_pass(Top, circuits=(Ckt,))

    assert repr(Ckt) == ("""\
Ckt = DefineCircuit("Ckt", "I", In(Bit), "O", Out(Bit))
magma_Bit_not_inst0 = magma_Bit_not()
wire(Ckt.I, magma_Bit_not_inst0.in)
wire(magma_Bit_not_inst0.out, Ckt.O)
EndCircuit()"""
    )
