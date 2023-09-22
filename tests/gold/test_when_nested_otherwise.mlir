module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_when_nested_otherwise(%I: i2, %S: i2) -> (O: i2) {
        %1 = hw.constant -1 : i2
        %0 = comb.icmp eq %S, %1 : i2
        %2 = comb.extract %S from 1 : (i2) -> i1
        %4 = hw.constant -1 : i2
        %3 = comb.xor %4, %I : i2
        %6 = sv.reg : !hw.inout<i2>
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
        %8 = sv.wire sym @test_when_nested_otherwise._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i2>
        sv.assign %8, %5 : i2
        %7 = sv.read_inout %8 : !hw.inout<i2>
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %7, %I) : i1, i2, i2
        %10 = hw.constant -1 : i1
        %9 = comb.xor %10, %0 : i1
        %11 = comb.and %9, %2 : i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%11, %7, %3) : i1, i2, i2
        %12 = comb.xor %10, %2 : i1
        %13 = comb.and %9, %12 : i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%13, %7, %I) : i1, i2, i2
        hw.output %7 : i2
    }
}
