import shutil
import os

import pytest

import magma as m
from magma.testing import check_files_equal

import fault as f


def _check_gold(filename):
    try:
        return check_files_equal(__file__,
                                 f"build/{filename}",
                                 f"gold/{filename}")
    except FileNotFoundError:
        return False


def _update_gold(filename):
    file_path = os.path.dirname(__file__)
    return shutil.copy(f"{file_path}/build/{filename}",
                       f"{file_path}/gold/{filename}")


def test_when_with_default():
    class test_when_with_default(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bit), O=m.Out(m.Bit))

        io.O @= io.I[1]
        with m.when(io.S):
            io.O @= io.I[0]

    m.compile("build/test_when_with_default", test_when_with_default,
              output="mlir")

    if _check_gold("test_when_with_default.mlir"):
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
    _update_gold("test_when_with_default.mlir")


def test_when_nested_with_default():
    class test_when_nested_with_default(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bits[2]), O=m.Out(m.Bit))

        io.O @= io.I[1]
        with m.when(io.S[0]) as c0:
            with m.when(io.S[1]) as c1:
                io.O @= io.I[0]

    m.compile("build/test_when_nested_with_default",
              test_when_nested_with_default, output="mlir")

    if _check_gold("test_when_nested_with_default.mlir"):
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

    _update_gold("test_when_nested_with_default.mlir")


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

    if _check_gold("test_when_override.mlir"):
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

    _update_gold("test_when_override.mlir")


def test_when_else():
    class test_when_else(m.Circuit):
        io = m.IO(I=m.In(m.Bits[2]), S=m.In(m.Bit), O=m.Out(m.Bit))

        with m.when(io.S):
            io.O @= io.I[0]
        with m.otherwise():
            io.O @= io.I[1]

    m.compile("build/test_when_else", test_when_else, output="mlir")

    if _check_gold("test_when_else.mlir"):
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

    _update_gold("test_when_else.mlir")


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

    if _check_gold("test_when_elsewhen.mlir"):
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

    _update_gold("test_when_elsewhen.mlir")


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

    if _check_gold("test_when_multiple_drivers.mlir"):
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

    _update_gold("test_when_multiple_drivers.mlir")


def test_when_memory():
    class test_when_memory(m.Circuit):
        io = m.IO(
            data0=m.In(m.Bits[8]), addr0=m.In(m.Bits[5]), en0=m.In(m.Bit),
            data1=m.In(m.Bits[8]), addr1=m.In(m.Bits[5]), en1=m.In(m.Bit),
            out=m.Out(m.Bits[8])
        ) + m.ClockIO()

        mem = m.Memory(32, m.Bits[8])()
        with m.when(io.en0):
            mem[io.addr0] @= io.data0
            io.out @= mem[io.addr1]
        with m.elsewhen(io.en1):
            mem[io.addr1] @= io.data1
            io.out @= mem[io.addr0]
        with m.otherwise():
            io.out @= 0xFF

    m.compile("build/test_when_memory", test_when_memory,
              output="mlir")

    if _check_gold("test_when_memory.mlir"):
        return

    tester = f.SynchronousTester(test_when_memory)
    tester.advance_cycle()
    tester.expect(test_when_memory.out, 0xFF)

    tester.advance_cycle()

    tester.poke(test_when_memory.data0, 0xDE)
    tester.poke(test_when_memory.addr0, 0xAD)

    tester.poke(test_when_memory.data1, 0xBE)
    tester.poke(test_when_memory.addr1, 0xEF)
    tester.poke(test_when_memory.en0, 1)
    tester.advance_cycle()

    tester.expect(test_when_memory.out, 0)
    tester.poke(test_when_memory.en0, 0)
    tester.poke(test_when_memory.en1, 1)
    tester.advance_cycle()

    tester.expect(test_when_memory.out, 0xDE)
    tester.poke(test_when_memory.en0, 1)
    tester.poke(test_when_memory.en1, 0)
    tester.poke(test_when_memory.addr1, 0xAD)
    tester.advance_cycle()

    tester.expect(test_when_memory.out, 0xDE)

    tester.compile_and_run("verilator", magma_output="mlir-verilog",
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))

    _update_gold("test_when_memory.mlir")


@pytest.mark.parametrize('T', [m.Array[2, m.Tuple[m.Bit, m.Bits[2]]],
                               m.Tuple[m.Bits[2], m.Bit]])
def test_when_nested(T):

    T_str = str(T)\
        .replace('(', '')\
        .replace(')', '')\
        .replace('[', '')\
        .replace(']', '')\
        .replace(',', '')\
        .replace(' ', '')

    class test_when_nested(m.Circuit):
        name = f"test_when_nested_{T_str}"
        io = m.IO(I=m.In(m.Array[2, T]),
                  S=m.In(m.Bit),
                  O=m.Out(T))

        io.O @= io.I[1]
        with m.when(io.S):
            io.O @= io.I[0]

    m.compile(f"build/test_when_nested_{T_str}", test_when_nested,
              output="mlir")

    if _check_gold(f"test_when_nested_{T_str}.mlir"):
        return

    # TODO: fault support for mlir nested types
    _update_gold(f"test_when_nested_{T_str}.mlir")
