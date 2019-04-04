import magma as m
from magma.operators import MantleImportError
from common import DeclareAnd
import pytest
from magma.testing import check_files_equal


def test_error():
    circ = m.DefineCircuit("test", "a", m.In(m.Bits[4]), "b", m.Out(m.Bits[4]))
    try:
        ~circ.a
        assert False, \
            "Operator should throw an error since mantle is not imported"
    except MantleImportError:
        pass


@pytest.mark.parametrize("width", [None, 3])
@pytest.mark.parametrize("output", ["verilog", "coreir"])
def test_assign(width, output):
    T = m.util.BitOrBits(width)
    name = f"test_assign_operator_{width}_{output}"
    circ = m.DefineCircuit(name, "a", m.In(T), "b", m.In(T),
                           "c", m.Out(T))
    and2 = DeclareAnd(width)()
    and2.I0 <= circ.a
    and2.I1 <= circ.b
    circ.c <= and2.O
    m.EndDefine()

    m.compile(f"build/{name}", circ, output)
    suffix = "v" if output == "verilog" else "json"
    assert check_files_equal(__file__, f"build/{name}.{suffix}",
                             f"gold/{name}.{suffix}")



@pytest.mark.parametrize("width", [None, 3])
@pytest.mark.parametrize("output", ["verilog", "coreir"])
def test_assign_to_var(width, output):
    T = m.util.BitOrBits(width)
    name = f"test_assign_operator2_{width}_{output}"
    circ = m.DefineCircuit(name, "a", m.In(T), "b", m.In(T),
                           "c", m.Out(T))
    and2 = DeclareAnd(width)()
    c, I0, I1 = and2.I0, and2.I1, circ.c
    I0 <= circ.a
    I1 <= circ.b
    c <= and2.O
    m.EndDefine()

    m.compile(f"build/{name}", circ, output)
    suffix = "v" if output == "verilog" else "json"
    assert check_files_equal(__file__, f"build/{name}.{suffix}",
                             f"gold/{name}.{suffix}")


@pytest.mark.parametrize("width", [None, 3])
def test_assign_error_0(width):
    T = m.util.BitOrBits(width)
    name = f"test_assign_operator_{width}"
    circ = m.DefineCircuit(name, "a", m.In(T), "b", m.In(T),
                           "c", m.Out(T))
    and2 = DeclareAnd(width)()
    try:
        and2.O <= circ.a
        assert False, "Should raise type error"
    except TypeError as e:
        assert str(e) == f"Cannot use <= to assign to output: {and2.O.debug_name} (trying to assign {circ.a.debug_name})"


@pytest.mark.parametrize("width", [None, 3])
def test_assign_error_1(width):
    T = m.util.BitOrBits(width)
    name = f"test_assign_operator_{width}"
    circ = m.DefineCircuit(name, "a", m.In(T), "b", m.In(T),
                           "c", m.Out(T))
    and2 = DeclareAnd(width)()
    try:
        circ.a <= and2.O
        assert False, "Should raise type error"
    except TypeError as e:
        assert str(e) == f"Cannot use <= to assign to output: {circ.a.debug_name} (trying to assign {and2.O.debug_name})"
