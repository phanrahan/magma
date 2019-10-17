import magma as m
from magma import *

def test_pair():
    # types

    A2 = Tuple[Bit, Bit]
    print(A2)
    assert isinstance(A2, TupleMeta)
    print(str(A2))
    assert A2 == A2

    B2 = Tuple[In(Bit), In(Bit)]
    assert isinstance(B2, TupleMeta)
    assert B2 == B2

    C2 = Tuple[Out(Bit), Out(Bit)]
    assert isinstance(C2, TupleMeta)
    #assert str(C2) == 'Tuple(x=Out(Bit),y=Out(Bit))'
    assert C2 == C2

def test_dict():
    # types
    class A2(Product):
        x = Bit
        y = Bit
    print(A2)
    assert isinstance(A2, ProductMeta)
    print(str(A2))
    #assert str(A2) == 'Tuple(x=Bit,y=Bit)'
    assert A2 == A2

    class B2(Product):
        x = In(Bit)
        y = In(Bit)
    assert isinstance(B2, ProductMeta)
    #assert str(B2) == 'Tuple(x=In(Bit),y=In(Bit))'
    assert B2 == B2

    class C2(Product):
        x = Out(Bit)
        y = Out(Bit)
    assert isinstance(C2, ProductMeta)
    #assert str(C2) == 'Tuple(x=Out(Bit),y=Out(Bit))'
    assert C2 == C2

    assert A2 != B2
    assert A2 != C2
    assert B2 != C2

def test_flip():
    class Product2(Product):
        x = In(Bit)
        y = Out(Bit)
    print(Product2)
    print(Flip(Product2))

    Tin = In(Product2)
    Tout = Out(Product2)

    print(Tin)
    print(Tout)

    assert Tin != Product2
    assert Tout != Product2
    assert Tin != Tout

    T = In(Tout)
    assert T == Tin

    #T = Flip(Tout)
    #assert T == Tin
    #print(T)

    T = Out(Tin)
    assert T == Tout

    #T = Flip(Tin)
    #assert T == Tout
    #print(T)

def test_wire():
    class Product2(Product):
        x = Bit
        y = Bit

    t0 = Product2(name='t0')
    #assert t0.direction is None

    t1 = Product2(name='t1')
    #assert t1.direction is None

    wire(t0, t1)

    assert t0.wired()
    assert t1.wired()

    assert t1.driven()

    assert t0.trace() is t1
    assert t1.trace() is t0

    #print t0.driven()
    assert t0.value() is None
    assert t1.value() is t0

    b0 = t0.x
    b1 = t1.x

    assert b0.port.wires is b1.port.wires

    wires = b0.port.wires
    assert len(b0.port.wires.inputs) == 1
    assert len(b0.port.wires.outputs) == 1
    print('inputs:', [str(p) for p in wires.inputs])
    print('outputs:', [str(p) for p in wires.outputs])

def test_val():
    class A2(Product):
        x = Bit
        y = Bit

    # constructor

    a = A2(name='a')
    print('created A2')
    assert isinstance(a, Product)
    assert str(a) == 'a'

    # selectors

    print('a["x"]')
    b = a['x']
    assert isinstance(b, Bit)
    assert str(b) == 'a.x'

    print('a.x')
    b = a.x
    assert isinstance(b, Bit)
    assert str(b) == 'a.x'


def test_nested():
    # Test for https://github.com/phanrahan/magma/issues/445
    def hierIO():
        class dictIO(Product):
            baseIO = make_baseIO()
            ctr = m.In(m.Bit)
        return dictIO

    def DefineCtrModule():
        class ctrModule(m.Circuit):
            name = "ctr_module"
            IO = ["ctr",m.In(m.Bit)]
        return ctrModule

    def make_baseIO():
        class dictIO(Product):
            in0 = m.In(m.Bit),
            out0 = m.Out(m.Bit)
        return dictIO

    def DefineBaseModule():
        class baseModule(m.Circuit):
            name = "base_module"
            IO = ["baseIO",make_baseIO()]
        return baseModule

    def DefineHier():
        class HierModule(m.Circuit):
            name = "hier_module"
            IO = ["hier", hierIO()]
            @classmethod
            def definition(io):
                baseM = DefineBaseModule()()
                ctrM = DefineCtrModule()()
                m.wire(baseM.baseIO,io.hier.baseIO)
                m.wire(ctrM.ctr,io.hier.ctr)
        return HierModule

    baseMH = DefineHier()
    m.compile("build/baseMH", baseMH, output="coreir-verilog")
