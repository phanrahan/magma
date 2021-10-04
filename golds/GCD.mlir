hw.module @Mux2xUInt16(%I0: i16, %I1: i16, %S: i1) -> (%O: i16) {
    %0 = hw.array_create %I1, %I0 : i16
    %1 = hw.struct_create (%0, %S) : !hw.struct<data: !hw.array<2xi16>, sel: i1>
    %2 = hw.struct_extract %1["data"] : !hw.struct<data: !hw.array<2xi16>, sel: i1>
    %3 = hw.struct_extract %1["sel"] : !hw.struct<data: !hw.array<2xi16>, sel: i1>
    %4 = hw.array_get %2[%3] : !hw.array<2xi16>
    hw.output %4 : i16
}
hw.module @Register(%I: i16, %CLK: i1) -> (%O: i16) {
    %0 = sv.reg {name = "reg_P16_inst0"} : !hw.inout<i16>
    %1 = hw.constant 0 : i16
    %2 = sv.read_inout %0 : !hw.inout<i16>
    sv.alwaysff(posedge %CLK) { sv.passign %0, %I : i16 }
    sv.initial { sv.bpassign %0, %1 : i16 }
    hw.output %2 : i16
}
hw.module @Mux2x_SequentialRegisterWrapperUInt16(%I0: i16, %I1: i16, %S: i1) -> (%O: i16) {
    %0 = hw.array_create %I1, %I0 : i16
    %1 = hw.struct_create (%0, %S) : !hw.struct<data: !hw.array<2xi16>, sel: i1>
    %2 = hw.struct_extract %1["data"] : !hw.struct<data: !hw.array<2xi16>, sel: i1>
    %3 = hw.struct_extract %1["sel"] : !hw.struct<data: !hw.array<2xi16>, sel: i1>
    %4 = hw.array_get %2[%3] : !hw.array<2xi16>
    hw.output %4 : i16
}
hw.module @GCD(%a: i16, %b: i16, %load: i1, %CLK: i1) -> (%O0: i16, %O1: i1) {
    %0 = hw.constant 0 : i16
    %1 = hw.constant 0 : i16
    %2 = hw.constant -1 : i1
    %3 = sv.wire : !hw.inout<i16>
    %4 = sv.wire : !hw.inout<i16>
    %5 = sv.wire : !hw.inout<i16>
    %6 = sv.wire : !hw.inout<i16>
    %7 = sv.wire : !hw.inout<i16>
    %8 = sv.wire : !hw.inout<i16>
    %9 = sv.wire : !hw.inout<i16>
    %10 = sv.wire : !hw.inout<i16>
    %11 = sv.read_inout %3 : !hw.inout<i16>
    %12 = sv.read_inout %4 : !hw.inout<i16>
    %13 = sv.read_inout %5 : !hw.inout<i16>
    %14 = sv.read_inout %6 : !hw.inout<i16>
    %15 = sv.read_inout %7 : !hw.inout<i16>
    %16 = sv.read_inout %8 : !hw.inout<i16>
    %17 = sv.read_inout %9 : !hw.inout<i16>
    %18 = sv.read_inout %10 : !hw.inout<i16>
    %19 = hw.instance "Register_inst0" @Register(%11, %CLK) : (i16, i1) -> (i16)
    %20 = comb.icmp eq %14, %0 : i16
    %21 = comb.sub %15, %12 : i16
    %22 = comb.icmp ult %13, %16 : i16
    %23 = hw.instance "Mux2xUInt16_inst2" @Mux2xUInt16(%18, %b, %load) : (i16, i16, i1) -> (i16)
    %24 = comb.sub %17, %19 : i16
    sv.assign %7, %19 : i16
    sv.assign %8, %19 : i16
    %25 = comb.xor %20, %2 : i1
    %26 = hw.instance "Mux2x_SequentialRegisterWrapperUInt16_inst0" @Mux2x_SequentialRegisterWrapperUInt16(%19, %21, %22) : (i16, i16, i1) -> (i16)
    %27 = hw.instance "Register_inst1" @Register(%23, %CLK) : (i16, i1) -> (i16)
    %28 = hw.instance "Mux2x_SequentialRegisterWrapperUInt16_inst1" @Mux2x_SequentialRegisterWrapperUInt16(%19, %26, %25) : (i16, i16, i1) -> (i16)
    %29 = comb.icmp eq %27, %1 : i16
    %30 = hw.instance "Mux2xUInt16_inst0" @Mux2xUInt16(%24, %27, %22) : (i16, i16, i1) -> (i16)
    sv.assign %4, %27 : i16
    sv.assign %5, %27 : i16
    sv.assign %6, %27 : i16
    sv.assign %9, %27 : i16
    %31 = hw.instance "Mux2xUInt16_inst1" @Mux2xUInt16(%28, %a, %load) : (i16, i16, i1) -> (i16)
    %32 = hw.instance "Mux2x_SequentialRegisterWrapperUInt16_inst2" @Mux2x_SequentialRegisterWrapperUInt16(%27, %30, %25) : (i16, i16, i1) -> (i16)
    sv.assign %3, %31 : i16
    sv.assign %10, %32 : i16
    hw.output %19, %29 : i16, i1
}
