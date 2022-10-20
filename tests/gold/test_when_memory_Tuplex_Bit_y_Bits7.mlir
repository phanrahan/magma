module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @Memory(%RADDR: i5, %CLK: i1, %WADDR: i5, %WDATA_x: i1, %WDATA_y: i7, %WE: i1) -> (RDATA_x: i1, RDATA_y: i7) {
        %0 = comb.extract %WDATA_y from 0 : (i7) -> i1
        %1 = comb.extract %WDATA_y from 1 : (i7) -> i1
        %2 = comb.extract %WDATA_y from 2 : (i7) -> i1
        %3 = comb.extract %WDATA_y from 3 : (i7) -> i1
        %4 = comb.extract %WDATA_y from 4 : (i7) -> i1
        %5 = comb.extract %WDATA_y from 5 : (i7) -> i1
        %6 = comb.extract %WDATA_y from 6 : (i7) -> i1
        %7 = comb.concat %6, %5, %4, %3, %2, %1, %0, %WDATA_x : i1, i1, i1, i1, i1, i1, i1, i1
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
    hw.module @test_when_memory_Tuplex_Bit_y_Bits7(%data0_x: i1, %data0_y: i7, %addr0: i5, %en0: i1, %data1_x: i1, %data1_y: i7, %addr1: i5, %en1: i1, %CLK: i1) -> (out_x: i1, out_y: i7) {
        %0 = hw.constant 1 : i1
        %6, %7 = hw.instance "Memory_inst0" @Memory(RADDR: %1: i5, CLK: %CLK: i1, WADDR: %2: i5, WDATA_x: %3: i1, WDATA_y: %4: i7, WE: %5: i1) -> (RDATA_x: i1, RDATA_y: i7)
        %8 = hw.constant 127 : i7
        %9 = hw.constant 0 : i5
        %10 = hw.constant 0 : i1
        %11 = hw.constant 0 : i7
        %12 = hw.constant 0 : i1
        %13 = hw.constant 0 : i5
        %14 = hw.constant 0 : i7
        %21 = sv.reg : !hw.inout<i5>
        %2 = sv.read_inout %21 : !hw.inout<i5>
        %22 = sv.reg : !hw.inout<i1>
        %15 = sv.read_inout %22 : !hw.inout<i1>
        %23 = sv.reg : !hw.inout<i7>
        %16 = sv.read_inout %23 : !hw.inout<i7>
        %24 = sv.reg : !hw.inout<i1>
        %5 = sv.read_inout %24 : !hw.inout<i1>
        %25 = sv.reg : !hw.inout<i5>
        %1 = sv.read_inout %25 : !hw.inout<i5>
        %26 = sv.reg : !hw.inout<i1>
        %17 = sv.read_inout %26 : !hw.inout<i1>
        %27 = sv.reg : !hw.inout<i7>
        %18 = sv.read_inout %27 : !hw.inout<i7>
        %28 = sv.reg : !hw.inout<i1>
        %19 = sv.read_inout %28 : !hw.inout<i1>
        %29 = sv.reg : !hw.inout<i7>
        %20 = sv.read_inout %29 : !hw.inout<i7>
        %30 = sv.reg : !hw.inout<i1>
        %3 = sv.read_inout %30 : !hw.inout<i1>
        %31 = sv.reg : !hw.inout<i7>
        %4 = sv.read_inout %31 : !hw.inout<i7>
        sv.alwayscomb {
            sv.bpassign %21, %9 : i5
            sv.bpassign %30, %12 : i1
            sv.bpassign %31, %11 : i7
            sv.bpassign %24, %12 : i1
            sv.bpassign %25, %13 : i5
            sv.bpassign %30, %12 : i1
            sv.bpassign %31, %14 : i7
            sv.if %en0 {
                sv.bpassign %21, %addr0 : i5
                sv.bpassign %24, %0 : i1
                sv.bpassign %25, %addr1 : i5
                sv.bpassign %28, %6 : i1
                sv.bpassign %29, %7 : i7
                sv.bpassign %30, %data0_x : i1
                sv.bpassign %31, %data0_y : i7
            } else {
                sv.if %en1 {
                    sv.bpassign %21, %addr1 : i5
                    sv.bpassign %24, %0 : i1
                    sv.bpassign %25, %addr0 : i5
                    sv.bpassign %28, %6 : i1
                    sv.bpassign %29, %7 : i7
                    sv.bpassign %30, %data1_x : i1
                    sv.bpassign %31, %data1_y : i7
                } else {
                    sv.bpassign %28, %0 : i1
                    sv.bpassign %29, %8 : i7
                }
            }
        }
        hw.output %19, %20 : i1, i7
    }
}
