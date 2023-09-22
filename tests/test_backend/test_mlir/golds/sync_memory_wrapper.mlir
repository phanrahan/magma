module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @Memory(%RADDR: i7, %CLK: i1, %WADDR: i7, %WDATA: i12, %WE: i1) -> (RDATA: i12) {
        %0 = hw.constant 1 : i1
        %2 = sv.reg name "coreir_mem128x12_inst0" : !hw.inout<!hw.array<128xi12>>
        %3 = sv.array_index_inout %2[%RADDR] : !hw.inout<!hw.array<128xi12>>, i7
        %4 = sv.read_inout %3 : !hw.inout<i12>
        %5 = sv.reg name "read_reg" : !hw.inout<i12>
        %1 = sv.read_inout %5 : !hw.inout<i12>
        %6 = sv.array_index_inout %2[%WADDR] : !hw.inout<!hw.array<128xi12>>, i7
        sv.alwaysff(posedge %CLK) {
            sv.if %WE {
                sv.passign %6, %WDATA : i12
            }
            sv.if %0 {
                sv.passign %5, %4 : i12
            }
        }
        hw.output %1 : i12
    }
    hw.module @sync_memory_wrapper(%RADDR: i7, %CLK: i1, %WADDR: i7, %WDATA: i12, %WE: i1) -> (RDATA: i12) {
        %0 = hw.instance "Memory_inst0" @Memory(RADDR: %RADDR: i7, CLK: %CLK: i1, WADDR: %WADDR: i7, WDATA: %WDATA: i12, WE: %WE: i1) -> (RDATA: i12)
        hw.output %0 : i12
    }
}
