import pytest
import magma as m
from test_combinational import compile_and_check, phi
from collections.abc import Sequence
import coreir
import ast_tools
from magma.circuit import DeclareCoreirCircuit

ast_tools.stack._SKIP_FRAME_DEBUG_FAIL = True


@m.cache_definition
def DefineCoreirReg(width, init=0, has_async_reset=False,
                    has_async_resetn=False, T=m.Bits):
    if width is None:
        width = 1
    name = "reg_P"  # TODO: Add support for clock interface
    config_args = {"init": coreir.type.BitVector[width](init)}
    gen_args = {"width": width}
    T = T[width]
    io = ["I", m.In(T), "CLK", m.In(m.Clock), "O", m.Out(T)]
    methods = []

    def reset(self, condition):
        wire(condition, self.rst)
        return self

    if has_async_resetn and has_async_reset:
        raise ValueError("Cannot have posedge and negedge asynchronous reset")
    if has_async_reset:
        io.extend(["arst", m.In(m.AsyncResetIn)])
        name += "R"  # TODO: This assumes ordering of clock parameters
        config_args["arst_posedge"] = True
    if has_async_resetn:
        io.extend(["arst", m.In(m.AsyncResetNIn)])
        name += "R"  # TODO: This assumes ordering of clock parameters
        config_args["arst_posedge"] = False

    def when(self, condition):
        m.wire(condition, self.en)
        return self

    # if has_ce:
    #     io.extend(["en", In(Enable)])
    #     name += "E"  # TODO: This assumes ordering of clock parameters
    #     methods.append(circuit_type_method("when", when))
    #     gen_args["has_en"] = True

    # default_kwargs = gen_args.copy()
    default_kwargs = {"init": coreir.type.BitVector[width](init)}
    # default_kwargs.update(config_args)

    coreir_name = "reg_arst" if (has_async_reset or has_async_resetn) else "reg"

    return DeclareCoreirCircuit(
        name,
        *io,
        stateful=True,
        circuit_type_methods=methods,
        default_kwargs=default_kwargs,
        coreir_genargs=gen_args,
        coreir_configargs=config_args,
        coreir_name=coreir_name,
        verilog_name="coreir_" + coreir_name,
        coreir_lib="coreir"
    )


@m.cache_definition
def DefineDFF(init=0, has_ce=False, has_reset=False, has_async_reset=False, has_async_resetn=False):
    Reg = DefineCoreirReg(None, init, has_async_reset, has_async_resetn)
    IO = ["I", m.In(m.Bit), "O", m.Out(m.Bit)]
    IO += m.ClockInterface(has_ce=has_ce, has_reset=has_reset,
                           has_async_reset=has_async_reset,
                           has_async_resetn=has_async_resetn)
    circ = m.DefineCircuit("DFF_init{}_has_ce{}_has_reset{}_has_async_reset{}".format(
        init, has_ce, has_reset, has_async_reset, has_async_resetn),
        *IO)
    value = Reg()
    m.wiredefaultclock(circ, value)
    m.wireclock(circ, value)
    I = circ.I
    if has_reset and (has_async_reset or has_async_resetn):
        raise ValueError("Cannot have synchronous and asynchronous reset")
    if has_async_resetn and has_async_reset:
        raise ValueError("Cannot have posedge and negedge asynchronous reset")
    if has_reset:
        I = Mux()(circ.I, bit(init), circ.RESET)
    if has_ce:
        I = Mux()(value.O[0], I, circ.CE)
    m.wire(I, value.I[0])
    m.wire(value.O[0], circ.O)
    m.EndDefine()
    return circ


