import pytest

import magma as m
from magma import *
from magma.testing.utils import has_error


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

    assert issubclass(m.In(m.Tuple[Bit, Bit]), m.In(m.Tuple[Bit, Bit]))
    assert isinstance(m.In(m.Tuple[Bit, Bit])(), m.In(m.Tuple[Bit, Bit]))

    assert issubclass(m.In(m.Tuple[Bit, Bit]), m.Tuple[Bit, Bit])
    assert isinstance(m.In(m.Tuple[Bit, Bit])(), m.Tuple[Bit, Bit])

    assert not issubclass(m.In(m.Tuple[Bit, Bit]), m.Out(m.Tuple[Bit, Bit]))
    assert not isinstance(m.In(m.Tuple[Bit, Bit])(), m.Out(m.Tuple[Bit, Bit]))

    assert issubclass(m.Out(m.Tuple[Bit, Bit]), m.Out(m.Tuple[Bit, Bit]))
    assert isinstance(m.Out(m.Tuple[Bit, Bit])(), m.Out(m.Tuple[Bit, Bit]))

    assert issubclass(m.Out(m.Tuple[Bit, Bit]), m.Tuple[Bit, Bit])
    assert isinstance(m.Out(m.Tuple[Bit, Bit])(), m.Tuple[Bit, Bit])

    assert not issubclass(m.Out(m.Tuple[Bit, Bit]), m.In(m.Tuple[Bit, Bit]))
    assert not isinstance(m.Out(m.Tuple[Bit, Bit])(), m.In(m.Tuple[Bit, Bit]))


def test_dict():
    # types
    class A2(Product, cache=True):
        x = Bit
        y = Bit
    print(A2)
    assert isinstance(A2, ProductMeta)
    print(str(A2))

    assert issubclass(In(A2), A2)
    assert issubclass(Out(A2), A2)
    assert issubclass(Flip(A2), A2)
    assert not issubclass(In(A2), Out(A2))
    assert not issubclass(Out(A2), In(A2))

    assert issubclass(Flip(In(A2)), Out(A2))
    assert issubclass(Flip(Out(A2)), In(A2))

    assert issubclass(Out(In(A2)), Out(A2))
    assert issubclass(In(Out(A2)), In(A2))

    assert not issubclass(Out(In(A2)), In(Out(A2)))
    assert not issubclass(In(Out(A2)), Out(In(A2)))

    assert not issubclass(Flip(In(A2)), Flip(Out(A2)))
    assert not issubclass(Flip(Out(A2)), Flip(In(A2)))

    assert isinstance(In(A2)(), A2)
    assert isinstance(Out(A2)(), A2)
    assert isinstance(Flip(A2)(), A2)
    assert not isinstance(In(A2)(), Out(A2))
    assert not isinstance(Out(A2)(), In(A2))

    assert isinstance(Flip(In(A2))(), Out(A2))
    assert isinstance(Flip(Out(A2))(), In(A2))

    assert isinstance(Out(In(A2))(), Out(A2))
    assert isinstance(In(Out(A2))(), In(A2))

    assert not isinstance(Out(In(A2))(), In(Out(A2)))
    assert not isinstance(In(Out(A2))(), Out(In(A2)))

    assert not isinstance(Flip(In(A2))(), Flip(Out(A2)))
    assert not isinstance(Flip(Out(A2))(), Flip(In(A2)))

    #assert str(A2) == 'Tuple(x=Bit,y=Bit)'
    assert A2 == A2

    class B2(Product, cache=True):
        x = In(Bit)
        y = In(Bit)
    assert isinstance(B2, ProductMeta)
    #assert str(B2) == 'Tuple(x=In(Bit),y=In(Bit))'
    assert B2 == B2

    class C2(Product, cache=True):
        x = Out(Bit)
        y = Out(Bit)
    assert isinstance(C2, ProductMeta)

    #assert str(C2) == 'Tuple(x=Out(Bit),y=Out(Bit))'
    assert C2 == C2

    assert A2 == B2
    assert A2 == C2
    assert B2 == C2

    assert A2 is not B2
    assert A2 is not C2
    assert B2 is not C2


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

    assert Tin == Product2
    assert Tout == Product2
    assert Tin == Tout

    assert Tin is not Product2
    assert Tout is not Product2
    assert Tin is not Tout

    T = In(Tout)
    assert T == Tin

    #T = Flip(Tout)
    #assert T == Tin
    # print(T)

    T = Out(Tin)
    assert T == Tout

    #T = Flip(Tin)
    #assert T == Tout
    # print(T)


