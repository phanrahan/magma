module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_recursive_non_port(%I: i2, %S: i1) -> (O0: i1, O1: i1) {
        %0 = comb.extract %I from 0 : (i2) -> i1
        %1 = comb.extract %I from 1 : (i2) -> i1
        %4 = sv.reg name "_WHEN_WIRE_51" : !hw.inout<i1>
        %2 = sv.read_inout %4 : !hw.inout<i1>
        %5 = sv.reg name "_WHEN_WIRE_52" : !hw.inout<i1>
        %3 = sv.read_inout %5 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %S {
                sv.bpassign %4, %0 : i1
                sv.bpassign %5, %2 : i1
            } else {
                sv.bpassign %4, %1 : i1
                sv.bpassign %5, %2 : i1
            }
        }
        sv.verbatim "WHEN_ASSERT_39: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %2, %0) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_40: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %3, %2) : i1, i1, i1
        %7 = hw.constant -1 : i1
        %6 = comb.xor %7, %S : i1
        sv.verbatim "WHEN_ASSERT_41: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%6, %2, %1) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_42: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%6, %3, %2) : i1, i1, i1
        hw.output %2, %3 : i1, i1
    }
}
