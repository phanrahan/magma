import magma as m
import operator
from common import DeclareAnd
import pytest
from magma.testing import check_files_equal


@pytest.mark.parametrize("width", [None, 3])
@pytest.mark.parametrize("output", ["verilog", "coreir"])
@pytest.mark.parametrize("op", [operator.imatmul, operator.le])
def test_assign(width, output, op):
    T = m.util.BitOrBits(width)

    class Circ(m.Circuit):
        name = f"test_assign_operator_{width}_{output}"
        io = m.IO(a=m.In(T), b=m.In(T), c=m.Out(T))
        and2 = DeclareAnd(width)()
        op(and2.I0, io.a)
        op(and2.I1, io.b)
        op(io.c, and2.O)

    m.compile(f"build/{Circ.name}", Circ, output)
    suffix = "v" if output == "verilog" else "json"
    assert check_files_equal(__file__, f"build/{Circ.name}.{suffix}",
                             f"gold/{Circ.name}.{suffix}")


@pytest.mark.parametrize("width", [None, 3])
@pytest.mark.parametrize("output", ["verilog", "coreir"])
@pytest.mark.parametrize("op", [operator.imatmul, operator.le])
def test_assign_to_var(width, output, op):
    T = m.util.BitOrBits(width)

    class Circ(m.Circuit):
        name = f"test_assign_operator2_{width}_{output}"
        io = m.IO(a=m.In(T), b=m.In(T), c=m.Out(T))
        and2 = DeclareAnd(width)()
        c, I0, I1 = and2.I0, and2.I1, io.c
        op(I0, io.a)
        op(I1, io.b)
        op(c, and2.O)

    m.compile(f"build/{Circ.name}", Circ, output)
    suffix = "v" if output == "verilog" else "json"
    assert check_files_equal(__file__, f"build/{Circ.name}.{suffix}",
                             f"gold/{Circ.name}.{suffix}")


@pytest.mark.parametrize("width", [None, 3])
def test_assign_error_0(width):
    T = m.util.BitOrBits(width)

    class Circ(m.Circuit):
        name = f"test_assign_operator_{width}"
        io = m.IO(a=m.In(T), b=m.In(T), c=m.Out(T))
        and2 = DeclareAnd(width)()
        with pytest.raises(
                TypeError,
                match=rf"Cannot use @= to assign to output: O \(trying to assign a\)"):  # noqa
            and2.O @= io.a


@pytest.mark.parametrize("width", [None, 3])
def test_assign_error_1(width):
    T = m.util.BitOrBits(width)

    class Circ(m.Circuit):
        name = f"test_assign_operator_{width}"
        io = m.IO(a=m.In(T), b=m.In(T), c=m.Out(T))
        and2 = DeclareAnd(width)()
        with pytest.raises(
                TypeError,
                match=rf"Cannot use @= to assign to output: a \(trying to assign O\)"):  # noqa
            io.a @= and2.O


@pytest.mark.parametrize('T', [m.Bit, m.Array[5, m.Bit], m.Bits[5],
                               m.Tuple[m.Bit, m.Bits[5]]])
def test_eq_neq_input(T):
    class Foo(m.Circuit):
        io = m.IO(O=m.Out(T))
        with pytest.raises(TypeError, match="Cannot use == on an input"):
            io.O == 1
        with pytest.raises(TypeError, match="Cannot use != on an input"):
            io.O != 1
