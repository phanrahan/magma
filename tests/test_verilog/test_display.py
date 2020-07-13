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
        m.display("%0t: ff.O=%d, ff.I=%d", m.time(), ff.O,
                  io.I).when(m.posedge(io.CLK)).if_(io.CE)

    m.compile("build/TestDisplay", TestDisplay, inline=True)
    assert not os.system('cd tests/test_verilog/build && '
                         'verilator --lint-only TestDisplay.v '
                         '--top-module TestDisplay')
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
0: ff.O=0, ff.I=1
10: ff.O=1, ff.I=0
40: ff.O=0, ff.I=1
50: ff.O=1, ff.I=1
""" in out, out


def test_fdisplay():
    FF = m.define_from_verilog("""
module FF(input I, output reg O, input CLK, input CE);
always @(posedge CLK) begin
  if (CE) O <= I;
end
endmodule
    """, type_map={"CLK": m.In(m.Clock), "CE": m.In(m.Enable)})[0]

    class TestFDisplay(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit)) + m.ClockIO(has_enable=True)
        ff = FF()
        io.O @= ff(io.I)
        with m.File("test_fdisplay.log", "a") as log_file:
            m.display("ff.O=%d, ff.I=%d", ff.O, io.I, file=log_file).when(m.posedge(io.CLK))\
                                                                    .if_(io.CE)

    m.compile("build/TestFDisplay", TestFDisplay, inline=True)
    assert not os.system('cd tests/test_verilog/build && '
                         'verilator --lint-only TestFDisplay.v '
                         '--top-module TestFDisplay')
    assert m.testing.check_files_equal(__file__,
                                       f"build/TestFDisplay.v",
                                       f"gold/TestFDisplay.v")

    tester = fault.SynchronousTester(TestFDisplay, TestFDisplay.CLK)
    tester.poke(TestFDisplay.CE, 1)
    tester.poke(TestFDisplay.I, 1)
    tester.expect(TestFDisplay.O, 0)
    tester.advance_cycle()
    tester.poke(TestFDisplay.I, 0)
    tester.expect(TestFDisplay.O, 1)
    tester.advance_cycle()
    tester.expect(TestFDisplay.O, 0)
    tester.poke(TestFDisplay.CE, 0)
    tester.poke(TestFDisplay.I, 1)
    tester.advance_cycle()
    tester.expect(TestFDisplay.O, 0)
    tester.poke(TestFDisplay.I, 1)
    tester.advance_cycle()
    tester.expect(TestFDisplay.O, 0)
    tester.poke(TestFDisplay.CE, 1)
    tester.advance_cycle()
    tester.expect(TestFDisplay.O, 1)
    tester.advance_cycle()

    directory = f"{os.path.abspath(os.path.dirname(__file__))}/build/"
    tester.compile_and_run(target="verilator", directory=directory,
                           flags=['-Wno-unused'], skip_compile=True)
    with open(os.path.join(directory, "test_fdisplay.log"), "r") as f:
        assert f"""\
ff.O=0, ff.I=1
ff.O=1, ff.I=0
ff.O=0, ff.I=1
ff.O=1, ff.I=1
""" in f.read()
