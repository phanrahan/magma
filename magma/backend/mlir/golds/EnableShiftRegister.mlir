hw.module @EnableShiftRegister(%I: i4, %shift: i1, %CLK: i1, %ASYNCRESET: i1) -> (O: i4) {
    %1 = sv.reg {name = "Register_inst0"} : !hw.inout<i4>
    sv.alwaysff(posedge %CLK) {
        sv.if %shift {
            sv.passign %1, %I : i4
        }
    } (asyncreset : posedge %ASYNCRESET) {
        sv.passign %1, %2 : i4
    }
    %2 = hw.constant 0 : i4
    sv.initial {
        sv.bpassign %1, %2 : i4
    }
    %0 = sv.read_inout %1 : !hw.inout<i4>
    %4 = sv.reg {name = "Register_inst1"} : !hw.inout<i4>
    sv.alwaysff(posedge %CLK) {
        sv.if %shift {
            sv.passign %4, %0 : i4
        }
    } (asyncreset : posedge %ASYNCRESET) {
        sv.passign %4, %2 : i4
    }
    sv.initial {
        sv.bpassign %4, %2 : i4
    }
    %3 = sv.read_inout %4 : !hw.inout<i4>
    %6 = sv.reg {name = "Register_inst2"} : !hw.inout<i4>
    sv.alwaysff(posedge %CLK) {
        sv.if %shift {
            sv.passign %6, %3 : i4
        }
    } (asyncreset : posedge %ASYNCRESET) {
        sv.passign %6, %2 : i4
    }
    sv.initial {
        sv.bpassign %6, %2 : i4
    }
    %5 = sv.read_inout %6 : !hw.inout<i4>
    %8 = sv.reg {name = "Register_inst3"} : !hw.inout<i4>
    sv.alwaysff(posedge %CLK) {
        sv.if %shift {
            sv.passign %8, %5 : i4
        }
    } (asyncreset : posedge %ASYNCRESET) {
        sv.passign %8, %2 : i4
    }
    sv.initial {
        sv.bpassign %8, %2 : i4
    }
    %7 = sv.read_inout %8 : !hw.inout<i4>
    hw.output %7 : i4
}
