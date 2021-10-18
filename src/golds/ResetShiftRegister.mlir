hw.module @Register(%I: i4, %CE: i1, %CLK: i1, %RESETN: i1) -> (%O: i4) {
    %2 = hw.array_create %0, %I : i4
    %1 = hw.array_get %2[%CE] : !hw.array<2xi4>
    %3 = hw.constant 0 : i4
    %5 = hw.constant -1 : i1
    %4 = comb.xor %5, %RESETN : i1
    %7 = hw.array_create %1, %3 : i4
    %6 = hw.array_get %7[%4] : !hw.array<2xi4>
    %8 = sv.reg {name = "reg_P4_inst0"} : !hw.inout<i4>
    sv.alwaysff(posedge %CLK) {
        sv.passign %8, %6 : i4
    }
    %9 = hw.constant 0 : i4
    sv.initial {
        sv.bpassign %8, %9 : i4
    }
    %0 = sv.read_inout %8 : !hw.inout<i4>
    hw.output %0 : i4
}
hw.module @ResetShiftRegister(%I: i4, %shift: i1, %CLK: i1, %RESETN: i1) -> (%O: i4) {
    %0 = hw.instance "Register_inst0" @Register(%I, %shift, %CLK, %RESETN) : (i4, i1, i1, i1) -> (i4)
    %1 = hw.instance "Register_inst1" @Register(%0, %shift, %CLK, %RESETN) : (i4, i1, i1, i1) -> (i4)
    %2 = hw.instance "Register_inst2" @Register(%1, %shift, %CLK, %RESETN) : (i4, i1, i1, i1) -> (i4)
    %3 = hw.instance "Register_inst3" @Register(%2, %shift, %CLK, %RESETN) : (i4, i1, i1, i1) -> (i4)
    hw.output %3 : i4
}