def test_wire():
    class Product2(Product):
        x = Bit
        y = Bit

    t0 = Product2(name='t0')

    t1 = Product2(name='t1')

    wire(t0, t1)

    assert t0.wired()
    assert t1.wired()

    assert t1.value() is t0
    assert t0.value() is t1

    assert t0.driving() == [t1]

    b0 = t0.x
    b1 = t1.x

    assert b0 is b1.value()
    assert b1 is b0.driving()[0]
    assert b1.value() is b0


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
            io = m.IO(ctr=m.In(m.Bit))
        return ctrModule

    def make_baseIO():
        class dictIO(Product):
            in0 = m.In(m.Bit),
            out0 = m.Out(m.Bit)
        return dictIO

    def DefineBaseModule():
        class baseModule(m.Circuit):
            name = "base_module"
            io = m.IO(baseIO=make_baseIO())
        return baseModule

    def DefineHier():
        class HierModule(m.Circuit):
            name = "hier_module"
            io = m.IO(hier=hierIO())
            baseM = DefineBaseModule()()
            ctrM = DefineCtrModule()()
            m.wire(baseM.baseIO, io.hier.baseIO)
            m.wire(ctrM.ctr, io.hier.ctr)
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
        })

    def IFC1(params):
        dictOut = {"port4": m.Out(m.Bit)}
        return m.Product.from_fields("IFC1", dictOut)

    def DefineMyCircuit(params):
        class MyCircuit(m.Circuit):
            io = m.IO(IFC0=IFC0(params).flip())
        return MyCircuit

    def DefineTop(params):
        class Top(m.Circuit):
            io = m.IO(IFC1=IFC1(params))
            m.wire(io.IFC1.port4, DefineMyCircuit(params)().IFC0.port4)
        return Top

    m.compile("top", DefineTop({'param0': 5}))


def test_flat_length():
    a = m.Product.from_fields("anon", dict(x=m.Bits[5], y=m.Bits[3], z=m.Bit))
    assert a.flat_length() == 9


def test_anon_product():
    product = m.Product.from_fields("anon", dict(x=m.Bits[5], y=m.Bits[3], z=m.Bit))
    assert isinstance(product, AnonymousProductMeta)
    assert isinstance(product, ProductMeta)

    anon_product = m.AnonProduct[dict(x=m.Bits[5], y=m.Bits[3], z=m.Bit)]
    assert isinstance(anon_product, AnonymousProductMeta)
    assert not isinstance(anon_product, ProductMeta)
    assert anon_product.flat_length() == product.flat_length()
    assert anon_product.x == product.x
    assert anon_product.y == product.y
    assert anon_product.z == product.z
    assert anon_product == product
    assert not anon_product is product


def test_mixed_direction_wrap():
    class ClocksT(m.Product):
        clk0 = m.In(m.Clock)
        clk1 = m.Out(m.Clock)

    class Main(m.Circuit):
        io = m.IO(clocks=ClocksT, count=m.Out(m.UInt[3]))
        count = m.Register(m.UInt[3])()
        count.CLK @= io.clocks.clk0
        io.count @= count(count.O + 1)

        tff = m.Register(m.Bit, has_enable=True)()
        tff.CLK @= io.clocks.clk0
        tff.CE @= m.enable(count.O == 3)
        io.clocks.clk1 @= m.clock(tff(tff.O ^ 1))

    m.compile('build/test_mixed_direction_wrap', Main)


def test_recursive_eq():
    class Foo(m.Circuit):
        io = m.IO(I0=m.In(m.Tuple[m.Bit, m.Bits[4]]),
                  I1=m.In(m.Tuple[m.Bit, m.Bits[4]]),
                  O=m.Out(m.Tuple[m.Bit, m.Bits[4]]))
        io.O @= io.I0 == io.I1


