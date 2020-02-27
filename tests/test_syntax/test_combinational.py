import magma as m
from magma.testing import check_files_equal
import pytest
import logging
import ast_tools
from ast_tools.passes import begin_rewrite, loop_unroll, end_rewrite
from hwtypes import BitVector

ast_tools.stack._SKIP_FRAME_DEBUG_FAIL = True


Not = m.DefineCircuit("Not", "I", m.In(m.Bit), "O", m.Out(m.Bit))
m.wire(0, Not.O)
m.EndDefine()


# TODO: Revert this to using mux primitive when moved to magma
@m.cache_definition
def _declare_muxn(height, width):
    def simulate(self, value_store, state_store):
        sel = BitVector[m.bitutils.clog2(height)](value_store.get_value(self.I.sel))
        out = BitVector[width](value_store.get_value(self.I.data[int(sel)]))
        value_store.set_value(self.O, out)
    return m.circuit.DeclareCoreirCircuit(f"coreir_commonlib_mux{height}x{width}",
        *["I", m.In(m.Product.from_fields("anon",
                                          dict(data=m.Array[height, m.Bits[width]],
                                               sel=m.Bits[m.bitutils.clog2(height)]))),
          "O", m.Out(m.Bits[width])],
        coreir_name="muxn",
        coreir_lib="commonlib",
        simulate=simulate,
        coreir_genargs={"width": width, "N": height}
    )


@m.cache_definition
def DefineMux(height=2, width=None, T=None):
    if T is not None:
        assert width is None, "Can only specify width **or** T"
        # Sanitize names for verilog by removing parens
        # TODO: Make this a reuseable feature
        suffix = str(T).replace("(", "").replace(")", "").replace(",", "_").replace("=", "_").replace("[", "").replace("]", "").replace(" ", "")
        T = T
    else:
        suffix = f"{width}"
        if width is None:
            T = Bit
        else:
            T = Bits[width]

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
        name = "Mux{}x{}".format(height, suffix)
        IO = io
        @classmethod
        def definition(interface):
            if T is not None and not (issubclass(T, m.Digital) or issubclass(T, m.Array) and issubclass(T.T, m.Bit)):
                if issubclass(T, m.Tuple):
                    for i in range(len(T.keys())):
                        Is = [getattr(interface, f"I{j}")[list(T.keys())[i]] for j in range(height)]
                        interface.O[i] <= DefineMux(height, T=list(T.types())[i])()(*Is, interface.S)
                else:
                    assert issubclass(T, m.Array), f"Expected array or type type, got {T}, type is {type(T)}"
                    for i in range(len(T)):
                        Is = [getattr(interface, f"I{j}")[i] for j in range(height)]
                        interface.O[i] <= DefineMux(height, T=type(Is[0]))()(*Is, interface.S)
            else:
                if T is None and width is None or issubclass(T, m.Digital):
                    mux = _declare_muxn(height, 1)()
                else:
                    mux = _declare_muxn(height, width if T is None else len(T))()
                for i in range(height):
                    if T is None and width is None or issubclass(T, m.Digital):
                        m.wire(getattr(interface, f"I{i}"), mux.I.data[i][0])
                    else:
                        m.wire(getattr(interface, f"I{i}"), mux.I.data[i])
                if height == 2:
                    m.wire(interface.S, mux.I.sel[0])
                else:
                    m.wire(interface.S, mux.I.sel)
                if T is None and width is None or issubclass(T, m.Digital):
                    m.wire(mux.O[0], interface.O)
                else:
                    m.wire(mux.O, interface.O)
    return _Mux


def Mux(height=2, width=None, T=None, **kwargs):
    return DefineMux(height, width, T=T)(**kwargs)


def phi(I, S, **kwargs):
    if isinstance(S, int):
        return I[S]
    elif S.const():
        return I[m.bitutils.seq2int(S.bits())]
    T = type(I[0])
    # Support using Bits(1) for select on 2 elements
    if len(I) == 2 and isinstance(S, m.Array) and \
            issubclass(S.T, m.Digital) and len(S) == 1:
        S = S[0]
    return Mux(len(I), T=T, **kwargs)(*I, S)


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
        metafunc.parametrize("target", ["coreir"])


def test_if_statement_basic(target):
    @m.circuit.combinational
    def basic_if(I: m.Bits[2], S: m.Bit) -> m.Bit:
        if S:
            return I[0]
        else:
            return I[1]
    compile_and_check("if_statement_basic", basic_if.circuit_definition,
                      target)


@pytest.mark.skip("Broken w.r.t. return value phis")
def test_if_statement_nested(target):
    @m.circuit.combinational
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
                      if_statement_nested.circuit_definition,
                      target)


def test_ternary(target):
    @m.circuit.combinational
    def ternary(I: m.Bits[2], S: m.Bit) -> m.Bit:
        return I[0] if S else I[1]
    compile_and_check("ternary", ternary.circuit_definition, target)


