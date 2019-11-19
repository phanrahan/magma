import magma as m
from magma import *

def test_pair():
    # types

    A2 = Tuple(Bit, Bit)
    print(A2)
    assert isinstance(A2, TupleKind)
    print(str(A2))
    assert A2 == A2

    B2 = Tuple(In(Bit), In(Bit))
    assert isinstance(B2, TupleKind)
    assert B2 == B2

    C2 = Tuple(Out(Bit), Out(Bit))
    assert isinstance(C2, TupleKind)
    #assert str(C2) == 'Tuple(x=Out(Bit),y=Out(Bit))'
    assert C2 == C2

def test_dict():
    # types

    A2 = Tuple(x=Bit, y=Bit)
    print(A2)
    assert isinstance(A2, TupleKind)
    print(str(A2))
    #assert str(A2) == 'Tuple(x=Bit,y=Bit)'
    assert A2 == A2

    B2 = Tuple(x=In(Bit), y=In(Bit))
    assert isinstance(B2, TupleKind)
    #assert str(B2) == 'Tuple(x=In(Bit),y=In(Bit))'
    assert B2 == B2

    C2 = Tuple(x=Out(Bit), y=Out(Bit))
    assert isinstance(C2, TupleKind)
    #assert str(C2) == 'Tuple(x=Out(Bit),y=Out(Bit))'
    assert C2 == C2

    assert A2 != B2
    assert A2 != C2
    assert B2 != C2

def test_flip():
    Tuple2 = Tuple(x=In(Bit), y=Out(Bit))
    print(Tuple2)
    print(Flip(Tuple2))

    Tin = In(Tuple2)
    Tout = Out(Tuple2)

    print(Tin)
    print(Tout)

    assert Tin != Tuple2
    assert Tout != Tuple2
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
    Tuple2 = Tuple(x=Bit, y=Bit)

    t0 = Tuple2(name='t0')
    #assert t0.direction is None

    t1 = Tuple2(name='t1')
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
    A2 = Tuple(x=Bit, y=Bit)

    # constructor

    a = A2(name='a')
    print('created A2')
    assert isinstance(a, TupleType)
    assert str(a) == 'a'

    # selectors

    print('a["x"]')
    b = a['x']
    assert isinstance(b, BitType)
    assert str(b) == 'a.x'

    print('a.x')
    b = a.x
    assert isinstance(b, BitType)
    assert str(b) == 'a.x'


def test_nested():
    # Test for https://github.com/phanrahan/magma/issues/445
    def hierIO():
        dictIO = {
            "baseIO": baseIO(),
            "ctr": m.In(m.Bit)
        }
        return m.Tuple(**dictIO)

    def DefineCtrModule():
        class ctrModule(m.Circuit):
            name = "ctr_module"
            IO = ["ctr",m.In(m.Bit)]
        return ctrModule

    def baseIO():
        dictIO = {
            "in0":m.In(m.Bit),
            "out0":m.Out(m.Bit)
        }
        return m.Tuple(**dictIO)

    def DefineBaseModule():
        class baseModule(m.Circuit):
            name = "base_module"
            IO = ["baseIO",baseIO()]
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


def test_tuple_nested_tuple_value():
    def IFC0(params):
        return m.Tuple(**{
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
        })

    def IFC1(params):
        dictOut = {"port4": m.Out(m.Bit)}
        return m.Tuple(**dictOut)

    def DefineMyCircuit(params):
        class MyCircuit(m.Circuit):
            IO = ["IFC0", IFC0(params).flip()]
        return MyCircuit

    def DefineTop(params):
        class Top(m.Circuit):
            IO = ["IFC1", IFC1(params)]
            @classmethod
            def definition(io):
               m.wire(io.IFC1.port4, DefineMyCircuit(params)().IFC0.port4)
        return Top


    m.compile("top", DefineTop({'param0': 5}))


def test_flat_length():
    a = m.Tuple(x=m.Bits[5], y=m.Bits[3], z=m.Bit)
    assert a.flat_length() == 9
