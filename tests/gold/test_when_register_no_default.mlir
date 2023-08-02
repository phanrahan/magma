module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_register_no_default(%I: i1, %E: i1, %CLK: i1) -> (O: i1) {
        %1 = hw.constant -1 : i1
        %0 = comb.xor %1, %I : i1
        %3 = sv.reg : !hw.inout<i1>
        %2 = sv.read_inout %3 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %E {
                sv.bpassign %3, %I : i1
            } else {
                sv.bpassign %3, %0 : i1
            }
        }
        %5 = sv.wire sym @test_register_no_default._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i1>
        sv.assign %5, %2 : i1
        %4 = sv.read_inout %5 : !hw.inout<i1>
        %7 = sv.reg name "Register_inst0" : !hw.inout<i1>
        sv.alwaysff(posedge %CLK) {
            sv.passign %7, %4 : i1
        }
        %8 = hw.constant 0 : i1
        sv.initial {
            sv.bpassign %7, %8 : i1
        }
        %6 = sv.read_inout %7 : !hw.inout<i1>
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%E, %4, %I) : i1, i1, i1
        %9 = comb.xor %1, %E : i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%9, %4, %0) : i1, i1, i1
        hw.output %6 : i1
    }
}
