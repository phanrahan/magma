import functools
import os
import pytest

import fault as f

import magma as m
from magma.primitives.when import InferredLatchError
from magma.testing.utils import check_gold, update_gold, SimpleMagmaProtocol
from magma.type_utils import type_to_sanitized_string


@functools.lru_cache(maxsize=None)
def _expects_error(error_type, process_error=None):

    def _decorator(fn):

        @functools.wraps(fn)
        def _wrapper(*args, **kwargs):
            with pytest.raises(error_type) as e:
                fn(*args, **kwargs)
            if process_error is not None:
                process_error(e)

        return _wrapper

    return _decorator


def test_with_default():
    class test_when_with_default(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bit), O=m.Out(m.Bit))

        io.O @= io.I[1]
        with m.when(io.S):
            io.O @= io.I[0]

    m.compile("build/test_when_with_default", test_when_with_default,
              output="mlir")

    if check_gold(__file__, "test_when_with_default.mlir"):
        return

    tester = f.Tester(test_when_with_default)
    tester.poke(test_when_with_default.I, 0b10)
    tester.poke(test_when_with_default.S, 0)
    tester.eval()
    tester.expect(test_when_with_default.O, 1)
    tester.poke(test_when_with_default.S, 1)
    tester.eval()
    tester.expect(test_when_with_default.O, 0)
    tester.poke(test_when_with_default.I, 0b01)
    tester.eval()
    tester.expect(test_when_with_default.O, 1)

    tester.compile_and_run("verilator", magma_output="mlir-verilog",
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))
    update_gold(__file__, "test_when_with_default.mlir")


def test_nested_with_default():
    class test_when_nested_with_default(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bits[2]), O=m.Out(m.Bit))

        io.O @= io.I[1]
        with m.when(io.S[0]) as c0:
            with m.when(io.S[1]) as c1:
                io.O @= io.I[0]

    m.compile("build/test_when_nested_with_default",
              test_when_nested_with_default, output="mlir")

    if check_gold(__file__, "test_when_nested_with_default.mlir"):
        return

    tester = f.Tester(test_when_nested_with_default)
    tester.poke(test_when_nested_with_default.I, 0b10)
    tester.poke(test_when_nested_with_default.S, 0b00)
    tester.eval()
    tester.expect(test_when_nested_with_default.O, 1)
    tester.poke(test_when_nested_with_default.S, 0b01)
    tester.eval()
    tester.expect(test_when_nested_with_default.O, 1)
    tester.poke(test_when_nested_with_default.S, 0b10)
    tester.eval()
    tester.expect(test_when_nested_with_default.O, 1)
    tester.poke(test_when_nested_with_default.S, 0b11)
    tester.eval()
    tester.expect(test_when_nested_with_default.O, 0)
    tester.poke(test_when_nested_with_default.I, 0b01)
    tester.eval()
    tester.expect(test_when_nested_with_default.O, 1)

    tester.compile_and_run("verilator", magma_output="mlir-verilog",
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))

    update_gold(__file__, "test_when_nested_with_default.mlir")


def test_override(caplog):
    class test_when_override(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bit), O=m.Out(m.Bit))

        io.O @= io.I[1]
        with m.when(io.S):
            io.O @= io.I[0]
        io.O @= io.I[1]
        io.I[0].unused()

    m.compile("build/test_when_override", test_when_override,
              output="mlir")

    if check_gold(__file__, "test_when_override.mlir"):
        return

    tester = f.Tester(test_when_override)
    tester.poke(test_when_override.I, 0b10)
    tester.poke(test_when_override.S, 0)
    tester.eval()
    tester.expect(test_when_override.O, 1)
    tester.poke(test_when_override.S, 1)
    tester.eval()
    tester.expect(test_when_override.O, 1)
    tester.poke(test_when_override.I, 0b01)
    tester.eval()
    tester.expect(test_when_override.O, 0)

    tester.compile_and_run("verilator", magma_output="mlir-verilog",
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"),
                           flags=['-Wno-UNUSED'])

    update_gold(__file__, "test_when_override.mlir")


def test_else():
    class test_when_else(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bit), O=m.Out(m.Bit))

        with m.when(io.S):
            io.O @= io.I[0]
        with m.otherwise():
            io.O @= io.I[1]

    m.compile("build/test_when_else", test_when_else, output="mlir")

    if check_gold(__file__, "test_when_else.mlir"):
        return

    tester = f.Tester(test_when_else)
    tester.poke(test_when_else.I, 0b10)
    tester.poke(test_when_else.S, 0)
    tester.eval()
    tester.expect(test_when_else.O, 1)
    tester.poke(test_when_else.S, 1)
    tester.eval()
    tester.expect(test_when_else.O, 0)
    tester.poke(test_when_else.I, 0b01)
    tester.eval()
    tester.expect(test_when_else.O, 1)

    tester.compile_and_run("verilator", magma_output="mlir-verilog",
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))

    update_gold(__file__, "test_when_else.mlir")


def test_elsewhen():
    class test_when_elsewhen(m.Circuit):
        io = m.IO(I=m.In(m.Bits[3]), S=m.In(m.Bits[2]), O=m.Out(m.Bit))

        with m.when(io.S[0]):
            io.O @= io.I[0]
        with m.elsewhen(io.S[1]):
            io.O @= io.I[1]
        with m.otherwise():
            io.O @= io.I[2]

    m.compile("build/test_when_elsewhen", test_when_elsewhen,
              output="mlir")

    if check_gold(__file__, "test_when_elsewhen.mlir"):
        return

    tester = f.Tester(test_when_elsewhen)
    tester.poke(test_when_elsewhen.I, 0b010)
    tester.poke(test_when_elsewhen.S, 0b00)
    tester.eval()
    tester.expect(test_when_elsewhen.O, 0)
    tester.poke(test_when_elsewhen.S, 0b01)
    tester.eval()
    tester.expect(test_when_elsewhen.O, 0)
    tester.poke(test_when_elsewhen.S, 0b10)
    tester.eval()
    tester.expect(test_when_elsewhen.O, 1)
    tester.poke(test_when_elsewhen.S, 0b11)
    tester.eval()
    tester.expect(test_when_elsewhen.O, 0)
    tester.poke(test_when_elsewhen.I, 0b101)
    tester.poke(test_when_elsewhen.S, 0b10)
    tester.eval()
    tester.expect(test_when_elsewhen.O, 0)

    tester.compile_and_run("verilator", magma_output="mlir-verilog",
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))

    update_gold(__file__, "test_when_elsewhen.mlir")


