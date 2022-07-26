hw.module @Memory(%RADDR: i5, %CLK: i1, %WADDR: i5, %WDATA: i8, %WE: i1) -> (RDATA: i8) {
    %1 = sv.reg {name = "coreir_mem32x8_inst0"} : !hw.inout<!hw.array<32xi8>>
    %2 = sv.array_index_inout %1[%RADDR] : !hw.inout<!hw.array<32xi8>>, i5
    %0 = sv.read_inout %2 : !hw.inout<i8>
    %3 = sv.array_index_inout %1[%WADDR] : !hw.inout<!hw.array<32xi8>>, i5
    sv.alwaysff(posedge %CLK) {
        sv.if %WE {
            sv.passign %3, %WDATA : i8
        }
    }
    hw.output %0 : i8
}
hw.module @test_when_memory_Bits8(%data0: i8, %addr0: i5, %en0: i1, %data1: i8, %addr1: i5, %en1: i1, %CLK: i1) -> (out: i8) {
    %0 = hw.constant 1 : i1
    %5 = hw.instance "Memory_inst0" @Memory(RADDR: %1: i5, CLK: %CLK: i1, WADDR: %2: i5, WDATA: %3: i8, WE: %4: i1) -> (RDATA: i8)
    %6 = hw.constant 255 : i8
    %8 = sv.reg {name = "WADDR_reg"} : !hw.inout<i5>
    %9 = sv.reg {name = "WDATA_reg"} : !hw.inout<i8>
    %10 = sv.reg {name = "WE_reg"} : !hw.inout<i1>
    %11 = sv.reg {name = "RADDR_reg"} : !hw.inout<i5>
    %12 = sv.reg {name = "out_reg"} : !hw.inout<i8>
    sv.alwayscomb {
        %13 = hw.constant 0 : i5
        sv.bpassign %8, %13 : i5
        %14 = hw.constant 0 : i8
        sv.bpassign %9, %14 : i8
        %15 = hw.constant 0 : i1
        sv.bpassign %10, %15 : i1
        sv.bpassign %11, %13 : i5
        sv.if %en0 {
            sv.bpassign %8, %addr0 : i5
            sv.bpassign %9, %data0 : i8
            sv.bpassign %10, %0 : i1
            sv.bpassign %11, %addr1 : i5
            sv.bpassign %12, %5 : i8
        } else {
            sv.if %en1 {
                sv.bpassign %8, %addr1 : i5
                sv.bpassign %9, %data1 : i8
                sv.bpassign %10, %0 : i1
                sv.bpassign %11, %addr0 : i5
                sv.bpassign %12, %5 : i8
            } else {
                sv.bpassign %12, %6 : i8
            }
        }
    }
    %2 = sv.read_inout %8 : !hw.inout<i5>
    %3 = sv.read_inout %9 : !hw.inout<i8>
    %4 = sv.read_inout %10 : !hw.inout<i1>
    %1 = sv.read_inout %11 : !hw.inout<i5>
    %7 = sv.read_inout %12 : !hw.inout<i8>
    hw.output %7 : i8
}
