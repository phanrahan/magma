hw.module @Register(%I: i4, %CE: i1, %CLK: i1, %ASYNCRESET: i1) -> (%O: i4) {
    %2 = hw.array_create %0, %I : i4
    %1 = hw.array_get %2[%CE] : !hw.array<2xi4>
    %3 = sv.reg {name = "reg_PR4_inst0"} : !hw.inout<i4>
    sv.alwaysff(posedge %CLK) {
        sv.passign %3, %1 : i4
    } (asyncreset : posedge %ASYNCRESET) {
        sv.passign %3, %4 : i4
    }
    %4 = hw.constant 0 : i4
    sv.initial {
        sv.bpassign %3, %4 : i4
    }
    %0 = sv.read_inout %3 : !hw.inout<i4>
    hw.output %0 : i4
}
hw.module @EnableShiftRegister(%I: i4, %shift: i1, %CLK: i1, %ASYNCRESET: i1) -> (%O: i4) {
    %0 = hw.instance "Register_inst0" @Register(%I, %shift, %CLK, %ASYNCRESET) : (i4, i1, i1, i1) -> (i4)
    %1 = hw.instance "Register_inst1" @Register(%0, %shift, %CLK, %ASYNCRESET) : (i4, i1, i1, i1) -> (i4)
    %2 = hw.instance "Register_inst2" @Register(%1, %shift, %CLK, %ASYNCRESET) : (i4, i1, i1, i1) -> (i4)
    %3 = hw.instance "Register_inst3" @Register(%2, %shift, %CLK, %ASYNCRESET) : (i4, i1, i1, i1) -> (i4)
    hw.output %3 : i4
}
