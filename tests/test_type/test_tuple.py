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
    class Product2(Product, cache=True):
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
    class Product2(Product, cache=True):
        x = Bit
        y = Bit
    print(list(id(v) for v in Product2.field_dict.items()))

    t0 = Wire(Product2, name='t0')
    #assert t0.direction is None

    t1 = Wire(Product2, name='t1')
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

    b0 = t0.x._value
    b1 = t1.x._value

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

    a = Wire(A2, name='a')
    print('created A2')
    assert isinstance(a._value, Product)
    assert str(a) == 'a'

    # selectors

    print('a.x')
    b = a.x._value
    assert isinstance(b, Bit)
    assert str(b) == 'a.x'


def test_nested():
    # Test for https://github.com/phanrahan/magma/issues/445
    class BaseIO(Product, cache=True):
        in0 = m.In(m.Bit)
        out0 = m.Out(m.Bit)

    class HierIO(Product, cache=True):
        baseIO = BaseIO
        ctr = m.In(m.Bit)

    def DefineCtrModule():
        class ctrModule(m.Circuit):
            name = "ctr_module"
            IO = ["ctr",m.In(m.Bit)]
        return ctrModule


    def DefineBaseModule():
        class baseModule(m.Circuit):
            name = "base_module"
            IO = ["baseIO",BaseIO]
        return baseModule

    def DefineHier():
        class HierModule(m.Circuit):
            name = "hier_module"
            IO = ["hier", HierIO]
            @classmethod
            def definition(io):
                baseM = DefineBaseModule()()
                ctrM = DefineCtrModule()()
                m.wire(baseM.baseIO,io.hier.baseIO)
                m.wire(ctrM.ctr,io.hier.ctr)
        return HierModule

    baseMH = DefineHier()
    m.compile("build/baseMH", baseMH, output="coreir-verilog")


def test_tuple_nested_tuple_value():
    def IFC0(params):
        return m.Product.from_fields("IFC0", {
            "port0": m.In(m.Bits[params['param0']]),
            "port1": m.In(m.Bits[params['param0']]),
            "port2": m.In(m.Array[params['param0'], m.Bits[2]]),
            "port3": m.In(m.Bits[params['param0']]),
            "port4": m.In(m.Bit),
            "port5": m.In(m.Bit),
            "port7": m.In(m.Bit),
            "port8": m.In(m.Bit),
            "port9": m.In(m.Bit),
            "port10": m.In(m.Bits[m.bitutils.clog2(params['param0'])]),
        }, cache=True)

    def IFC1(params):
        dictOut = {"port4": m.Out(m.Bit)}
        return m.Product.from_fields("IFC1", dictOut)

    def DefineMyCircuit(params):
        class MyCircuit(m.Circuit):
            IO = ["IFC0", m.Flip(IFC0(params))]
        return MyCircuit

    def DefineTop(params):
        class Top(m.Circuit):
            IO = ["IFC1", IFC1(params)]
            @classmethod
            def definition(io):
               m.wire(io.IFC1.port4, DefineMyCircuit(params)().IFC0.port4)
        return Top


    m.compile("top", DefineTop({'param0': 5}))
