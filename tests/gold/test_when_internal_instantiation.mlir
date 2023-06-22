module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_internal_instantiation(%I: i2, %S: i1) -> (O: i1) {
        %0 = comb.extract %I from 0 : (i2) -> i1
        %1 = hw.constant 1 : i1
        %2 = comb.and %0, %1 : i1
        %3 = comb.extract %I from 1 : (i2) -> i1
        %4 = hw.constant 1 : i1
        %5 = comb.xor %3, %4 : i1
        %7 = sv.reg name "_WHEN_WIRE_53" : !hw.inout<i1>
        %6 = sv.read_inout %7 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %S {
                sv.bpassign %7, %2 : i1
            } else {
                sv.bpassign %7, %5 : i1
            }
        }
        sv.verbatim "WHEN_ASSERT_56: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %6, %2) : i1, i1, i1
        %9 = hw.constant -1 : i1
        %8 = comb.xor %9, %S : i1
        sv.verbatim "WHEN_ASSERT_57: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%8, %6, %5) : i1, i1, i1
        hw.output %6 : i1
    }
}
