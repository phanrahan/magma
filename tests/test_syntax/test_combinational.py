import magma as m
from magma.testing import check_files_equal
import pytest
import logging
import ast_tools
from ast_tools.passes import begin_rewrite, end_rewrite

ast_tools.stack._SKIP_FRAME_DEBUG_FAIL = True


Not = m.DefineCircuit("Not", "I", m.In(m.Bit), "O", m.Out(m.Bit))
m.wire(0, Not.O)
m.EndDefine()


@m.cache_definition
def DefineMux(height=2, width=None):
    if width is None:
        T = m.Bit
    else:
        T = m.Bits[width]

    io = []
    for i in range(height):
        io += ["I{}".format(i), m.In(T)]
    if height == 2:
        select_type = m.Bit
    else:
        select_type = m.Bits[m.bitutils.clog2(height)]
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


def mux(I, S):
    if isinstance(S, int):
        return I[S]
    elif S.const():
        return I[m.bitutils.seq2int(S.bits())]
    return Mux(len(I), get_length(I[0]))(*I, S)


def compile_and_check(output_file, circuit_definition, target):
    m.compile(f"build/{output_file}", circuit_definition, output=target)
    if target in ["verilog", "coreir-verilog"]:
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
    @end_rewrite()
    @m.circuit.combinational()
    @begin_rewrite()
    def basic_if(I: m.Bits[2], S: m.Bit) -> m.Bit:
        if S:
            return I[0]
        else:
            return I[1]
    compile_and_check("if_statement_basic", basic_if,
                      target)


@pytest.mark.skip("Broken w.r.t. return value phis")
def test_if_statement_nested(target):
    @end_rewrite()
    @m.circuit.combinational()
    @begin_rewrite()
    def if_statement_nested(I: m.Bits[4], S: m.Bits[2]) -> m.Bit:
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
                      if_statement_nested,
                      target)


def test_ternary(target):
    @end_rewrite()
    @m.circuit.combinational()
    @begin_rewrite()
    def ternary(I: m.Bits[2], S: m.Bit) -> m.Bit:
        return I[0] if S else I[1]
    compile_and_check("ternary", ternary, target)


def test_ternary_nested(target):
    @end_rewrite()
    @m.circuit.combinational()
    @begin_rewrite()
    def ternary_nested(I: m.Bits[4], S: m.Bits[2]) -> m.Bit:
        return I[0] if S[0] else I[1] if S[1] else I[2]
    compile_and_check("ternary_nested", ternary_nested,
                      target)


def test_ternary_nested2(target):
    @end_rewrite()
    @m.circuit.combinational()
    @begin_rewrite()
    def ternary_nested2(I: m.Bits[4], S: m.Bits[2]) -> m.Bit:
        return (I[0] if S[0] else I[1]) if S[1] else I[2]
    compile_and_check("ternary_nested2", ternary_nested2,
                      target)


@end_rewrite()
@m.circuit.combinational()
@begin_rewrite()
def basic_func(I: m.Bits[2], S: m.Bit) -> m.Bit:
    if S:
        return I[0]
    else:
        return I[1]


def test_function_composition(target):
    @end_rewrite()
    @m.circuit.combinational()
    @begin_rewrite()
    def basic_function_call(I: m.Bits[2], S: m.Bit) -> m.Bit:
        return basic_func()(I, S)
    compile_and_check("basic_function_call",
                      basic_function_call, target)


def test_return_py_tuple(target):
    @end_rewrite()
    @m.circuit.combinational()
    @begin_rewrite()
    def return_py_tuple(I: m.Bits[2]) -> (m.Bit, m.Bit):
        return I[0], I[1]
    compile_and_check("return_py_tuple", return_py_tuple,
                      target)


