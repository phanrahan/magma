hw.module @Mux2xUInt4(%I0: i4, %I1: i4, %S: i1) -> (%O: i4) {
    %0 = hw.array_create %I1, %I0 : i4
    %1 = hw.struct_create (%0, %S) : !hw.struct<data: !hw.array<2xi4>, sel: i1>
    %2 = hw.struct_extract %1["data"] : !hw.struct<data: !hw.array<2xi4>, sel: i1>
    %3 = hw.struct_extract %1["sel"] : !hw.struct<data: !hw.array<2xi4>, sel: i1>
    %4 = hw.array_get %2[%3] : !hw.array<2xi4>
    hw.output %4 : i4
}
hw.module @Register(%I: i4, %CE: i1, %CLK: i1, %ASYNCRESET: i1) -> (%O: i4) {
    %0 = sv.wire : !hw.inout<i4>
    %1 = sv.read_inout %0 : !hw.inout<i4>
    %2 = comb.reg_arst %1, %CLK, %ASYNCRESET : i4
    %3 = hw.instance "enable_mux" @Mux2xUInt4(%2, %I, %CE) : (i4, i4, i1) -> (i4)
    sv.assign %0, %3 : i4
    hw.output %2 : i4
}
hw.module @EnableShiftRegister(%I: i4, %shift: i1, %CLK: i1, %ASYNCRESET: i1) -> (%O: i4) {
    %0 = hw.instance "Register_inst0" @Register(%I, %shift, %CLK, %ASYNCRESET) : (i4, i1, i1, i1) -> (i4)
    %1 = hw.instance "Register_inst1" @Register(%0, %shift, %CLK, %ASYNCRESET) : (i4, i1, i1, i1) -> (i4)
    %2 = hw.instance "Register_inst2" @Register(%1, %shift, %CLK, %ASYNCRESET) : (i4, i1, i1, i1) -> (i4)
    %3 = hw.instance "Register_inst3" @Register(%2, %shift, %CLK, %ASYNCRESET) : (i4, i1, i1, i1) -> (i4)
    hw.output %3 : i4
}
