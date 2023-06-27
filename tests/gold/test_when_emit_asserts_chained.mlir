module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_emit_asserts_chained(%I: i2, %S: i2) -> (O: i1) {
        %0 = comb.extract %S from 1 : (i2) -> i1
        %1 = comb.extract %S from 0 : (i2) -> i1
        %2 = comb.extract %I from 1 : (i2) -> i1
        %3 = comb.extract %I from 0 : (i2) -> i1
        %5 = sv.reg name "_WHEN_WIRE_0" : !hw.inout<i1>
        %4 = sv.read_inout %5 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %5, %2 : i1
            sv.if %1 {
                sv.bpassign %5, %3 : i1
            }
        }
        %7 = hw.constant -1 : i1
        %6 = comb.xor %7, %4 : i1
        %9 = sv.reg name "_WHEN_WIRE_1" : !hw.inout<i1>
        %8 = sv.read_inout %9 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %9, %4 : i1
            sv.if %0 {
                sv.bpassign %9, %6 : i1
            }
        }
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%1, %4, %3) : i1, i1, i1
        %10 = comb.xor %7, %1 : i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%10, %4, %2) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %8, %6) : i1, i1, i1
        %11 = comb.xor %7, %0 : i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%11, %8, %4) : i1, i1, i1
        hw.output %8 : i1
    }
}
