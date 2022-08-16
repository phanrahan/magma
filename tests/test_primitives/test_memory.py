import os
import pytest

import fault
from hwtypes import BitVector, Bit

import magma as m
from magma.backend.mlir.mlir_to_verilog import circt_opt_binary_exists
from magma.testing import check_files_equal
from magma.testing.utils import check_gold, update_gold


def test_memory_basic():
    class test_memory_basic(m.Circuit):
        io = m.IO(
            raddr=m.In(m.Bits[2]),
            rdata=m.Out(m.Bits[5]),
            waddr=m.In(m.Bits[2]),
            wdata=m.In(m.Bits[5]),
            clk=m.In(m.Clock),
            wen=m.In(m.Enable)

        )
        Mem4x5 = m.Memory(4, m.Bits[5])()
        io.rdata @= Mem4x5[io.raddr]
        with m.when(io.wen):
            Mem4x5[io.waddr] @= io.wdata

    m.compile("build/test_memory_basic", test_memory_basic, output="mlir")

    if check_gold(__file__, "test_memory_basic.mlir"):
        return

    if not circt_opt_binary_exists():
        return

    tester = fault.SynchronousTester(test_memory_basic, test_memory_basic.clk)
    expected = []
    for i in range(4):
        tester.circuit.waddr = i
        tester.circuit.wdata = wdata = BitVector.random(5)
        expected.append(wdata)
        tester.circuit.wen = 1
        tester.advance_cycle()
    tester.circuit.wen = 0
    for i in range(4):
        tester.circuit.raddr = i
        tester.advance_cycle()
        tester.circuit.rdata.expect(expected[i])
    tester.compile_and_run("verilator", magma_output="mlir-verilog",
                           flags=["-Wno-unused"],
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))
    update_gold(__file__, "test_memory_basic.mlir")


def test_memory_product():
    class T(m.Product):
        X = m.Bit
        Y = m.Bits[5]

    class test_memory_product(m.Circuit):
        io = m.IO(
            raddr=m.In(m.Bits[2]),
            rdata=m.Out(T),
            waddr=m.In(m.Bits[2]),
            wdata=m.In(T),
            clk=m.In(m.Clock),
            wen=m.In(m.Enable)

        )
        Mem4xT = m.Memory(4, T)()
        Mem4xT.RADDR @= io.raddr
        io.rdata @= Mem4xT.RDATA
        Mem4xT.WADDR @= io.waddr
        Mem4xT.WDATA @= io.wdata
        Mem4xT.WE @= 1

    m.compile("build/test_memory_product", test_memory_product, inline=True)
    assert check_files_equal(__file__, f"build/test_memory_product.v",
                             f"gold/test_memory_product.v")
    tester = fault.SynchronousTester(test_memory_product,
                                     test_memory_product.clk)
    expected = []
    for i in range(4):
        tester.circuit.waddr = i
        tester.circuit.wdata = wdata = (BitVector.random(1),
                                        BitVector.random(5))
        expected.append(wdata)
        tester.circuit.wen = 1
        tester.advance_cycle()
    tester.circuit.wen = 0
    for i in range(4):
        tester.circuit.raddr = i
        tester.advance_cycle()
        tester.circuit.rdata.expect(expected[i])
    tester.compile_and_run("verilator", skip_compile=True,
                           flags=["-Wno-unused"],
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))


def test_memory_product_init():
    class T(m.Product):
        X = m.SInt[8]
        Y = m.SInt[8]

    test_data = [
        {"X": 0, "Y": -128},
        {"X": -128, "Y": 127},
        {"X": -1, "Y": -1},
        {"X": 127, "Y": 0},
    ]

    class test_memory_product_init(m.Circuit):
        init_value = [
            m.product(X=m.sint(d["X"], 8), Y=m.sint(d["Y"], 8))
            for d in test_data
        ]

        io = m.IO(
            raddr=m.In(m.Bits[2]),
            rdata=m.Out(T),
            clk=m.In(m.Clock),
        )
        Mem4xT = m.Memory(len(test_data), T, read_only=True,
                          init=tuple(init_value))()
        Mem4xT.RADDR @= io.raddr
        io.rdata @= Mem4xT.RDATA

    m.compile("build/test_memory_product_init", test_memory_product_init,
              inline=True)

    assert check_files_equal(__file__, f"build/test_memory_product_init.v",
                             f"gold/test_memory_product_init.v")
    tester = fault.SynchronousTester(test_memory_product_init,
                                     test_memory_product_init.clk)
    for i in range(4):
        tester.circuit.raddr = i
        tester.advance_cycle()
        tester.circuit.rdata.X.expect(test_data[i]["X"])
        tester.circuit.rdata.Y.expect(test_data[i]["Y"])
    tester.compile_and_run("verilator", skip_compile=True,
                           flags=["-Wno-unused"],
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))


