module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @register_array_of_bit(%I: i4, %CLK: i1) -> (O: i4) {
        %1 = sv.reg name "Register_inst0" : !hw.inout<i4>
        sv.alwaysff(posedge %CLK) {
            sv.passign %1, %I : i4
        }
        %3 = hw.constant 3 : i4
        sv.initial {
            sv.bpassign %1, %3 : i4
        }
        %0 = sv.read_inout %1 : !hw.inout<i4>
        hw.output %0 : i4
    }
}
