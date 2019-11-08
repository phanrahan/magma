import pytest
import magma as m
from test_combinational import compile_and_check, phi
from collections.abc import Sequence
import coreir
import ast_tools
from magma.circuit import DeclareCoreirCircuit

ast_tools.stack._SKIP_FRAME_DEBUG_FAIL = True


@m.cache_definition
def DefineCoreirReg(width, init=0, has_reset=False, T=m.Bits):
    if width is None:
        width = 1
    name = "reg_P"  # TODO: Add support for clock interface
    config_args = {"init": coreir.type.BitVector[width](init)}
    gen_args = {"width": width}
    T = T[width]
    io = ["I", m.In(T), "clk", m.In(m.Clock), "O", m.Out(T)]
    methods = []

    def reset(self, condition):
        wire(condition, self.rst)
        return self

    if has_reset:
        io.extend(["arst", m.In(m.AsyncReset)])
        name += "R"  # TODO: This assumes ordering of clock parameters
        # methods.append(circuit_type_method("reset", reset))
        # gen_args["has_rst"] = True

    def when(self, condition):
        wire(condition, self.en)
        return self

    # if has_ce:
    #     io.extend(["en", In(Enable)])
    #     name += "E"  # TODO: This assumes ordering of clock parameters
    #     methods.append(circuit_type_method("when", when))
    #     gen_args["has_en"] = True

    # default_kwargs = gen_args.copy()
    default_kwargs = {"init": coreir.type.BitVector[width](init)}
    # default_kwargs.update(config_args)

    return DeclareCoreirCircuit(
        name,
        *io,
        stateful=True,
        circuit_type_methods=methods,
        default_kwargs=default_kwargs,
        coreir_genargs=gen_args,
        coreir_configargs=config_args,
        coreir_name="reg_arst" if has_reset else "reg",
        verilog_name="coreir_" + ("reg_arst" if has_reset else "reg"),
        coreir_lib="coreir"
    )


@m.cache_definition
def DefineRegister(n, init=None, has_ce=False, has_reset=False,
                   has_async_reset=False, _type=m.Bits):
    T = _type[n]
    return DefineCoreirReg(n, init, has_async_reset, _type)


def Register(n, init=0, has_ce=False, has_reset=False, has_async_reset=False,
             **kwargs):
    return DefineRegister(n, init, has_ce, has_reset,
                          has_async_reset)(**kwargs)


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
            self.x: m.Bits[2] = m.Bits[2](0)
            self.y: m.Bits[2] = m.Bits[2](0)

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

def test_product(target, async_reset):
    Data = m.Bits[16]

    class Instr(m.Product):
        a=m.Bit
        b=Data

    @m.circuit.sequential(async_reset=async_reset)
    class Foo():
        def __init__(self):
            self.s: Data = Data(0)
        def __call__(self, instr: Instr) -> (Data,m.Bit):
            a = instr.a
            b = instr.b
            self.s = ~self.s
            if a:
                return b, s[0]
            else:
                return ~b, ~a

    compile_and_check("TestProduct" + ("ARST" if async_reset else ""), Foo, target)


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
                self.value: m.Bits[width] = m.Bits[width](init)

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
