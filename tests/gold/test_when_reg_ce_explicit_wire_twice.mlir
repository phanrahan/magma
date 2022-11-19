module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_reg_ce_explicit_wire_twice(%I: i8, %x: i1, %y: i1, %CLK: i1) -> (O: i8) {
        %2 = sv.reg : !hw.inout<i8>
        %1 = sv.read_inout %2 : !hw.inout<i8>
        sv.alwayscomb {
            sv.bpassign %2, %0 : i8
            sv.if %y {
                sv.bpassign %2, %I : i8
            }
        }
        %4 = hw.constant -1 : i8
        %3 = comb.xor %4, %I : i8
        %6 = sv.reg : !hw.inout<i8>
        %5 = sv.read_inout %6 : !hw.inout<i8>
        sv.alwayscomb {
            sv.bpassign %6, %1 : i8
            sv.if %x {
                sv.bpassign %6, %3 : i8
            }
        }
        %8 = hw.constant -1 : i1
        %7 = comb.xor %8, %y : i1
        %9 = sv.reg {name = "x"} : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.if %7 {
                sv.passign %9, %5 : i8
            }
        }
        %10 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %9, %10 : i8
        }
        %0 = sv.read_inout %9 : !hw.inout<i8>
        hw.output %0 : i8
    }
}