def test_memory_arr():
    class T(m.Product):
        X = m.Bit
        Y = m.Bits[5]

    class test_memory_arr(m.Circuit):
        io = m.IO(
            raddr=m.In(m.Bits[2]),
            rdata=m.Out(m.Array[2, T]),
            waddr=m.In(m.Bits[2]),
            wdata=m.In(m.Array[2, T]),
            clk=m.In(m.Clock),
            wen=m.In(m.Enable)

        )
        Mem4xT = m.Memory(4, m.Array[2, T])()
        Mem4xT.RADDR @= io.raddr
        io.rdata @= Mem4xT.RDATA
        Mem4xT.WADDR @= io.waddr
        Mem4xT.WDATA @= io.wdata
        Mem4xT.WE @= 1

    m.compile("build/test_memory_arr", test_memory_arr, inline=True)

    assert check_files_equal(__file__, f"build/test_memory_arr.v",
                             f"gold/test_memory_arr.v")
    tester = fault.SynchronousTester(test_memory_arr,
                                     test_memory_arr.clk)
    expected = []
    for i in range(4):
        tester.circuit.waddr = i
        tester.circuit.wdata = wdata = [
            (BitVector.random(1), BitVector.random(5)) for _ in range(2)
        ]
        expected.append(wdata)
        tester.circuit.wen = 1
        tester.advance_cycle()
    tester.circuit.wen = 0
    for i in range(4):
        tester.circuit.raddr = i
        tester.advance_cycle()
        tester.circuit.rdata.expect(expected[i])
    tester.compile_and_run("verilator", skip_compile=True,
                           flags=["-Wno-unused"],
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))


@pytest.mark.parametrize('en', [True, False])
def test_memory_read_latency(en):
    class test_memory_read_latency(m.Circuit):
        name = f"test_memory_read_latency_{en}"
        io = m.IO(
            raddr=m.In(m.Bits[2]),
            rdata=m.Out(m.Bits[5]),
            waddr=m.In(m.Bits[2]),
            wdata=m.In(m.Bits[5]),
            clk=m.In(m.Clock),
            wen=m.In(m.Enable),
        )
        Mem4x5 = m.Memory(4, m.Bits[5], read_latency=2,
                          has_read_enable=en)()
        if en:
            io += m.IO(ren=m.In(m.Enable))
            rdata = Mem4x5.read(io.raddr, io.ren)
        else:
            rdata = Mem4x5.read(io.raddr)
        io.rdata @= Mem4x5.RDATA
        Mem4x5.write(io.wdata, io.waddr, io.wen)

    m.compile(f"build/test_memory_read_latency_{en}",
              test_memory_read_latency)

    assert check_files_equal(__file__,
                             f"build/test_memory_read_latency_{en}.v",
                             f"gold/test_memory_read_latency_{en}.v")
    tester = fault.SynchronousTester(test_memory_read_latency,
                                     test_memory_read_latency.clk)
    expected = []
    for i in range(4):
        tester.circuit.waddr = i
        tester.circuit.wdata = wdata = BitVector.random(5)
        expected.append(wdata)
        tester.circuit.wen = 1
        tester.advance_cycle()
    tester.circuit.wen = 0
    expected = [expected[0]] + expected
    if en:
        # Reads haven't started yet
        expected[0] = 0
        tester.circuit.ren = 1
    for i in range(5):
        tester.circuit.raddr = i
        tester.advance_cycle()
        tester.circuit.rdata.expect(expected[i])
    if en:
        # Check read addr 0 again
        tester.circuit.raddr = 0
        tester.advance_cycle()
        tester.advance_cycle()
        tester.circuit.rdata.expect(expected[1])
        # Read enable low, should hold expect[1] (skip first 0)
        tester.circuit.ren = 0
        tester.circuit.raddr = 1
        tester.advance_cycle()
        tester.advance_cycle()
        tester.circuit.rdata.expect(expected[1])
        tester.advance_cycle()
        tester.circuit.rdata.expect(expected[1])
        # Read enable high, should see expect[2] in two cycles
        tester.circuit.ren = 1
        tester.advance_cycle()
        tester.circuit.rdata.expect(expected[1])
        tester.advance_cycle()
        tester.circuit.rdata.expect(expected[2])
    tester.compile_and_run("verilator", skip_compile=True,
                           flags=["-Wno-unused"],
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))


def test_memory_read_only():
    init = (7, 10, 19, 0)

    class test_memory_read_only(m.Circuit):
        io = m.IO(
            raddr=m.In(m.Bits[2]),
            rdata=m.Out(m.Bits[5]),
            clk=m.In(m.Clock),
        )
        Mem4x5 = m.Memory(4, m.Bits[5], read_only=True, init=init)()
        Mem4x5.RADDR @= io.raddr
        io.rdata @= Mem4x5.RDATA

    m.compile("build/test_memory_read_only", test_memory_read_only)

    assert check_files_equal(__file__, f"build/test_memory_read_only.v",
                             f"gold/test_memory_read_only.v")
    tester = fault.SynchronousTester(test_memory_read_only,
                                     test_memory_read_only.clk)
    for i in range(4):
        tester.circuit.raddr = i
        tester.advance_cycle()
        tester.circuit.rdata.expect(init[i])
    tester.compile_and_run("verilator", skip_compile=True,
                           flags=["-Wno-unused"],
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))
