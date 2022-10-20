module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @Memory(%RADDR: i7, %CLK: i1, %WADDR: i7, %WDATA: i12, %WE: i1) -> (RDATA: i12) {
        %1 = sv.reg {name = "coreir_mem128x12_inst0"} : !hw.inout<!hw.array<128xi12>>
        %2 = sv.array_index_inout %1[%RADDR] : !hw.inout<!hw.array<128xi12>>, i7
        %0 = sv.read_inout %2 : !hw.inout<i12>
        %3 = sv.array_index_inout %1[%WADDR] : !hw.inout<!hw.array<128xi12>>, i7
        sv.alwaysff(posedge %CLK) {
            sv.if %WE {
                sv.passign %3, %WDATA : i12
            }
        }
        hw.output %0 : i12
    }
    hw.module @simple_memory_wrapper(%RADDR: i7, %CLK: i1, %WADDR: i7, %WDATA: i12, %WE: i1) -> (RDATA: i12) {
        %0 = hw.instance "Memory_inst0" @Memory(RADDR: %RADDR: i7, CLK: %CLK: i1, WADDR: %WADDR: i7, WDATA: %WDATA: i12, WE: %WE: i1) -> (RDATA: i12)
        hw.output %0 : i12
    }
}
