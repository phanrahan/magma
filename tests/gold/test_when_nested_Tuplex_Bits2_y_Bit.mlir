module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_when_nested_Tuplex_Bits2_y_Bit(%I_0_x: i2, %I_0_y: i1, %I_1_x: i2, %I_1_y: i1, %S: i1) -> (O_x: i2, O_y: i1) {
        %2 = sv.reg : !hw.inout<i2>
        %0 = sv.read_inout %2 : !hw.inout<i2>
        %3 = sv.reg : !hw.inout<i1>
        %1 = sv.read_inout %3 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %2, %I_1_x : i2
            sv.bpassign %3, %I_1_y : i1
            sv.if %S {
                sv.bpassign %2, %I_0_x : i2
                sv.bpassign %3, %I_0_y : i1
            }
        }
        %5 = sv.wire sym @test_when_nested_Tuplex_Bits2_y_Bit._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i2>
        sv.assign %5, %0 : i2
        %4 = sv.read_inout %5 : !hw.inout<i2>
        %7 = sv.wire sym @test_when_nested_Tuplex_Bits2_y_Bit._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i1>
        sv.assign %7, %1 : i1
        %6 = sv.read_inout %7 : !hw.inout<i1>
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %4, %I_0_x) : i1, i2, i2
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %6, %I_0_y) : i1, i1, i1
        %9 = hw.constant -1 : i1
        %8 = comb.xor %9, %S : i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%8, %4, %I_1_x) : i1, i2, i2
        %10 = comb.xor %9, %S : i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%10, %6, %I_1_y) : i1, i1, i1
        hw.output %4, %6 : i2, i1
    }
}