def _check_err(value, name):
    expected = f"Cannot use {name} without a previous when"
    assert str(value) == expected


@pytest.mark.parametrize('fn,name', [
    (lambda x: m.elsewhen(x), 'elsewhen'),
    (lambda x: m.otherwise(), 'otherwise')])
def test_bad_syntax(fn, name):
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bits[3]), S=m.In(m.Bits[2]), O=m.Out(m.Bit))

        io.O @= 0

        with pytest.raises(SyntaxError) as e:
            # This should not have a _PREV_WHEN_COND to use
            with fn(io.S[1]):
                io.O @= io.I[1]
        _check_err(e.value, name)

        with m.when(io.S[0]):
            io.O @= io.I[0]

        # This when should clear _PREV_WHEN_COND
        with m.when(io.S[1]):
            # This should not have a _PREV_WHEN_COND to use
            with pytest.raises(SyntaxError) as e:
                with fn(io.S[1]):
                    io.O @= io.I[1]
            _check_err(e.value, name)


@pytest.mark.parametrize('fn,name', [
    (lambda x: m.elsewhen(x), 'elsewhen'),
    (lambda x: m.otherwise(), 'otherwise')])
def test_bad_otherwise(fn, name):
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bits[3]), S=m.In(m.Bits[2]), O=m.Out(m.Bit))

        with m.when(io.S[0]):
            io.O @= io.I[0]

        # This when should clear _PREV_WHEN_COND
        with m.otherwise():
            io.O @= io.I[1]

        # This should not have a _PREV_WHEN_COND to use
        with pytest.raises(SyntaxError) as e:
            with fn(io.S[1]):
                io.O @= io.I[1]
        _check_err(e.value, name)


def test_multiple_drivers():
    class test_when_multiple_drivers(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bits[2]),
                  O0=m.Out(m.Bit), O1=m.Out(m.Bit))

        io.O0 @= io.I[1]
        io.O1 @= io.I[0]
        with m.when(io.S[0]) as c0:
            with m.when(io.S[1]) as c1:
                io.O0 @= io.I[0]
                io.O1 @= io.I[1]

    m.compile("build/test_when_multiple_drivers", test_when_multiple_drivers,
              output="mlir")

    if check_gold(__file__, "test_when_multiple_drivers.mlir"):
        return

    tester = f.Tester(test_when_multiple_drivers)
    tester.poke(test_when_multiple_drivers.I, 0b10)
    tester.poke(test_when_multiple_drivers.S, 0b00)
    tester.eval()
    tester.expect(test_when_multiple_drivers.O0, 1)
    tester.expect(test_when_multiple_drivers.O1, 0)
    tester.poke(test_when_multiple_drivers.S, 0b01)
    tester.eval()
    tester.expect(test_when_multiple_drivers.O0, 1)
    tester.expect(test_when_multiple_drivers.O1, 0)
    tester.poke(test_when_multiple_drivers.S, 0b10)
    tester.eval()
    tester.expect(test_when_multiple_drivers.O0, 1)
    tester.expect(test_when_multiple_drivers.O1, 0)
    tester.poke(test_when_multiple_drivers.S, 0b11)
    tester.eval()
    tester.expect(test_when_multiple_drivers.O0, 0)
    tester.expect(test_when_multiple_drivers.O1, 1)
    tester.poke(test_when_multiple_drivers.I, 0b01)
    tester.eval()
    tester.expect(test_when_multiple_drivers.O0, 1)
    tester.expect(test_when_multiple_drivers.O1, 0)

    tester.compile_and_run("verilator", magma_output="mlir-verilog",
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))

    update_gold(__file__, "test_when_multiple_drivers.mlir")


@pytest.mark.parametrize('T, bits_to_fault_value', [
    (m.Bits[8], lambda x: x),
    (
        m.AnonProduct[{"x": m.Bit, "y": m.Bits[7]}],
        lambda x: (bool(x[7]), int(x[:7])),
    )
])
def test_memory(T, bits_to_fault_value):
    T_str = type_to_sanitized_string(T)

    class test_when_memory(m.Circuit):
        name = f"test_when_memory_{T_str}"
        io = m.IO(
            data0=m.In(T), addr0=m.In(m.Bits[5]), en0=m.In(m.Bit),
            data1=m.In(T), addr1=m.In(m.Bits[5]), en1=m.In(m.Bit),
            out=m.Out(T)
        ) + m.ClockIO()

        mem = m.Memory(32, T)()
        with m.when(io.en0):
            mem[io.addr0] @= io.data0
            io.out @= mem[io.addr1]
        with m.elsewhen(io.en1):
            mem[io.addr1] @= io.data1
            io.out @= mem[io.addr0]
        with m.otherwise():
            io.out @= m.from_bits(T, m.Bits[8](0xFF))

    m.compile(f"build/test_when_memory_{T_str}", test_when_memory,
              output="mlir", flatten_all_tuples=True)

    if check_gold(__file__, f"test_when_memory_{T_str}.mlir"):
        return

    tester = f.SynchronousTester(test_when_memory, clock=test_when_memory.CLK)
    tester.advance_cycle()
    tester.expect(test_when_memory.out, bits_to_fault_value(m.Bits[8](0xFF)))

    tester.advance_cycle()

    tester.poke(test_when_memory.data0, bits_to_fault_value(m.Bits[8](0xDE)))
    tester.poke(test_when_memory.addr0, 0xAD)

    tester.poke(test_when_memory.data1, bits_to_fault_value(m.Bits[8](0xBE)))
    tester.poke(test_when_memory.addr1, 0xEF)
    tester.poke(test_when_memory.en0, 1)
    tester.advance_cycle()

    tester.expect(test_when_memory.out, 0)
    tester.poke(test_when_memory.en0, 0)
    tester.poke(test_when_memory.en1, 1)
    tester.advance_cycle()

    tester.expect(test_when_memory.out, bits_to_fault_value(m.Bits[8](0xDE)))
    tester.poke(test_when_memory.en0, 1)
    tester.poke(test_when_memory.en1, 0)
    tester.poke(test_when_memory.addr1, 0xAD)
    tester.advance_cycle()

    tester.expect(test_when_memory.out, bits_to_fault_value(m.Bits[8](0xDE)))

    tester.compile_and_run("verilator", magma_output="mlir-verilog",
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"),
                           magma_opts={"flatten_all_tuples": True},
                           flags=['-Wno-UNUSED'])

    update_gold(__file__, f"test_when_memory_{T_str}.mlir")


