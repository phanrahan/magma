module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_when_emit_asserts_elsewhen_otherwise(%I: i2, %S: i2) -> (O: i1) {
        %0 = comb.extract %S from 0 : (i2) -> i1
        %1 = comb.extract %I from 0 : (i2) -> i1
        %2 = comb.extract %S from 1 : (i2) -> i1
        %4 = hw.constant -1 : i1
        %3 = comb.xor %4, %1 : i1
        %5 = comb.extract %I from 1 : (i2) -> i1
        %7 = sv.reg : !hw.inout<i1>
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
        %9 = sv.wire sym @test_when_emit_asserts_elsewhen_otherwise._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i1>
        sv.assign %9, %6 : i1
        %8 = sv.read_inout %9 : !hw.inout<i1>
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %8, %1) : i1, i1, i1
        %10 = comb.xor %4, %0 : i1
        %11 = comb.and %10, %2 : i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%11, %8, %3) : i1, i1, i1
        %12 = comb.xor %4, %2 : i1
        %13 = comb.and %10, %12 : i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%13, %8, %5) : i1, i1, i1
        hw.output %8 : i1
    }
}
