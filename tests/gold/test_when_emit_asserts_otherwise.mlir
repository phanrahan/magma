module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_emit_asserts_otherwise(%I: i2, %S: i1) -> (O: i1) {
        %0 = comb.extract %I from 0 : (i2) -> i1
        %1 = comb.extract %I from 1 : (i2) -> i1
        %3 = sv.reg : !hw.inout<i1>
        %2 = sv.read_inout %3 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %S {
                sv.bpassign %3, %0 : i1
            } else {
                sv.bpassign %3, %1 : i1
            }
        }
        sv.verbatim "always @(*) WHEN_ASSERT_525: assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %2, %0) : i1, i1, i1
        %5 = hw.constant -1 : i1
        %4 = comb.xor %5, %S : i1
        sv.verbatim "always @(*) WHEN_ASSERT_526: assert (~({{0}}) | ({{1}} == {{2}}));" (%4, %2, %1) : i1, i1, i1
        hw.output %2 : i1
    }
}
