module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_when_emit_asserts_tuple_elab_True(%I_0_0: i8, %I_0_1: i1, %I_1_0: i8, %I_1_1: i1, %S: i1, %CLK: i1) -> (O_0: i8, O_1: i1) {
        %4 = sv.reg : !hw.inout<i8>
        %2 = sv.read_inout %4 : !hw.inout<i8>
        %5 = sv.reg : !hw.inout<i1>
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
        %7 = sv.wire sym @test_when_emit_asserts_tuple_elab_True._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i8>
        sv.assign %7, %2 : i8
        %6 = sv.read_inout %7 : !hw.inout<i8>
        %9 = sv.wire sym @test_when_emit_asserts_tuple_elab_True._WHEN_ASSERT_1 name "_WHEN_ASSERT_1" : !hw.inout<i1>
        sv.assign %9, %3 : i1
        %8 = sv.read_inout %9 : !hw.inout<i1>
        %10 = sv.reg name "Register_inst0" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.passign %10, %6 : i8
        }
        %11 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %10, %11 : i8
        }
        %0 = sv.read_inout %10 : !hw.inout<i8>
        %12 = sv.reg name "Register_inst0" : !hw.inout<i1>
        sv.alwaysff(posedge %CLK) {
            sv.passign %12, %8 : i1
        }
        %13 = hw.constant 0 : i1
        sv.initial {
            sv.bpassign %12, %13 : i1
        }
        %1 = sv.read_inout %12 : !hw.inout<i1>
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %6, %0) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %8, %1) : i1, i1, i1
        %15 = hw.constant -1 : i1
        %14 = comb.xor %15, %S : i1
        %16 = comb.and %14, %I_0_1 : i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%16, %6, %0) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%16, %8, %1) : i1, i1, i1
        %17 = comb.or %S, %16 : i1
        %18 = comb.xor %15, %17 : i1
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%18, %6, %0) : i1, i8, i8
        %19 = comb.or %S, %16 : i1
        %20 = comb.xor %15, %19 : i1
        sv.verbatim "WHEN_ASSERT_5: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%20, %8, %1) : i1, i1, i1
        hw.output %0, %1 : i8, i1
    }
}
