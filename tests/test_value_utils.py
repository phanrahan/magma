import magma as m
from magma.value_utils import (ValueVisitor, ArraySelector, TupleSelector,
                               make_selector)


class _Prod(m.Product):
    x = m.Array[5, m.Bits[10]]
    y = m.Array[10, m.Bit]


def test_value_visitor():
    class _Visitor(ValueVisitor):
        def __init__(self):
            self.values = []

        def visit_Array(self, value):
            self.values.append(("Array", value))
            ValueVisitor.generic_visit(self, value)

        def visit_Tuple(self, value):
            self.values.append(("Tuple", value))
            ValueVisitor.generic_visit(self, value)

        def visit_Digital(self, value):
            self.values.append(("Digital", value))
            ValueVisitor.generic_visit(self, value)

        def visit_Bits(self, value):
            self.values.append(("Bits", value))
            ValueVisitor.generic_visit(self, value)

    T = m.Array[10, _Prod]
    v = _Visitor()
    value = T()
    v.visit(value)
    expected = [("Array", value)]
    for t in value:
        expected.append(("Tuple", t))
        expected.append(("Array", t.x))
        for tt in t.x:
            expected.append(("Bits", tt))
            for ttt in tt:
                expected.append(("Digital", ttt))
        expected.append(("Array", t.y))
        for tt in t.y:
            expected.append(("Digital", tt))

    assert len(expected) == len(v.values)
    assert all(e_str == v_str and e_val is v_val
               for ((e_str, e_val), (v_str, v_val)) in zip(expected, v.values))


def test_selector():
    T = m.Array[10, _Prod]

    class _Foo(m.Circuit):
        name = "Foo"
        io = m.IO(I=m.In(T))

    selector = ArraySelector(
        index=0,
        child=TupleSelector(
            key="x",
            child=ArraySelector(
                index=0,
                child=None)))

    assert str(selector) == "[0].x[0]"
    assert selector.select(_Foo.I) is _Foo.I[0].x[0]
