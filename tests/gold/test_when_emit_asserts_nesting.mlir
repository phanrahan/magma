module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_emit_asserts_nesting(%I: i2, %S: i2) -> (O: i1) {
        %0 = comb.extract %S from 0 : (i2) -> i1
        %1 = comb.extract %S from 1 : (i2) -> i1
        %2 = comb.extract %I from 1 : (i2) -> i1
        %3 = comb.extract %I from 0 : (i2) -> i1
        %5 = hw.constant -1 : i2
        %4 = comb.icmp eq %S, %5 : i2
        %7 = hw.constant -1 : i1
        %6 = comb.xor %7, %3 : i1
        %9 = sv.reg name "_WHEN_WIRE_160" : !hw.inout<i1>
        %8 = sv.read_inout %9 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %9, %2 : i1
            sv.if %0 {
                sv.if %1 {
                    sv.bpassign %9, %3 : i1
                } else {
                    sv.if %4 {
                        sv.bpassign %9, %6 : i1
                    }
                }
            }
        }
        %10 = comb.and %0, %1 : i1
        sv.verbatim "WHEN_ASSERT_378: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%10, %8, %3) : i1, i1, i1
        %11 = comb.xor %7, %1 : i1
        %12 = comb.and %0, %11 : i1
        %13 = comb.and %12, %4 : i1
        sv.verbatim "WHEN_ASSERT_379: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%13, %8, %6) : i1, i1, i1
        hw.output %8 : i1
    }
}
