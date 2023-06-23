module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_with_default(%I: i2, %S: i1) -> (O: i1) {
        %0 = comb.extract %I from 1 : (i2) -> i1
        %1 = comb.extract %I from 0 : (i2) -> i1
        %3 = sv.reg name "_WHEN_WIRE_1" : !hw.inout<i1>
        %2 = sv.read_inout %3 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %3, %0 : i1
            sv.if %S {
                sv.bpassign %3, %1 : i1
            }
        }
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %2, %1) : i1, i1, i1
        hw.output %2 : i1
    }
}