def test_ternary_nested(target):
    @m.circuit.combinational
    def ternary_nested(I: m.Bits[4], S: m.Bits[2]) -> m.Bit:
        return I[0] if S[0] else I[1] if S[1] else I[2]
    compile_and_check("ternary_nested", ternary_nested.circuit_definition,
                      target)


def test_ternary_nested2(target):
    @m.circuit.combinational
    def ternary_nested2(I: m.Bits[4], S: m.Bits[2]) -> m.Bit:
        return (I[0] if S[0] else I[1]) if S[1] else I[2]
    compile_and_check("ternary_nested2", ternary_nested2.circuit_definition,
                      target)


@m.circuit.combinational
def basic_func(I: m.Bits[2], S: m.Bit) -> m.Bit:
    if S:
        return I[0]
    else:
        return I[1]


def test_function_composition(target):
    @m.circuit.combinational
    def basic_function_call(I: m.Bits[2], S: m.Bit) -> m.Bit:
        return basic_func(I, S)
    compile_and_check("basic_function_call",
                      basic_function_call.circuit_definition, target)


def test_return_py_tuple(target):
    @m.circuit.combinational
    def return_py_tuple(I: m.Bits[2]) -> (m.Bit, m.Bit):
        return I[0], I[1]
    compile_and_check("return_py_tuple", return_py_tuple.circuit_definition,
                      target)


def test_return_magma_tuple(target):
    @m.circuit.combinational
    def return_magma_tuple(I: m.Bits[2]) -> m.Tuple[m.Bit, m.Bit]:
        return m.tuple_([I[0], I[1]])
    compile_and_check("return_magma_tuple",
                      return_magma_tuple.circuit_definition, target)


def test_return_magma_named_tuple(target):

    class O(m.Product):
        x = m.Bit
        y = m.Bit

    @m.circuit.combinational
    def return_magma_named_tuple(I: m.Bits[2]) -> O:
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
        io = m.IO(a=m.In(m.Bit),
                  c=m.Out(m.Bit))

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
        io = m.IO(a=m.In(m.Bit),
                  c=m.Out(m.Bit))

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
        io = m.IO(a=m.In(m.Bit),
                  c=m.Out(m.Bit),
                  d=m.Out(m.Bit))

        @classmethod
        def definition(io):
            c, d = logic(io.a)
            m.wire(c, io.c)
            m.wire(d, io.d)

    compile_and_check("optional_assignment", Foo, target)


def test_map_circuit(target):
    @m.circuit.combinational
    def logic(a: m.Bits[10]) -> m.Bits[10]:
        return m.join(m.map_(Not, 10))(a)

    class Foo(m.Circuit):
        io = m.IO(a=m.In(m.Bits[10]),
                  c=m.Out(m.Bits[10]))

        @classmethod
        def definition(io):
            c = logic(io.a)
            m.wire(c, io.c)

    compile_and_check("test_map_circuit", Foo, target)


def test_renamed_args(target):
    @m.circuit.combinational
    def invert(a: m.Bit) -> m.Bit:
        return Not()(a)

    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))

        @classmethod
        def definition(io):
            io.O <= invert(a=io.I)

    compile_and_check("test_renamed_args", Foo, target)


def test_renamed_args_wire(target):
    @m.circuit.combinational
    def invert(a: m.Bit) -> m.Bit:
        return Not()(a)

    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit))

        @classmethod
        def definition(io):
            inv = invert.circuit_definition()
            inv.a <= io.I
            io.O <= inv.O

    compile_and_check("test_renamed_args_wire", Foo, target)


@pytest.mark.parametrize("val", [0, 1])
def test_custom_env(target, val):
    def basic_fun(I: m.Bit, S: m.Bit) -> m.Bit:
        if S:
            return I
        else:
            return m.Bit(_custom_local_var_)

    _globals = globals()
    _globals.update({'_custom_local_var_': val})
    env = ast_tools.stack.SymbolTable(locals=locals(), globals=_globals)
    _basic_fun = m.circuit.combinational(basic_fun, env=env)
    compile_and_check(f"custom_env{val}", _basic_fun.circuit_definition, target)


def test_loop_unroll(target):

    n = 4
    @m.circuit.combinational
    @end_rewrite()
    @loop_unroll()
    @begin_rewrite()
    def logic(a: m.Bits[n]) -> m.Bits[n]:
        O = []
        for i in ast_tools.macros.unroll(range(n)):
            O.append(a[n - 1 - i])
        return m.bits(O, n)

    compile_and_check("test_loop_unroll", logic.circuit_definition,
                      target)


def test_loop_unroll_with_if(target):
    n = 4
    @m.circuit.combinational
    @end_rewrite()
    @loop_unroll()
    @begin_rewrite()
    def logic(a: m.Bits[n]) -> m.Bits[n]:
        O = []
        for i in ast_tools.macros.unroll(range(n)):
            b = a[n - 1 - i]
            if i % 2:
                b = Not()(b)
            O.append(b)
        return m.bits(O, n)

    compile_and_check("test_loop_unroll_nested_if", logic.circuit_definition,
                      target)
