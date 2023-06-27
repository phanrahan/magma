module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_emit_asserts_tuple_elab(%I_0_0: i8, %I_0_1: i1, %I_1_0: i8, %I_1_1: i1, %S: i1, %CLK: i1) -> (O_0: i8, O_1: i1) {
        %4 = sv.reg name "_WHEN_WIRE_0" : !hw.inout<i8>
        %2 = sv.read_inout %4 : !hw.inout<i8>
        %5 = sv.reg name "_WHEN_WIRE_1" : !hw.inout<i1>
        %3 = sv.read_inout %5 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %4, %0 : i8
            sv.bpassign %5, %1 : i1
            sv.if %S {
                sv.bpassign %4, %0 : i8
                sv.bpassign %5, %1 : i1
            } else {
                sv.if %I_0_1 {
                    sv.bpassign %4, %0 : i8
                    sv.bpassign %5, %1 : i1
                }
            }
        }
        %6 = sv.reg name "Register_inst0" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %6, %2 : i8
        }
        %7 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %6, %7 : i8
        }
        %0 = sv.read_inout %6 : !hw.inout<i8>
        %8 = sv.reg name "Register_inst0" : !hw.inout<i1>
        sv.alwaysff(posedge %CLK) {
            sv.passign %8, %3 : i1
        }
        %9 = hw.constant 0 : i1
        sv.initial {
            sv.bpassign %8, %9 : i1
        }
        %1 = sv.read_inout %8 : !hw.inout<i1>
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %2, %0) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %3, %1) : i1, i1, i1
        %11 = hw.constant -1 : i1
        %10 = comb.xor %11, %S : i1
        %12 = comb.and %10, %I_0_1 : i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%12, %2, %0) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%12, %3, %1) : i1, i1, i1
        %13 = comb.or %S, %12 : i1
        %14 = comb.xor %11, %13 : i1
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%14, %2, %0) : i1, i8, i8
        %15 = comb.or %S, %12 : i1
        %16 = comb.xor %11, %15 : i1
        sv.verbatim "WHEN_ASSERT_5: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%16, %3, %1) : i1, i1, i1
        hw.output %0, %1 : i8, i1
    }
}
