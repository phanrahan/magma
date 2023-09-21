module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_when_reg_ce_implicit_override(%I: i8, %x: i1, %y: i1, %CLK: i1) -> (O: i8) {
        %0 = hw.constant 1 : i1
        %4 = sv.reg : !hw.inout<i8>
        %2 = sv.read_inout %4 : !hw.inout<i8>
        %5 = sv.reg : !hw.inout<i1>
        %3 = sv.read_inout %5 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %4, %1 : i8
            sv.if %y {
                sv.bpassign %4, %I : i8
            }
        }
        %7 = sv.wire sym @test_when_reg_ce_implicit_override._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i8>
        sv.assign %7, %2 : i8
        %6 = sv.read_inout %7 : !hw.inout<i8>
        %8 = sv.reg name "Register_inst0" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.if %x {
                sv.passign %8, %6 : i8
            }
        }
        %9 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %8, %9 : i8
        }
        %1 = sv.read_inout %8 : !hw.inout<i8>
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%y, %6, %I) : i1, i8, i8
        %11 = hw.constant -1 : i1
        %10 = comb.xor %11, %y : i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%10, %6, %1) : i1, i8, i8
        hw.output %1 : i8
    }
}
