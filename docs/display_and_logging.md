# m.display

Magma supports using verilog display with the coreir-verilog backend using the
`m.display` function.  This function accepts a standard display format string
as the first argument and a variable number of arguments corresponding to magma
values.  These magma values will be interpolated into the generated display
statement to display their runtime values.

`m.display` returns an object that supports method-chaining for specifying
event triggers and conditions.  For example, to trigger display only on the
positive edge of a clock, one would write `m.display("<str>"
*args).when(m.posedge(io.CLK))`.  Currently magma provides the `m.posedge` and
`m.negedge` events.  You can also guard the display statement with a condition using
the `if_` method, for example to only display when the clock enable is high,
one would write `m.display("<str>").if_(io.CE)`.

Here is a full example:
```python
class Main(m.Circuit):
    io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit)) + m.ClockIO(has_enable=True)
    ff = FF()
    io.O @= ff(io.I)
    m.display("ff.O=%d, ff.I=%d", ff.O, ff.I).when(m.posedge(io.CLK))\
                                             .if_(io.CE)
```

This produces the following snippet of verilog for the display statement:
```verilog
always @(posedge CLK) begin
    if (CE) $display("ff.O=%d, ff.I=%d", FF_inst0.O, FF_inst0.I);
end
```

# m.log
Magma provides a wrapper around display to manage logging verbosity.  There are four levels: 
```
DEBUG = 0
INFO = 1
WARNING = 2
ERROR = 3
```

You can use these wrappers by invoking the corresponding logging functions:
```
m.debug
m.info
m.warning
m.error
```
They the provide the same interface as `m.display`.  They will prepend an uppercase
string of the form `[<LEVEL_NAME>] ` to the display statement, e.g. `[INFO]
<display str>.`

To control verbosity in the downstream tool, simply set the preprocessor
variable `MAGMA_LOG_LEVEL` to the desired value.  Magma will only display log
messages when the configured log level is less than or equal to the
corresponding logging function's level.  So, to only show warnings and errors,
set the level to 2, to show all messages, set the level to 0.  To show no
messages, set the level to 4.  The default level is 1.

