module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_emit_asserts_tuple(%I_0_0: i8, %I_0_1: i1, %I_1_0: i8, %I_1_1: i1, %S: i1) -> (O_0: i8, O_1: i1) {
        %2 = sv.reg name "_WHEN_WIRE_155" : !hw.inout<i8>
        %0 = sv.read_inout %2 : !hw.inout<i8>
        %3 = sv.reg name "_WHEN_WIRE_156" : !hw.inout<i1>
        %1 = sv.read_inout %3 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %2, %I_1_0 : i8
            sv.bpassign %3, %I_1_1 : i1
            sv.if %S {
                sv.bpassign %2, %I_0_0 : i8
                sv.bpassign %3, %I_0_1 : i1
            }
        }
        sv.verbatim "WHEN_ASSERT_370: assert property (({{0}}) |-> ({{{1}}, {{2}}} == {{{3}}, {{4}}}));" (%S, %1, %0, %I_0_1, %I_0_0) : i1, i1, i8, i1, i8
        hw.output %0, %1 : i8, i1
    }
}
