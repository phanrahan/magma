module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_reg_ce_implicit_wire_twice(%I: i8, %x: i1, %y: i1, %CLK: i1) -> (O: i8) {
        %0 = hw.constant 1 : i1
        %1 = hw.constant 0 : i1
        %5 = sv.reg : !hw.inout<i8>
        %3 = sv.read_inout %5 : !hw.inout<i8>
        %6 = sv.reg : !hw.inout<i1>
        %4 = sv.read_inout %6 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %5, %2 : i8
            sv.bpassign %6, %1 : i1
            sv.if %y {
                sv.bpassign %5, %I : i8
                sv.bpassign %6, %0 : i1
            }
        }
        %8 = hw.constant -1 : i8
        %7 = comb.xor %8, %I : i8
        %9 = hw.constant 1 : i1
        %12 = sv.reg : !hw.inout<i8>
        %10 = sv.read_inout %12 : !hw.inout<i8>
        %13 = sv.reg : !hw.inout<i1>
        %11 = sv.read_inout %13 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %12, %3 : i8
            sv.bpassign %13, %4 : i1
            sv.if %x {
                sv.bpassign %12, %7 : i8
                sv.bpassign %13, %9 : i1
            }
        }
        %14 = sv.reg name "Register_inst0" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.if %11 {
                sv.passign %14, %10 : i8
            }
        }
        %15 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %14, %15 : i8
        }
        %2 = sv.read_inout %14 : !hw.inout<i8>
        hw.output %2 : i8
    }
}
