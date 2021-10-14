hw.module @Mux2xUInt16(%I0: i16, %I1: i16, %S: i1) -> (%O: i16) {
    %0 = hw.array_create %I1, %I0 : i16
    %1 = comb.merge %S : i1
    %2 = hw.struct_create (%0, %1) : !hw.struct<data: !hw.array<2xi16>, sel: i1>
    %4 = hw.struct_extract %2["data"] : !hw.struct<data: !hw.array<2xi16>, sel: i1>
    %5 = hw.struct_extract %2["sel"] : !hw.struct<data: !hw.array<2xi16>, sel: i1>
    %3 = hw.array_get %4[%5] : !hw.array<2xi16>
    hw.output %3 : i16
}
hw.module @Register(%I: i16, %CLK: i1) -> (%O: i16) {
    %1 = sv.reg {name = "reg_P16_inst0"} : !hw.inout<i16>
    sv.alwaysff(posedge %CLK) {
        sv.passign %1, %I : i16
    }
    %0 = sv.read_inout %1 : !hw.inout<i16>
    hw.output %0 : i16
}
hw.module @Mux2x_SequentialRegisterWrapperUInt16(%I0: i16, %I1: i16, %S: i1) -> (%O: i16) {
    %0 = hw.array_create %I1, %I0 : i16
    %1 = comb.merge %S : i1
    %2 = hw.struct_create (%0, %1) : !hw.struct<data: !hw.array<2xi16>, sel: i1>
    %4 = hw.struct_extract %2["data"] : !hw.struct<data: !hw.array<2xi16>, sel: i1>
    %5 = hw.struct_extract %2["sel"] : !hw.struct<data: !hw.array<2xi16>, sel: i1>
    %3 = hw.array_get %4[%5] : !hw.array<2xi16>
    hw.output %3 : i16
}
hw.module @GCD(%a: i16, %b: i16, %load: i1, %CLK: i1) -> (%O0: i16, %O1: i1) {
    %2 = comb.sub %0, %1 : i16
    %3 = comb.ult %0, %1 : i1
    %4 = hw.instance "Mux2xUInt16_inst0" @Mux2xUInt16(%2, %0, %3) : (i16, i16, i1) -> (i16)
    %5 = hw.constant 0 : i16
    %6 = comb.eq %0, %5 : i1
    %8 = hw.constant -1 : i1
    %7 = comb.xor %8, %6 : i1
    %9 = hw.instance "Mux2x_SequentialRegisterWrapperUInt16_inst2" @Mux2x_SequentialRegisterWrapperUInt16(%0, %4, %7) : (i16, i16, i1) -> (i16)
    %10 = hw.instance "Mux2xUInt16_inst2" @Mux2xUInt16(%9, %b, %load) : (i16, i16, i1) -> (i16)
    %0 = hw.instance "Register_inst1" @Register(%10, %CLK) : (i16, i1) -> (i16)
    %11 = comb.sub %1, %0 : i16
    %12 = hw.instance "Mux2x_SequentialRegisterWrapperUInt16_inst0" @Mux2x_SequentialRegisterWrapperUInt16(%1, %11, %3) : (i16, i16, i1) -> (i16)
    %13 = hw.instance "Mux2x_SequentialRegisterWrapperUInt16_inst1" @Mux2x_SequentialRegisterWrapperUInt16(%1, %12, %7) : (i16, i16, i1) -> (i16)
    %14 = hw.instance "Mux2xUInt16_inst1" @Mux2xUInt16(%13, %a, %load) : (i16, i16, i1) -> (i16)
    %1 = hw.instance "Register_inst0" @Register(%14, %CLK) : (i16, i1) -> (i16)
    %15 = hw.constant 0 : i16
    %16 = comb.eq %0, %15 : i1
    hw.output %1, %16 : i16, i1
}