@pytest.mark.parametrize(
    'T, x',
    [
        (m.Array[2, m.AnonProduct[{"x": m.Bit, "y": m.Bits[2]}]],
         [[(0, 1), (1, 0)], [(1, 0), (0, 1)]]),
        (m.AnonProduct[{"x": m.Bits[2], "y": m.Bit}],
         [(0b10, 0b1), (0b01, 0b0)])
    ]
)
def test_nested(T, x):
    T_str = type_to_sanitized_string(T)

    class test_when_nested(m.Circuit):
        name = f"test_when_nested_{T_str}"
        io = m.IO(I=m.In(m.Array[2, T]),
                  S=m.In(m.Bit),
                  O=m.Out(T))

        io.O @= io.I[1]
        with m.when(io.S):
            io.O @= io.I[0]

    m.compile(f"build/test_when_nested_{T_str}", test_when_nested,
              output="mlir", flatten_all_tuples=True)

    if check_gold(__file__, f"test_when_nested_{T_str}.mlir"):
        return

    tester = f.Tester(test_when_nested)
    tester.poke(test_when_nested.I, x)
    tester.poke(test_when_nested.S, 0)
    tester.eval()
    tester.expect(test_when_nested.O, x[1])
    tester.poke(test_when_nested.S, 1)
    tester.eval()
    tester.expect(test_when_nested.O, x[0])

    tester.compile_and_run("verilator", magma_output="mlir-verilog",
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"),
                           magma_opts={"flatten_all_tuples": True})
    update_gold(__file__, f"test_when_nested_{T_str}.mlir")


def test_non_port():

    class _Test(m.Circuit):
        name = "test_non_port"
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bit), O=m.Out(m.Bit))

        x = m.Bit()
        with m.when(io.S):
            x @= io.I[0]
        with m.otherwise():
            x @= io.I[1]
        io.O @= x

    basename = "test_when_non_port"
    m.compile(f"build/{basename}", _Test, output="mlir")
    assert check_gold(__file__, f"{basename}.mlir")


def test_recursive_non_port():

    class _Test(m.Circuit):
        name = "test_recursive_non_port"
        io = m.IO(
            I=m.In(m.Bits[2]),
            S=m.In(m.Bit),
            O0=m.Out(m.Bit),
            O1=m.Out(m.Bit),
        )

        x = m.Bit()
        with m.when(io.S):
            x @= io.I[0]
            io.O1 @= x
        with m.otherwise():
            x @= io.I[1]
            io.O1 @= x
        io.O0 @= x

    basename = "test_when_recursive_non_port"
    # TODO(leonardt): Remove this when proper analysis is added
    with pytest.raises(NotImplementedError):
        m.compile(f"build/{basename}", _Test, output="mlir")
        assert check_gold(__file__, f"{basename}.mlir")


def test_internal_instantiation():

    class _Test(m.Circuit):
        name = "test_internal_instantiation"
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bit), O=m.Out(m.Bit))

        with m.when(io.S):
            io.O @= io.I[0] & 1
        with m.otherwise():
            io.O @= io.I[1] ^ 1

    basename = "test_when_internal_instantiation"
    m.compile(f"build/{basename}", _Test, output="mlir")
    assert check_gold(__file__, f"{basename}.mlir")


@pytest.mark.skip("Test does not pass due to when issue (#1156)")
def test_internal_instantiation_complex():

    class _Test(m.Circuit):
        name = "test_internal_instantiation_complex"
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bits[2]), O=m.Out(m.Bit))

        with m.when(io.S[0]):
            x = m.Bit(name="x")
            with m.when(io.S[1]):
                x @= io.I[0] & 1
            with m.otherwise():
                x @= io.I[1] ^ 1
            io.O @= x
        with m.otherwise():
            io.O @= 0b11

    basename = "test_when_internal_instantiation_complex"
    m.compile(f"build/{basename}", _Test, output="mlir")
    assert check_gold(__file__, f"{basename}.mlir")


def test_register_default():

    class _Test(m.Circuit):
        name = "test_register_default"
        io = m.IO(I=m.In(m.Bit), E=m.In(m.Bit), O=m.Out(m.Bit))

        reg = m.Register(m.Bit)()

        with m.when(io.E):
            reg.I @= io.I

        io.O @= reg.O

    basename = "test_when_register_default"
    m.compile(f"build/{basename}", _Test, output="mlir")
    assert check_gold(__file__, f"{basename}.mlir")


def test_register_no_default():

    class _Test(m.Circuit):
        name = "test_register_no_default"
        io = m.IO(I=m.In(m.Bit), E=m.In(m.Bit), O=m.Out(m.Bit))

        reg = m.Register(m.Bit)()

        with m.when(io.E):
            reg.I @= io.I
        with m.otherwise():
            reg.I @= ~io.I

        io.O @= reg.O

    basename = "test_when_register_no_default"
    m.compile(f"build/{basename}", _Test, output="mlir")
    assert check_gold(__file__, f"{basename}.mlir")


