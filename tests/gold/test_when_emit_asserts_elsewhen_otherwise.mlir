module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_emit_asserts_elsewhen_otherwise(%I: i2, %S: i2) -> (O: i1) {
        %0 = comb.extract %S from 0 : (i2) -> i1
        %1 = comb.extract %I from 0 : (i2) -> i1
        %2 = comb.extract %S from 1 : (i2) -> i1
        %4 = hw.constant -1 : i1
        %3 = comb.xor %4, %1 : i1
        %5 = comb.extract %I from 1 : (i2) -> i1
        %7 = sv.reg name "_WHEN_WIRE_159" : !hw.inout<i1>
        %6 = sv.read_inout %7 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %0 {
                sv.bpassign %7, %1 : i1
            } else {
                sv.if %2 {
                    sv.bpassign %7, %3 : i1
                } else {
                    sv.bpassign %7, %5 : i1
                }
            }
        }
        sv.verbatim "WHEN_ASSERT_432: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %6, %1) : i1, i1, i1
        %8 = comb.xor %4, %0 : i1
        %9 = comb.and %8, %2 : i1
        sv.verbatim "WHEN_ASSERT_433: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%9, %6, %3) : i1, i1, i1
        %10 = comb.xor %4, %2 : i1
        %11 = comb.and %8, %10 : i1
        sv.verbatim "WHEN_ASSERT_434: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%11, %6, %5) : i1, i1, i1
        hw.output %6 : i1
    }
}
