import os

import fault
from hwtypes import BitVector, Bit

import magma as m
from magma.testing import check_files_equal


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
        Mem4x5[io.waddr] @= io.wdata

    m.compile("build/test_memory_basic", test_memory_basic)

    assert check_files_equal(__file__, f"build/test_memory_basic.v",
                             f"gold/test_memory_basic.v")
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
    tester.compile_and_run("verilator", skip_compile=True,
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))


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

    m.compile("build/test_memory_product", test_memory_product)

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
    tester.circuit.WEN = 0
    for i in range(4):
        tester.circuit.raddr = i
        tester.advance_cycle()
        tester.circuit.rdata.expect(expected[i])
    tester.compile_and_run("verilator", skip_compile=True,
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

    m.compile("build/test_memory_arr", test_memory_arr)

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
    tester.circuit.WEN = 0
    for i in range(4):
        tester.circuit.raddr = i
        tester.advance_cycle()
        tester.circuit.rdata.expect(expected[i])
    tester.compile_and_run("verilator", skip_compile=True,
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))


def test_memory_read_latency():
    class test_memory_read_latency(m.Circuit):
        io = m.IO(
            raddr=m.In(m.Bits[2]),
            rdata=m.Out(m.Bits[5]),
            waddr=m.In(m.Bits[2]),
            wdata=m.In(m.Bits[5]),
            clk=m.In(m.Clock),
            wen=m.In(m.Enable)

        )
        Mem4x5 = m.Memory(4, m.Bits[5], read_latency=2)()
        Mem4x5.RADDR @= io.raddr
        io.rdata @= Mem4x5.RDATA
        Mem4x5.WADDR @= io.waddr
        Mem4x5.WDATA @= io.wdata

    m.compile("build/test_memory_read_latency", test_memory_read_latency)

    assert check_files_equal(__file__, f"build/test_memory_read_latency.v",
                             f"gold/test_memory_read_latency.v")
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
    for i in range(5):
        tester.circuit.raddr = i
        tester.advance_cycle()
        tester.circuit.rdata.expect(expected[i])
    tester.compile_and_run("verilator", skip_compile=True,
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
                           directory=os.path.join(os.path.dirname(__file__),
                                                  "build"))


def test_memory_warning(caplog):
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
        Mem4x5[io.waddr] @= io.wdata

        io.rdata @= Mem4x5[io.raddr]
        Mem4x5[io.waddr] @= io.wdata

    assert "Reading __getitem__ result from a Memory instance with RADDR already driven, will overwrite previous value" in caplog.messages  # noqa
    assert "Wiring __getitem__ result from a Memory instance with WADDR or WDATA already driven, will overwrite previous values" in caplog.messages  # noqa
