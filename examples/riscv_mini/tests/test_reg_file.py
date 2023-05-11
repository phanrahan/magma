import fault

from riscv_mini.reg_file import RegFile


def test_reg_file_basic():
    DATAWIDTH = 16
    RegFile16 = RegFile(DATAWIDTH)
    t = fault.Tester(RegFile16, RegFile16.CLK)
    for i in range(0, 32):
        t.circuit.waddr = i
        t.circuit.wen = 1
        t.circuit.wdata = i
        t.step(2)
    t.circuit.wen = 0

    for i in range(0, 32):
        t.circuit.raddr1 = i
        t.circuit.raddr2 = i
        t.eval()
        t.circuit.rdata1.expect(i)
        t.circuit.rdata2.expect(i)

    # Test 0 reg
    t.circuit.waddr = 0
    t.circuit.wdata = 2
    t.circuit.wen = 1
    t.step(2)
    t.circuit.wen = 0

    t.circuit.raddr1 = 0
    t.circuit.raddr2 = 0
    t.eval()
    t.circuit.rdata1.expect(0)
    t.circuit.rdata2.expect(0)
    t.compile_and_run(target="verilator", flags=["-Wno-unused",
                                                 "-Wno-undriven"],
                      magma_opts={"flatten_all_tuples": True,
                                  "disallow_local_variables": True,
                                  "check_circt_opt_version": False},
                      magma_output="mlir-verilog")