@_expects_error(InferredLatchError)
def test_latch_error_simple():

    class _Test(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bit), O=m.Out(m.Bit))

        with m.when(io.S):
            io.O @= io.I[0]

    m.compile("build/_Test", _Test, output="mlir")


@_expects_error(InferredLatchError)
def test_latch_error_elsewhen():

    class _Test(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bit), O=m.Out(m.Bit))

        with m.when(io.S):
            io.O @= io.I[0]
        with m.elsewhen(io.S ^ 1):
            io.O @= 1

    m.compile("build/_Test", _Test, output="mlir")


@_expects_error(InferredLatchError)
def test_latch_error_nested():

    class _Test(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bits[2]), O=m.Out(m.Bit))

        with m.when(io.S[0]):
            with m.when(io.S[1]):
                io.O @= io.I[0]

    m.compile("build/_Test", _Test, output="mlir")


def test_latch_no_error_nested():

    class _Test(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bits[2]), O=m.Out(m.Bit))

        with m.when(io.S[0]):
            io.O @= io.I[1]
            with m.when(io.S[1]):
                io.O @= io.I[0]
        with m.otherwise():
            io.O @= 1

    m.compile("build/_Test", _Test, output="mlir")


def test_latch_no_error_nested2():

    class _Test(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bits[2]), O=m.Out(m.Bit))

        with m.when(io.S[0]):
            with m.when(io.S[1]):
                io.O @= io.I[0]
            with m.otherwise():
                io.O @= io.I[1]
        with m.otherwise():
            io.O @= 1

    m.compile("build/_Test", _Test, output="mlir")


def test_double_elsewhen():

    class _Test(m.Circuit):
        name = "test_when_double_elsewhen"
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bits[2]), O=m.Out(m.Bit))

        with m.when(io.S[0]):
            io.O @= io.I[0]
        with m.elsewhen(io.S[1]):
            io.O @= io.I[1]
        with m.elsewhen(io.S.reduce_and()):
            io.O @= 1
        with m.otherwise():
            io.O @= 3

    basename = "test_when_double_elsewhen"
    m.compile(f"build/{basename}", _Test, output="mlir")
    assert check_gold(__file__, f"{basename}.mlir")


def test_nested_otherwise():
    class test_when_nested_otherwise(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bits[2]),
                  O=m.Out(m.Bits[2]))

        with m.when(io.S.reduce_and()):
            io.O @= io.I
        with m.otherwise():
            with m.when(io.S[1]):
                io.O @= ~io.I
            with m.otherwise():
                io.O @= io.I

    m.compile("build/test_when_nested_otherwise",
              test_when_nested_otherwise, output="mlir",
              flatten_all_tuples=True)

    assert check_gold(__file__, "test_when_nested_otherwise.mlir")


def test_lazy_array_resolve(caplog):

    class _Test(m.Circuit):
        name = "test_when_lazy_array_resolve"
        io = m.IO(I=m.In(m.SInt[2]), S=m.In(m.Bit), O=m.Out(m.SInt[2]))
        with m.when(io.S):
            io.O @= io.I
        with m.otherwise():
            io.O @= m.sint(m.uint(io.I) >> 1)

    m.compile(f"build/{_Test.name}", _Test, output="mlir")
    assert check_gold(__file__, f"{_Test.name}.mlir")


def test_lazy_array(caplog):

    class _Test(m.Circuit):
        name = "test_when_lazy_array"
        io = m.IO(S=m.In(m.Bit), O=m.Out(m.Bits[2]))

        x = m.Bits[2](name="x")

        with m.when(io.S):
            x[0] @= 0
            x[1] @= 1
        with m.otherwise():
            x[0] @= 1
            x[1] @= 0

        io.O @= x

    basename = "test_when_lazy_array"
    m.compile(f"build/{basename}", _Test, output="mlir")
    assert check_gold(__file__, f"{basename}.mlir")


def test_lazy_array_slice(caplog):

    class _Test(m.Circuit):
        name = "test_when_lazy_array_slice"
        io = m.IO(S=m.In(m.Bit), O=m.Out(m.Bits[4]))

        x = m.Bits[4](name="x")

        with m.when(io.S):
            x[:2] @= 0
            x[2:] @= 1
        with m.otherwise():
            x[:2] @= 1
            x[2:] @= 0

        io.O @= x

    m.compile(f"build/{_Test.name}", _Test, output="mlir")
    assert check_gold(__file__, f"{_Test.name}.mlir")


def test_lazy_array_nested(caplog):

    class _Test(m.Circuit):
        name = "test_when_lazy_array_nested"

        T = m.Product.from_fields("anon", {"x": m.Bit, "y": m.Bit})
        io = m.IO(S=m.In(m.Bit), O=m.Out(m.Array[2, T]))

        x = m.Array[2, T](name="x")

        with m.when(io.S):
            x[0][0] @= 0
            x[0][1] @= 1
            x[1][0] @= 0
            x[1][1] @= 1
        with m.otherwise():
            x[0][0] @= 1
            x[0][1] @= 0
            x[1][0] @= 1
            x[1][1] @= 0

        io.O @= x

    m.compile(f"build/{_Test.name}", _Test, output="mlir")
    assert check_gold(__file__, f"{_Test.name}.mlir")


def test_lazy_array_protocol(caplog):

    T = SimpleMagmaProtocol[m.Bit]

    class _Test(m.Circuit):
        name = "test_when_lazy_array_protocol"
        io = m.IO(S=m.In(m.Bit), O=m.Out(m.Array[2, T]))

        x = m.Array[2, T](name="x")

        with m.when(io.S):
            x[0] @= 0
            x[1] @= 0
        with m.otherwise():
            x[0] @= 1
            x[1] @= 1

        io.O @= x

    m.compile(f"build/{_Test.name}", _Test, output="mlir")
    assert check_gold(__file__, f"{_Test.name}.mlir")


