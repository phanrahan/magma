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
    %4 = sv.reg {name = "WADDR_reg"} : !hw.inout<i2>
    %5 = sv.reg {name = "WDATA_reg"} : !hw.inout<i5>
    %6 = sv.reg {name = "WE_reg"} : !hw.inout<i1>
    sv.alwayscomb {
        %7 = hw.constant 0 : i2
        sv.bpassign %4, %7 : i2
        %8 = hw.constant 0 : i5
        sv.bpassign %5, %8 : i5
        %9 = hw.constant 0 : i1
        sv.bpassign %6, %9 : i1
        sv.if %wen {
            sv.bpassign %4, %waddr : i2
        }
        sv.if %wen {
            sv.bpassign %5, %wdata : i5
        }
        sv.if %wen {
            sv.bpassign %6, %0 : i1
        }
    }
    %1 = sv.read_inout %4 : !hw.inout<i2>
    %2 = sv.read_inout %5 : !hw.inout<i5>
    %3 = sv.read_inout %6 : !hw.inout<i1>
    %10 = hw.instance "Memory_inst0" @Memory(RADDR: %raddr: i2, CLK: %clk: i1, WADDR: %1: i2, WDATA: %2: i5, WE: %3: i1) -> (RDATA: i5)
    hw.output %10 : i5
}