@m.cache_definition
def DefineRegister(n, init=0, has_ce=False, has_reset=False,
                   has_async_reset=False, has_async_resetn=False, _type=m.Bits,
                   reset_priority=True, ):
    if has_reset and (has_async_reset or has_async_resetn):
        raise ValueError("Cannot have synchronous and asynchronous reset")
    if has_async_resetn and has_async_reset:
        raise ValueError("Cannot have posedge and negedge asynchronous reset")

    if has_reset or has_ce:
        if n is None:
            T = m.Bit
        else:
            T = _type[n]
        class Register(m.Circuit):
            name = f"Register_has_ce_{has_ce}_has_reset_{has_reset}_" \
                   f"has_async_reset_{has_async_reset}_" \
                   f"has_async_resetn_{has_async_resetn}_" \
                   f"type_{_type.__name__}_n_{n}"
            IO = ["I", m.In(T), "O", m.Out(T)]
            IO += m.ClockInterface(has_ce=has_ce,
                                   has_reset=has_reset,
                                   has_async_reset=has_async_reset,
                                   has_async_resetn=has_async_resetn)

            @classmethod
            def definition(io):
                reg = DefineCoreirReg(n, init, has_async_reset,
                                      has_async_resetn, _type)(name="value")
                I = io.I
                O = reg.O
                if n is None:
                    O = O[0]
                if has_reset and has_ce:
                    if reset_priority:
                        I = mantle.mux([O, I], io.CE, name="enable_mux")
                        I = mantle.mux([I, m.bits(init, n)], io.RESET)
                    else:
                        I = mantle.mux([I, m.bits(init, n)], io.RESET)
                        I = mantle.mux([O, I], io.CE, name="enable_mux")
                elif has_ce:
                    I = mantle.mux([O, I], io.CE, name="enable_mux")
                elif has_reset:
                    I = mantle.mux([I, m.bits(init, n)], io.RESET)
                if n is None:
                    m.wire(I, reg.I[0])
                else:
                    m.wire(I, reg.I)
                m.wire(io.O, O)
                m.wireclock(io, reg)
                m.wiredefaultclock(io, reg)

        return Register
    elif n is None:
        if _type is not m.Bits:
            raise NotImplementedError()
        return DefineDFF(init, has_ce, has_async_reset=has_async_reset)
    else:
        return DefineCoreirReg(n, init, has_async_reset, has_async_resetn,
                               _type)


def Register(n, init=0, has_ce=False, has_reset=False, has_async_reset=False,
             has_async_resetn=False, _type = m.Bits, **kwargs):
    return DefineRegister(n, init, has_ce, has_reset, has_async_reset,
                          has_async_resetn=has_async_resetn, _type=_type)(**kwargs)


def pytest_generate_tests(metafunc):
    if 'target' in metafunc.fixturenames:
        metafunc.parametrize("target", ["coreir", "coreir-verilog"])
    if 'async_reset' in metafunc.fixturenames:
        metafunc.parametrize("async_reset", [True, False])


def _run_verilator(circuit, directory):
    import subprocess
    def run_from_directory(cmd):
        return subprocess.call(cmd, cwd=directory, shell=True)
    top = circuit.name
    assert not run_from_directory(
        f"verilator -Wall -Wno-INCABSPATH -Wno-DECLFILENAME --cc {top}.v "
        f"--exe ../{top}_driver.cpp --top-module {top}")
    assert not run_from_directory(
        f"make -C obj_dir -j -f V{top}.mk V{top}")
    assert not run_from_directory(
        f"./obj_dir/V{top}")


def test_seq_simple(target, async_reset):
    @m.circuit.sequential(async_reset=async_reset)
    class TestBasic:
        def __init__(self):
            self.x: m.Bits[2] = m.bits(0, 2)
            self.y: m.Bits[2] = m.bits(0, 2)

        def __call__(self, I: m.Bits[2]) -> m.Bits[2]:
            O = self.y
            self.y = self.x
            self.x = I
            return O

    compile_and_check("TestBasic" + ("ARST" if async_reset else ""), TestBasic, target)
    if target == "coreir-verilog" and not async_reset:
        """
        The following sequence was used to create the verilator driver:

        tester = fault.Tester(TestBasic, clock=TestBasic.CLK)
        tester.circuit.I = 1
        tester.step(2)
        tester.circuit.I = 2
        tester.step(2)
        tester.circuit.O.expect(1)
        tester.circuit.I = 3
        tester.step(2)
        tester.circuit.O.expect(2)
        tester.circuit.I = 0
        tester.step(2)
        tester.circuit.O.expect(3)

        """
        _run_verilator(TestBasic, directory="tests/test_syntax/build")

def test_seq_call(target):
    @m.circuit.sequential
    class TestCall:
        def __init__(self):
            self.x: m.Bits[2] = m.bits(0, 2)
            self.y: m.Bits[3] = m.bits(0, 3)

        def __call__(self, I: m.Bits[2]) -> m.Bits[3]:
            O = self.y
            self.y = m.zext(self.x, 1)
            self.x = I
            return O

    compile_and_check("TestCall", TestCall, target)

def test_custom_env(target):

    _globals = globals()
    _globals.update({'_custom_local_var_':2})
    env = ast_tools.stack.SymbolTable(locals=locals(),globals=_globals)

    class TestBasic:
        def __init__(self):
            self.x: m.Bits[2] = m.bits(_custom_local_var_, 2)
            self.y: m.Bits[2] = m.bits(0, 2)

        def __call__(self, I: m.Bits[2]) -> m.Bits[2]:
            O = self.y
            self.y = self.x
            self.x = I
            return O

    _TestBasic = m.circuit.sequential(TestBasic,env=env)
    compile_and_check("CustomEnv", _TestBasic, target)

