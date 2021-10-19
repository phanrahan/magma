hw.module @ResetShiftRegister(%I: i4, %shift: i1, %CLK: i1, %RESETN: i1) -> (%O: i4) {
    %1 = sv.reg {name = "Register_inst0"} : !hw.inout<i4>
    sv.alwaysff(posedge %shift) {
        sv.passign %1, %I : i4
    } (syncreset : negedge %CLK) {
        sv.passign %1, %2 : i4
    }
    %2 = hw.constant 0 : i4
    sv.initial {
        sv.bpassign %1, %2 : i4
    }
    %0 = sv.read_inout %1 : !hw.inout<i4>
    %4 = sv.reg {name = "Register_inst1"} : !hw.inout<i4>
    sv.alwaysff(posedge %shift) {
        sv.passign %4, %0 : i4
    } (syncreset : negedge %CLK) {
        sv.passign %4, %5 : i4
    }
    %5 = hw.constant 0 : i4
    sv.initial {
        sv.bpassign %4, %5 : i4
    }
    %3 = sv.read_inout %4 : !hw.inout<i4>
    %7 = sv.reg {name = "Register_inst2"} : !hw.inout<i4>
    sv.alwaysff(posedge %shift) {
        sv.passign %7, %3 : i4
    } (syncreset : negedge %CLK) {
        sv.passign %7, %8 : i4
    }
    %8 = hw.constant 0 : i4
    sv.initial {
        sv.bpassign %7, %8 : i4
    }
    %6 = sv.read_inout %7 : !hw.inout<i4>
    %10 = sv.reg {name = "Register_inst3"} : !hw.inout<i4>
    sv.alwaysff(posedge %shift) {
        sv.passign %10, %6 : i4
    } (syncreset : negedge %CLK) {
        sv.passign %10, %11 : i4
    }
    %11 = hw.constant 0 : i4
    sv.initial {
        sv.bpassign %10, %11 : i4
    }
    %9 = sv.read_inout %10 : !hw.inout<i4>
    hw.output %9 : i4
}
