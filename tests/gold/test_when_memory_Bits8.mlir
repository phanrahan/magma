module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
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
        %7 = hw.constant 0 : i5
        %8 = hw.constant 0 : i8
        %9 = hw.constant 0 : i1
        %10 = hw.constant 0 : i5
        %12 = sv.reg : !hw.inout<i5>
        %2 = sv.read_inout %12 : !hw.inout<i5>
        %13 = sv.reg : !hw.inout<i8>
        %3 = sv.read_inout %13 : !hw.inout<i8>
        %14 = sv.reg : !hw.inout<i1>
        %4 = sv.read_inout %14 : !hw.inout<i1>
        %15 = sv.reg : !hw.inout<i5>
        %1 = sv.read_inout %15 : !hw.inout<i5>
        %16 = sv.reg : !hw.inout<i8>
        %11 = sv.read_inout %16 : !hw.inout<i8>
        sv.alwayscomb {
            sv.bpassign %12, %7 : i5
            sv.bpassign %13, %8 : i8
            sv.bpassign %14, %9 : i1
            sv.bpassign %15, %10 : i5
            sv.if %en0 {
                sv.bpassign %12, %addr0 : i5
                sv.bpassign %13, %data0 : i8
                sv.bpassign %14, %0 : i1
                sv.bpassign %15, %addr1 : i5
                sv.bpassign %16, %5 : i8
            } else {
                sv.if %en1 {
                    sv.bpassign %12, %addr1 : i5
                    sv.bpassign %13, %data1 : i8
                    sv.bpassign %14, %0 : i1
                    sv.bpassign %15, %addr0 : i5
                    sv.bpassign %16, %5 : i8
                } else {
                    sv.bpassign %16, %6 : i8
                }
            }
        }
        hw.output %11 : i8
    }
}
