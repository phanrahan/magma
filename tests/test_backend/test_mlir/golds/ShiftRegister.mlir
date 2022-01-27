hw.module @ShiftRegister(%I: i1, %CLK: i1) -> (O: i1) {
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
    sv.initial {
        sv.bpassign %4, %2 : i1
    }
    %3 = sv.read_inout %4 : !hw.inout<i1>
    %6 = sv.reg {name = "Register_inst2"} : !hw.inout<i1>
    sv.alwaysff(posedge %CLK) {
        sv.passign %6, %3 : i1
    }
    sv.initial {
        sv.bpassign %6, %2 : i1
    }
    %5 = sv.read_inout %6 : !hw.inout<i1>
    %8 = sv.reg {name = "Register_inst3"} : !hw.inout<i1>
    sv.alwaysff(posedge %CLK) {
        sv.passign %8, %5 : i1
    }
    sv.initial {
        sv.bpassign %8, %2 : i1
    }
    %7 = sv.read_inout %8 : !hw.inout<i1>
    hw.output %7 : i1
}
