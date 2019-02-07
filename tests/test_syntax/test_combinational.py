import magma as m
from magma.testing import check_files_equal
import pytest
import logging


@m.cache_definition
def DefineMux(height=2, width=None):
    if width is None:
        T = m.Bit
    else:
        T = m.Bits(width)

    io = []
    for i in range(height):
        io += ["I{}".format(i), m.In(T)]
    if height == 2:
        select_type = m.Bit
    else:
        select_type = m.Bits(m.bitutils.clog2(height))
    io += ['S', m.In(select_type)]
    io += ['O', m.Out(T)]

    class _Mux(m.Circuit):
        name = f"Mux{height}" + (f"_x{width}" if width else "")
        IO = io
    return _Mux


def Mux(height=2, width=None, **kwargs):
    return DefineMux(height, width)(**kwargs)


def get_length(value):
    if isinstance(value, m._BitType):
        return None
    elif isinstance(value, m.ArrayType):
        return len(value)
    else:
        raise NotImplementedError(f"Cannot get_length of {type(value)}")


def phi(I, S):
    if isinstance(S, int):
        return I[S]
    elif S.const():
        return I[m.bitutils.seq2int(S.bits())]
    return Mux(len(I), get_length(I[0]))(*I, S)


def compile_and_check(output_file, circuit_definition, target):
    m.compile(f"build/{output_file}", circuit_definition, output=target)
    if target == "verilog":
        suffix = "v"
    elif target == "coreir":
        suffix = "json"
    else:
        raise NotImplementedError()
    assert check_files_equal(__file__, f"build/{output_file}.{suffix}",
                             f"gold/{output_file}.{suffix}")


def pytest_generate_tests(metafunc):
    if 'target' in metafunc.fixturenames:
        metafunc.parametrize("target", ["verilog", "coreir"])


def test_if_statement_basic(target):
    @m.circuit.combinational
    def basic_if(I: m.Bits(2), S: m.Bit) -> m.Bit:
        if S:
            return I[0]
        else:
            return I[1]
    compile_and_check("if_statement_basic", basic_if.circuit_definition,
                      target)


def test_if_statement_nested(target):
    @m.circuit.combinational
    def if_statement_nested(I: m.Bits(4), S: m.Bits(2)) -> m.Bit:
        if S[0]:
            if S[1]:
                return I[0]
            else:
                return I[1]
        else:
            if S[1]:
                return I[2]
            else:
                return I[3]
    compile_and_check("if_statement_nested",
                      if_statement_nested.circuit_definition,
                      target)


def test_ternary(target):
    @m.circuit.combinational
    def ternary(I: m.Bits(2), S: m.Bit) -> m.Bit:
        return I[0] if S else I[1]
    compile_and_check("ternary", ternary.circuit_definition, target)


def test_ternary_nested(target):
    @m.circuit.combinational
    def ternary_nested(I: m.Bits(4), S: m.Bits(2)) -> m.Bit:
        return I[0] if S[0] else I[1] if S[1] else I[2]
    compile_and_check("ternary_nested", ternary_nested.circuit_definition,
                      target)


def test_ternary_nested2(target):
    @m.circuit.combinational
    def ternary_nested2(I: m.Bits(4), S: m.Bits(2)) -> m.Bit:
        return (I[0] if S[0] else I[1]) if S[1] else I[2]
    compile_and_check("ternary_nested2", ternary_nested2.circuit_definition,
                      target)


@m.circuit.combinational
def basic_func(I: m.Bits(2), S: m.Bit) -> m.Bit:
    if S:
        return I[0]
    else:
        return I[1]


def test_function_composition(target):
    @m.circuit.combinational
    def basic_function_call(I: m.Bits(2), S: m.Bit) -> m.Bit:
        return basic_func(I, S)
    compile_and_check("basic_function_call",
                      basic_function_call.circuit_definition, target)


