hw.module @Register(%I: i16, %CLK: i1) -> (%O: i16) {
    %0 = sv.reg {name = "reg_P16_inst0"} : !hw.inout<i16>
    %1 = hw.constant 0 : i16
    %2 = sv.read_inout %0 : !hw.inout<i16>
    sv.alwaysff(posedge %CLK) { sv.passign %0, %I : i16 }
    sv.initial { sv.bpassign %0, %1 : i16 }
    hw.output %2 : i16
}
hw.module @counter(%CLK: i1) -> (%y: i16) {
    %0 = hw.constant 1 : i16
    %1 = sv.wire : !hw.inout<i16>
    %2 = sv.read_inout %1 : !hw.inout<i16>
    %3 = comb.add %2, %0 : i16
    %4 = hw.instance "Register_inst0" @Register(%3, %CLK) : (i16, i1) -> (i16)
    sv.assign %1, %4 : i16
    hw.output %4 : i16
}
