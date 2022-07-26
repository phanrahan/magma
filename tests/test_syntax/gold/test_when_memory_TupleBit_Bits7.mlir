hw.module @Memory(%RADDR: i5, %CLK: i1, %WADDR: i5, %WDATA__0: i1, %WDATA__1: i7, %WE: i1) -> (RDATA__0: i1, RDATA__1: i7) {
    %0 = comb.extract %WDATA__1 from 0 : (i7) -> i1
    %1 = comb.extract %WDATA__1 from 1 : (i7) -> i1
    %2 = comb.extract %WDATA__1 from 2 : (i7) -> i1
    %3 = comb.extract %WDATA__1 from 3 : (i7) -> i1
    %4 = comb.extract %WDATA__1 from 4 : (i7) -> i1
    %5 = comb.extract %WDATA__1 from 5 : (i7) -> i1
    %6 = comb.extract %WDATA__1 from 6 : (i7) -> i1
    %7 = comb.concat %6, %5, %4, %3, %2, %1, %0, %WDATA__0 : i1, i1, i1, i1, i1, i1, i1, i1
    %9 = sv.reg {name = "coreir_mem32x8_inst0"} : !hw.inout<!hw.array<32xi8>>
    %10 = sv.array_index_inout %9[%RADDR] : !hw.inout<!hw.array<32xi8>>, i5
    %8 = sv.read_inout %10 : !hw.inout<i8>
    %11 = sv.array_index_inout %9[%WADDR] : !hw.inout<!hw.array<32xi8>>, i5
    sv.alwaysff(posedge %CLK) {
        sv.if %WE {
            sv.passign %11, %7 : i8
        }
    }
    %12 = comb.extract %8 from 0 : (i8) -> i1
    %13 = comb.extract %8 from 1 : (i8) -> i1
    %14 = comb.extract %8 from 2 : (i8) -> i1
    %15 = comb.extract %8 from 3 : (i8) -> i1
    %16 = comb.extract %8 from 4 : (i8) -> i1
    %17 = comb.extract %8 from 5 : (i8) -> i1
    %18 = comb.extract %8 from 6 : (i8) -> i1
    %19 = comb.extract %8 from 7 : (i8) -> i1
    %20 = comb.concat %19, %18, %17, %16, %15, %14, %13 : i1, i1, i1, i1, i1, i1, i1
    hw.output %12, %20 : i1, i7
}
hw.module @test_when_memory_TupleBit_Bits7(%data0__0: i1, %data0__1: i7, %addr0: i5, %en0: i1, %data1__0: i1, %data1__1: i7, %addr1: i5, %en1: i1, %CLK: i1) -> (out__0: i1, out__1: i7) {
    %0 = hw.constant 1 : i1
    %6, %7 = hw.instance "Memory_inst0" @Memory(RADDR: %1: i5, CLK: %CLK: i1, WADDR: %2: i5, WDATA__0: %3: i1, WDATA__1: %4: i7, WE: %5: i1) -> (RDATA__0: i1, RDATA__1: i7)
    %8 = hw.constant 127 : i7
    %11 = sv.reg {name = "WADDR_reg"} : !hw.inout<i5>
    %12 = sv.reg {name = "Memory_inst0.WDATA[0]_reg"} : !hw.inout<i1>
    %13 = sv.reg {name = "Memory_inst0.WDATA[1]_reg"} : !hw.inout<i7>
    %14 = sv.reg {name = "WE_reg"} : !hw.inout<i1>
    %15 = sv.reg {name = "RADDR_reg"} : !hw.inout<i5>
    %16 = sv.reg {name = "test_when_memory_TupleBit_Bits7.out[0]_reg"} : !hw.inout<i1>
    %17 = sv.reg {name = "test_when_memory_TupleBit_Bits7.out[1]_reg"} : !hw.inout<i7>
    sv.alwayscomb {
        %18 = hw.constant 0 : i5
        sv.bpassign %11, %18 : i5
        %19 = hw.constant 0 : i1
        sv.bpassign %12, %19 : i1
        %20 = hw.constant 0 : i7
        sv.bpassign %13, %20 : i7
        %21 = hw.constant 0 : i1
        sv.bpassign %14, %21 : i1
        sv.bpassign %15, %18 : i5
        sv.if %en0 {
            sv.bpassign %11, %addr0 : i5
            sv.bpassign %12, %data0__0 : i1
            sv.bpassign %13, %data0__1 : i7
            sv.bpassign %14, %0 : i1
            sv.bpassign %15, %addr1 : i5
            sv.bpassign %16, %6 : i1
            sv.bpassign %17, %7 : i7
        } else {
            sv.if %en1 {
                sv.bpassign %11, %addr1 : i5
                sv.bpassign %12, %data1__0 : i1
                sv.bpassign %13, %data1__1 : i7
                sv.bpassign %14, %0 : i1
                sv.bpassign %15, %addr0 : i5
                sv.bpassign %16, %6 : i1
                sv.bpassign %17, %7 : i7
            } else {
                sv.bpassign %16, %0 : i1
                sv.bpassign %17, %8 : i7
            }
        }
    }
    %2 = sv.read_inout %11 : !hw.inout<i5>
    %3 = sv.read_inout %12 : !hw.inout<i1>
    %4 = sv.read_inout %13 : !hw.inout<i7>
    %5 = sv.read_inout %14 : !hw.inout<i1>
    %1 = sv.read_inout %15 : !hw.inout<i5>
    %9 = sv.read_inout %16 : !hw.inout<i1>
    %10 = sv.read_inout %17 : !hw.inout<i7>
    hw.output %9, %10 : i1, i7
}
