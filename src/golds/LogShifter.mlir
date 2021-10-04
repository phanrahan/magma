hw.module @Register(%I: i16, %CLK: i1) -> (%O: i16) {
    %0 = sv.reg {name = "reg_P16_inst0"} : !hw.inout<i16>
    %1 = hw.constant 0 : i16
    %2 = sv.read_inout %0 : !hw.inout<i16>
    sv.alwaysff(posedge %CLK) { sv.passign %0, %I : i16 }
    sv.initial { sv.bpassign %0, %1 : i16 }
    hw.output %2 : i16
}
hw.module @Mux2xUInt16(%I0: i16, %I1: i16, %S: i1) -> (%O: i16) {
    %0 = hw.array_create %I1, %I0 : i16
    %1 = hw.struct_create (%0, %S) : !hw.struct<data: !hw.array<2xi16>, sel: i1>
    %2 = hw.struct_extract %1["data"] : !hw.struct<data: !hw.array<2xi16>, sel: i1>
    %3 = hw.struct_extract %1["sel"] : !hw.struct<data: !hw.array<2xi16>, sel: i1>
    %4 = hw.array_get %2[%3] : !hw.array<2xi16>
    hw.output %4 : i16
}
hw.module @LogShifter(%I: i16, %shift_amount: i4, %CLK: i1) -> (%O: i16) {
    %0 = hw.constant 1 : i1
    %1 = hw.constant 8 : i16
    %2 = hw.constant 1 : i1
    %3 = hw.constant 4 : i16
    %4 = hw.constant 1 : i1
    %5 = hw.constant 2 : i16
    %6 = hw.constant 1 : i1
    %7 = hw.constant 1 : i16
    %8 = hw.constant -1 : i1
    %9 = hw.constant -1 : i1
    %10 = hw.constant -1 : i1
    %11 = hw.constant -1 : i1
    %12 = comb.extract %shift_amount from 3 : (i4) -> i1
    %13 = comb.extract %shift_amount from 2 : (i4) -> i1
    %14 = comb.extract %shift_amount from 1 : (i4) -> i1
    %15 = comb.extract %shift_amount from 0 : (i4) -> i1
    %16 = comb.shl %I, %1 : i16
    %17 = comb.xor %12, %0 : i1
    %18 = comb.xor %13, %2 : i1
    %19 = comb.xor %14, %4 : i1
    %20 = comb.xor %15, %6 : i1
    %21 = comb.xor %17, %8 : i1
    %22 = comb.xor %18, %9 : i1
    %23 = comb.xor %19, %10 : i1
    %24 = comb.xor %20, %11 : i1
    %25 = hw.instance "Mux2xUInt16_inst0" @Mux2xUInt16(%I, %16, %21) : (i16, i16, i1) -> (i16)
    %26 = hw.instance "Register_inst0" @Register(%25, %CLK) : (i16, i1) -> (i16)
    %27 = comb.shl %26, %3 : i16
    %28 = hw.instance "Mux2xUInt16_inst1" @Mux2xUInt16(%26, %27, %22) : (i16, i16, i1) -> (i16)
    %29 = hw.instance "Register_inst1" @Register(%28, %CLK) : (i16, i1) -> (i16)
    %30 = comb.shl %29, %5 : i16
    %31 = hw.instance "Mux2xUInt16_inst2" @Mux2xUInt16(%29, %30, %23) : (i16, i16, i1) -> (i16)
    %32 = hw.instance "Register_inst2" @Register(%31, %CLK) : (i16, i1) -> (i16)
    %33 = comb.shl %32, %7 : i16
    %34 = hw.instance "Mux2xUInt16_inst3" @Mux2xUInt16(%32, %33, %24) : (i16, i16, i1) -> (i16)
    hw.output %34 : i16
}