def test_seq_hierarchy(target, async_reset):
    @m.cache_definition
    def DefineCustomRegister(width, init=0):
        @m.circuit.sequential(async_reset=async_reset)
        class Register:
            def __init__(self):
                self.value: m.Bits[width] = m.bits(init, width)

            def __call__(self, I: m.Bits[width]) -> m.Bits[width]:
                O = self.value
                self.value = I
                return O

        return Register

    CustomRegister0 = DefineCustomRegister(2, init=0)
    CustomRegister1 = DefineCustomRegister(2, init=1)

    @m.circuit.sequential(async_reset=async_reset)
    class TestShiftRegister:
        def __init__(self):
            self.x: CustomRegister0 = CustomRegister0()
            self.y: CustomRegister1 = CustomRegister1()

        def __call__(self, I: m.Bits[2]) -> m.Bits[2]:
            x_prev = self.x(I)
            y_prev = self.y(x_prev)
            return y_prev

    compile_and_check("TestShiftRegister" + ("ARST" if async_reset else ""), TestShiftRegister, target)
    if target == "coreir-verilog" and not async_reset:
        """
        The following sequence was used to create the verilator driver:

        tester = fault.Tester(TestShiftRegister, clock=TestShiftRegister.CLK)
        tester.circuit.I = 1
        tester.step(2)
        tester.circuit.I = 2
        tester.step(2)
        tester.circuit.O.expect(1)
        tester.circuit.I = 3
        tester.step(2)
        tester.circuit.O.expect(2)
        tester.circuit.I = 0
        tester.step(2)
        tester.circuit.O.expect(3)

        """
        _run_verilator(TestShiftRegister, directory="tests/test_syntax/build")


def test_multiple_return(target, async_reset):
    T = m.Bits[4]

    @m.circuit.sequential(async_reset=async_reset)
    class Register:
        def __init__(self):
            self.value: T = T(0)

        def __call__(self, value: T, en: m.Bit) -> T:
            retvalue = self.value
            if en:
                self.value = value
            else:
                self.value = self.value
            return retvalue

    @m.circuit.sequential(async_reset=async_reset)
    class RegisterMode:
        def __init__(self):
            self.register: Register = Register(0)

        def __call__(self, mode: m.Bits[2], const_: T, value: T, clk_en: m.Bit,
                     config_we: m.Bit, config_data: T) -> (T, T):
            if config_we == m.Bit(1):
                reg_val = self.register(config_data, m.Bit(1))
                return reg_val, reg_val
            elif mode == m.bits(0, 2):
                reg_val = self.register(value, m.Bit(False))
                return const_, reg_val
            elif mode == m.bits(1, 2):
                reg_val = self.register(value, m.Bit(False))
                return value, reg_val
            elif mode == m.bits(2, 2):
                reg_val = self.register(value, clk_en)
                return reg_val, reg_val

    print(repr(type(RegisterMode.instances[1])))
    compile_and_check("RegisterMode" + ("ARST" if async_reset else ""), RegisterMode, target)


def test_array_of_bits(target):
    @m.circuit.sequential(async_reset=True)
    class ArrayOfBitsSeq:
        def __init__(self):
            self.register_array: m.Array[15, m.Bits[1024]] = \
                m.array([m.bits(0, 1024) for _ in range(15)])

        def __call__(self, I: m.Array[15, m.Bits[1024]]) -> \
                m.Array[15, m.Bits[1024]]:
            O = self.register_array
            self.register_array = I
            return O

    compile_and_check("ArrayOfBitsSeq", ArrayOfBitsSeq, target)


def test_rd_ptr(target):
    @m.circuit.sequential(async_reset=True)
    class RdPtr:
        def __init__(self):
            self.rd_ptr: m.UInt[10] = m.uint(0, 10)

        def __call__(self, read: m.Bit) -> m.Bits[10]:
            orig_rd_ptr = self.rd_ptr

            # FIXME: Bug in magma sequential means we always have to specify a next
            # value (won't use current value by default)
            self.rd_ptr = orig_rd_ptr

            if read:
                self.rd_ptr = self.rd_ptr + 1
            return orig_rd_ptr

    compile_and_check("RdPtr", RdPtr, target)


