hw.module @Register(%I: i1, %CLK: i1) -> (%O: i1) {
    %0 = sv.reg {name = "reg_P1_inst0"} : !hw.inout<i1>
    %1 = hw.constant 0 : i1
    %2 = sv.read_inout %0 : !hw.inout<i1>
    sv.alwaysff(posedge %CLK) { sv.passign %0, %I : i1 }
    sv.initial { sv.bpassign %0, %1 : i1 }
    %3 = comb.extract %2 from 0 : (i1) -> i1
    hw.output %3 : i1
}
hw.module @ShiftRegister(%I: i1, %CLK: i1) -> (%O: i1) {
    %0 = hw.instance "Register_inst0" @Register(%I, %CLK) : (i1, i1) -> (i1)
    %1 = hw.instance "Register_inst1" @Register(%0, %CLK) : (i1, i1) -> (i1)
    %2 = hw.instance "Register_inst2" @Register(%1, %CLK) : (i1, i1) -> (i1)
    %3 = hw.instance "Register_inst3" @Register(%2, %CLK) : (i1, i1) -> (i1)
    hw.output %3 : i1
}