def test_lazy_array_slice_driving_resolve(caplog):

    class _Test(m.Circuit):
        name = "test_when_lazy_array_slice_driving_resolve"
        io = m.IO(S=m.In(m.Bit), O=m.Out(m.Bits[4]))

        x = m.Bits[4](name="x")

        with m.when(io.S):
            x @= 2
        with m.otherwise():
            x @= 4

        io.O @= x
        x.value()[0]  # triggers driving bulk wire logic
        x[0] @= 1

    m.compile(f"build/{_Test.name}", _Test, output="mlir")
    assert check_gold(__file__, f"{_Test.name}.mlir")


def test_lazy_array_slice_driving_resolve_2(caplog):

    class _Test(m.Circuit):
        name = "test_when_lazy_array_slice_driving_resolve_2"
        io = m.IO(I=m.In(m.Bits[4]), S=m.In(m.Bit), O=m.Out(m.Bits[4]))

        x = m.Bits[4](name="x")

        with m.when(io.S):
            x @= io.I
        with m.otherwise():
            x @= 4

        io.O @= x
        io.I[0]  # triggers driving bulk wire logic
        x[-1] @= io.I[0]  # triggers driving bulk wire logic

    m.compile(f"build/{_Test.name}", _Test, output="mlir")
    assert check_gold(__file__, f"{_Test.name}.mlir")


def test_lazy_array_slice_overlap(caplog):

    class _Test(m.Circuit):
        name = "test_when_lazy_array_slice_overlap"
        io = m.IO(I=m.In(m.Bits[4]), S=m.In(m.Bit), O=m.Out(m.Bits[4]))

        with m.when(io.S):
            io.O @= io.I
        with m.otherwise():
            io.O[:2] @= io.I[2:]
            io.O[2:] @= io.I[:2]

    m.compile(f"build/{_Test.name}", _Test, output="mlir")
    assert check_gold(__file__, f"{_Test.name}.mlir")


def test_lazy_array_multiple_whens(caplog):

    class _Test(m.Circuit):
        name = "test_when_lazy_array_multiple_whens"
        io = m.IO(I=m.In(m.Bits[4]), S=m.In(m.Bit), O=m.Out(m.Bits[4]))

        with m.when(io.S):
            io.O @= io.I
        with m.otherwise():
            io.O[:2] @= io.I[2:]
            io.O[2:] @= io.I[:2]

        with m.when(~io.S):
            io.O @= io.I

    m.compile(f"build/{_Test.name}", _Test, output="mlir")
    assert check_gold(__file__, f"{_Test.name}.mlir")


def test_reg_ce():

    class _Test(m.Circuit):
        name = "test_when_reg_ce"
        io = m.IO(I=m.In(m.Bits[8]), O=m.Out(m.Bits[8]),
                  CE=m.In(m.Bit))

        x = m.Register(m.Bits[8], has_enable=True)()
        with m.when(io.CE):
            x.I @= io.I
        io.O @= x.O

    m.compile(f"build/{_Test.name}", _Test, output="mlir")
    assert check_gold(__file__, f"{_Test.name}.mlir")


def test_reg_ce_multiple():

    class _Test(m.Circuit):
        name = "test_when_reg_ce_multiple"
        io = m.IO(I=m.In(m.Bits[8]), O=m.Out(m.Bits[8]),
                  CE=m.In(m.Bits[2]))

        x = m.Register(m.Bits[8], has_enable=True)()
        with m.when(io.CE[0]):
            x.I @= io.I
        with m.elsewhen(io.CE[1]):
            x.I @= ~io.I

        io.O @= x.O

    m.compile(f"build/{_Test.name}", _Test, output="mlir")
    assert check_gold(__file__, f"{_Test.name}.mlir")


def test_when_latch_nested_multiple():
    # Should not raise a LatchError
    class _Test(m.Circuit):
        name = "test_when_latch_nested_multiple"
        io = m.IO(op=m.In(m.Bits[32]), O=m.Out(m.Bits[32]))

        pc = m.Register(m.Bits[32])()
        rc = m.Bits[32](name="rc")
        ra = m.Bits[32](0)
        rb = m.Bits[32](0)
        rai = m.Bits[8](0)
        rbi = m.Bits[8](0)
        rci = m.Bits[8](0)

        rc @= m.Bits[32](0)
        io.O @= rc
        with m.when(io.op[0]):
            pc.I @= pc.O
        with m.elsewhen(io.op[1]):
            pc.I @= 0
        with m.otherwise():
            with m.when(io.op == 0):
                rc @= ra + rb
            with m.elsewhen(io.op == 1):
                rc @= m.zext((rai << 8) | rbi, 24)
            with m.when(rci == 255):
                io.O @= 0xDE
            pc.I @= pc.O + 1


def test_reg_ce_already_wired():

    class _Test(m.Circuit):
        name = "test_when_reg_ce_already_wired"
        io = m.IO(I=m.In(m.Bits[8]), O=m.Out(m.Bits[8]),
                  x=m.In(m.Bit), y=m.In(m.Bit))

        x = m.Register(m.Bits[8], has_enable=True)()
        x.CE @= io.x
        with m.when(io.y):
            x.I @= io.I
        io.O @= x.O

    m.compile(f"build/{_Test.name}", _Test, output="mlir")
    assert check_gold(__file__, f"{_Test.name}.mlir")


def test_reg_ce_explicit_wire():

    class _Test(m.Circuit):
        name = "test_when_reg_ce_explicit_wire"
        io = m.IO(I=m.In(m.Bits[8]), O=m.Out(m.Bits[8]),
                  x=m.In(m.Bit), y=m.In(m.Bit))

        x = m.Register(m.Bits[8], has_enable=True)()
        with m.when(io.y):
            x.I @= io.I
            x.CE @= io.x
        io.O @= x.O

    m.compile(f"build/{_Test.name}", _Test, output="mlir")
    assert check_gold(__file__, f"{_Test.name}.mlir")


