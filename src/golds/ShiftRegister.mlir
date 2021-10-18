hw.module @ShiftRegister(%I: i1, %CLK: i1) -> (%O: i1) {
    %1 = sv.reg {name = "Register_inst0"} : !hw.inout<i1>
    sv.alwaysff(posedge %CLK) {
        sv.passign %1, %I : i1
    }
    %2 = hw.constant 0 : i1
    sv.initial {
        sv.bpassign %1, %2 : i1
    }
    %0 = sv.read_inout %1 : !hw.inout<i1>
    %4 = sv.reg {name = "Register_inst1"} : !hw.inout<i1>
    sv.alwaysff(posedge %CLK) {
        sv.passign %4, %0 : i1
    }
    %5 = hw.constant 0 : i1
    sv.initial {
        sv.bpassign %4, %5 : i1
    }
    %3 = sv.read_inout %4 : !hw.inout<i1>
    %7 = sv.reg {name = "Register_inst2"} : !hw.inout<i1>
    sv.alwaysff(posedge %CLK) {
        sv.passign %7, %3 : i1
    }
    %8 = hw.constant 0 : i1
    sv.initial {
        sv.bpassign %7, %8 : i1
    }
    %6 = sv.read_inout %7 : !hw.inout<i1>
    %10 = sv.reg {name = "Register_inst3"} : !hw.inout<i1>
    sv.alwaysff(posedge %CLK) {
        sv.passign %10, %6 : i1
    }
    %11 = hw.constant 0 : i1
    sv.initial {
        sv.bpassign %10, %11 : i1
    }
    %9 = sv.read_inout %10 : !hw.inout<i1>
    hw.output %9 : i1
}
