module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_emit_asserts_basic(%I: i2, %S: i1) -> (O: i1) {
        %0 = comb.extract %I from 1 : (i2) -> i1
        %1 = comb.extract %I from 0 : (i2) -> i1
        %5 = sv.reg : !hw.inout<i1>
        %2 = sv.read_inout %5 : !hw.inout<i1>
        %6 = sv.reg : !hw.inout<i1>
        %3 = sv.read_inout %6 : !hw.inout<i1>
        %7 = sv.reg : !hw.inout<i1>
        %4 = sv.read_inout %7 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %7, %0 : i1
            sv.if %S {
                sv.bpassign %7, %1 : i1
            }
        }
        sv.verbatim "WHEN_ASSERT_0: always @(*) assert (~({{0}}) | ({{1}} == {{2}}));" (%S, %4, %1) : i1, i1, i1
        %9 = hw.constant -1 : i1
        %8 = comb.xor %9, %S : i1
        sv.verbatim "WHEN_ASSERT_1: always @(*) assert (~({{0}}) | ({{1}} == {{2}}));" (%8, %4, %0) : i1, i1, i1
        hw.output %4 : i1
    }
}