def test_key_error():

    class _(m.Circuit):
        T = m.Tuple[m.Bit, m.Bit]
        io = m.IO(I=m.In(T), O=m.Out(T))
        with pytest.raises(KeyError):
            io.I["bar"]
        with pytest.raises(KeyError):
            io.I[None]
        with pytest.raises(KeyError):
            io.I[object()]


def test_mixed_direction_lazy_resolve(caplog):

    class T(m.Product):
        x = m.In(m.Bit)
        y = m.Out(m.Bit)

    class U(m.Product):
        x = m.Bit
        y = m.Bit

    class Foo(m.Circuit):
        io = m.IO(I=T, O=m.Flip(T))
        u = U()
        u @= io.I  # bulk wire
        u.y @= io.O.y
        io.O.x @= u.x
        assert io.O.x.value() is u.x
        assert u.y.value() is io.O.y
        assert u.x.value() is io.I.x
        assert io.I.y.value() is u.y

    assert not caplog.messages, "Should not raise wiring errors"


def test_tuple_key_ordering(caplog):
    T0 = m.AnonProduct[{"x": m.Bit, "y": m.Bits[8]}]
    T1 = m.AnonProduct[{"y": m.Bits[8], "x": m.Bit}]

    class tuple_key_ordering(m.Circuit):
        io = m.IO(I=m.In(T0), O=m.Out(T1))
        io.O.wire(io.I)

    msg = """\
\033[1mtests/test_type/test_tuple.py:369\033[0m: Cannot wire tuple_key_ordering.I (type=Tuple(x=Out(Bit),y=Out(Bits[8])), keys=['y', 'x']) to  tuple_key_ordering.O (type=Tuple(y=In(Bits[8]),x=In(Bit)), keys=['x', 'y']) because the tuples do not have the same keys
>>         io.O.wire(io.I)\
"""

    assert has_error(caplog, msg)


def test_tuple_key_ordering_recursive(caplog):
    T0 = m.AnonProduct[{"x": m.Bit, "y": m.Bits[8]}]
    T1 = m.AnonProduct[{"y": m.Bits[8], "x": m.Bit}]

    class tuple_key_ordering(m.Circuit):
        io = m.IO(I=m.In(m.Array[2, T0]), O=m.Out(m.Array[2, T1]))
        io.O @= io.I

    msg = """\
\033[1mtests/test_type/test_tuple.py:385\033[0m: Cannot wire tuple_key_ordering.I (Array[(2, AnonProduct[{'x': Bit[Out], 'y': Bits[(8, Out(Bit))]}])]) to tuple_key_ordering.O (Array[(2, AnonProduct[{'y': Bits[(8, In(Bit))], 'x': Bit[In]}])])
>>         io.O @= io.I\
"""

    assert has_error(caplog, msg)


def test_tuple_key_ordering_recursive_2(caplog):
    T0 = m.AnonProduct[{"x": m.Bit, "y": m.Bits[8]}]
    T1 = m.AnonProduct[{"y": m.Bits[8], "x": m.Bit}]
    T2 = m.AnonProduct[{"y": T0, "x": m.Bit}]
    T3 = m.AnonProduct[{"y": T1, "x": m.Bit}]

    class tuple_key_ordering(m.Circuit):
        io = m.IO(I=m.In(T2), O=m.Out(T3))
        io.O.wire(io.I)

    msg = """\
\033[1mtests/test_type/test_tuple.py:403\033[0m: Cannot wire tuple_key_ordering.I (type=Tuple(y=Tuple(x=Out(Bit),y=Out(Bits[8])),x=Out(Bit)), to  tuple_key_ordering.O (type=Tuple(y=Tuple(y=In(Bits[8]),x=In(Bit)),x=In(Bit)))because the key y is not wireable
>>         io.O.wire(io.I)\
"""

    assert has_error(caplog, msg)


def test_tuple_same_key_value():
    T0 = m.AnonProduct[{"x": m.Bit, "y": m.Bits[8]}]
    T1 = m.AnonProduct[{"y": m.Bits[8], "x": m.Bit}]

    a = m.Out(T0)()
    b = m.In(T1)()
    b.x @= a.x
    b.y @= a.y
    assert isinstance(b.value(), m.Out(T1)), type(b.value())
