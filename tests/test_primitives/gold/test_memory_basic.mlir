hw.module @Memory(%RADDR: i2, %CLK: i1, %WADDR: i2, %WDATA: i5, %WE: i1) -> (RDATA: i5) {
    %1 = sv.reg {name = "coreir_mem4x5_inst0"} : !hw.inout<!hw.array<4xi5>>
    %2 = sv.array_index_inout %1[%RADDR] : !hw.inout<!hw.array<4xi5>>, i2
    %0 = sv.read_inout %2 : !hw.inout<i5>
    %3 = sv.array_index_inout %1[%WADDR] : !hw.inout<!hw.array<4xi5>>, i2
    sv.alwaysff(posedge %CLK) {
        sv.if %WE {
            sv.passign %3, %WDATA : i5
        }
    }
    hw.output %0 : i5
}
hw.module @test_memory_basic(%raddr: i2, %waddr: i2, %wdata: i5, %clk: i1, %wen: i1) -> (rdata: i5) {
    %0 = hw.constant 1 : i1
    %1 = hw.constant 0 : i2
    %2 = hw.constant 0 : i5
    %3 = hw.constant 0 : i1
    %7 = sv.reg : !hw.inout<i2>
    %4 = sv.read_inout %7 : !hw.inout<i2>
    %8 = sv.reg : !hw.inout<i5>
    %5 = sv.read_inout %8 : !hw.inout<i5>
    %9 = sv.reg : !hw.inout<i1>
    %6 = sv.read_inout %9 : !hw.inout<i1>
    sv.alwayscomb {
        sv.bpassign %7, %1 : i2
        sv.bpassign %8, %2 : i5
        sv.bpassign %9, %3 : i1
        sv.if %wen {
            sv.bpassign %7, %waddr : i2
            sv.bpassign %8, %wdata : i5
            sv.bpassign %9, %0 : i1
        }
    }
    %10 = hw.instance "Memory_inst0" @Memory(RADDR: %raddr: i2, CLK: %clk: i1, WADDR: %4: i2, WDATA: %5: i5, WE: %6: i1) -> (RDATA: i5)
    hw.output %10 : i5
}
