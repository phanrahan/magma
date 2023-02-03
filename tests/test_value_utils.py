import pytest

import magma as m
from magma.value_utils import (
    ValueVisitor,
    ArraySelector,
    TupleSelector,
    make_selector,
    fill,
)


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


@pytest.mark.parametrize("fill_value", (True, False))
def test_fill(fill_value):
    S = m.AnonProduct[{"x": m.Bits[8], "y": m.Bit}]
    T = m.AnonProduct[{"s": S, "u": m.Array[4, m.Bits[6]]}]

    t = T()
    fill(t, fill_value)

    value = t.value()
    assert value is not None

    assert value.s.const()
    assert value.s.x.const()
    assert value.s.y.const()
    assert int(value.s.x) == (0 if not fill_value else 255)
    assert int(value.s.y) == (0 if not fill_value else 1)

    assert value.u.const()
    for u_i in value.u:
        assert u_i.const()
        assert int(u_i) == (0 if not fill_value else 63)


def test_selector_stop_at():
    class T(m.Product):
        x = m.Bit
        y = m.Tuple[m.Bit, m.Bits[8]]

    class _Foo(m.Circuit):
        name = "Foo"
        io = m.IO(I=m.In(T))

        selector = make_selector(io.I.y[1][0], stop_at=io.I.y)
        assert selector.select(io.I.y) is io.I.y[1][0]
