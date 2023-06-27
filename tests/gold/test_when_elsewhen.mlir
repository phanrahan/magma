module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_elsewhen(%I: i3, %S: i2) -> (O: i1) {
        %0 = comb.extract %S from 0 : (i2) -> i1
        %1 = comb.extract %I from 0 : (i3) -> i1
        %2 = comb.extract %S from 1 : (i2) -> i1
        %3 = comb.extract %I from 1 : (i3) -> i1
        %4 = comb.extract %I from 2 : (i3) -> i1
        %6 = sv.reg name "_WHEN_WIRE_0" : !hw.inout<i1>
        %5 = sv.read_inout %6 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %0 {
                sv.bpassign %6, %1 : i1
            } else {
                sv.if %2 {
                    sv.bpassign %6, %3 : i1
                } else {
                    sv.bpassign %6, %4 : i1
                }
            }
        }
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %5, %1) : i1, i1, i1
        %8 = hw.constant -1 : i1
        %7 = comb.xor %8, %0 : i1
        %9 = comb.and %7, %2 : i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%9, %5, %3) : i1, i1, i1
        %10 = comb.xor %8, %2 : i1
        %11 = comb.and %7, %10 : i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%11, %5, %4) : i1, i1, i1
        hw.output %5 : i1
    }
}
