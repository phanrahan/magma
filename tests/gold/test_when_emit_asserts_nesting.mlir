module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_when_emit_asserts_nesting(%I: i2, %S: i2) -> (O: i1) {
        %0 = comb.extract %S from 0 : (i2) -> i1
        %1 = comb.extract %S from 1 : (i2) -> i1
        %2 = comb.extract %I from 1 : (i2) -> i1
        %3 = comb.extract %I from 0 : (i2) -> i1
        %5 = hw.constant -1 : i2
        %4 = comb.icmp eq %S, %5 : i2
        %7 = hw.constant -1 : i1
        %6 = comb.xor %7, %3 : i1
        %9 = sv.reg : !hw.inout<i1>
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
        %11 = sv.wire sym @test_when_emit_asserts_nesting._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i1>
        sv.assign %11, %8 : i1
        %10 = sv.read_inout %11 : !hw.inout<i1>
        %12 = comb.and %0, %1 : i1
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%12, %10, %3) : i1, i1, i1
        %13 = comb.xor %7, %1 : i1
        %14 = comb.and %0, %13 : i1
        %15 = comb.and %14, %4 : i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%15, %10, %6) : i1, i1, i1
        %16 = comb.or %12, %15 : i1
        %17 = comb.xor %7, %16 : i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%17, %10, %2) : i1, i1, i1
        hw.output %10 : i1
    }
}
