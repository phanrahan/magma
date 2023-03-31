module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
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
        %6 = sv.reg name "Register_inst0" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.if %x {
                sv.passign %6, %2 : i8
            }
        }
        %7 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %6, %7 : i8
        }
        %1 = sv.read_inout %6 : !hw.inout<i8>
        hw.output %1 : i8
    }
}
