module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_when_partial_array_assign(in %I: i2, in %S: i1, out O: i2) {
        %0 = comb.extract %I from 1 : (i2) -> i1
        %1 = comb.extract %I from 0 : (i2) -> i1
        %3 = sv.reg : !hw.inout<i1>
        %2 = sv.read_inout %3 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %S {
                sv.bpassign %3, %1 : i1
            } else {
                sv.bpassign %3, %0 : i1
            }
        }
        %5 = sv.wire sym @test_when_partial_array_assign._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i1>
        sv.assign %5, %2 : i1
        %4 = sv.read_inout %5 : !hw.inout<i1>
        %6 = comb.concat %4, %0 : i1, i1
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %4, %1) : i1, i1, i1
        %8 = hw.constant -1 : i1
        %7 = comb.xor %8, %S : i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%7, %4, %0) : i1, i1, i1
        hw.output %6 : i2
    }
}
