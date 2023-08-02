module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_nested_Array2_AnonProductxBit_yBits2_Bit_True(%I_0_0_x: i1, %I_0_0_y: i2, %I_0_1_x: i1, %I_0_1_y: i2, %I_1_0_x: i1, %I_1_0_y: i2, %I_1_1_x: i1, %I_1_1_y: i2, %S: i1) -> (O_0_x: i1, O_0_y: i2, O_1_x: i1, O_1_y: i2) {
        %4 = sv.reg : !hw.inout<i1>
        %0 = sv.read_inout %4 : !hw.inout<i1>
        %5 = sv.reg : !hw.inout<i2>
        %1 = sv.read_inout %5 : !hw.inout<i2>
        %6 = sv.reg : !hw.inout<i1>
        %2 = sv.read_inout %6 : !hw.inout<i1>
        %7 = sv.reg : !hw.inout<i2>
        %3 = sv.read_inout %7 : !hw.inout<i2>
        sv.alwayscomb {
            sv.bpassign %4, %I_1_0_x : i1
            sv.bpassign %5, %I_1_0_y : i2
            sv.bpassign %6, %I_1_1_x : i1
            sv.bpassign %7, %I_1_1_y : i2
            sv.if %S {
                sv.bpassign %4, %I_0_0_x : i1
                sv.bpassign %5, %I_0_0_y : i2
                sv.bpassign %6, %I_0_1_x : i1
                sv.bpassign %7, %I_0_1_y : i2
            }
        }
        %9 = sv.wire sym @test_when_nested_Array2_AnonProductxBit_yBits2_Bit_True._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i1>
        sv.assign %9, %0 : i1
        %8 = sv.read_inout %9 : !hw.inout<i1>
        %11 = sv.wire sym @test_when_nested_Array2_AnonProductxBit_yBits2_Bit_True._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i2>
        sv.assign %11, %1 : i2
        %10 = sv.read_inout %11 : !hw.inout<i2>
        %13 = sv.wire sym @test_when_nested_Array2_AnonProductxBit_yBits2_Bit_True._WHEN_ASSERT_2 name "_WHEN_ASSERT_2" : !hw.inout<i1>
        sv.assign %13, %2 : i1
        %12 = sv.read_inout %13 : !hw.inout<i1>
        %15 = sv.wire sym @test_when_nested_Array2_AnonProductxBit_yBits2_Bit_True._WHEN_ASSERT_3 name "_WHEN_ASSERT_3" : !hw.inout<i2>
        sv.assign %15, %3 : i2
        %14 = sv.read_inout %15 : !hw.inout<i2>
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %8, %I_0_0_x) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %10, %I_0_0_y) : i1, i2, i2
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %12, %I_0_1_x) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %14, %I_0_1_y) : i1, i2, i2
        %17 = hw.constant -1 : i1
        %16 = comb.xor %17, %S : i1
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%16, %8, %I_1_0_x) : i1, i1, i1
        %18 = comb.xor %17, %S : i1
        sv.verbatim "WHEN_ASSERT_5: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%18, %10, %I_1_0_y) : i1, i2, i2
        %19 = comb.xor %17, %S : i1
        sv.verbatim "WHEN_ASSERT_6: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%19, %12, %I_1_1_x) : i1, i1, i1
        %20 = comb.xor %17, %S : i1
        sv.verbatim "WHEN_ASSERT_7: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%20, %14, %I_1_1_y) : i1, i2, i2
        hw.output %8, %10, %12, %14 : i1, i2, i1, i2
    }
}
