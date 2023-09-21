module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_when_emit_asserts_chained(%I: i2, %S: i2) -> (O: i1) {
        %0 = comb.extract %S from 1 : (i2) -> i1
        %1 = comb.extract %S from 0 : (i2) -> i1
        %2 = comb.extract %I from 1 : (i2) -> i1
        %3 = comb.extract %I from 0 : (i2) -> i1
        %5 = sv.reg : !hw.inout<i1>
        %4 = sv.read_inout %5 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %5, %2 : i1
            sv.if %1 {
                sv.bpassign %5, %3 : i1
            }
        }
        %7 = sv.wire sym @test_when_emit_asserts_chained._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i1>
        sv.assign %7, %4 : i1
        %6 = sv.read_inout %7 : !hw.inout<i1>
        %9 = hw.constant -1 : i1
        %8 = comb.xor %9, %6 : i1
        %11 = sv.reg : !hw.inout<i1>
        %10 = sv.read_inout %11 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %11, %6 : i1
            sv.if %0 {
                sv.bpassign %11, %8 : i1
            }
        }
        %13 = sv.wire sym @test_when_emit_asserts_chained._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i1>
        sv.assign %13, %10 : i1
        %12 = sv.read_inout %13 : !hw.inout<i1>
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%1, %6, %3) : i1, i1, i1
        %14 = comb.xor %9, %1 : i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%14, %6, %2) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %12, %8) : i1, i1, i1
        %15 = comb.xor %9, %0 : i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%15, %12, %6) : i1, i1, i1
        hw.output %12 : i1
    }
}
