module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_nested_with_default(%I: i2, %S: i2) -> (O: i1) {
        %0 = comb.extract %S from 0 : (i2) -> i1
        %1 = comb.extract %S from 1 : (i2) -> i1
        %2 = comb.extract %I from 1 : (i2) -> i1
        %3 = comb.extract %I from 0 : (i2) -> i1
        %5 = sv.reg name "_WHEN_WIRE_0" : !hw.inout<i1>
        %4 = sv.read_inout %5 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %5, %2 : i1
            sv.if %0 {
                sv.if %1 {
                    sv.bpassign %5, %3 : i1
                }
            }
        }
        %6 = comb.and %0, %1 : i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%6, %4, %3) : i1, i1, i1
        %8 = hw.constant -1 : i1
        %7 = comb.xor %8, %6 : i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%7, %4, %2) : i1, i1, i1
        hw.output %4 : i1
    }
}
