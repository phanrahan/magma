import os
import pytest

import magma as m
from magma.testing.utils import check_gold, update_gold
from magma.type_utils import type_to_sanitized_string
from magma.backend.mlir.check_latches import LatchError

import fault as f


def test_when_with_default():
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


def test_when_nested_with_default():
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


def test_when_override(caplog):
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

    expected = ("Wiring a previously conditionally wired value "
                "(test_when_override.O), existing conditional drivers will be "
                "discarded")
    assert str(caplog.records[0].msg) == expected

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


def test_when_else():
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


def test_when_elsewhen():
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
def test_when_bad_syntax(fn, name):
    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bits[3]), S=m.In(m.Bits[2]), O=m.Out(m.Bit))

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
def test_when_bad_otherwise(fn, name):
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


def test_when_multiple_drivers():
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
    (m.Tuple[m.Bit, m.Bits[7]], lambda x: (bool(x[7]), int(x[:7])))
])
def test_when_memory(T, bits_to_fault_value):
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

    tester = f.SynchronousTester(test_when_memory)
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
        (m.Array[2, m.Tuple[m.Bit, m.Bits[2]]],
         [[(0, 1), (1, 0)], [(1, 0), (0, 1)]]),
        (m.Tuple[m.Bits[2], m.Bit],
         [(0b10, 0b1), (0b01, 0b0)])
    ]
)
def test_when_nested(T, x):
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


def test_when_register_default():
    class test_when_register_default(m.Circuit):
        io = m.IO(I=m.In(m.Bit), E=m.In(m.Bit), O=m.Out(m.Bit))

        reg = m.Register(m.Bit)()

        with m.when(io.E):
            reg.I @= io.I

        io.O @= reg.O

    m.compile("build/test_when_register_default", test_when_register_default,
              output="mlir")

    if check_gold(__file__, "test_when_register_default.mlir"):
        return

    tester = f.SynchronousTester(test_when_register_default)
    tester.poke(test_when_register_default.I, 1)
    tester.poke(test_when_register_default.E, 0)
    tester.advance_cycle()
    tester.expect(test_when_register_default.O, 0)
    tester.advance_cycle()
    tester.poke(test_when_register_default.E, 1)
    tester.advance_cycle()
    tester.poke(test_when_register_default.I, 0)
    tester.poke(test_when_register_default.E, 0)
    tester.expect(test_when_register_default.O, 1)
    tester.advance_cycle()
    tester.expect(test_when_register_default.O, 1)
    tester.poke(test_when_register_default.E, 1)
    tester.advance_cycle()
    tester.expect(test_when_register_default.O, 0)

    tester.compile_and_run("verilator", magma_output="mlir-verilog",
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))
    update_gold(__file__, "test_when_register_default.mlir")


def test_when_latch_error_simple():
    class test_when_latch_error_simple(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bit), O=m.Out(m.Bit))

        with m.when(io.S):
            io.O @= io.I[0]

    with pytest.raises(LatchError) as e:
        m.compile("build/test_when_latch_error_simple",
                  test_when_latch_error_simple,
                  output="mlir")

    expected = ("Error while compiling test_when_latch_error_simple("
                "I: In(Bits[2]), S: In(Bit), O: Out(Bit)),"
                " detected potential latches: [test_when_latch_error_simple.O]")
    assert str(e.value) == expected


def test_when_latch_error_elsewhen():
    class test_when_latch_error_elsewhen(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bit), O=m.Out(m.Bit))

        with m.when(io.S):
            io.O @= io.I[0]
        with m.elsewhen(io.S ^ 1):
            io.O @= 1

    with pytest.raises(LatchError) as e:
        m.compile("build/test_when_latch_error_elsewhen",
                  test_when_latch_error_elsewhen,
                  output="mlir")

    expected = ("Error while compiling test_when_latch_error_elsewhen("
                "I: In(Bits[2]), S: In(Bit), O: Out(Bit)),"
                " detected potential latches: "
                "[test_when_latch_error_elsewhen.O]")
    assert str(e.value) == expected


def test_when_latch_error_nested():
    class test_when_latch_error_nested(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bits[2]), O=m.Out(m.Bit))

        with m.when(io.S[0]):
            with m.when(io.S[1]):
                io.O @= io.I[0]

    with pytest.raises(LatchError) as e:
        m.compile("build/test_when_latch_error_nested",
                  test_when_latch_error_nested,
                  output="mlir")

    expected = ("Error while compiling test_when_latch_error_nested("
                "I: In(Bits[2]), S: In(Bits[2]), O: Out(Bit)),"
                " detected potential latches: "
                "[test_when_latch_error_nested.O]")
    assert str(e.value) == expected


def test_when_latch_no_error_nested():
    class test_when_latch_no_error_nested(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bits[2]), O=m.Out(m.Bit))

        with m.when(io.S[0]):
            io.O @= io.I[1]
            with m.when(io.S[1]):
                io.O @= io.I[0]
        with m.otherwise():
            io.O @= 1

    m.compile("build/test_when_latch_no_error_nested",
              test_when_latch_no_error_nested,
              output="mlir")


def test_when_latch_no_error_nested2():
    class test_when_latch_no_error_nested2(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bits[2]), O=m.Out(m.Bit))

        with m.when(io.S[0]):
            with m.when(io.S[1]):
                io.O @= io.I[0]
            with m.otherwise():
                io.O @= io.I[1]
        with m.otherwise():
            io.O @= 1

    m.compile("build/test_when_latch_no_error_nested",
              test_when_latch_no_error_nested2,
              output="mlir")


def test_when_mixed_wiring():
    class test_when_mixed_wiring(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bit), O=m.Out(m.Bit))

        with m.when(io.S):
            io.O @= io.I[0] & 1
        with m.otherwise():
            io.O @= io.I[1] ^ 1

    m.compile("build/test_when_mixed_wiring", test_when_mixed_wiring,
              output="mlir")

    if check_gold(__file__, "test_when_mixed_wiring.mlir"):
        return

    tester = f.Tester(test_when_mixed_wiring)
    tester.poke(test_when_mixed_wiring.I, 0b10)
    tester.poke(test_when_mixed_wiring.S, 0)
    tester.eval()
    tester.expect(test_when_mixed_wiring.O, 0)
    tester.poke(test_when_mixed_wiring.S, 1)
    tester.eval()
    tester.expect(test_when_mixed_wiring.O, 0)
    tester.poke(test_when_mixed_wiring.I, 0b11)
    tester.eval()
    tester.expect(test_when_mixed_wiring.O, 1)
    tester.poke(test_when_mixed_wiring.S, 0)
    tester.eval()
    tester.expect(test_when_mixed_wiring.O, 0)

    tester.compile_and_run("verilator", magma_output="mlir-verilog",
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))
    update_gold(__file__, "test_when_mixed_wiring.mlir")