Here's a full example using verilator and pytest
```python
import magma as m
import magma.testing
import shutil
import os
import fault

def test_log(capsys):
    FF = m.define_from_verilog("""
module FF(input I, output reg O, input CLK, input CE);
always @(posedge CLK) begin
  if (CE) O <= I;
end
endmodule
    """, type_map={"CLK": m.In(m.Clock), "CE": m.In(m.Enable)})[0]

    class TestLog(m.Circuit):
        io = m.IO(I=m.In(m.Bit), O=m.Out(m.Bit)) + m.ClockIO(has_enable=True)
        ff = FF()
        io.O @= ff(io.I)
        m.log.debug("ff.O=%d, ff.I=%d", ff.O, ff.I).when(m.posedge(io.CLK))\
                                                   .if_(io.CE)
        m.log.info("ff.O=%d, ff.I=%d", ff.O, ff.I).when(m.posedge(io.CLK))\
                                                  .if_(io.CE)
        m.log.warning("ff.O=%d, ff.I=%d", ff.O, ff.I).when(m.posedge(io.CLK))\
                                                     .if_(io.CE)
        m.log.error("ff.O=%d, ff.I=%d", ff.O, ff.I).when(m.posedge(io.CLK))\
                                                   .if_(io.CE)

    m.compile("build/TestLog", TestLog)
    assert not os.system('cd tests/test_verilog/build && '
                         'verilator --lint-only TestLog.v')
    assert m.testing.check_files_equal(__file__,
                                       f"build/TestLog.v",
                                       f"gold/TestLog.v")

    tester = fault.SynchronousTester(TestLog, TestLog.CLK)
    tester.poke(TestLog.CE, 1)
    tester.poke(TestLog.I, 1)
    tester.expect(TestLog.O, 0)
    tester.advance_cycle()
    tester.poke(TestLog.I, 0)
    tester.expect(TestLog.O, 1)
    tester.advance_cycle()
    tester.expect(TestLog.O, 0)
    tester.poke(TestLog.CE, 0)
    tester.poke(TestLog.I, 1)
    tester.advance_cycle()
    tester.expect(TestLog.O, 0)
    tester.poke(TestLog.I, 1)
    tester.advance_cycle()
    tester.expect(TestLog.O, 0)
    tester.poke(TestLog.CE, 1)
    tester.advance_cycle()
    tester.expect(TestLog.O, 1)
    tester.advance_cycle()

    directory = f"{os.path.abspath(os.path.dirname(__file__))}/build/"
    tester.compile_and_run(target="verilator", directory=directory,
                           flags=['-Wno-unused'], skip_compile=True,
                           disp_type="realtime")
    out, err = capsys.readouterr()
    # No debug
    assert f"""
[INFO] ff.O=0, ff.I=1
[WARNING] ff.O=0, ff.I=1
[ERROR] ff.O=0, ff.I=1
[INFO] ff.O=1, ff.I=0
[WARNING] ff.O=1, ff.I=0
[ERROR] ff.O=1, ff.I=0
[INFO] ff.O=0, ff.I=1
[WARNING] ff.O=0, ff.I=1
[ERROR] ff.O=0, ff.I=1
[INFO] ff.O=1, ff.I=1
[WARNING] ff.O=1, ff.I=1
[ERROR] ff.O=1, ff.I=1
""" in out, out

    # Force recompile for new define
    shutil.rmtree(os.path.join(directory, "obj_dir"))
    tester.compile_and_run(target="verilator", directory=directory,
                           flags=['-Wno-unused', '+define+MAGMA_LOG_LEVEL=2'], skip_compile=True,
                           disp_type="realtime")
    out, err = capsys.readouterr()
    # No Info
    assert f"""
[WARNING] ff.O=0, ff.I=1
[ERROR] ff.O=0, ff.I=1
[WARNING] ff.O=1, ff.I=0
[ERROR] ff.O=1, ff.I=0
[WARNING] ff.O=0, ff.I=1
[ERROR] ff.O=0, ff.I=1
[WARNING] ff.O=1, ff.I=1
[ERROR] ff.O=1, ff.I=1
""" in out, out

    # Force recompile for new define
    shutil.rmtree(os.path.join(directory, "obj_dir"))
    tester.compile_and_run(target="verilator", directory=directory,
                           flags=['-Wno-unused', '+define+MAGMA_LOG_LEVEL=3'], skip_compile=True,
                           disp_type="realtime")
    out, err = capsys.readouterr()
    # Only Error
    assert f"""
[ERROR] ff.O=0, ff.I=1
[ERROR] ff.O=1, ff.I=0
[ERROR] ff.O=0, ff.I=1
[ERROR] ff.O=1, ff.I=1
""" in out, out

    # Force recompile for new define
    shutil.rmtree(os.path.join(directory, "obj_dir"))
    tester.compile_and_run(target="verilator", directory=directory,
                           flags=['-Wno-unused', '+define+MAGMA_LOG_LEVEL=0'], skip_compile=True,
                           disp_type="realtime")
    out, err = capsys.readouterr()
    # All
    assert f"""
[DEBUG] ff.O=0, ff.I=1
[INFO] ff.O=0, ff.I=1
[WARNING] ff.O=0, ff.I=1
[ERROR] ff.O=0, ff.I=1
[DEBUG] ff.O=1, ff.I=0
[INFO] ff.O=1, ff.I=0
[WARNING] ff.O=1, ff.I=0
[ERROR] ff.O=1, ff.I=0
[DEBUG] ff.O=0, ff.I=1
[INFO] ff.O=0, ff.I=1
[WARNING] ff.O=0, ff.I=1
[ERROR] ff.O=0, ff.I=1
[DEBUG] ff.O=1, ff.I=1
[INFO] ff.O=1, ff.I=1
[WARNING] ff.O=1, ff.I=1
[ERROR] ff.O=1, ff.I=1
""" in out, out
```
