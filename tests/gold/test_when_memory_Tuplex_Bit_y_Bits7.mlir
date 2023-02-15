module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @Memory(%RADDR: i5, %CLK: i1, %WADDR: i5, %WDATA_x: i1, %WDATA_y: i7, %WE: i1) -> (RDATA_x: i1, RDATA_y: i7) {
        %0 = comb.extract %WDATA_y from 0 : (i7) -> i1
        %1 = comb.extract %WDATA_y from 1 : (i7) -> i1
        %2 = comb.extract %WDATA_y from 2 : (i7) -> i1
        %3 = comb.extract %WDATA_y from 3 : (i7) -> i1
        %4 = comb.extract %WDATA_y from 4 : (i7) -> i1
        %5 = comb.extract %WDATA_y from 5 : (i7) -> i1
        %6 = comb.extract %WDATA_y from 6 : (i7) -> i1
        %7 = comb.concat %WDATA_x, %0, %1, %2, %3, %4, %5, %6 : i1, i1, i1, i1, i1, i1, i1, i1
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
        %20 = comb.concat %13, %14, %15, %16, %17, %18, %19 : i1, i1, i1, i1, i1, i1, i1
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
        %18 = sv.reg : !hw.inout<i5>
        %2 = sv.read_inout %18 : !hw.inout<i5>
        %19 = sv.reg : !hw.inout<i1>
        %3 = sv.read_inout %19 : !hw.inout<i1>
        %20 = sv.reg : !hw.inout<i7>
        %4 = sv.read_inout %20 : !hw.inout<i7>
        %21 = sv.reg : !hw.inout<i1>
        %5 = sv.read_inout %21 : !hw.inout<i1>
        %22 = sv.reg : !hw.inout<i5>
        %1 = sv.read_inout %22 : !hw.inout<i5>
        %23 = sv.reg : !hw.inout<i1>
        %14 = sv.read_inout %23 : !hw.inout<i1>
        %24 = sv.reg : !hw.inout<i7>
        %15 = sv.read_inout %24 : !hw.inout<i7>
        %25 = sv.reg : !hw.inout<i1>
        %16 = sv.read_inout %25 : !hw.inout<i1>
        %26 = sv.reg : !hw.inout<i7>
        %17 = sv.read_inout %26 : !hw.inout<i7>
        sv.alwayscomb {
            sv.bpassign %18, %9 : i5
            sv.bpassign %19, %12 : i1
            sv.bpassign %20, %11 : i7
            sv.bpassign %21, %12 : i1
            sv.bpassign %22, %13 : i5
            sv.if %en0 {
                sv.bpassign %18, %addr0 : i5
                sv.bpassign %19, %data0_x : i1
                sv.bpassign %20, %data0_y : i7
                sv.bpassign %21, %0 : i1
                sv.bpassign %22, %addr1 : i5
                sv.bpassign %25, %6 : i1
                sv.bpassign %26, %7 : i7
            } else {
                sv.if %en1 {
                    sv.bpassign %18, %addr1 : i5
                    sv.bpassign %19, %data1_x : i1
                    sv.bpassign %20, %data1_y : i7
                    sv.bpassign %21, %0 : i1
                    sv.bpassign %22, %addr0 : i5
                    sv.bpassign %25, %6 : i1
                    sv.bpassign %26, %7 : i7
                } else {
                    sv.bpassign %25, %0 : i1
                    sv.bpassign %26, %8 : i7
                }
            }
        }
        hw.output %16, %17 : i1, i7
    }
}
