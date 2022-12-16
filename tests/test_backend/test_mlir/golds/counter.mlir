module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @counter(%CLK: i1) -> (y: i16) {
        %0 = hw.constant 1 : i16
        %2 = comb.add %1, %0 : i16
        %3 = sv.reg {name = "Register_inst0"} : !hw.inout<i16>
        sv.alwaysff(posedge %CLK) {
            sv.passign %3, %2 : i16
        }
        %4 = hw.constant 0 : i16
        sv.initial {
            sv.bpassign %3, %4 : i16
        }
        %1 = sv.read_inout %3 : !hw.inout<i16>
        hw.output %1 : i16
    }
}
