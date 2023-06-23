module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_reg_ce_explicit_wire(%I: i8, %x: i1, %y: i1, %CLK: i1) -> (O: i8) {
        %0 = hw.constant 0 : i1
        %4 = sv.reg name "_WHEN_WIRE_88" : !hw.inout<i8>
        %2 = sv.read_inout %4 : !hw.inout<i8>
        %5 = sv.reg name "_WHEN_WIRE_89" : !hw.inout<i1>
        %3 = sv.read_inout %5 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %4, %1 : i8
            sv.bpassign %5, %0 : i1
            sv.if %y {
                sv.bpassign %4, %I : i8
                sv.bpassign %5, %x : i1
            }
        }
        %6 = sv.reg name "Register_inst0" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.if %3 {
                sv.passign %6, %2 : i8
            }
        }
        %7 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %6, %7 : i8
        }
        %1 = sv.read_inout %6 : !hw.inout<i8>
        sv.verbatim "WHEN_ASSERT_130: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%y, %2, %I) : i1, i8, i8
        sv.verbatim "WHEN_ASSERT_131: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%y, %3, %x) : i1, i1, i1
        hw.output %1 : i8
    }
}
