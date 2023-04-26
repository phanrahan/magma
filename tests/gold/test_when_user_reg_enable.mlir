module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module.extern @Register(%I: i8, %CE: i1, %CLK: i1) -> (O: i8)
    hw.module @test_when_user_reg_enable(%I: i8, %x: i2, %CLK: i1) -> (O: i8) {
        %0 = comb.extract %x from 0 : (i2) -> i1
        %1 = hw.constant 1 : i1
        %2 = comb.extract %x from 1 : (i2) -> i1
        %4 = hw.constant -1 : i8
        %3 = comb.xor %4, %I : i8
        %5 = hw.constant 0 : i1
        %9 = sv.reg : !hw.inout<i8>
        %7 = sv.read_inout %9 : !hw.inout<i8>
        %10 = sv.reg : !hw.inout<i1>
        %8 = sv.read_inout %10 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %9, %6 : i8
            sv.bpassign %10, %5 : i1
            sv.if %0 {
                sv.bpassign %9, %I : i8
                sv.bpassign %10, %1 : i1
            } else {
                sv.if %2 {
                    sv.bpassign %9, %3 : i8
                    sv.bpassign %10, %1 : i1
                }
            }
        }
        %6 = hw.instance "Register_inst0" @Register(I: %7: i8, CE: %8: i1, CLK: %CLK: i1) -> (O: i8)
        sv.verbatim "always @(*) WHEN_ASSERT_192: assert (~({{0}}) | ({{1}} == {{2}}));" (%0, %7, %I) : i1, i8, i8
        %11 = hw.constant 1 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_193: assert (~({{0}}) | ({{1}} == {{2}}));" (%0, %8, %11) : i1, i1, i1
        %13 = hw.constant -1 : i1
        %12 = comb.xor %13, %0 : i1
        %14 = comb.and %12, %2 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_194: assert (~({{0}}) | ({{1}} == {{2}}));" (%14, %7, %3) : i1, i8, i8
        %15 = hw.constant 1 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_195: assert (~({{0}}) | ({{1}} == {{2}}));" (%14, %8, %15) : i1, i1, i1
        %16 = comb.xor %13, %2 : i1
        %17 = comb.and %12, %16 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_196: assert (~({{0}}) | ({{1}} == {{2}}));" (%17, %7, %6) : i1, i8, i8
        %18 = hw.constant 0 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_197: assert (~({{0}}) | ({{1}} == {{2}}));" (%17, %8, %18) : i1, i1, i1
        hw.output %6 : i8
    }
}
