module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @Memory(%RADDR: i5, %CLK: i1, %WADDR: i5, %WDATA: i8, %WE: i1) -> (RDATA: i8) {
        %1 = sv.reg name "coreir_mem32x8_inst0" : !hw.inout<!hw.array<32xi8>>
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
        %3 = sv.wire sym @test_when_memory_Bits8._WHEN_ASSERT_3 name "_WHEN_ASSERT_3" : !hw.inout<i5>
        sv.assign %3, %1 : i5
        %2 = sv.read_inout %3 : !hw.inout<i5>
        %6 = sv.wire sym @test_when_memory_Bits8._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i5>
        sv.assign %6, %4 : i5
        %5 = sv.read_inout %6 : !hw.inout<i5>
        %9 = sv.wire sym @test_when_memory_Bits8._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i8>
        sv.assign %9, %7 : i8
        %8 = sv.read_inout %9 : !hw.inout<i8>
        %12 = sv.wire sym @test_when_memory_Bits8._WHEN_ASSERT_2 name "_WHEN_ASSERT_2" : !hw.inout<i1>
        sv.assign %12, %10 : i1
        %11 = sv.read_inout %12 : !hw.inout<i1>
        %13 = hw.instance "Memory_inst0" @Memory(RADDR: %2: i5, CLK: %CLK: i1, WADDR: %5: i5, WDATA: %8: i8, WE: %11: i1) -> (RDATA: i8)
        %14 = hw.constant 255 : i8
        %15 = hw.constant 0 : i5
        %16 = hw.constant 0 : i8
        %17 = hw.constant 0 : i1
        %18 = hw.constant 0 : i5
        %20 = sv.reg : !hw.inout<i5>
        %4 = sv.read_inout %20 : !hw.inout<i5>
        %21 = sv.reg : !hw.inout<i8>
        %7 = sv.read_inout %21 : !hw.inout<i8>
        %22 = sv.reg : !hw.inout<i1>
        %10 = sv.read_inout %22 : !hw.inout<i1>
        %23 = sv.reg : !hw.inout<i5>
        %1 = sv.read_inout %23 : !hw.inout<i5>
        %24 = sv.reg : !hw.inout<i8>
        %19 = sv.read_inout %24 : !hw.inout<i8>
        sv.alwayscomb {
            sv.bpassign %20, %15 : i5
            sv.bpassign %21, %16 : i8
            sv.bpassign %22, %17 : i1
            sv.bpassign %23, %18 : i5
            sv.if %en0 {
                sv.bpassign %20, %addr0 : i5
                sv.bpassign %21, %data0 : i8
                sv.bpassign %22, %0 : i1
                sv.bpassign %23, %addr1 : i5
                sv.bpassign %24, %13 : i8
            } else {
                sv.if %en1 {
                    sv.bpassign %20, %addr1 : i5
                    sv.bpassign %21, %data1 : i8
                    sv.bpassign %22, %0 : i1
                    sv.bpassign %23, %addr0 : i5
                    sv.bpassign %24, %13 : i8
                } else {
                    sv.bpassign %24, %14 : i8
                }
            }
        }
        %26 = sv.wire sym @test_when_memory_Bits8._WHEN_ASSERT_4 name "_WHEN_ASSERT_4" : !hw.inout<i8>
        sv.assign %26, %19 : i8
        %25 = sv.read_inout %26 : !hw.inout<i8>
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%en0, %5, %addr0) : i1, i5, i5
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%en0, %8, %data0) : i1, i8, i8
        %27 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%en0, %11, %27) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%en0, %2, %addr1) : i1, i5, i5
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%en0, %25, %13) : i1, i8, i8
        %29 = hw.constant -1 : i1
        %28 = comb.xor %29, %en0 : i1
        %30 = comb.and %28, %en1 : i1
        sv.verbatim "WHEN_ASSERT_5: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%30, %5, %addr1) : i1, i5, i5
        sv.verbatim "WHEN_ASSERT_6: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%30, %8, %data1) : i1, i8, i8
        %31 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_7: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%30, %11, %31) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_8: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%30, %2, %addr0) : i1, i5, i5
        sv.verbatim "WHEN_ASSERT_9: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%30, %25, %13) : i1, i8, i8
        %32 = comb.xor %29, %en1 : i1
        %33 = comb.and %28, %32 : i1
        %34 = hw.constant 255 : i8
        sv.verbatim "WHEN_ASSERT_10: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%33, %25, %34) : i1, i8, i8
        %35 = comb.or %en0, %30 : i1
        %36 = comb.xor %29, %35 : i1
        %37 = hw.constant 0 : i5
        sv.verbatim "WHEN_ASSERT_11: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%36, %5, %37) : i1, i5, i5
        %38 = comb.or %en0, %30 : i1
        %39 = comb.xor %29, %38 : i1
        %40 = hw.constant 0 : i8
        sv.verbatim "WHEN_ASSERT_12: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%39, %8, %40) : i1, i8, i8
        %41 = comb.or %en0, %30 : i1
        %42 = comb.xor %29, %41 : i1
        %43 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_13: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%42, %11, %43) : i1, i1, i1
        %44 = comb.or %en0, %30 : i1
        %45 = comb.xor %29, %44 : i1
        %46 = hw.constant 0 : i5
        sv.verbatim "WHEN_ASSERT_14: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%45, %2, %46) : i1, i5, i5
        hw.output %25 : i8
    }
}
