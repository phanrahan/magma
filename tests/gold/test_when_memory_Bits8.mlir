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
        %5 = hw.instance "Memory_inst0" @Memory(RADDR: %1: i5, CLK: %CLK: i1, WADDR: %2: i5, WDATA: %3: i8, WE: %4: i1) -> (RDATA: i8)
        %6 = hw.constant 255 : i8
        %7 = hw.constant 0 : i5
        %8 = hw.constant 0 : i8
        %9 = hw.constant 0 : i1
        %10 = hw.constant 0 : i5
        %12 = sv.reg name "_WHEN_WIRE_0" : !hw.inout<i5>
        %2 = sv.read_inout %12 : !hw.inout<i5>
        %13 = sv.reg name "_WHEN_WIRE_1" : !hw.inout<i8>
        %3 = sv.read_inout %13 : !hw.inout<i8>
        %14 = sv.reg name "_WHEN_WIRE_2" : !hw.inout<i1>
        %4 = sv.read_inout %14 : !hw.inout<i1>
        %15 = sv.reg name "_WHEN_WIRE_3" : !hw.inout<i5>
        %1 = sv.read_inout %15 : !hw.inout<i5>
        %16 = sv.reg name "_WHEN_WIRE_4" : !hw.inout<i8>
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
        sv.verbatim "WHEN_ASSERT_13: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%en0, %2, %addr0) : i1, i5, i5
        sv.verbatim "WHEN_ASSERT_14: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%en0, %3, %data0) : i1, i8, i8
        %17 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_15: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%en0, %4, %17) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_16: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%en0, %1, %addr1) : i1, i5, i5
        sv.verbatim "WHEN_ASSERT_17: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%en0, %11, %5) : i1, i8, i8
        %19 = hw.constant -1 : i1
        %18 = comb.xor %19, %en0 : i1
        %20 = comb.and %18, %en1 : i1
        sv.verbatim "WHEN_ASSERT_18: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%20, %2, %addr1) : i1, i5, i5
        sv.verbatim "WHEN_ASSERT_19: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%20, %3, %data1) : i1, i8, i8
        %21 = hw.constant 1 : i1
        sv.verbatim "WHEN_ASSERT_20: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%20, %4, %21) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_21: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%20, %1, %addr0) : i1, i5, i5
        sv.verbatim "WHEN_ASSERT_22: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%20, %11, %5) : i1, i8, i8
        %22 = comb.xor %19, %en1 : i1
        %23 = comb.and %18, %22 : i1
        %24 = hw.constant 255 : i8
        sv.verbatim "WHEN_ASSERT_23: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%23, %11, %24) : i1, i8, i8
        %25 = comb.or %en0, %20 : i1
        %26 = comb.xor %19, %25 : i1
        %27 = hw.constant 0 : i5
        sv.verbatim "WHEN_ASSERT_24: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%26, %2, %27) : i1, i5, i5
        %28 = comb.or %en0, %20 : i1
        %29 = comb.xor %19, %28 : i1
        %30 = hw.constant 0 : i8
        sv.verbatim "WHEN_ASSERT_25: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%29, %3, %30) : i1, i8, i8
        %31 = comb.or %en0, %20 : i1
        %32 = comb.xor %19, %31 : i1
        %33 = hw.constant 0 : i1
        sv.verbatim "WHEN_ASSERT_26: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%32, %4, %33) : i1, i1, i1
        %34 = comb.or %en0, %20 : i1
        %35 = comb.xor %19, %34 : i1
        %36 = hw.constant 0 : i5
        sv.verbatim "WHEN_ASSERT_27: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%35, %1, %36) : i1, i5, i5
        hw.output %11 : i8
    }
}
