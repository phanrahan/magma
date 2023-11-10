module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_when_nested_with_default(in %I: i2, in %S: i2, out O: i1) {
        %0 = comb.extract %S from 0 : (i2) -> i1
        %1 = comb.extract %S from 1 : (i2) -> i1
        %2 = comb.extract %I from 1 : (i2) -> i1
        %3 = comb.extract %I from 0 : (i2) -> i1
        %5 = sv.reg : !hw.inout<i1>
        %4 = sv.read_inout %5 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %5, %2 : i1
            sv.if %0 {
                sv.if %1 {
                    sv.bpassign %5, %3 : i1
                }
            }
        }
        %7 = sv.wire sym @test_when_nested_with_default._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i1>
        sv.assign %7, %4 : i1
        %6 = sv.read_inout %7 : !hw.inout<i1>
        %8 = comb.and %0, %1 : i1
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%8, %6, %3) : i1, i1, i1
        %10 = hw.constant -1 : i1
        %9 = comb.xor %10, %8 : i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%9, %6, %2) : i1, i1, i1
        hw.output %6 : i1
    }
}