def test_return_magma_tuple(target):
    @end_rewrite()
    @m.circuit.combinational()
    @begin_rewrite()
    def return_magma_tuple(I: m.Bits[2]) -> m.Tuple(m.Bit, m.Bit):
        return m.tuple_([I[0], I[1]])
    compile_and_check("return_magma_tuple",
                      return_magma_tuple, target)


def test_return_magma_named_tuple(target):
    @end_rewrite()
    @m.circuit.combinational()
    @begin_rewrite()
    def return_magma_named_tuple(I: m.Bits[2]) -> m.Tuple(x=m.Bit, y=m.Bit):
        return m.namedtuple(x=I[0], y=I[1])
    compile_and_check("return_magma_named_tuple",
                      return_magma_named_tuple, target)


EQ = m.DefineCircuit("eq", "I0", m.In(m.Bit), "I1", m.In(m.Bit), "O",
                     m.Out(m.Bit))
m.wire(0, EQ.O)
m.EndDefine()


def test_simple_circuit_1(target):

    @end_rewrite()
    @m.circuit.combinational()
    @begin_rewrite()
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
            c = logic()(io.a)
            m.wire(c, io.c)

    compile_and_check("simple_circuit_1", Foo, target)


def test_multiple_assign(target):
    @end_rewrite()
    @m.circuit.combinational()
    @begin_rewrite()
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
            c = logic()(io.a)
            m.wire(c, io.c)

    compile_and_check("multiple_assign", Foo, target)


def test_optional_assignment(target):
    EQ2 = m.DefineCircuit("eq2", "I0", m.In(m.Bits[2]), "I1", m.In(m.Bits[2]), "O",
                          m.Out(m.Bit))
    m.wire(0, EQ2.O)
    m.EndDefine()

    @end_rewrite()
    @m.circuit.combinational()
    @begin_rewrite()
    def logic(a: m.Bits[2]) -> (m.Bits[2], m.Bits[2]):
        d = m.bits(0, 2)
        if EQ2()(a, m.bits(0, 2)):
            c = m.bits(1, 2)
        else:
            c = m.bits(2, 2)
            d = m.bits(3, 2)
        return (c, d)

    class Foo(m.Circuit):
        IO = ["a", m.In(m.Bits[2]),
              "c", m.Out(m.Bits[2]),
              "d", m.Out(m.Bits[2])]

        @classmethod
        def definition(io):
            c, d = logic()(io.a)
            m.wire(c, io.c)
            m.wire(d, io.d)

    compile_and_check("optional_assignment", Foo, target)


def test_map_circuit(target):
    @end_rewrite()
    @m.circuit.combinational()
    @begin_rewrite()
    def logic(a: m.Bits[10]) -> m.Bits[10]:
        return m.join(m.map_(Not, 10))(a)

    class Foo(m.Circuit):
        IO = ["a", m.In(m.Bits[10]),
              "c", m.Out(m.Bits[10])]

        @classmethod
        def definition(io):
            c = logic()(io.a)
            m.wire(c, io.c)

    compile_and_check("test_map_circuit", Foo, target)


def test_renamed_args(target):
    @end_rewrite()
    @m.circuit.combinational()
    @begin_rewrite()
    def invert(a: m.Bit) -> m.Bit:
        return Not()(a)

    class Foo(m.Circuit):
        IO = ["I", m.In(m.Bit), "O", m.Out(m.Bit)]

        @classmethod
        def definition(io):
            io.O <= invert()(a=io.I)

    compile_and_check("test_renamed_args", Foo, target)


def test_renamed_args_wire(target):
    @end_rewrite()
    @m.circuit.combinational()
    @begin_rewrite()
    def invert(a: m.Bit) -> m.Bit:
        return Not()(a)

    class Foo(m.Circuit):
        IO = ["I", m.In(m.Bit), "O", m.Out(m.Bit)]

        @classmethod
        def definition(io):
            inv = invert()
            inv.a <= io.I
            io.O <= inv.O

    compile_and_check("test_renamed_args_wire", Foo, target)
