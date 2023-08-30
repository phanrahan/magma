module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @multiport_memory(%raddr_0: i2, %raddr_1: i2, %waddr_0: i2, %wdata_0: i5, %we_0: i1, %waddr_1: i2, %wdata_1: i5, %we_1: i1, %clk: i1) -> (rdata_0: i5, rdata_1: i5) {
        %2 = sv.reg name "MultiportMemory_inst0" : !hw.inout<!hw.array<4xi5>>
        %3 = sv.array_index_inout %2[%raddr_0] : !hw.inout<!hw.array<4xi5>>, i2
        %4 = sv.array_index_inout %2[%raddr_1] : !hw.inout<!hw.array<4xi5>>, i2
        %0 = sv.read_inout %3 : !hw.inout<i5>
        %1 = sv.read_inout %4 : !hw.inout<i5>
        %5 = sv.array_index_inout %2[%waddr_0] : !hw.inout<!hw.array<4xi5>>, i2
        %6 = sv.array_index_inout %2[%waddr_1] : !hw.inout<!hw.array<4xi5>>, i2
        sv.alwaysff(posedge %clk) {
            sv.if %we_0 {
                sv.passign %5, %wdata_0 : i5
            }
            sv.if %we_1 {
                sv.passign %6, %wdata_1 : i5
            }
        }
        hw.output %0, %1 : i5, i5
    }
}