def test_namedtuple_seq():
    class A(m.Product):
        a0 = m.Bit
        a1 = m.SInt[8]

    @m.circuit.sequential(async_reset=False)
    class TestNamedTuple:
        def __init__(self):
            self.a0: m.Bit = m.bit(0)
            self.a1: m.SInt[8] = 0

        def __call__(self, a: A, b: m.Bit) -> A:
            if b:
                new_a = a
            else:
                new_a = m.namedtuple(a0=self.a0, a1=self.a1)

            self.a0 = new_a.a0
            self.a1 = new_a.a1

            return new_a

    m.compile("build/test_named_tuple_seq", TestNamedTuple, output="coreir-verilog")


def test_product_reg(target):
    class A(m.Product):
        a0 = m.Bit
        a1 = m.SInt[8]

    @m.circuit.sequential(async_reset=True)
    class TestProductReg:
        def __init__(self):
            self.a: A = m.namedtuple(a0=1, a1=2)

        def __call__(self, a: A, b: m.Bit) -> A:
            if b:
                new_a = a
            else:
                new_a = self.a

            self.a = new_a

            return new_a

    compile_and_check("TestProductReg", TestProductReg, target)


def test_nested_product_reg(target):
    class Child(m.Product):
        c0 = m.UInt[4]
        c1 = m.Bit

    class A(m.Product):
        a0 = m.Bit
        a1 = Child
        a2 = m.SInt[8]

    @m.circuit.sequential(async_reset=True)
    class TestNestedProductReg:
        def __init__(self):
            self.a: A = m.namedtuple(a0=1, a1=m.namedtuple(c0=3, c1=0), a2=2)

        def __call__(self, a: A, b: m.Bit) -> A:
            if b:
                new_a = a
            else:
                new_a = self.a

            self.a = new_a

            return new_a

    compile_and_check("TestNestedProductReg", TestNestedProductReg, target)


def test_product_access(target):
    class A(m.Product):
        a0 = m.Bits[8]
        a1 = m.Bits[8]

    @m.circuit.sequential(async_reset=False)
    class TestProductAccess:
        def __init__(self):
            self.a: A = m.namedtuple(a0=0, a1=0)

        def __call__(self, sel: m.Bit, value: m.Bits[8]) -> A:
            if sel:
                a = m.namedtuple(a0=value, a1=self.a.a1)
            else:
                a = m.namedtuple(a0=self.a.a0, a1=value)

            self.a = a
            return a

    compile_and_check("TestProductAccess", TestProductAccess, target)


def test_no_init(target):
    @m.circuit.sequential(async_reset=True)
    class TestNoInit:
        def __call__(self, a: m.Bit, b: m.Bit) -> m.Bit:
            return a & b

    compile_and_check("TestNoInit", TestNoInit, target)


def test_replace_array(target):
    A = m.Array[2, m.Bit]

    @m.circuit.sequential(async_reset=False)
    class TestReplaceArray:
        def __call__(self) -> A:
            val0 = A([m.bit(0), m.bit(1)])
            val1 = m.replace(val0, dict([(0, m.bit(1))]))
            return val1

    compile_and_check("TestReplaceArray", TestReplaceArray, target)

    @m.circuit.sequential(async_reset=False)
    class TestReplaceArrayStrKey:
        def __call__(self) -> A:
            val0 = A([m.bit(0), m.bit(1)])
            val1 = m.replace(val0, {"0": m.bit(1)})
            return val1

    compile_and_check("TestReplaceArrayStrKey", TestReplaceArrayStrKey, target)


def test_replace_tuple(target):
    A = m.Tuple[m.Bit, m.Bit]

    @m.circuit.sequential(async_reset=False)
    class TestReplaceTuple:
        def __call__(self) -> A:
            val0 = m.tuple_([m.bit(0), m.bit(1)])
            val1 = m.replace(val0, dict([(0, m.bit(1))]))
            return val1

    compile_and_check("TestReplaceTuple", TestReplaceTuple, target)

    @m.circuit.sequential(async_reset=False)
    class TestReplaceTupleStrKey:
        def __call__(self) -> A:
            val0 = m.tuple_([m.bit(0), m.bit(1)])
            val1 = m.replace(val0, {"0": m.bit(1)})
            return val1

    compile_and_check("TestReplaceTupleStrKey", TestReplaceTupleStrKey, target)


def test_replace_product(target):
    class A(m.Product):
        x = m.Bit
        y = m.Bit

    @m.circuit.sequential(async_reset=False)
    class TestReplaceProduct:
        def __call__(self) -> A:
            val0 = m.namedtuple(x=m.bit(0), y=m.bit(1))
            val1 = m.replace(val0, dict(x=m.bit(1)))
            return val1

    compile_and_check("TestReplaceProduct", TestReplaceProduct, target)
