module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_when_elsewhen(%I: i3, %S: i2) -> (O: i1) {
        %0 = comb.extract %S from 0 : (i2) -> i1
        %1 = comb.extract %I from 0 : (i3) -> i1
        %2 = comb.extract %S from 1 : (i2) -> i1
        %3 = comb.extract %I from 1 : (i3) -> i1
        %4 = comb.extract %I from 2 : (i3) -> i1
        %6 = sv.reg : !hw.inout<i1>
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
        %8 = sv.wire sym @test_when_elsewhen._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i1>
        sv.assign %8, %5 : i1
        %7 = sv.read_inout %8 : !hw.inout<i1>
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %7, %1) : i1, i1, i1
        %10 = hw.constant -1 : i1
        %9 = comb.xor %10, %0 : i1
        %11 = comb.and %9, %2 : i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%11, %7, %3) : i1, i1, i1
        %12 = comb.xor %10, %2 : i1
        %13 = comb.and %9, %12 : i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%13, %7, %4) : i1, i1, i1
        hw.output %7 : i1
    }
}
