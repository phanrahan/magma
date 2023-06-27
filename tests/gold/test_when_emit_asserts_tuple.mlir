module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_emit_asserts_tuple(%I_0_0: i8, %I_0_1: i1, %I_1_0: i8, %I_1_1: i1, %S: i1) -> (O_0: i8, O_1: i1) {
        %2 = sv.reg name "_WHEN_WIRE_0" : !hw.inout<i8>
        %0 = sv.read_inout %2 : !hw.inout<i8>
        %3 = sv.reg name "_WHEN_WIRE_1" : !hw.inout<i1>
        %1 = sv.read_inout %3 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %2, %I_1_0 : i8
            sv.bpassign %3, %I_1_1 : i1
            sv.if %S {
                sv.bpassign %2, %I_0_0 : i8
                sv.bpassign %3, %I_0_1 : i1
            }
        }
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %0, %I_0_0) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %1, %I_0_1) : i1, i1, i1
        %5 = hw.constant -1 : i1
        %4 = comb.xor %5, %S : i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%4, %0, %I_1_0) : i1, i8, i8
        %6 = comb.xor %5, %S : i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%6, %1, %I_1_1) : i1, i1, i1
        hw.output %0, %1 : i8, i1
    }
}
