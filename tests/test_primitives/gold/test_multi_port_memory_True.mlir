module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_multi_port_memory(%raddr_0: i2, %raddr_1: i2, %waddr_0: i2, %wdata_0: i5, %we_0: i1, %waddr_1: i2, %wdata_1: i5, %we_1: i1, %clk: i1, %re_0: i1, %re_1: i1) -> (rdata_0: i5, rdata_1: i5) {
        %2 = sv.reg {name = "MultiPortMemory_inst0"} : !hw.inout<!hw.array<4xi5>>
        %3 = sv.array_index_inout %2[%raddr_0] : !hw.inout<!hw.array<4xi5>>, i2
        %4 = sv.reg {name = "read_reg_0"} : !hw.inout<i5>
        %0 = sv.read_inout %4 : !hw.inout<i5>
        %5 = sv.read_inout %3 : !hw.inout<i5>
        %6 = sv.array_index_inout %2[%raddr_1] : !hw.inout<!hw.array<4xi5>>, i2
        %7 = sv.reg {name = "read_reg_1"} : !hw.inout<i5>
        %1 = sv.read_inout %7 : !hw.inout<i5>
        %8 = sv.read_inout %6 : !hw.inout<i5>
        %9 = sv.array_index_inout %2[%waddr_0] : !hw.inout<!hw.array<4xi5>>, i2
        %10 = sv.array_index_inout %2[%waddr_1] : !hw.inout<!hw.array<4xi5>>, i2
        sv.alwaysff(posedge %clk) {
            sv.if %we_0 {
                sv.passign %9, %wdata_0 : i5
            }
            sv.if %we_1 {
                sv.passign %10, %wdata_1 : i5
            }
            sv.if %re_0 {
                sv.passign %4, %5 : i5
            }
            sv.if %re_1 {
                sv.passign %7, %8 : i5
            }
        }
        hw.output %0, %1 : i5, i5
    }
}
