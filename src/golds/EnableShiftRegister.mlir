hw.module @Mux2xUInt4(%I0: i4, %I1: i4, %S: i1) -> (%O: i4) {
    %0 = hw.array_create %I1, %I0 : i4
    %1 = comb.merge %S : i1
    %2 = hw.struct_create (%0, %1) : !hw.struct<data: !hw.array<2xi4>, sel: i1>
    %4 = hw.struct_extract %2["data"] : !hw.struct<data: !hw.array<2xi4>, sel: i1>
    %5 = hw.struct_extract %2["sel"] : !hw.struct<data: !hw.array<2xi4>, sel: i1>
    %3 = hw.array_get %4[%5] : !hw.array<2xi4>
    hw.output %3 : i4
}
hw.module @Register(%I: i4, %CE: i1, %CLK: i1, %ASYNCRESET: i1) -> (%O: i4) {
    %1 = hw.instance "enable_mux" @Mux2xUInt4(%0, %I, %CE) : (i4, i4, i1) -> (i4)
    %0 = comb.reg_arst %1, %CLK, %ASYNCRESET : i4
    hw.output %0 : i4
}
hw.module @EnableShiftRegister(%I: i4, %shift: i1, %CLK: i1, %ASYNCRESET: i1) -> (%O: i4) {
    %0 = hw.instance "Register_inst0" @Register(%I, %shift, %CLK, %ASYNCRESET) : (i4, i1, i1, i1) -> (i4)
    %1 = hw.instance "Register_inst1" @Register(%0, %shift, %CLK, %ASYNCRESET) : (i4, i1, i1, i1) -> (i4)
    %2 = hw.instance "Register_inst2" @Register(%1, %shift, %CLK, %ASYNCRESET) : (i4, i1, i1, i1) -> (i4)
    %3 = hw.instance "Register_inst3" @Register(%2, %shift, %CLK, %ASYNCRESET) : (i4, i1, i1, i1) -> (i4)
    hw.output %3 : i4
}
