module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @complex_register_wrapper(%a_x: i8, %a_y: i1, %b: !hw.array<6xi16>, %CLK: i1, %CE: i1, %ASYNCRESET: i1) -> (y_u_x: i8, y_u_y: i1, y_v: !hw.array<6xi16>) {
        %2 = sv.reg {name = "Register_inst0"} : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.if %CE {
                sv.passign %2, %a_x : i8
            }
        } (asyncreset : posedge %ASYNCRESET) {
            sv.passign %2, %3 : i8
        }
        %3 = hw.constant 10 : i8
        sv.initial {
            sv.bpassign %2, %3 : i8
        }
        %0 = sv.read_inout %2 : !hw.inout<i8>
        %4 = sv.reg {name = "Register_inst0"} : !hw.inout<i1>
        sv.alwaysff(posedge %CLK) {
            sv.if %CE {
                sv.passign %4, %a_y : i1
            }
        } (asyncreset : posedge %ASYNCRESET) {
            sv.passign %4, %5 : i1
        }
        %5 = hw.constant 1 : i1
        sv.initial {
            sv.bpassign %4, %5 : i1
        }
        %1 = sv.read_inout %4 : !hw.inout<i1>
        %7 = sv.reg {name = "Register_inst1"} : !hw.inout<!hw.array<6xi16>>
        sv.alwaysff(posedge %CLK) {
            sv.passign %7, %b : !hw.array<6xi16>
        }
        %9 = hw.constant 0 : i16
        %10 = hw.constant 2 : i16
        %11 = hw.constant 4 : i16
        %12 = hw.constant 6 : i16
        %13 = hw.constant 8 : i16
        %14 = hw.constant 10 : i16
        %8 = hw.array_create %9, %10, %11, %12, %13, %14 : i16
        sv.initial {
            sv.bpassign %7, %8 : !hw.array<6xi16>
        }
        %6 = sv.read_inout %7 : !hw.inout<!hw.array<6xi16>>
        %16 = sv.reg {name = "Register_inst2"} : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.if %CE {
                sv.passign %16, %a_x : i8
            }
        }
        %17 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %16, %17 : i8
        }
        %15 = sv.read_inout %16 : !hw.inout<i8>
        hw.output %0, %1, %6 : i8, i1, !hw.array<6xi16>
    }
}
