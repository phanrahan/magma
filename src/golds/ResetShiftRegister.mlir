hw.module @Mux2xUInt4(%I0: i4, %I1: i4, %S: i1) -> (%O: i4) {
    %0 = hw.array_create %I1, %I0 : i4
    %1 = hw.struct_create (%0, %S) : !hw.struct<data: !hw.array<2xi4>, sel: i1>
    %2 = hw.struct_extract %1["data"] : !hw.struct<data: !hw.array<2xi4>, sel: i1>
    %3 = hw.struct_extract %1["sel"] : !hw.struct<data: !hw.array<2xi4>, sel: i1>
    %4 = hw.array_get %2[%3] : !hw.array<2xi4>
    hw.output %4 : i4
}
hw.module @Register(%I: i4, %CE: i1, %CLK: i1, %RESETN: i1) -> (%O: i4) {
    %0 = hw.constant 0 : i4
    %1 = sv.reg {name = "reg_P4_inst0"} : !hw.inout<i4>
    %2 = hw.constant 0 : i4
    %3 = hw.constant -1 : i1
    %4 = sv.read_inout %1 : !hw.inout<i4>
    sv.initial { sv.bpassign %1, %2 : i4 }
    %5 = comb.xor %RESETN, %3 : i1
    %6 = hw.instance "enable_mux" @Mux2xUInt4(%4, %I, %CE) : (i4, i4, i1) -> (i4)
    %7 = hw.instance "Mux2xUInt4_inst0" @Mux2xUInt4(%6, %0, %5) : (i4, i4, i1) -> (i4)
    sv.alwaysff(posedge %CLK) { sv.passign %1, %7 : i4 }
    hw.output %4 : i4
}
hw.module @ResetShiftRegister(%I: i4, %shift: i1, %CLK: i1, %RESETN: i1) -> (%O: i4) {
    %0 = hw.instance "Register_inst0" @Register(%I, %shift, %CLK, %RESETN) : (i4, i1, i1, i1) -> (i4)
    %1 = hw.instance "Register_inst1" @Register(%0, %shift, %CLK, %RESETN) : (i4, i1, i1, i1) -> (i4)
    %2 = hw.instance "Register_inst2" @Register(%1, %shift, %CLK, %RESETN) : (i4, i1, i1, i1) -> (i4)
    %3 = hw.instance "Register_inst3" @Register(%2, %shift, %CLK, %RESETN) : (i4, i1, i1, i1) -> (i4)
    hw.output %3 : i4
}
