module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_nested_otherwise(%I: i2, %S: i2) -> (O: i2) {
        %1 = hw.constant -1 : i2
        %0 = comb.icmp eq %S, %1 : i2
        %2 = comb.extract %S from 1 : (i2) -> i1
        %4 = hw.constant -1 : i2
        %3 = comb.xor %4, %I : i2
        %6 = sv.reg name "_WHEN_WIRE_0" : !hw.inout<i2>
        %5 = sv.read_inout %6 : !hw.inout<i2>
        sv.alwayscomb {
            sv.if %0 {
                sv.bpassign %6, %I : i2
            } else {
                sv.if %2 {
                    sv.bpassign %6, %3 : i2
                } else {
                    sv.bpassign %6, %I : i2
                }
            }
        }
        sv.verbatim "WHEN_ASSERT_80: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %5, %I) : i1, i2, i2
        %8 = hw.constant -1 : i1
        %7 = comb.xor %8, %0 : i1
        %9 = comb.and %7, %2 : i1
        sv.verbatim "WHEN_ASSERT_81: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%9, %5, %3) : i1, i2, i2
        %10 = comb.xor %8, %2 : i1
        %11 = comb.and %7, %10 : i1
        sv.verbatim "WHEN_ASSERT_82: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%11, %5, %I) : i1, i2, i2
        hw.output %5 : i2
    }
}
