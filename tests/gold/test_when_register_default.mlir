module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_register_default(%I: i1, %E: i1, %CLK: i1) -> (O: i1) {
        %2 = sv.reg : !hw.inout<i1>
        %1 = sv.read_inout %2 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %2, %0 : i1
            sv.if %E {
                sv.bpassign %2, %I : i1
            }
        }
        %3 = sv.reg {name = "Register_inst0"} : !hw.inout<i1>
        sv.alwaysff(posedge %CLK) {
            sv.passign %3, %1 : i1
        }
        %4 = hw.constant 0 : i1
        sv.initial {
            sv.bpassign %3, %4 : i1
        }
        %0 = sv.read_inout %3 : !hw.inout<i1>
        hw.output %0 : i1
    }
}
