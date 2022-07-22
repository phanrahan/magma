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
hw.module @test_when_memory(%data0: i8, %addr0: i5, %en0: i1, %data1: i8, %addr1: i5, %en1: i1, %CLK: i1) -> (out: i8) {
    %0 = hw.constant 1 : i1
    %5 = hw.instance "Memory_inst0" @Memory(RADDR: %1: i5, CLK: %CLK: i1, WADDR: %2: i5, WDATA: %3: i8, WE: %4: i1) -> (RDATA: i8)
    %6 = hw.constant 1 : i1
    %7 = hw.constant 255 : i8
    %9 = sv.reg {name = "O_0_0_reg"} : !hw.inout<i5>
    %10 = sv.reg {name = "O_1_0_reg"} : !hw.inout<i8>
    %11 = sv.reg {name = "O_2_0_reg"} : !hw.inout<i1>
    %12 = sv.reg {name = "O_3_0_reg"} : !hw.inout<i5>
    %13 = sv.reg {name = "O_4_0_reg"} : !hw.inout<i8>
    sv.alwayscomb {
        %14 = hw.constant 0 : i5
        sv.bpassign %9, %14 : i5
        %15 = hw.constant 0 : i8
        sv.bpassign %10, %15 : i8
        %16 = hw.constant 0 : i1
        sv.bpassign %11, %16 : i1
        sv.bpassign %12, %14 : i5
        sv.if %en0 {
            sv.bpassign %9, %addr0 : i5
            sv.bpassign %10, %data0 : i8
            sv.bpassign %11, %6 : i1
            sv.bpassign %12, %addr1 : i5
            sv.bpassign %13, %5 : i8
        } else {
            sv.if %en1 {
                sv.bpassign %9, %addr1 : i5
                sv.bpassign %10, %data1 : i8
                sv.bpassign %11, %6 : i1
                sv.bpassign %12, %addr0 : i5
                sv.bpassign %13, %5 : i8
            } else {
                sv.bpassign %13, %7 : i8
            }
        }
    }
    %2 = sv.read_inout %9 : !hw.inout<i5>
    %3 = sv.read_inout %10 : !hw.inout<i8>
    %4 = sv.read_inout %11 : !hw.inout<i1>
    %1 = sv.read_inout %12 : !hw.inout<i5>
    %8 = sv.read_inout %13 : !hw.inout<i8>
    hw.output %8 : i8
}