def test_reg_ce_explicit_wire_with_default():

    class _Test(m.Circuit):
        name = "test_when_reg_ce_explicit_wire_with_default"
        io = m.IO(I=m.In(m.Bits[8]), O=m.Out(m.Bits[8]),
                  x=m.In(m.Bit), y=m.In(m.Bit))

        x = m.Register(m.Bits[8], has_enable=True)()
        x.CE @= 1
        with m.when(io.y):
            x.I @= io.I
            x.CE @= io.x
        io.O @= x.O

    m.compile(f"build/{_Test.name}", _Test, output="mlir")
    assert check_gold(__file__, f"{_Test.name}.mlir")


def test_reg_ce_implicit_wire_twice():

    class _Test(m.Circuit):
        name = "test_when_reg_ce_implicit_wire_twice"
        io = m.IO(I=m.In(m.Bits[8]), O=m.Out(m.Bits[8]),
                  x=m.In(m.Bit), y=m.In(m.Bit))

        x = m.Register(m.Bits[8], has_enable=True)()
        with m.when(io.y):
            x.I @= io.I
        with m.when(io.x):
            x.I @= ~io.I
        io.O @= x.O

    m.compile(f"build/{_Test.name}", _Test, output="mlir")
    assert check_gold(__file__, f"{_Test.name}.mlir")


def test_reg_ce_explicit_wire_twice():

    class _Test(m.Circuit):
        name = "test_when_reg_ce_explicit_wire_twice"
        io = m.IO(I=m.In(m.Bits[8]), O=m.Out(m.Bits[8]),
                  x=m.In(m.Bit), y=m.In(m.Bit))

        x = m.Register(m.Bits[8], has_enable=True)()
        x.CE @= ~io.y
        with m.when(io.y):
            x.I @= io.I
        with m.when(io.x):
            x.I @= ~io.I
        io.O @= x.O

    m.compile(f"build/{_Test.name}", _Test, output="mlir")
    assert check_gold(__file__, f"{_Test.name}.mlir")


def test_user_reg():

    class Register(m.AbstractRegister):
        def __init__(self, T):
            self.io = m.IO(I=m.In(T), O=m.Out(T)) + m.ClockIO()
            self.verilog = """\
reg [7:0] x;
always @(posedge CLK)
    x <= I;
assign O = x;
"""

        def get_enable(self, inst):
            return None

    class _Test(m.Circuit):
        name = "test_when_user_reg"
        io = m.IO(I=m.In(m.Bits[8]), O=m.Out(m.Bits[8]), x=m.In(m.Bit))

        x = Register(m.Bits[8])()
        with m.when(io.x):
            x.I @= io.I

        io.O @= x.O

    m.compile(f"build/{_Test.name}", _Test, output="mlir")
    assert check_gold(__file__, f"{_Test.name}.mlir")


def test_user_reg_enable():

    class Register(m.AbstractRegister):
        def __init__(self, T):
            self.io = m.IO(I=m.In(T), O=m.Out(T), CE=m.In(m.Enable))
            self.io += m.ClockIO()
            self.verilog = """\
    reg [7:0] x;
    always @(posedge CLK)
        if (CE)
            x <= I;
    assign O = x;
    """

        def get_enable(self, inst):
            return inst.CE

    class _Test(m.Circuit):
        name = "test_when_user_reg_enable"
        io = m.IO(I=m.In(m.Bits[8]), O=m.Out(m.Bits[8]), x=m.In(m.Bits[2]))

        x = Register(m.Bits[8])()
        io.I[0]  # force elaboration to test enable logic
        with m.when(io.x[0]):
            x.I @= io.I
        with m.elsewhen(io.x[1]):
            x.I @= ~io.I

        io.O @= x.O

    m.compile(f"build/{_Test.name}", _Test, output="mlir")
    assert check_gold(__file__, f"{_Test.name}.mlir")


def test_when_output_resolve():

    class _Test(m.Circuit):
        name = "test_when_output_resolve"
        io = m.IO(I=m.In(m.Bits[8]),
                  x=m.In(m.Bit),
                  O0=m.Out(m.Bits[8]),
                  O1=m.Out(m.Bits[2]))

        x = m.Bits[8](name="x")
        x @= io.I

        with m.when(io.x):
            io.O0 @= x
        with m.otherwise():
            io.O0 @= ~x

        io.O1[1] @= io.O0.value()[0]  # direct reference to when builder output
        io.O1[0] @= io.O0.value()[1]  # direct reference to when builder output

    m.compile(f"build/{_Test.name}", _Test, output="mlir")
    assert check_gold(__file__, f"{_Test.name}.mlir")


def test_when_output_resolve2():

    class _Test(m.Circuit):
        name = "test_when_output_resolve2"
        io = m.IO(I=m.In(m.Bits[8]),
                  x=m.In(m.Bit),
                  O0=m.Out(m.Bits[8]),
                  O1=m.Out(m.Bits[8]))

        with m.when(io.x):
            io.O0 @= io.I
        with m.otherwise():
            io.O0 @= ~io.I

        io.O1 @= io.O0.value()  # direct reference to when builder output
        io.O1[0]  # force resolve

    m.compile(f"build/{_Test.name}", _Test, output="mlir")
    assert check_gold(__file__, f"{_Test.name}.mlir")


def test_when_spurious_assign():

    class U(m.Product):
        x = m.Bits[8]
        y = m.Bit

    class T(m.Product):
        x = m.Bits[8]
        y = U

    class _Test(m.Circuit):
        name = "test_when_spurious_assign"
        io = m.IO(x=m.In(m.Bits[8]),
                  y=m.In(m.Bit),
                  z=m.In(m.Bits[2]),
                  O=m.Out(T))
        reg = m.Register(T, has_enable=True)()
        io.O @= reg.O

        with m.when(io.z[0]):
            with m.when(io.z[1]):
                reg.I.y.x @= io.x
            with m.otherwise():
                reg.I.y.x @= 1
        with m.otherwise():
            reg.I.y.x @= ~io.x

        with m.when(io.z[1]):
            reg.I.y.y @= io.y
        with m.otherwise():
            reg.I.y.y @= ~io.y

        reg.I.x @= io.x
        reg.CE.rewire(io.z[0])

    m.compile(f"build/{_Test.name}", _Test,
              output="mlir", flatten_all_tuples=True)
    assert check_gold(__file__, f"{_Test.name}.mlir")


