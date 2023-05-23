import pytest

import magma as m
import magma.testing


def test_simple():

    class _Top(m.Circuit):
        name = "inline_verilog2_simple"
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit), arr=m.In(m.Bits[2]))
        io += m.ClockIO()
        io.O <= m.register(io.I)
        m.inline_verilog2(
            "assert property (@(posedge CLK) {I} |-> ##1 {O});\n",
            O=io.O,
            I=io.I,
        )
        m.inline_verilog2(
            "assert property (@(posedge CLK) {io.arr[0]} |-> ##1 {io.arr[1]});\n",
        )

    m.compile(f"build/test_inline_verilog2_simple", _Top, output="mlir-verilog")
    assert m.testing.check_files_equal(
        __file__,
        f"build/test_inline_verilog2_simple.mlir",
        f"gold/test_inline_verilog2_simple.mlir",
    )


def test_tuple():

    class RV(m.Product):
        data = m.In(m.Bits[5])
        valid = m.In(m.Bit)
        ready = m.Out(m.Bit)

    RVDATAIN = m.Array[2, RV]

    class InnerInnerDelayUnit(m.Circuit):
        name = "InnerInnerDelayUnit"
        io = m.IO(INPUT=RVDATAIN, OUTPUT=m.Flip(RVDATAIN))

    class InnerDelayUnit(m.Circuit):
        io = m.IO(INPUT=RVDATAIN, OUTPUT=m.Flip(RVDATAIN)) + m.ClockIO()

        delay = InnerInnerDelayUnit(name="inner_inner_delay")
        delay.INPUT[0] <= io.INPUT[1]
        delay.INPUT[1] <= io.INPUT[0]
        io.OUTPUT[0] <= delay.OUTPUT[1]
        io.OUTPUT[1] <= delay.OUTPUT[0]

    class DelayUnit(m.Circuit):
        io = m.IO(INPUT=RVDATAIN, OUTPUT=m.Flip(RVDATAIN)) + m.ClockIO()

        delay = InnerDelayUnit(name="inner_delay")
        delay.INPUT[0] <= io.INPUT[1]
        delay.INPUT[1] <= io.INPUT[0]
        io.OUTPUT[0] <= delay.OUTPUT[1]
        io.OUTPUT[1] <= delay.OUTPUT[0]

    top_name = "inline_verilog2_tuple"

    class _Top(m.Circuit):
        io = m.IO(I=RVDATAIN, O=m.Flip(RVDATAIN)) + m.ClockIO()
        name = top_name

        delay = DelayUnit()
        delay.INPUT[0] <= io.I[1]
        delay.INPUT[1] <= io.I[0]
        io.O[1] <= delay.OUTPUT[0]
        io.O[0] <= delay.OUTPUT[1]

        assertion = (
            "assert property (@(posedge CLK) {valid_out} |-> ##3 {ready_out});"
        )

        m.inline_verilog(
            assertion,
            valid_out=io.I[0].valid,
            ready_out=io.O[1].ready,
        )

        # Test inst ref.
        m.inline_verilog(
            assertion,
            valid_out=delay.OUTPUT[1].valid,
            ready_out=delay.INPUT[0].ready,
        )

        # Test recursive ref.
        m.inline_verilog(
            assertion,
            valid_out=delay.inner_delay.OUTPUT[0].valid,
            ready_out=delay.inner_delay.INPUT[1].ready,
        )

        # Test double recursive ref.
        m.inline_verilog(
            assertion,
            valid_out=delay.inner_delay.inner_inner_delay.OUTPUT[0].valid,
            ready_out=delay.inner_delay.inner_inner_delay.INPUT[1].ready,
        )

    basename = f"test_{top_name}"
    m.compile(f"build/{basename}", _Top, output="mlir-verilog")
    assert m.testing.check_files_equal(
        __file__,
        f"build/{basename}.mlir",
        f"gold/{basename}.mlir",
    )
