module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_register_default(in %I: i1, in %E: i1, in %CLK: i1, out O: i1) {
        %2 = sv.reg : !hw.inout<i1>
        %1 = sv.read_inout %2 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %2, %0 : i1
            sv.if %E {
                sv.bpassign %2, %I : i1
            }
        }
        %4 = sv.wire sym @test_register_default._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i1>
        sv.assign %4, %1 : i1
        %3 = sv.read_inout %4 : !hw.inout<i1>
        %5 = sv.reg name "Register_inst0" : !hw.inout<i1>
        sv.alwaysff(posedge %CLK) {
            sv.passign %5, %3 : i1
        }
        %6 = hw.constant 0 : i1
        sv.initial {
            sv.bpassign %5, %6 : i1
        }
        %0 = sv.read_inout %5 : !hw.inout<i1>
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%E, %3, %I) : i1, i1, i1
        %8 = hw.constant -1 : i1
        %7 = comb.xor %8, %E : i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%7, %3, %0) : i1, i1, i1
        hw.output %0 : i1
    }
}
