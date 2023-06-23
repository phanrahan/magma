module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_reg_ce_already_wired(%I: i8, %x: i1, %y: i1, %CLK: i1) -> (O: i8) {
        %2 = sv.reg name "_WHEN_WIRE_87" : !hw.inout<i8>
        %1 = sv.read_inout %2 : !hw.inout<i8>
        sv.alwayscomb {
            sv.bpassign %2, %0 : i8
            sv.if %y {
                sv.bpassign %2, %I : i8
            }
        }
        %3 = sv.reg name "Register_inst0" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.if %x {
                sv.passign %3, %1 : i8
            }
        }
        %4 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %3, %4 : i8
        }
        %0 = sv.read_inout %3 : !hw.inout<i8>
        sv.verbatim "WHEN_ASSERT_129: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%y, %1, %I) : i1, i8, i8
        hw.output %0 : i8
    }
}
