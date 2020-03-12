import magma as m
import magma.testing
import os
import fault


def test_display(capsys):
    FF = m.define_from_verilog("""
module FF(input I, output reg O, input CLK, input CE);
always @(posedge CLK) begin
  if (CE) O <= I;
end
endmodule
    """, type_map={"CLK": m.In(m.Clock), "CE": m.In(m.Enable)})[0]

    class TestDisplay(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit)) + m.ClockIO(has_enable=True)
        ff = FF()
        io.O @= ff(io.I)
        m.display("ff.O=%d, ff.I=%d", ff.O, ff.I).when(m.posedge(io.CLK))\
                                                 .if_(io.CE)

    m.compile("build/TestDisplay", TestDisplay)
    assert not os.system('cd tests/test_verilog/build && '
                         'verilator --lint-only TestDisplay.v')
    assert m.testing.check_files_equal(__file__,
                                       f"build/TestDisplay.v",
                                       f"gold/TestDisplay.v")

    tester = fault.SynchronousTester(TestDisplay, TestDisplay.CLK)
    tester.poke(TestDisplay.CE, 1)
    tester.poke(TestDisplay.I, 1)
    tester.expect(TestDisplay.O, 0)
    tester.advance_cycle()
    tester.poke(TestDisplay.I, 0)
    tester.expect(TestDisplay.O, 1)
    tester.advance_cycle()
    tester.expect(TestDisplay.O, 0)
    tester.poke(TestDisplay.CE, 0)
    tester.poke(TestDisplay.I, 1)
    tester.advance_cycle()
    tester.expect(TestDisplay.O, 0)
    tester.poke(TestDisplay.I, 1)
    tester.advance_cycle()
    tester.expect(TestDisplay.O, 0)
    tester.poke(TestDisplay.CE, 1)
    tester.advance_cycle()
    tester.expect(TestDisplay.O, 1)
    tester.advance_cycle()

    directory = f"{os.path.abspath(os.path.dirname(__file__))}/build/"
    tester.compile_and_run(target="verilator", directory=directory,
                           flags=['-Wno-unused'], skip_compile=True,
                           disp_type="realtime")
    out, err = capsys.readouterr()
    assert f"""
ff.O=0, ff.I=1
ff.O=1, ff.I=0
ff.O=0, ff.I=1
ff.O=1, ff.I=1
""" in out
