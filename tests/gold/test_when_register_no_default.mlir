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
        %5 = sv.reg {name = "reg"} : !hw.inout<i1>
        sv.alwaysff(posedge %CLK) {
            sv.passign %5, %2 : i1
        }
        %6 = hw.constant 0 : i1
        sv.initial {
            sv.bpassign %5, %6 : i1
        }
        %4 = sv.read_inout %5 : !hw.inout<i1>
        hw.output %4 : i1
    }
}
