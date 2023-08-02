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
        %9 = sv.reg name "coreir_mem32x8_inst0" : !hw.inout<!hw.array<32xi8>>
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
        %3 = sv.wire sym @test_when_memory_Tuplex_Bit_y_Bits7._WHEN_ASSERT_4 name "_WHEN_ASSERT_4" : !hw.inout<i5>
        sv.assign %3, %1 : i5
        %2 = sv.read_inout %3 : !hw.inout<i5>
        %6 = sv.wire sym @test_when_memory_Tuplex_Bit_y_Bits7._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i5>
        sv.assign %6, %4 : i5
        %5 = sv.read_inout %6 : !hw.inout<i5>
        %9 = sv.wire sym @test_when_memory_Tuplex_Bit_y_Bits7._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i1>
        sv.assign %9, %7 : i1
        %8 = sv.read_inout %9 : !hw.inout<i1>
        %12 = sv.wire sym @test_when_memory_Tuplex_Bit_y_Bits7._WHEN_ASSERT_2 name "_WHEN_ASSERT_2" : !hw.inout<i7>
        sv.assign %12, %10 : i7
        %11 = sv.read_inout %12 : !hw.inout<i7>
        %15 = sv.wire sym @test_when_memory_Tuplex_Bit_y_Bits7._WHEN_ASSERT_3 name "_WHEN_ASSERT_3" : !hw.inout<i1>
        sv.assign %15, %13 : i1
        %14 = sv.read_inout %15 : !hw.inout<i1>
        %16, %17 = hw.instance "Memory_inst0" @Memory(RADDR: %2: i5, CLK: %CLK: i1, WADDR: %5: i5, WDATA_x: %8: i1, WDATA_y: %11: i7, WE: %14: i1) -> (RDATA_x: i1, RDATA_y: i7)
        %18 = hw.constant 127 : i7
        %19 = hw.constant 0 : i5
        %20 = hw.constant 0 : i1
        %21 = hw.constant 0 : i7
        %22 = hw.constant 0 : i1
        %23 = hw.constant 0 : i5
        %24 = hw.constant 0 : i7
        %27 = sv.reg : !hw.inout<i5>
        %4 = sv.read_inout %27 : !hw.inout<i5>
        %28 = sv.reg : !hw.inout<i1>
        %7 = sv.read_inout %28 : !hw.inout<i1>
        %29 = sv.reg : !hw.inout<i7>
        %10 = sv.read_inout %29 : !hw.inout<i7>
        %30 = sv.reg : !hw.inout<i1>
        %13 = sv.read_inout %30 : !hw.inout<i1>
        %31 = sv.reg : !hw.inout<i5>
        %1 = sv.read_inout %31 : !hw.inout<i5>
        %32 = sv.reg : !hw.inout<i1>
        %25 = sv.read_inout %32 : !hw.inout<i1>
        %33 = sv.reg : !hw.inout<i7>
        %26 = sv.read_inout %33 : !hw.inout<i7>
        sv.alwayscomb {
            sv.bpassign %27, %19 : i5
            sv.bpassign %30, %22 : i1
            sv.bpassign %31, %23 : i5
            sv.bpassign %28, %22 : i1
            sv.bpassign %29, %24 : i7
            sv.if %en0 {
                sv.bpassign %27, %addr0 : i5
                sv.bpassign %30, %0 : i1
                sv.bpassign %31, %addr1 : i5
                sv.bpassign %32, %16 : i1
                sv.bpassign %33, %17 : i7
                sv.bpassign %28, %data0_x : i1
                sv.bpassign %29, %data0_y : i7
            } else {
                sv.if %en1 {
                    sv.bpassign %27, %addr1 : i5
                    sv.bpassign %30, %0 : i1
                    sv.bpassign %31, %addr0 : i5
                    sv.bpassign %32, %16 : i1
                    sv.bpassign %33, %17 : i7
                    sv.bpassign %28, %data1_x : i1
                    sv.bpassign %29, %data1_y : i7
                } else {
                    sv.bpassign %32, %0 : i1
                    sv.bpassign %33, %18 : i7
                }
            }
        }
        %35 = sv.wire sym @test_when_memory_Tuplex_Bit_y_Bits7._WHEN_ASSERT_5 name "_WHEN_ASSERT_5" : !hw.inout<i1>
        sv.assign %35, %25 : i1
        %34 = sv.read_inout %35 : !hw.inout<i1>
        %37 = sv.wire sym @test_when_memory_Tuplex_Bit_y_Bits7._WHEN_ASSERT_6 name "_WHEN_ASSERT_6" : !hw.inout<i7>
        sv.assign %37, %26 : i7
        %36 = sv.read_inout %37 : !hw.inout<i7>
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%en0, %5, %addr0) : i1, i5, i5
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%en0, %8, %data0_x) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%en0, %11, %data0_y) : i1, i7, i7
        %38 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%en0, %14, %38) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%en0, %2, %addr1) : i1, i5, i5
        sv.verbatim "WHEN_ASSERT_5: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%en0, %34, %16) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_6: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%en0, %36, %17) : i1, i7, i7
        %40 = hw.constant -1 : i1
        %39 = comb.xor %40, %en0 : i1
        %41 = comb.and %39, %en1 : i1
        sv.verbatim "WHEN_ASSERT_7: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%41, %5, %addr1) : i1, i5, i5
        %42 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_8: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%41, %14, %42) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_9: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%41, %2, %addr0) : i1, i5, i5
        sv.verbatim "WHEN_ASSERT_10: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%41, %34, %16) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_11: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%41, %36, %17) : i1, i7, i7
        sv.verbatim "WHEN_ASSERT_12: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%41, %8, %data1_x) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_13: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%41, %11, %data1_y) : i1, i7, i7
        %43 = comb.xor %40, %en1 : i1
        %44 = comb.and %39, %43 : i1
        %45 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_14: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%44, %34, %45) : i1, i1, i1
        %46 = hw.constant 127 : i7
        sv.verbatim "WHEN_ASSERT_15: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%44, %36, %46) : i1, i7, i7
        %47 = comb.or %en0, %41 : i1
        %48 = comb.xor %40, %47 : i1
        %49 = hw.constant 0 : i5
        sv.verbatim "WHEN_ASSERT_16: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%48, %5, %49) : i1, i5, i5
        %50 = comb.or %en0, %41 : i1
        %51 = comb.xor %40, %50 : i1
        %52 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_17: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%51, %14, %52) : i1, i1, i1
        %53 = comb.or %en0, %41 : i1
        %54 = comb.xor %40, %53 : i1
        %55 = hw.constant 0 : i5
        sv.verbatim "WHEN_ASSERT_18: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%54, %2, %55) : i1, i5, i5
        %56 = comb.or %en0, %41 : i1
        %57 = comb.xor %40, %56 : i1
        %58 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_19: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%57, %8, %58) : i1, i1, i1
        %59 = comb.or %en0, %41 : i1
        %60 = comb.xor %40, %59 : i1
        %61 = hw.constant 0 : i7
        sv.verbatim "WHEN_ASSERT_20: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%60, %11, %61) : i1, i7, i7
        hw.output %34, %36 : i1, i7
    }
}
