import magma as m
from magma.type_utils import (isprotocol, isdigital, isbits, isarray, istuple,
                              isuint, issint, TypeVisitor, TypeTransformer)


class _Prod(m.Product):
    x = m.Array[5, m.Bits[10]]
    y = m.Array[10, m.Bit]


class _FooTypeMeta(m.MagmaProtocolMeta):
    def _to_magma_(cls):
        return cls.T

    def _qualify_magma_(cls, direction: m.Direction):
        return cls[cls.T.qualify(direction)]

    def _flip_magma_(cls):
        return cls[cls.T.flip()]

    def _from_magma_value_(cls, val: m.Type):
        return cls(val)

    def __getitem__(cls, T):
        return type(cls)(f"Foo{T}", (cls, ), {"T": T})


class _FooType(m.MagmaProtocol, metaclass=_FooTypeMeta):
    def __init__(self, val = None):
        if val is None:
            val = self.T()
        self._val = val

    def _get_magma_value_(self):
        return self._val


def test_is_functions():

    assert isprotocol(_FooType)
    assert not isprotocol(m.Bit)

    assert isdigital(m.Bit)
    assert isdigital(m.Clock)
    assert isdigital(m.Reset)
    assert not isdigital(m.Bits)

    assert isbits(m.Bits)
    assert isbits(m.Bits[8])
    assert isbits(m.UInt[8])
    assert not isbits(m.Bit)

    assert isarray(m.Array)
    assert isarray(m.Array[10, m.Bit])
    assert isarray(m.Bits)
    assert not isarray(m.Bit)

    assert istuple(_Prod)
    assert istuple(m.Product.from_fields("anon", dict(x=m.Bit)))
    assert not istuple(m.Bit)

    assert isuint(m.UInt)
    assert isuint(m.UInt[8])
    assert not isuint(m.SInt)

    assert issint(m.SInt)
    assert issint(m.SInt[8])
    assert not issint(m.UInt)


def test_type_visitor_basic():

    class _Visitor(TypeVisitor):
        def __init__(self):
            self.indent = 0
            self.string = ""

        def _print(self, s):
            self.string += s + "\n"

        def generic_visit(self, T):
            self._print(((4 * self.indent) * " ") + str(T))
            self.indent += 1
            super().generic_visit(T)
            self.indent -= 1

    T = m.Array[10, _Prod]

    v = _Visitor()
    v.visit(T)

    assert v.string == \
"""Array[(10, _Prod)]
    Tuple(x=Array[(5, Bits[10])],y=Array[(10, Bit)])
        Array[(5, Bits[10])]
            Bits[10]
        Array[(10, Bit)]
            Bit
"""


def test_type_transformer():

    class _Transformer(TypeTransformer):
        def visit_Digital(self, T):
            return m.Clock

    T = m.Array[10, _Prod]
    Tnew = _Transformer().visit(T)

    assert issubclass(Tnew, m.Array)
    assert Tnew.N == 10
    Prod = Tnew.T
    assert issubclass(Prod, m.Tuple)
    fields = Prod.field_dict
    assert set(fields.keys()) == {"x", "y"}
    assert fields["x"] is m.Array[5, m.Bits[10]]
    assert fields["y"] is m.Array[10, m.Clock]