def test_reg_ce_implicit_override():

    class _Test(m.Circuit):
        name = "test_when_reg_ce_implicit_override"
        io = m.IO(I=m.In(m.Bits[8]), O=m.Out(m.Bits[8]),
                  x=m.In(m.Bit), y=m.In(m.Bit))

        x = m.Register(m.Bits[8], has_enable=True)()
        with m.when(io.y):
            x.I @= io.I
        x.CE @= io.x
        io.O @= x.O

    m.compile(f"build/{_Test.name}", _Test, output="mlir")
    assert check_gold(__file__, f"{_Test.name}.mlir")


def test_when_tuple_bulk_resolve(caplog):

    class V(m.Product):
        x = m.Bits[8]
        y = m.Bits[8]

    class U(m.Product):
        x = V
        y = V

    class T(m.Product):
        x = m.Bits[8]
        y = U

    class _Test(m.Circuit):
        name = "test_when_tuple_bulk_resolve"
        io = m.IO(I=m.In(T), S=m.In(m.Bits[2]), O=m.Out(T))

        x = m.Register(T)(name="x")
        y = m.Register(T)(name="y")
        with m.when(io.S[0]):
            x.I @= x.O
            y.I @= y.O
        with m.otherwise():
            with m.when(io.S[1]):
                x.I.x @= io.I.x
                x.I.y @= io.I.y
            with m.otherwise():
                x.I @= x.O
            y.I @= x.O
        io.O @= x.O

    assert not caplog.messages
    m.compile(f"build/{_Test.name}", _Test, output="mlir",
              flatten_all_tuples=True)
    assert check_gold(__file__, f"{_Test.name}.mlir")


def test_when_type_error():

    with pytest.raises(TypeError):
        class Foo(m.Circuit):
            io = m.IO(I=m.In(m.Bits[8]), O=m.Out(m.Bits[8]))
            with m.when(io.I):
                assert False, "Should raise type error for non bit type"

    with pytest.raises(TypeError):
        class Foo(m.Circuit):
            io = m.IO(I=m.In(m.Bits[8]), O=m.Out(m.Bits[8]))
            with m.when(io.I[0]):
                io.O @= 1
            with m.elsewhen(io.I):
                assert False, "Should raise type error for non bit type"


def test_when_partial_array_assign():
    class test_when_partial_array_assign(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bit), O=m.Out(m.Bits[2]))

        io.O[0] @= io.I[1]
        with m.when(io.S):
            io.O[1] @= io.I[0]
        with m.otherwise():
            io.O[1] @= io.I[1]

    m.compile("build/test_when_partial_array_assign",
              test_when_partial_array_assign, output="mlir")

    assert check_gold(__file__, "test_when_partial_array_assign.mlir")


def test_when_2d_array_assign():
    class test_when_2d_array_assign(m.Circuit):
        io = m.IO(I=m.In(m.Array[2, m.Bits[2]]), S=m.In(m.Bit),
                  O=m.Out(m.Array[2, m.Bits[2]]))

        with m.when(io.S):
            io.O @= io.I
        with m.otherwise():
            io.O[0] @= io.I[1]
            io.O[1] @= io.I[0]

    m.compile("build/test_when_2d_array_assign",
              test_when_2d_array_assign, output="mlir")

    assert check_gold(__file__, "test_when_2d_array_assign.mlir")


def test_when_nested_array_assign():
    class T(m.Product):
        x = m.Bit
        y = m.Tuple[m.Bit, m.Bits[8]]

    class test_when_nested_array_assign(m.Circuit):
        io = m.IO(I=m.In(T), S=m.In(m.Bit),
                  O=m.Out(T))
        io.O.x @= io.I.x
        io.O.y[0] @= io.I.y[0]

        with m.when(io.S):
            io.O.y[1] @= io.I.y[1]
        with m.otherwise():
            io.O.y[1] @= io.I.y[1][::-1]

    m.compile("build/test_when_nested_array_assign",
              test_when_nested_array_assign, output="mlir",
              flatten_all_tuples=True)

    assert check_gold(__file__, "test_when_nested_array_assign.mlir")


def test_when_partial_assign_order():
    class test_when_partial_assign_order(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bits[2]),
                  O0=m.Out(m.Bits[2]), O1=m.Out(m.Bits[2]),
                  O2=m.Out(m.Bits[2]))

        io.O0 @= io.I
        with m.when(io.S[0]):
            io.O1 @= m.bits((~io.I)[::-1])
            io.O2 @= io.I
        with m.elsewhen(io.S[1]):
            io.O1 @= io.I
            io.O2 @= io.I
        with m.otherwise():
            io.O1 @= ~io.I
            io.O0 @= m.bits(io.I[::-1])
            io.O2 @= ~io.I

    m.compile("build/test_when_partial_assign_order",
              test_when_partial_assign_order, output="mlir")

    assert check_gold(__file__, "test_when_partial_assign_order.mlir")


def test_when_3d_array_assign():
    class test_when_3d_array_assign(m.Circuit):
        T = m.Array[2, m.Array[2, m.Bits[2]]]
        io = m.IO(I=m.In(T), S=m.In(m.Bit), O=m.Out(T))

        with m.when(io.S):
            io.O @= io.I
        with m.otherwise():
            io.O[1][0] @= io.I[0][1]
            io.O[1][1] @= io.I[0][0]
            io.O[0][0] @= io.I[1][1]
            io.O[0][1] @= io.I[1][0]

    m.compile("build/test_when_3d_array_assign",
              test_when_3d_array_assign, output="mlir")

    assert check_gold(__file__, "test_when_3d_array_assign.mlir")


