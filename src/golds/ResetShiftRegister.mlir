hw.module @Mux2xUInt4(%I0: i4, %I1: i4, %S: i1) -> (%O: i4) {
    %0 = hw.array_create %I1, %I0 : i4
    %1 = comb.merge %S : i1
    %2 = hw.struct_create (%0, %1) : !hw.struct<data: !hw.array<2xi4>, sel: i1>
    %4 = hw.struct_extract %2["data"] : !hw.struct<data: !hw.array<2xi4>, sel: i1>
    %5 = hw.struct_extract %2["sel"] : !hw.struct<data: !hw.array<2xi4>, sel: i1>
    %3 = hw.array_get %4[%5] : !hw.array<2xi4>
    hw.output %3 : i4
}
hw.module @Register(%I: i4, %CE: i1, %CLK: i1, %RESETN: i1) -> (%O: i4) {
    %1 = hw.instance "enable_mux" @Mux2xUInt4(%0, %I, %CE) : (i4, i4, i1) -> (i4)
    %2 = hw.constant 0 : i4
    %4 = hw.constant -1 : i1
    %3 = comb.xor %4, %RESETN : i1
    %5 = hw.instance "Mux2xUInt4_inst0" @Mux2xUInt4(%1, %2, %3) : (i4, i4, i1) -> (i4)
    %6 = sv.reg {name = "reg_P4_inst0"} : !hw.inout<i4>
    sv.alwaysff(posedge %CLK) {
        sv.passign %6, %5 : i4
    }
    %0 = sv.read_inout %6 : !hw.inout<i4>
    hw.output %0 : i4
}
hw.module @ResetShiftRegister(%I: i4, %shift: i1, %CLK: i1, %RESETN: i1) -> (%O: i4) {
    %0 = hw.instance "Register_inst0" @Register(%I, %shift, %CLK, %RESETN) : (i4, i1, i1, i1) -> (i4)
    %1 = hw.instance "Register_inst1" @Register(%0, %shift, %CLK, %RESETN) : (i4, i1, i1, i1) -> (i4)
    %2 = hw.instance "Register_inst2" @Register(%1, %shift, %CLK, %RESETN) : (i4, i1, i1, i1) -> (i4)
    %3 = hw.instance "Register_inst3" @Register(%2, %shift, %CLK, %RESETN) : (i4, i1, i1, i1) -> (i4)
    hw.output %3 : i4
}