def test_return_py_tuple(target):
    @m.circuit.combinational
    def return_py_tuple(I: m.Bits(2)) -> (m.Bit, m.Bit):
        return I[0], I[1]
    compile_and_check("return_py_tuple", return_py_tuple.circuit_definition,
                      target)


def test_return_magma_tuple(target):
    @m.circuit.combinational
    def return_magma_tuple(I: m.Bits(2)) -> m.Tuple(m.Bit, m.Bit):
        return m.tuple_([I[0], I[1]])
    compile_and_check("return_magma_tuple",
                      return_magma_tuple.circuit_definition, target)


def test_return_magma_named_tuple(target):
    @m.circuit.combinational
    def return_magma_named_tuple(I: m.Bits(2)) -> m.Tuple(x=m.Bit, y=m.Bit):
        return m.namedtuple(x=I[0], y=I[1])
    compile_and_check("return_magma_named_tuple",
                      return_magma_named_tuple.circuit_definition, target)


def test_simple_circuit_1(target):
    EQ = m.DefineCircuit("eq", "I0", m.In(m.Bit), "I1", m.In(m.Bit), "O",
                         m.Out(m.Bit))
    m.wire(0, EQ.O)
    m.EndDefine()

    @m.circuit.combinational
    def logic(a: m.Bit) -> (m.Bit,):
        if EQ()(a, m.bit(0)):
            c = m.bit(1)
        else:
            c = m.bit(0)
        return (c,)

    class Foo(m.Circuit):
        IO = ["a", m.In(m.Bit),
              "c", m.Out(m.Bit)]

        @classmethod
        def definition(io):
            c = logic(io.a)
            m.wire(c, io.c)

    compile_and_check("simple_circuit_1", Foo, target)


def test_multiple_assign(target):
    EQ = m.DefineCircuit("eq", "I0", m.In(m.Bit), "I1", m.In(m.Bit), "O",
                         m.Out(m.Bit))
    m.wire(0, EQ.O)
    m.EndDefine()

    @m.circuit.combinational
    def logic(a: m.Bit) -> (m.Bit,):
        if EQ()(a, m.bit(0)):
            c = m.bit(1)
            c = m.bit(0)
        else:
            c = m.bit(0)
            c = m.bit(1)
        return (c,)

    class Foo(m.Circuit):
        IO = ["a", m.In(m.Bit),
              "c", m.Out(m.Bit)]

        @classmethod
        def definition(io):
            c = logic(io.a)
            m.wire(c, io.c)

    compile_and_check("multiple_assign", Foo, target)


def test_optional_assignment(target):

    EQ = m.DefineCircuit("eq", "I0", m.In(m.Bit), "I1", m.In(m.Bit), "O",
                         m.Out(m.Bit))
    m.wire(0, EQ.O)
    m.EndDefine()

    @m.circuit.combinational
    def logic(a: m.Bit) -> (m.Bit, m.Bit):
        d = m.bit(1)
        if EQ()(a, m.bit(0)):
            c = m.bit(1)
        else:
            c = m.bit(0)
            d = m.bit(1)
        return (c, d)

    class Foo(m.Circuit):
        IO = ["a", m.In(m.Bit),
              "c", m.Out(m.Bit),
              "d", m.Out(m.Bit)]

        @classmethod
        def definition(io):
            c, d = logic(io.a)
            m.wire(c, io.c)
            m.wire(d, io.d)

    compile_and_check("optional_assignment", Foo, target)


def test_map_circuit(target):
    Not = m.DefineCircuit("Not", "I", m.In(m.Bit), "O", m.Out(m.Bit))
    m.wire(0, Not.O)
    m.EndDefine()

    @m.circuit.combinational
    def logic(a: m.Bits(10)) -> m.Bits(10):
        return m.join(m.map_(Not, 10))(a)

    class Foo(m.Circuit):
        IO = ["a", m.In(m.Bits(10)),
              "c", m.Out(m.Bits(10))]

        @classmethod
        def definition(io):
            c = logic(io.a)
            m.wire(c, io.c)

    compile_and_check("test_map_circuit", Foo, target)


