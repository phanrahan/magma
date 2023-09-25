import pytest

import magma as m
import magma.testing
from magma.inline_verilog2 import InlineVerilogError


def _compile_and_check(top: m.DefineCircuitKind, **opts):
    basename = f"test_{top.name}"
    if opts.get('flatten_all_tuples', False):
        basename += "_flatten_all_tuples"
    m.compile(f"build/{basename}", top, output="mlir", **opts)
    assert m.testing.check_files_equal(
        __file__,
        f"build/{basename}.mlir",
        f"gold/{basename}.mlir",
    )


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

    _compile_and_check(_Top)


@pytest.mark.parametrize('flatten_all_tuples', [True, False])
def test_tuple(flatten_all_tuples):

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

    class _Top(m.Circuit):
        io = m.IO(I=RVDATAIN, O=m.Flip(RVDATAIN)) + m.ClockIO()
        name = "inline_verilog2_tuple"

        delay = DelayUnit()
        delay.INPUT[0] <= io.I[1]
        delay.INPUT[1] <= io.I[0]
        io.O[1] <= delay.OUTPUT[0]
        io.O[0] <= delay.OUTPUT[1]

        assertion = (
            "assert property (@(posedge CLK) {valid_out} |-> ##3 {ready_out});"
        )

        m.inline_verilog2(
            assertion,
            valid_out=io.I[0].valid,
            ready_out=io.O[1].ready,
        )

        # Test inst ref.
        m.inline_verilog2(
            assertion,
            valid_out=delay.OUTPUT[1].valid,
            ready_out=delay.INPUT[0].ready,
        )

        # Test recursive ref.
        m.inline_verilog2(
            assertion,
            valid_out=delay.inner_delay.OUTPUT[0].valid,
            ready_out=delay.inner_delay.INPUT[1].ready,
        )

        # Test double recursive ref.
        m.inline_verilog2(
            assertion,
            valid_out=delay.inner_delay.inner_inner_delay.OUTPUT[0].valid,
            ready_out=delay.inner_delay.inner_inner_delay.INPUT[1].ready,
        )

    _compile_and_check(_Top, flatten_all_tuples=flatten_all_tuples)


def test_undriven_port_error():

    def gen():

        class _(m.Circuit):
            io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit), arr=m.In(m.Bits[2])) + m.ClockIO()
            # Expect an error because io.O is undriven.
            m.inline_verilog2(
                "assert property (@(posedge CLK) {I} |-> ##1 {O});",
                O=io.O, I=io.I,
            )

    with pytest.raises(InlineVerilogError) as e:
        gen()

    assert str(e.value) == "Found reference to undriven input port: LazyCircuit.O"


def test_uniquification():
    # Check that 2 modules that differ only in their inlined modules (e.g. one
    # displays in "%d" format, the other "%x") are uniquified.

    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bit))
        m.inline_verilog2("always @(*) $display(\"%d\\n\", {io.I});")

    Bar = Foo

    class Foo(m.Circuit):
        io = m.IO(I=m.In(m.Bit))
        m.inline_verilog2("always @(*) $display(\"%x\\n\", {io.I});")

    class _Top(m.Circuit):
        name = "inline_verilog2_uniquification"
        io = m.IO(I=m.In(m.Bit))
        Bar()(io.I)
        Foo()(io.I)

    _compile_and_check(_Top)


def test_share_default_clocks():

    class _Top(m.Circuit):
        name = "inline_verilog2_share_default_clocks"
        io = m.IO(x=m.In(m.Bit), y=m.In(m.Bit)) + m.ClockIO(has_reset=True)

        clk = m.Clock()
        rst = m.Reset()
        m.inline_verilog2(
            "assert property (@(posedge {clk}) "
            "disable iff (! {rst}) {io.x} |-> ##1 {io.y});"
        )
        m.inline_verilog2(
            "assert property (@(posedge {clk}) "
            "disable iff (! {rst}) {io.x} |-> ##1 {io.y});"
        )

    _compile_and_check(_Top)


def test_passthrough_wire():

    class _Top(m.Circuit):
        name = "test_inline_verilog2_passthrough_wire"
        T = m.AnonProduct[dict(x=m.Bit, y=m.Bits[4])]
        io = m.IO(I=m.In(T), O=m.Out(T))
        io.O @= io.I

        m.inline_verilog2("assert {io.I.y[0]} == {io.I.y[1]}")
        m.inline_verilog2("assert {io.I.y[1:3]} == {io.I.y[2:4]}")

    _compile_and_check(_Top)


def test_clock_output():

    class _Top(m.Circuit):
        name = "test_inline_verilog2_clock_output"
        io = m.IO(x=m.In(m.Clock), y=m.In(m.Clock))
        m.inline_verilog2("Foo bar (.x({io.x}), .y({io.y}))")

    _compile_and_check(_Top)


def test_wire_insertion_bad_verilog():
    # See #1133 (https://github.com/phanrahan/magma/issues/1133).

    class _Top(m.Circuit):
        name = "test_inline_verilog2_wire_insertion_bad_verilog"
        io = m.IO(I=m.In(m.Bits[32]), O=m.Out(m.Bit))
        m.inline_verilog2("`ifdef LOGGING_ON")
        m.inline_verilog2("$display(\"%x\", {io.I[0]});")
        m.inline_verilog2("`endif LOGGING_ON")
        io.O @= io.I[0]

    _compile_and_check(_Top)
