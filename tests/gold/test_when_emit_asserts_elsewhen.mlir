module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_emit_asserts_elsewhen(%I: i2, %S: i2) -> (O: i1) {
        %0 = comb.extract %S from 0 : (i2) -> i1
        %1 = comb.extract %I from 1 : (i2) -> i1
        %2 = comb.extract %I from 0 : (i2) -> i1
        %3 = comb.extract %S from 1 : (i2) -> i1
        %5 = hw.constant -1 : i1
        %4 = comb.xor %5, %2 : i1
        %7 = sv.reg : !hw.inout<i1>
        %6 = sv.read_inout %7 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %7, %1 : i1
            sv.if %0 {
                sv.bpassign %7, %2 : i1
            } else {
                sv.if %3 {
                    sv.bpassign %7, %4 : i1
                }
            }
        }
        sv.verbatim "always @(*) WHEN_ASSERT_527: assert (~({{0}}) | ({{1}} == {{2}}));" (%0, %6, %2) : i1, i1, i1
        %8 = comb.xor %5, %0 : i1
        %9 = comb.and %8, %3 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_528: assert (~({{0}}) | ({{1}} == {{2}}));" (%9, %6, %4) : i1, i1, i1
        %10 = comb.xor %5, %3 : i1
        %11 = comb.and %8, %10 : i1
        sv.verbatim "always @(*) WHEN_ASSERT_529: assert (~({{0}}) | ({{1}} == {{2}}));" (%11, %6, %1) : i1, i1, i1
        hw.output %6 : i1
    }
}
