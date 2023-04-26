module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_nested_Array2_AnonProductxBit_yBits2_Bit(%I_0_0_x: i1, %I_0_0_y: i2, %I_0_1_x: i1, %I_0_1_y: i2, %I_1_0_x: i1, %I_1_0_y: i2, %I_1_1_x: i1, %I_1_1_y: i2, %S: i1) -> (O_0_x: i1, O_0_y: i2, O_1_x: i1, O_1_y: i2) {
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
        sv.verbatim "always @(*) WHEN_ASSERT_51: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %0, %I_0_0_x) : i1, i1, i1
        sv.verbatim "always @(*) WHEN_ASSERT_52: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %1, %I_0_0_y) : i1, i2, i2
        sv.verbatim "always @(*) WHEN_ASSERT_53: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %2, %I_0_1_x) : i1, i1, i1
        sv.verbatim "always @(*) WHEN_ASSERT_54: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %3, %I_0_1_y) : i1, i2, i2
        %9 = hw.constant -1 : i1
        %8 = comb.xor %9, %S : i1
        sv.verbatim "always @(*) WHEN_ASSERT_55: assert (~({{0}}) | ({{1}} == {{2}}));" (%8, %0, %I_1_0_x) : i1, i1, i1
        sv.verbatim "always @(*) WHEN_ASSERT_56: assert (~({{0}}) | ({{1}} == {{2}}));" (%8, %1, %I_1_0_y) : i1, i2, i2
        sv.verbatim "always @(*) WHEN_ASSERT_57: assert (~({{0}}) | ({{1}} == {{2}}));" (%8, %2, %I_1_1_x) : i1, i1, i1
        sv.verbatim "always @(*) WHEN_ASSERT_58: assert (~({{0}}) | ({{1}} == {{2}}));" (%8, %3, %I_1_1_y) : i1, i2, i2
        hw.output %0, %1, %2, %3 : i1, i2, i1, i2
    }
}
