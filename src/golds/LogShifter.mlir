hw.module @Register(%I: i16, %CLK: i1) -> (%O: i16) {
    %1 = sv.reg {name = "reg_P16_inst0"} : !hw.inout<i16>
    sv.alwaysff(posedge %CLK) {
        sv.passign %1, %I : i16
    }
    %2 = hw.constant 0 : i16
    sv.initial {
        sv.bpassign %1, %2 : i16
    }
    %0 = sv.read_inout %1 : !hw.inout<i16>
    hw.output %0 : i16
}
hw.module @Mux2xUInt16(%I0: i16, %I1: i16, %S: i1) -> (%O: i16) {
    %0 = hw.array_create %I1, %I0 : i16
    %1 = comb.merge %S : i1
    %2 = hw.struct_create (%0, %1) : !hw.struct<data: !hw.array<2xi16>, sel: i1>
    %4 = hw.struct_extract %2["data"] : !hw.struct<data: !hw.array<2xi16>, sel: i1>
    %5 = hw.struct_extract %2["sel"] : !hw.struct<data: !hw.array<2xi16>, sel: i1>
    %3 = hw.array_get %4[%5] : !hw.array<2xi16>
    hw.output %3 : i16
}
hw.module @LogShifter(%I: i16, %shift_amount: i4, %CLK: i1) -> (%O: i16) {
    %0 = hw.constant 8 : i16
    %1 = comb.shl %I, %0 : i16
    %2 = comb.extract %shift_amount from 3 : (i4) -> i1
    %3 = hw.constant 1 : i1
    %4 = comb.xor %2, %3 : i1
    %6 = hw.constant -1 : i1
    %5 = comb.xor %6, %4 : i1
    %7 = hw.instance "Mux2xUInt16_inst0" @Mux2xUInt16(%I, %1, %5) : (i16, i16, i1) -> (i16)
    %8 = hw.instance "Register_inst0" @Register(%7, %CLK) : (i16, i1) -> (i16)
    %9 = hw.constant 4 : i16
    %10 = comb.shl %8, %9 : i16
    %11 = comb.extract %shift_amount from 2 : (i4) -> i1
    %12 = hw.constant 1 : i1
    %13 = comb.xor %11, %12 : i1
    %15 = hw.constant -1 : i1
    %14 = comb.xor %15, %13 : i1
    %16 = hw.instance "Mux2xUInt16_inst1" @Mux2xUInt16(%8, %10, %14) : (i16, i16, i1) -> (i16)
    %17 = hw.instance "Register_inst1" @Register(%16, %CLK) : (i16, i1) -> (i16)
    %18 = hw.constant 2 : i16
    %19 = comb.shl %17, %18 : i16
    %20 = comb.extract %shift_amount from 1 : (i4) -> i1
    %21 = hw.constant 1 : i1
    %22 = comb.xor %20, %21 : i1
    %24 = hw.constant -1 : i1
    %23 = comb.xor %24, %22 : i1
    %25 = hw.instance "Mux2xUInt16_inst2" @Mux2xUInt16(%17, %19, %23) : (i16, i16, i1) -> (i16)
    %26 = hw.instance "Register_inst2" @Register(%25, %CLK) : (i16, i1) -> (i16)
    %27 = hw.constant 1 : i16
    %28 = comb.shl %26, %27 : i16
    %29 = comb.extract %shift_amount from 0 : (i4) -> i1
    %30 = hw.constant 1 : i1
    %31 = comb.xor %29, %30 : i1
    %33 = hw.constant -1 : i1
    %32 = comb.xor %33, %31 : i1
    %34 = hw.instance "Mux2xUInt16_inst3" @Mux2xUInt16(%26, %28, %32) : (i16, i16, i1) -> (i16)
    hw.output %34 : i16
}
