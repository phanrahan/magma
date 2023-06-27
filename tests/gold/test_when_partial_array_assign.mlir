module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_partial_array_assign(%I: i2, %S: i1) -> (O: i2) {
        %0 = comb.extract %I from 1 : (i2) -> i1
        %1 = comb.extract %I from 0 : (i2) -> i1
        %3 = sv.reg name "_WHEN_WIRE_0" : !hw.inout<i1>
        %2 = sv.read_inout %3 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %S {
                sv.bpassign %3, %1 : i1
            } else {
                sv.bpassign %3, %0 : i1
            }
        }
        %4 = comb.concat %2, %0 : i1, i1
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %2, %1) : i1, i1, i1
        %6 = hw.constant -1 : i1
        %5 = comb.xor %6, %S : i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%5, %2, %0) : i1, i1, i1
        hw.output %4 : i2
    }
}
