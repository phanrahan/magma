module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_multiple_drivers(%I: i2, %S: i2) -> (O0: i1, O1: i1) {
        %0 = comb.extract %S from 0 : (i2) -> i1
        %1 = comb.extract %S from 1 : (i2) -> i1
        %2 = comb.extract %I from 1 : (i2) -> i1
        %3 = comb.extract %I from 0 : (i2) -> i1
        %6 = sv.reg : !hw.inout<i1>
        %4 = sv.read_inout %6 : !hw.inout<i1>
        %7 = sv.reg : !hw.inout<i1>
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
        %9 = sv.wire sym @test_when_multiple_drivers._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i1>
        sv.assign %9, %4 : i1
        %8 = sv.read_inout %9 : !hw.inout<i1>
        %11 = sv.wire sym @test_when_multiple_drivers._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i1>
        sv.assign %11, %5 : i1
        %10 = sv.read_inout %11 : !hw.inout<i1>
        %12 = comb.and %0, %1 : i1
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%12, %8, %3) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%12, %10, %2) : i1, i1, i1
        %14 = hw.constant -1 : i1
        %13 = comb.xor %14, %12 : i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%13, %8, %2) : i1, i1, i1
        %15 = comb.xor %14, %12 : i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%15, %10, %3) : i1, i1, i1
        hw.output %8, %10 : i1, i1
    }
}
