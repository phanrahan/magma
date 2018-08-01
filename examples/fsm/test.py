import magma as m
import fault
import shutil
from top import MagmaFSM as top_magma

top_verilog = m.DefineFromVerilogFile("top.v")[0]
print(top_verilog)

tester = fault.Tester(top_verilog, top_verilog.clk)

# Reset
tester.poke(top_verilog.rst, 0)
tester.eval()
tester.poke(top_verilog.rst, 1)
tester.eval()
tester.poke(top_verilog.rst, 0)

tester.poke(top_verilog.clk, 0)
tester.poke(top_verilog.frameValid, 0)
tester.poke(top_verilog.real_href, 0)
tester.eval()

# Should be zero in the begininning
tester.expect(top_verilog.pixel_valid, 0)

# Get into HBLANK state
tester.poke(top_verilog.frameValid, 1)
tester.step(2)

# Should still be zero until we assert real_href
tester.expect(top_verilog.pixel_valid, 0)
# frameValid doesn't matter at this point
tester.poke(top_verilog.frameValid, 0)

# Get into HACT state
tester.poke(top_verilog.real_href, 1)
tester.step(2)

# should be valid now we're in HACT
tester.expect(top_verilog.pixel_valid, 1)

PIX_PER_LINE = 120  # Defined in verilog file
# Should be valid for the length of a line (minus 1 for the first one we
# already checked)
for i in range(PIX_PER_LINE - 1):
    tester.step(2)
    tester.expect(top_verilog.pixel_valid, 1)

# should no longer be valid
tester.step(2)
tester.expect(top_verilog.pixel_valid, 0)

# Copy top.v into build directory so verilator can find it
shutil.copy("top.v", "build/VerilogFSM.v")
tester.compile_and_run()

tester.circuit = top_magma
tester.compile_and_run()
