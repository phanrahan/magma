module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_multiple_drivers(%I: i2, %S: i2) -> (O0: i1, O1: i1) {
        %0 = comb.extract %S from 0 : (i2) -> i1
        %1 = comb.extract %S from 1 : (i2) -> i1
        %2 = comb.extract %I from 1 : (i2) -> i1
        %3 = comb.extract %I from 0 : (i2) -> i1
        %6 = sv.reg name "_WHEN_WIRE_12" : !hw.inout<i1>
        %4 = sv.read_inout %6 : !hw.inout<i1>
        %7 = sv.reg name "_WHEN_WIRE_13" : !hw.inout<i1>
        %5 = sv.read_inout %7 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %6, %2 : i1
            sv.bpassign %7, %3 : i1
            sv.if %0 {
                sv.if %1 {
                    sv.bpassign %6, %3 : i1
                    sv.bpassign %7, %2 : i1
                }
            }
        }
        %8 = comb.and %0, %1 : i1
        sv.verbatim "WHEN_ASSERT_7: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%8, %4, %3) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_8: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%8, %5, %2) : i1, i1, i1
        hw.output %4, %5 : i1, i1
    }
}
