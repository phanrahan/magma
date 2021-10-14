hw.module @Register(%I: i16, %CLK: i1) -> (%O: i16) {
    %1 = sv.reg {name = "reg_P16_inst0"} : !hw.inout<i16>
    sv.alwaysff(posedge %CLK) {
        sv.passign %1, %I : i16
    }
    %0 = sv.read_inout %1 : !hw.inout<i16>
    hw.output %0 : i16
}
hw.module @counter(%CLK: i1) -> (%y: i16) {
    %0 = hw.constant 1 : i16
    %2 = comb.add %1, %0 : i16
    %1 = hw.instance "Register_inst0" @Register(%2, %CLK) : (i16, i1) -> (i16)
    hw.output %1 : i16
}