def test_when_array_resolved_after():
    class test_when_array_resolved_after(m.Circuit):
        io = m.IO(I=m.In(m.Bits[8]), S=m.In(m.Bit), O=m.Out(m.Bits[16]))

        x = m.Bits[8]()

        x @= ~io.I
        with m.when(io.S):
            x @= io.I

        io.O @= m.concat(m.Bits[8](0), x)  # trigger resolve

    m.compile("build/test_when_array_resolved_after",
              test_when_array_resolved_after, output="mlir")

    assert check_gold(__file__, "test_when_array_resolved_after.mlir")


def test_when_array_3d_bulk_child():
    class test_when_array_3d_bulk_child(m.Circuit):
        T = m.Array[2, m.Array[2, m.Bits[2]]]
        io = m.IO(I=m.In(T), S=m.In(m.Bit), O=m.Out(T))

        with m.when(io.S):
            io.O @= io.I
        with m.otherwise():
            io.O[1] @= io.I[0]
            io.O[0] @= io.I[1]

    m.compile("build/test_when_array_3d_bulk_child",
              test_when_array_3d_bulk_child, output="mlir")

    assert check_gold(__file__, "test_when_array_3d_bulk_child.mlir")


def test_when_temporary_resolved():
    class test_when_temporary_resolved(m.Circuit):
        io = m.IO(I=m.In(m.Bits[8]), S=m.In(m.Bits[2]), O=m.Out(m.Bits[8]))

        N = 8
        const = 4
        count = m.Register(m.Bits[N])()
        x = m.zext_to(count.O, N + 1) + m.zext_to(io.I, N + 1)
        y = x[0:N]
        z = m.zext_to((count.O - const), N)

        countNext = m.Bits[N]()

        with m.when(io.S[0]):
            countNext @= z
        with m.elsewhen(io.S[1]):
            countNext @= y
        with m.otherwise():
            countNext @= y - const

        # Force resolve
        for i in range(8):
            count.I[i] @= countNext[i]
        io.O @= countNext

    m.compile("build/test_when_temporary_resolved",
              test_when_temporary_resolved, output="mlir",
              disallow_local_variables=True)

    assert check_gold(__file__, "test_when_temporary_resolved.mlir")


def test_when_2d_array_assign_slice():
    class test_when_2d_array_assign_slice(m.Circuit):
        io = m.IO(I=m.In(m.Array[4, m.Bits[2]]), S=m.In(m.Bit),
                  O=m.Out(m.Array[4, m.Bits[2]]))

        with m.when(io.S):
            io.O @= io.I
        with m.otherwise():
            io.O[:2] @= io.I[2:]
            io.O[2:] @= io.I[:2]

    m.compile("build/test_when_2d_array_assign_slice",
              test_when_2d_array_assign_slice, output="mlir")

    assert check_gold(__file__, "test_when_2d_array_assign_slice.mlir")


def test_when_unique():

    class Gen(m.Generator2):
        def __init__(self, width: int):
            self.io = io = m.IO(
                a=m.In(m.Bits[8]),
                y=m.Out(m.Bits[8]),
            )
            with m.when(io.a[0]):
                io.y @= m.zext_to(io.a[:width], 8)
            with m.otherwise():
                io.y @= io.a

    class test_when_unique(m.Circuit):
        io = m.IO(
            a=m.In(m.Bits[8]),
            y=m.Out(m.Bits[8]),
        )
        io.y @= Gen(2)()(io.a) | Gen(4)()(io.a)

    m.compile("build/test_when_unique", test_when_unique, output="mlir")
    assert check_gold(__file__, "test_when_unique.mlir")


def test_when_tuple_as_bits_resolve():

    class V(m.Product):
        x = m.Bits[8]
        y = m.Bit

    class T(m.Product):
        y = m.Bit
        z = V
        x = m.Array[2, m.Bits[8]]

    class U(m.Product):
        x = T
        y = m.Bits[8]

    class test_when_tuple_as_bits_resolve(m.Circuit):
        io = m.IO(I=m.In(U), S=m.In(m.Bit),
                  O=m.Out(U), X=m.Out(m.Bits[U.flat_length()]))
        io.O.y @= io.I.y
        with m.when(io.S):
            for i in range(2):
                io.O.x.x[i] @= io.I.x.x[i]
            io.O.x.y @= io.I.x.y
            for key, port in io.O.x.items():
                if key == "z":
                    port @= m.mux([io.I.x.z, io.I.x.z], io.S)
        with m.otherwise():
            io.O @= io.I
        io.X @= m.as_bits(io.O.value())

    m.compile("build/test_when_tuple_as_bits_resolve",
              test_when_tuple_as_bits_resolve, output="mlir",
              flatten_all_tuples=True, disallow_local_variables=True)
    assert check_gold(__file__, "test_when_tuple_as_bits_resolve.mlir")


def test_when_alwcomb_order():
    class test_when_alwcomb_order(m.Circuit):
        io = m.IO(I=m.In(m.Bits[8]), S=m.In(m.Bits[1]), O=m.Out(m.Bits[8]))
        x = m.Bits[8]()

        io.O @= x
        with m.when(io.S[0]):
            x @= io.I
        with m.otherwise():
            x @= ~io.I
            io.O @= ~x

    with pytest.raises(NotImplementedError):
        m.compile("build/test_when_alwcomb_order", test_when_alwcomb_order,
                  output="mlir")


# TODO: In this case, we'll generate elaborated assignments, but it should
# be possible for us to pack these into a concat/create assignment
# def test_when_2d_array_assign():
#     class test_when_2d_array_assign(m.Circuit):
#         io = m.IO(I=m.In(m.Array[2, m.Bits[2]]), S=m.In(m.Bit),
#                   O=m.Out(m.Array[2, m.Bits[2]]))

#         with m.when(io.S):
#             io.O[0] @= io.I[1]
#             io.O[1] @= io.I[0]
#         with m.otherwise():
#             io.O[0] @= io.I[0]
#             io.O[1] @= io.I[1]

#     m.compile("build/test_when_2d_array_assign",
#               test_when_2d_array_assign, output="mlir")

#     assert check_gold(__file__, "test_when_2d_array_assign.mlir")
